"""Outbound URL hardening — refuse server-side fetches of private/internal hosts (SSRF).

Any URL an authenticated user can make the server fetch (RSS feeds, custom
LLM provider endpoints, scraped/researched pages) must resolve only to
publicly-routable addresses. See specs/functional/security-hardening.md §5.

Set COACH_ALLOW_PRIVATE_URLS=1 to disable (single-user/local deployments
that point custom providers at localhost, e.g. Ollama).
"""

import asyncio
import ipaddress
import os
import socket
from urllib.parse import urlparse

import structlog

logger = structlog.get_logger()

_ALLOWED_SCHEMES = {"http", "https"}


class UnsafeURLError(ValueError):
    """URL refused: not http(s) or targets a non-public address."""


def _private_urls_allowed() -> bool:
    return os.getenv("COACH_ALLOW_PRIVATE_URLS", "").strip().lower() in {"1", "true", "yes"}


def _is_public_address(ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    # is_global already excludes loopback, RFC 1918, link-local (incl. cloud
    # metadata 169.254.169.254), CGNAT 100.64/10, and IPv6 unique-local; the
    # extra checks are belt-and-braces against stdlib edge cases.
    return ip.is_global and not (
        ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_multicast
        or ip.is_reserved
        or ip.is_unspecified
    )


def validate_public_url(url: str) -> None:
    """Raise UnsafeURLError unless url is http(s) to a publicly-routable host.

    Resolves the hostname (blocking DNS lookup — use ensure_public_url from
    async code); every resolved address must be public.
    """
    if _private_urls_allowed():
        return

    try:
        parsed = urlparse(url)
    except Exception:
        raise UnsafeURLError("URL could not be parsed")

    if parsed.scheme not in _ALLOWED_SCHEMES:
        raise UnsafeURLError("URL must be http or https")

    host = parsed.hostname
    if not host:
        raise UnsafeURLError("URL has no host")

    # Literal IP: check directly, no DNS
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        ip = None
    if ip is not None:
        if not _is_public_address(ip):
            raise UnsafeURLError("URL targets a non-public address")
        return

    try:
        addrinfo = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        raise UnsafeURLError("URL host could not be resolved")
    if not addrinfo:
        raise UnsafeURLError("URL host could not be resolved")

    for family, _type, _proto, _canon, sockaddr in addrinfo:
        try:
            resolved = ipaddress.ip_address(sockaddr[0])
        except ValueError:
            raise UnsafeURLError("URL host resolved to an unrecognized address")
        if not _is_public_address(resolved):
            logger.warning("url_guard.blocked", url=url, resolved=str(resolved))
            raise UnsafeURLError("URL resolves to a non-public address")


async def ensure_public_url(url: str) -> None:
    """Async wrapper: run the (blocking) validation off the event loop."""
    await asyncio.to_thread(validate_public_url, url)


def public_url_event_hooks() -> dict:
    """httpx event hooks validating every request in a redirect chain.

    Usage: httpx.AsyncClient(follow_redirects=True, event_hooks=public_url_event_hooks())
    A public URL that redirects to an internal address is refused at the hop.
    """

    async def _check_request(request) -> None:
        await ensure_public_url(str(request.url))

    return {"request": [_check_request]}
