"""Read-only Google (Gmail + Calendar) access for brief sections.

Backend-managed OAuth: authorization-code flow with offline access, refresh
token stored Fernet-encrypted in per-user secrets. Plain httpx against the
Google REST APIs - no SDK dependency. All access is read-only scoped.
"""

import os
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

import httpx
import structlog
from jose import JWTError, jwt

logger = structlog.get_logger()

AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
CALENDAR_EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
GMAIL_BASE = "https://gmail.googleapis.com/gmail/v1/users/me"

SCOPES = (
    "https://www.googleapis.com/auth/gmail.readonly "
    "https://www.googleapis.com/auth/calendar.readonly"
)

REFRESH_TOKEN_SECRET = "google_refresh_token"
ACCOUNT_EMAIL_SECRET = "google_account_email"

STATE_TTL_MINUTES = 10
HTTP_TIMEOUT = 20.0

GMAIL_QUERY = (
    "is:unread newer_than:7d (is:important OR category:primary) "
    "-category:promotions -category:social"
)


def is_configured() -> bool:
    return bool(os.getenv("GOOGLE_CLIENT_ID") and os.getenv("GOOGLE_CLIENT_SECRET"))


def _redirect_uri() -> str:
    return os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/v1/google/callback")


def _jwt_secret() -> str:
    return os.getenv("NEXTAUTH_SECRET", "")


def make_state_token(user_id: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=STATE_TTL_MINUTES)
    return jwt.encode(
        {"sub": user_id, "purpose": "google_oauth", "exp": expires},
        _jwt_secret(),
        algorithm="HS256",
    )


def decode_state_token(state: str) -> str | None:
    """Return the user id from a valid state token, else None."""
    try:
        payload = jwt.decode(state, _jwt_secret(), algorithms=["HS256"])
    except JWTError:
        return None
    if payload.get("purpose") != "google_oauth":
        return None
    return payload.get("sub")


def build_auth_url(state: str) -> str:
    params = {
        "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
        "redirect_uri": _redirect_uri(),
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
    }
    return f"{AUTH_ENDPOINT}?{urlencode(params)}"


def exchange_code(code: str) -> dict:
    """Exchange an authorization code for tokens. Raises httpx errors on failure."""
    response = httpx.post(
        TOKEN_ENDPOINT,
        data={
            "code": code,
            "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET", ""),
            "redirect_uri": _redirect_uri(),
            "grant_type": "authorization_code",
        },
        timeout=HTTP_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def store_connection(user_id: str, refresh_token: str, email: str | None) -> None:
    from user_crud import get_or_create_user
    from web.deps_base import get_secret_key
    from web.user_store import set_user_secret

    # The callback is unauthenticated (identity comes from the signed state),
    # so the user row may not exist yet on a fresh account.
    get_or_create_user(user_id)
    key = get_secret_key()
    set_user_secret(user_id, REFRESH_TOKEN_SECRET, refresh_token, key)
    if email:
        set_user_secret(user_id, ACCOUNT_EMAIL_SECRET, email, key)


def clear_connection(user_id: str) -> None:
    from web.user_store import delete_user_secret

    delete_user_secret(user_id, REFRESH_TOKEN_SECRET)
    delete_user_secret(user_id, ACCOUNT_EMAIL_SECRET)


def get_connected_email(user_id: str) -> str | None:
    try:
        from web.deps_base import get_secret_key
        from web.user_store import get_user_secret

        return get_user_secret(user_id, ACCOUNT_EMAIL_SECRET, get_secret_key())
    except Exception:
        return None


def is_connected(user_id: str) -> bool:
    try:
        from web.deps_base import get_secret_key
        from web.user_store import get_user_secret

        return bool(get_user_secret(user_id, REFRESH_TOKEN_SECRET, get_secret_key()))
    except Exception:
        return False


def _access_token(user_id: str) -> str | None:
    """Mint an access token from the stored refresh token; None when unavailable.

    A revoked refresh token (invalid_grant) clears the stored connection.
    """
    try:
        from web.deps_base import get_secret_key
        from web.user_store import get_user_secret

        refresh_token = get_user_secret(user_id, REFRESH_TOKEN_SECRET, get_secret_key())
    except Exception:
        return None
    if not refresh_token or not is_configured():
        return None

    try:
        response = httpx.post(
            TOKEN_ENDPOINT,
            data={
                "refresh_token": refresh_token,
                "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET", ""),
                "grant_type": "refresh_token",
            },
            timeout=HTTP_TIMEOUT,
        )
        if response.status_code == 400 and "invalid_grant" in response.text:
            logger.info("google.refresh_token_revoked", user_id=user_id)
            clear_connection(user_id)
            return None
        response.raise_for_status()
        return response.json().get("access_token")
    except httpx.HTTPError as exc:
        logger.warning("google.token_refresh_failed", error=str(exc))
        return None


def fetch_profile_email(access_token: str) -> str | None:
    try:
        response = httpx.get(
            f"{GMAIL_BASE}/profile",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=HTTP_TIMEOUT,
        )
        response.raise_for_status()
        return response.json().get("emailAddress")
    except httpx.HTTPError as exc:
        logger.warning("google.profile_fetch_failed", error=str(exc))
        return None


def fetch_calendar_events(user_id: str, days: int = 7) -> list[dict] | None:
    """Normalized events for the next `days` days; None when not connected/errored."""
    token = _access_token(user_id)
    if not token:
        return None

    now = datetime.now(timezone.utc)
    try:
        response = httpx.get(
            CALENDAR_EVENTS_URL,
            params={
                "timeMin": now.isoformat(),
                "timeMax": (now + timedelta(days=days)).isoformat(),
                "singleEvents": "true",
                "orderBy": "startTime",
                "maxResults": 50,
            },
            headers={"Authorization": f"Bearer {token}"},
            timeout=HTTP_TIMEOUT,
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        logger.warning("google.calendar_fetch_failed", error=str(exc))
        return None

    events = []
    for item in response.json().get("items", []):
        start = item.get("start", {})
        end = item.get("end", {})
        events.append(
            {
                "title": item.get("summary", "(no title)"),
                "start": start.get("dateTime") or start.get("date") or "",
                "end": end.get("dateTime") or end.get("date") or "",
                "all_day": "date" in start,
                "location": item.get("location", ""),
            }
        )
    return events


def fetch_important_emails(user_id: str, limit: int = 12) -> list[dict] | None:
    """Unread important/primary emails from the last week; None when unavailable."""
    token = _access_token(user_id)
    if not token:
        return None

    headers = {"Authorization": f"Bearer {token}"}
    try:
        listing = httpx.get(
            f"{GMAIL_BASE}/messages",
            params={"q": GMAIL_QUERY, "maxResults": limit},
            headers=headers,
            timeout=HTTP_TIMEOUT,
        )
        listing.raise_for_status()
    except httpx.HTTPError as exc:
        logger.warning("google.gmail_list_failed", error=str(exc))
        return None

    emails = []
    for ref in listing.json().get("messages", [])[:limit]:
        try:
            detail = httpx.get(
                f"{GMAIL_BASE}/messages/{ref['id']}",
                params={
                    "format": "metadata",
                    "metadataHeaders": ["From", "Subject", "Date"],
                },
                headers=headers,
                timeout=HTTP_TIMEOUT,
            )
            detail.raise_for_status()
        except httpx.HTTPError as exc:
            logger.warning("google.gmail_detail_failed", error=str(exc))
            continue
        payload = detail.json()
        header_map = {
            header["name"].lower(): header["value"]
            for header in payload.get("payload", {}).get("headers", [])
        }
        emails.append(
            {
                "from": header_map.get("from", ""),
                "subject": header_map.get("subject", "(no subject)"),
                "date": header_map.get("date", ""),
                "snippet": (payload.get("snippet") or "")[:200],
            }
        )
    return emails
