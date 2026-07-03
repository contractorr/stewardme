"""Read-only Gmail + Calendar for brief sections via bring-your-own credentials.

No OAuth and no Google app verification. Each user supplies their own read
credentials, stored Fernet-encrypted in per-user secrets (same store as the
LLM key):

  - Calendar: a secret iCal URL (Calendar settings -> "Secret address in iCal
    format"). Fetched SSRF-guarded, parsed with ``icalendar`` +
    ``recurring_ical_events`` (RRULE expansion over the window).
  - Gmail: address + app password, read over IMAP (imap.gmail.com) using
    Gmail's ``X-GM-RAW`` search extension. Stdlib ``imaplib``/``email`` only.

All access is read-only. Fetchers return ``None`` (never raise) on any failure
so brief generation degrades gracefully; verification helpers raise
``ValueError`` so routes can reject bad credentials at save time.
"""

import email as email_lib
import imaplib
from datetime import date, datetime, timedelta, timezone
from email.header import decode_header, make_header

import httpx
import structlog

logger = structlog.get_logger()

CAL_URL_SECRET = "calendar_ical_url"
GMAIL_ADDR_SECRET = "gmail_address"
GMAIL_PW_SECRET = "gmail_app_password"

IMAP_HOST = "imap.gmail.com"
HTTP_TIMEOUT = 20.0
IMAP_TIMEOUT = 20.0

# Same importance filter the OAuth implementation used, via Gmail's IMAP
# X-GM-RAW search extension (accepts Gmail search syntax verbatim).
GMAIL_QUERY = (
    "is:unread newer_than:7d (is:important OR category:primary) "
    "-category:promotions -category:social"
)


# --- per-user secret helpers -------------------------------------------------


def _key() -> str:
    from web.deps_base import get_secret_key

    return get_secret_key()


def _get(user_id: str, secret_key: str) -> str | None:
    try:
        from web.user_store import get_user_secret

        return get_user_secret(user_id, secret_key, _key())
    except Exception:
        return None


def _set(user_id: str, secret_key: str, value: str) -> None:
    from user_crud import get_or_create_user
    from web.user_store import set_user_secret

    get_or_create_user(user_id)
    set_user_secret(user_id, secret_key, value, _key())


def _del(user_id: str, secret_key: str) -> None:
    from web.user_store import delete_user_secret

    delete_user_secret(user_id, secret_key)


# --- connection status -------------------------------------------------------


def calendar_connected(user_id: str) -> bool:
    return bool(_get(user_id, CAL_URL_SECRET))


def gmail_connected(user_id: str) -> bool:
    return bool(_get(user_id, GMAIL_ADDR_SECRET) and _get(user_id, GMAIL_PW_SECRET))


def gmail_address(user_id: str) -> str | None:
    return _get(user_id, GMAIL_ADDR_SECRET)


def status(user_id: str) -> dict:
    return {
        "calendar_connected": calendar_connected(user_id),
        "gmail_connected": gmail_connected(user_id),
        "gmail_address": gmail_address(user_id),
    }


# --- store / clear -----------------------------------------------------------


def store_calendar(user_id: str, url: str) -> None:
    _set(user_id, CAL_URL_SECRET, url)


def clear_calendar(user_id: str) -> None:
    _del(user_id, CAL_URL_SECRET)


def store_gmail(user_id: str, address: str, app_password: str) -> None:
    _set(user_id, GMAIL_ADDR_SECRET, address)
    _set(user_id, GMAIL_PW_SECRET, app_password)


def clear_gmail(user_id: str) -> None:
    _del(user_id, GMAIL_ADDR_SECRET)
    _del(user_id, GMAIL_PW_SECRET)


# --- calendar (iCal) ---------------------------------------------------------


def _parse_ical(content: bytes):
    import icalendar

    cal = icalendar.Calendar.from_ical(content)
    if getattr(cal, "name", None) != "VCALENDAR":
        raise ValueError("not an iCalendar feed")
    return cal


async def verify_calendar(url: str) -> None:
    """Fetch + parse the feed; raise ValueError if unsafe/unreachable/not iCal."""
    from url_guard import UnsafeURLError, ensure_public_url, public_url_event_hooks

    try:
        await ensure_public_url(url)
    except UnsafeURLError as exc:
        raise ValueError(str(exc)) from exc
    try:
        async with httpx.AsyncClient(
            follow_redirects=True,
            event_hooks=public_url_event_hooks(),
            timeout=HTTP_TIMEOUT,
        ) as client:
            resp = await client.get(url)
            resp.raise_for_status()
    except (httpx.HTTPError, UnsafeURLError) as exc:
        raise ValueError(f"Could not fetch the calendar URL: {exc}") from exc
    try:
        _parse_ical(resp.content)
    except Exception as exc:
        raise ValueError("That URL did not return a valid iCalendar feed") from exc


def _fetch_ical_content(url: str) -> bytes | None:
    """SSRF-guarded synchronous fetch (generation path; async hooks unavailable)."""
    from url_guard import UnsafeURLError, validate_public_url

    try:
        validate_public_url(url)
        resp = httpx.get(url, follow_redirects=False, timeout=HTTP_TIMEOUT)
        hops = 0
        while resp.is_redirect and hops < 3:
            nxt = str(resp.next_request.url) if resp.next_request else ""
            if not nxt:
                break
            validate_public_url(nxt)  # re-validate every hop
            resp = httpx.get(nxt, follow_redirects=False, timeout=HTTP_TIMEOUT)
            hops += 1
        resp.raise_for_status()
        return resp.content
    except (httpx.HTTPError, UnsafeURLError) as exc:
        logger.warning("google_sync.calendar_fetch_failed", error=str(exc))
        return None


def _iso(value) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return ""


def fetch_calendar_events(user_id: str, days: int = 7) -> list[dict] | None:
    """Normalized events for the next ``days`` days; None when not connected/errored."""
    url = _get(user_id, CAL_URL_SECRET)
    if not url:
        return None
    content = _fetch_ical_content(url)
    if content is None:
        return None

    try:
        import recurring_ical_events

        cal = _parse_ical(content)
        now = datetime.now(timezone.utc)
        occurrences = recurring_ical_events.of(cal).between(now, now + timedelta(days=days))
    except Exception as exc:
        logger.warning("google_sync.calendar_parse_failed", error=str(exc))
        return None

    events: list[dict] = []
    for comp in occurrences:
        start = comp.get("DTSTART")
        end = comp.get("DTEND")
        start_dt = start.dt if start is not None else None
        end_dt = end.dt if end is not None else None
        all_day = isinstance(start_dt, date) and not isinstance(start_dt, datetime)
        events.append(
            {
                "title": str(comp.get("SUMMARY", "(no title)")),
                "start": _iso(start_dt),
                "end": _iso(end_dt),
                "all_day": all_day,
                "location": str(comp.get("LOCATION", "")),
            }
        )
    # All-day events (date-only start) sort before timed events on the same day.
    events.sort(key=lambda e: e["start"] or "~")
    return events


# --- gmail (IMAP) ------------------------------------------------------------


def _imap_connect(address: str, app_password: str) -> imaplib.IMAP4_SSL:
    imap = imaplib.IMAP4_SSL(IMAP_HOST, timeout=IMAP_TIMEOUT)
    imap.login(address, app_password)
    return imap


def _decode(value: str) -> str:
    try:
        return str(make_header(decode_header(value)))
    except Exception:
        return value


def verify_gmail(address: str, app_password: str) -> None:
    """IMAP login test; raise ValueError on failure."""
    try:
        imap = _imap_connect(address, app_password)
    except (imaplib.IMAP4.error, OSError) as exc:
        raise ValueError(
            "Gmail login failed. Use a 16-character app password "
            "(requires 2-Step Verification), not your normal password."
        ) from exc
    try:
        imap.logout()
    except Exception:
        pass


def fetch_important_emails(user_id: str, limit: int = 12) -> list[dict] | None:
    """Unread important/primary emails from the last week; None when unavailable."""
    address = _get(user_id, GMAIL_ADDR_SECRET)
    app_password = _get(user_id, GMAIL_PW_SECRET)
    if not (address and app_password):
        return None

    try:
        imap = _imap_connect(address, app_password)
    except (imaplib.IMAP4.error, OSError) as exc:
        logger.warning("google_sync.imap_login_failed", error=str(exc))
        return None

    try:
        imap.select("INBOX", readonly=True)
        typ, data = imap.search(None, "X-GM-RAW", f'"{GMAIL_QUERY}"')
        if typ != "OK" or not data or not data[0]:
            return []
        message_ids = data[0].split()[-limit:][::-1]  # newest first, capped

        emails: list[dict] = []
        for mid in message_ids:
            typ, msg_data = imap.fetch(mid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
            if typ != "OK" or not msg_data or not isinstance(msg_data[0], tuple):
                continue
            msg = email_lib.message_from_bytes(msg_data[0][1])
            emails.append(
                {
                    "from": _decode(msg.get("From", "")),
                    "subject": _decode(msg.get("Subject", "(no subject)")),
                    "date": msg.get("Date", ""),
                    "snippet": "",
                }
            )
        return emails
    except (imaplib.IMAP4.error, OSError) as exc:
        logger.warning("google_sync.imap_fetch_failed", error=str(exc))
        return None
    finally:
        try:
            imap.logout()
        except Exception:
            pass
