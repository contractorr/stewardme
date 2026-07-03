"""Bring-your-own-credential Gmail + Calendar route tests.

Only the network verification calls (iCal fetch, IMAP login) are mocked; the
credential store round-trip through per-user secrets is exercised for real.
"""

from unittest.mock import AsyncMock, patch

import pytest

CAL = "/api/v1/google/calendar"
GMAIL = "/api/v1/google/gmail"
STATUS = "/api/v1/google/status"

ICAL_URL = (
    "https://calendar.google.com/calendar/ical/x%40group.calendar.google.com/private-abc/basic.ics"
)


@pytest.fixture(autouse=True)
def _clean_after(client, auth_headers):
    """Ensure no connection leaks between tests (shared session client/DB)."""
    yield
    client.delete(CAL, headers=auth_headers)
    client.delete(GMAIL, headers=auth_headers)


def test_status_shape_when_empty(client, auth_headers):
    resp = client.get(STATUS, headers=auth_headers)
    assert resp.status_code == 200
    body = resp.json()
    assert set(body) == {"calendar_connected", "gmail_connected", "gmail_address"}
    assert body["calendar_connected"] is False
    assert body["gmail_connected"] is False


def test_status_requires_auth(client):
    assert client.get(STATUS).status_code in (401, 403)


def test_connect_calendar_happy(client, auth_headers):
    with patch("web.google_sync.verify_calendar", new=AsyncMock(return_value=None)):
        resp = client.put(CAL, json={"ical_url": ICAL_URL}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["calendar_connected"] is True
    # persisted: a fresh status call still reports connected
    assert client.get(STATUS, headers=auth_headers).json()["calendar_connected"] is True


def test_connect_calendar_bad_url_rejected(client, auth_headers):
    with patch(
        "web.google_sync.verify_calendar",
        new=AsyncMock(side_effect=ValueError("URL targets a non-public address")),
    ):
        resp = client.put(CAL, json={"ical_url": "http://169.254.169.254/"}, headers=auth_headers)
    assert resp.status_code == 400
    assert "non-public" in resp.json()["detail"]
    # nothing stored
    assert client.get(STATUS, headers=auth_headers).json()["calendar_connected"] is False


def test_disconnect_calendar(client, auth_headers):
    with patch("web.google_sync.verify_calendar", new=AsyncMock(return_value=None)):
        client.put(CAL, json={"ical_url": ICAL_URL}, headers=auth_headers)
    resp = client.delete(CAL, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["calendar_connected"] is False


def test_connect_gmail_happy(client, auth_headers):
    with patch("web.google_sync.verify_gmail", return_value=None):
        resp = client.put(
            GMAIL,
            json={"address": "me@gmail.com", "app_password": "abcd efgh ijkl mnop"},
            headers=auth_headers,
        )
    assert resp.status_code == 200
    body = resp.json()
    assert body["gmail_connected"] is True
    assert body["gmail_address"] == "me@gmail.com"


def test_connect_gmail_bad_login_rejected(client, auth_headers):
    with patch("web.google_sync.verify_gmail", side_effect=ValueError("Gmail login failed.")):
        resp = client.put(
            GMAIL,
            json={"address": "me@gmail.com", "app_password": "wrong"},
            headers=auth_headers,
        )
    assert resp.status_code == 400
    assert "login failed" in resp.json()["detail"].lower()
    assert client.get(STATUS, headers=auth_headers).json()["gmail_connected"] is False


def test_disconnect_gmail(client, auth_headers):
    with patch("web.google_sync.verify_gmail", return_value=None):
        client.put(
            GMAIL,
            json={"address": "me@gmail.com", "app_password": "abcd efgh ijkl mnop"},
            headers=auth_headers,
        )
    resp = client.delete(GMAIL, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["gmail_connected"] is False
