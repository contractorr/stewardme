"""Tests for per-user route rate limits (LLM + general buckets)."""

from unittest.mock import patch

import web.rate_limit as rate_limit_module
from web.rate_limit import check_route_rate_limit, reset_rate_limits

from .test_advisor_routes import _ENGINE_PATCH, _mock_get_engine


def _set_limits(monkeypatch, *, enabled=True, llm=3, general=1000):
    monkeypatch.setattr(rate_limit_module, "_route_limit_cache", (enabled, llm, general))


def _ask(client, headers):
    return client.post(
        "/api/advisor/ask",
        json={"question": "What should I focus on?"},
        headers=headers,
    )


class TestLLMRouteLimit:
    def test_429_past_limit_with_retry_after(self, client, auth_headers, monkeypatch):
        _set_limits(monkeypatch, llm=3)
        with patch(_ENGINE_PATCH, side_effect=_mock_get_engine):
            for _ in range(3):
                assert _ask(client, auth_headers).status_code == 200

            res = _ask(client, auth_headers)

        assert res.status_code == 429
        assert "Retry-After" in res.headers
        assert int(res.headers["Retry-After"]) >= 1

    def test_second_user_unaffected(self, client, auth_headers, auth_headers_b, monkeypatch):
        _set_limits(monkeypatch, llm=2)
        with patch(_ENGINE_PATCH, side_effect=_mock_get_engine):
            for _ in range(2):
                assert _ask(client, auth_headers).status_code == 200
            assert _ask(client, auth_headers).status_code == 429

            assert _ask(client, auth_headers_b).status_code == 200

    def test_disabled_config_lifts_limit(self, client, auth_headers, monkeypatch):
        _set_limits(monkeypatch, enabled=False, llm=1)
        with patch(_ENGINE_PATCH, side_effect=_mock_get_engine):
            for _ in range(3):
                assert _ask(client, auth_headers).status_code == 200

    def test_window_resets_after_reset(self, client, auth_headers, monkeypatch):
        _set_limits(monkeypatch, llm=1)
        with patch(_ENGINE_PATCH, side_effect=_mock_get_engine):
            assert _ask(client, auth_headers).status_code == 200
            assert _ask(client, auth_headers).status_code == 429
        reset_rate_limits()
        _set_limits(monkeypatch, llm=1)
        with patch(_ENGINE_PATCH, side_effect=_mock_get_engine):
            assert _ask(client, auth_headers).status_code == 200


class TestGeneralRouteLimit:
    def test_general_limit_returns_429(self, client, auth_headers, monkeypatch):
        _set_limits(monkeypatch, llm=1000, general=5)
        last = None
        for _ in range(6):
            last = client.get("/api/settings", headers=auth_headers)
        assert last.status_code == 429
        assert "Retry-After" in last.headers

    def test_health_never_limited(self, client, monkeypatch):
        _set_limits(monkeypatch, llm=1, general=1)
        for _ in range(5):
            assert client.get("/api/health").status_code == 200

    def test_general_limit_keys_per_token(self, client, auth_headers, auth_headers_b, monkeypatch):
        _set_limits(monkeypatch, llm=1000, general=3)
        for _ in range(3):
            client.get("/api/settings", headers=auth_headers)
        assert client.get("/api/settings", headers=auth_headers).status_code == 429
        assert client.get("/api/settings", headers=auth_headers_b).status_code != 429


class TestCheckRouteRateLimit:
    def test_raises_past_limit(self, monkeypatch):
        reset_rate_limits()
        _set_limits(monkeypatch, llm=2)
        check_route_rate_limit("u1", "llm")
        check_route_rate_limit("u1", "llm")
        import pytest as _pytest

        with _pytest.raises(Exception) as exc_info:
            check_route_rate_limit("u1", "llm")
        assert getattr(exc_info.value, "status_code", None) == 429
        reset_rate_limits()
