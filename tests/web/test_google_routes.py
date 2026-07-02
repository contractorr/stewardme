"""Tests for the Google (Gmail + Calendar) connection routes."""

from unittest.mock import patch

import pytest

from web import google_sync


@pytest.fixture
def google_env(monkeypatch):
    monkeypatch.setenv("GOOGLE_CLIENT_ID", "test-client-id")
    monkeypatch.setenv("GOOGLE_CLIENT_SECRET", "test-client-secret")
    monkeypatch.setenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/v1/google/callback")


def test_status_unavailable_without_env(client, auth_headers, monkeypatch):
    monkeypatch.delenv("GOOGLE_CLIENT_ID", raising=False)
    monkeypatch.delenv("GOOGLE_CLIENT_SECRET", raising=False)
    resp = client.get("/api/v1/google/status", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json() == {"available": False, "connected": False, "email": None}


def test_auth_url_unavailable_without_env(client, auth_headers, monkeypatch):
    monkeypatch.delenv("GOOGLE_CLIENT_ID", raising=False)
    resp = client.get("/api/v1/google/auth-url", headers=auth_headers)
    assert resp.status_code == 503


def test_auth_url_shape(client, auth_headers, google_env):
    resp = client.get("/api/v1/google/auth-url", headers=auth_headers)
    assert resp.status_code == 200
    url = resp.json()["url"]
    assert url.startswith("https://accounts.google.com/o/oauth2/v2/auth?")
    assert "gmail.readonly" in url
    assert "calendar.readonly" in url
    assert "access_type=offline" in url
    assert "state=" in url


def test_state_token_return_to_roundtrip():
    state = google_sync.make_state_token("test:u", return_to="onboarding")
    assert google_sync.decode_state_token(state) == ("test:u", "/onboarding")

    # Unknown return_to values fall back to the brief page.
    state = google_sync.make_state_token("test:u", return_to="https://evil.example")
    assert google_sync.decode_state_token(state) == ("test:u", "/brief")


def test_auth_url_embeds_return_to(client, auth_headers, google_env):
    resp = client.get("/api/v1/google/auth-url?return_to=onboarding", headers=auth_headers)
    assert resp.status_code == 200
    from urllib.parse import parse_qs, urlparse

    state = parse_qs(urlparse(resp.json()["url"]).query)["state"][0]
    _user, path = google_sync.decode_state_token(state)
    assert path == "/onboarding"


def test_callback_redirects_to_onboarding_return_path(client, google_env):
    state = google_sync.make_state_token("test:user-ob", return_to="onboarding")
    with (
        patch(
            "web.google_sync.exchange_code",
            return_value={"refresh_token": "rt-ob", "access_token": "at-ob"},
        ),
        patch("web.google_sync.fetch_profile_email", return_value="ob@gmail.test"),
    ):
        resp = client.get(
            f"/api/v1/google/callback?code=abc&state={state}",
            follow_redirects=False,
        )
    assert resp.status_code == 302
    assert "/onboarding?google=connected" in resp.headers["location"]


def test_callback_rejects_bad_state(client, google_env):
    resp = client.get(
        "/api/v1/google/callback?code=abc&state=not-a-valid-token",
        follow_redirects=False,
    )
    assert resp.status_code == 302
    assert "google=error" in resp.headers["location"]


def test_callback_requires_refresh_token(client, google_env):
    state = google_sync.make_state_token("test:user1")
    with patch("web.google_sync.exchange_code", return_value={"access_token": "at"}):
        resp = client.get(
            f"/api/v1/google/callback?code=abc&state={state}",
            follow_redirects=False,
        )
    assert resp.status_code == 302
    assert "google=error" in resp.headers["location"]


def test_connect_status_disconnect_lifecycle(
    client, auth_headers, auth_token, google_env, jwt_secret
):
    from jose import jwt as jose_jwt

    user_id = jose_jwt.decode(auth_token, jwt_secret, algorithms=["HS256"])["sub"]
    state = google_sync.make_state_token(user_id)

    with (
        patch(
            "web.google_sync.exchange_code",
            return_value={"refresh_token": "rt-123", "access_token": "at-456"},
        ),
        patch("web.google_sync.fetch_profile_email", return_value="me@gmail.test"),
    ):
        resp = client.get(
            f"/api/v1/google/callback?code=abc&state={state}",
            follow_redirects=False,
        )
    assert resp.status_code == 302
    assert "google=connected" in resp.headers["location"]

    status = client.get("/api/v1/google/status", headers=auth_headers).json()
    assert status == {"available": True, "connected": True, "email": "me@gmail.test"}

    resp = client.post("/api/v1/google/disconnect", headers=auth_headers)
    assert resp.status_code == 200
    status = client.get("/api/v1/google/status", headers=auth_headers).json()
    assert status["connected"] is False


def test_google_requires_auth(client):
    assert client.get("/api/v1/google/status").status_code in (401, 403)
    assert client.get("/api/v1/google/auth-url").status_code in (401, 403)


def test_brief_includes_calendar_and_email_when_connected(client, auth_headers):
    events = [
        {
            "title": "Design review",
            "start": "2026-07-02T15:00:00+00:00",
            "end": "2026-07-02T16:00:00+00:00",
            "all_day": False,
            "location": "Meet",
        }
    ]
    emails = [
        {
            "from": "Sam <sam@work.test>",
            "subject": "Launch plan sign-off needed",
            "date": "Thu, 2 Jul 2026 09:00:00 +0000",
            "snippet": "Can you confirm the scope by Friday?",
        }
    ]
    with (
        patch("web.brief_generator._resolve_llm", return_value=(None, None, None)),
        patch("web.google_sync.fetch_calendar_events", return_value=events),
        patch("web.google_sync.fetch_important_emails", return_value=emails),
    ):
        brief = client.post("/api/v1/brief/generate?force=true", headers=auth_headers).json()

    kinds = {section["kind"]: section for section in brief["sections"]}
    assert "calendar" in kinds
    assert "Design review" in kinds["calendar"]["body"]
    assert kinds["calendar"]["items"] == events
    assert "email" in kinds
    assert "Launch plan sign-off needed" in kinds["email"]["body"]


def test_brief_omits_google_sections_when_not_connected(client, auth_headers):
    with (
        patch("web.brief_generator._resolve_llm", return_value=(None, None, None)),
        patch("web.google_sync.fetch_calendar_events", return_value=None),
        patch("web.google_sync.fetch_important_emails", return_value=None),
    ):
        brief = client.post("/api/v1/brief/generate?force=true", headers=auth_headers).json()

    kinds = [section["kind"] for section in brief["sections"]]
    assert "calendar" not in kinds
    assert "email" not in kinds
    assert "signals" in kinds
