"""Tests for the outbound URL SSRF guard (specs/functional/security-hardening.md §5)."""

import socket

import pytest

from url_guard import UnsafeURLError, ensure_public_url, validate_public_url


@pytest.fixture(autouse=True)
def _guard_enabled(monkeypatch):
    monkeypatch.delenv("COACH_ALLOW_PRIVATE_URLS", raising=False)


def _fake_addrinfo(*ips):
    def fake(host, port, **kwargs):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, 0)) for ip in ips]

    return fake


class TestLiteralIPs:
    """Literal IPs are checked without DNS — fully deterministic."""

    @pytest.mark.parametrize(
        "url",
        [
            "http://127.0.0.1/feed",
            "http://127.0.0.1:8000/api/admin",
            "http://10.0.0.5/",
            "http://192.168.1.1/router",
            "http://172.16.0.1/",
            "http://169.254.169.254/latest/meta-data/",
            "http://100.64.0.1/",
            "http://0.0.0.0/",
            "http://[::1]/",
            "http://[fc00::1]/",
        ],
    )
    def test_non_public_literal_rejected(self, url):
        with pytest.raises(UnsafeURLError):
            validate_public_url(url)

    def test_public_literal_accepted(self):
        validate_public_url("http://8.8.8.8/")


class TestSchemes:
    @pytest.mark.parametrize("url", ["ftp://example.com/", "file:///etc/passwd", "gopher://x.y/"])
    def test_non_http_rejected(self, url):
        with pytest.raises(UnsafeURLError):
            validate_public_url(url)

    def test_missing_host_rejected(self):
        with pytest.raises(UnsafeURLError):
            validate_public_url("http://")


class TestHostnameResolution:
    def test_private_resolution_rejected(self, monkeypatch):
        monkeypatch.setattr(socket, "getaddrinfo", _fake_addrinfo("10.1.2.3"))
        with pytest.raises(UnsafeURLError):
            validate_public_url("https://internal.example.com/feed")

    def test_public_resolution_accepted(self, monkeypatch):
        monkeypatch.setattr(socket, "getaddrinfo", _fake_addrinfo("93.184.216.34"))
        validate_public_url("https://example.com/feed")

    def test_mixed_resolution_rejected(self, monkeypatch):
        # Every resolved address must be public
        monkeypatch.setattr(socket, "getaddrinfo", _fake_addrinfo("93.184.216.34", "127.0.0.1"))
        with pytest.raises(UnsafeURLError):
            validate_public_url("https://rebind.example.com/")

    def test_resolution_failure_rejected(self, monkeypatch):
        def fail(host, port, **kwargs):
            raise socket.gaierror("NXDOMAIN")

        monkeypatch.setattr(socket, "getaddrinfo", fail)
        with pytest.raises(UnsafeURLError):
            validate_public_url("https://does-not-exist.example.com/")


class TestEscapeHatch:
    @pytest.mark.parametrize("value", ["1", "true", "yes"])
    def test_private_urls_allowed_when_env_set(self, monkeypatch, value):
        monkeypatch.setenv("COACH_ALLOW_PRIVATE_URLS", value)
        validate_public_url("http://localhost:11434/v1")  # e.g. local Ollama
        validate_public_url("http://127.0.0.1:8000/")

    def test_disabled_values_still_block(self, monkeypatch):
        monkeypatch.setenv("COACH_ALLOW_PRIVATE_URLS", "0")
        with pytest.raises(UnsafeURLError):
            validate_public_url("http://127.0.0.1/")


async def test_ensure_public_url_async_wrapper():
    with pytest.raises(UnsafeURLError):
        await ensure_public_url("http://169.254.169.254/latest/meta-data/")
    await ensure_public_url("http://8.8.8.8/")
