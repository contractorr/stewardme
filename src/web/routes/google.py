"""Google (Gmail + Calendar) connection routes: status, auth-url, callback, disconnect."""

import os

import structlog
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse

from web import google_sync
from web.auth import get_current_user

logger = structlog.get_logger()

router = APIRouter(prefix="/api/google", tags=["google"])


def _frontend_redirect(result: str) -> RedirectResponse:
    origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
    return RedirectResponse(url=f"{origin}/brief?google={result}", status_code=302)


@router.get("/status")
async def google_status(user: dict = Depends(get_current_user)):
    available = google_sync.is_configured()
    connected = available and google_sync.is_connected(user["id"])
    return {
        "available": available,
        "connected": connected,
        "email": google_sync.get_connected_email(user["id"]) if connected else None,
    }


@router.get("/auth-url")
async def google_auth_url(user: dict = Depends(get_current_user)):
    if not google_sync.is_configured():
        raise HTTPException(status_code=503, detail="Google integration is not configured")
    state = google_sync.make_state_token(user["id"])
    return {"url": google_sync.build_auth_url(state)}


@router.get("/callback")
async def google_callback(
    code: str | None = Query(None),
    state: str | None = Query(None),
    error: str | None = Query(None),
):
    """OAuth redirect target - unauthenticated; identity comes from the signed state."""
    if error or not code or not state:
        return _frontend_redirect("error")

    user_id = google_sync.decode_state_token(state)
    if not user_id:
        return _frontend_redirect("error")

    try:
        tokens = google_sync.exchange_code(code)
    except Exception as exc:
        logger.warning("google.code_exchange_failed", error=str(exc))
        return _frontend_redirect("error")

    refresh_token = tokens.get("refresh_token")
    if not refresh_token:
        logger.warning("google.no_refresh_token", user_id=user_id)
        return _frontend_redirect("error")

    email = None
    access_token = tokens.get("access_token")
    if access_token:
        email = google_sync.fetch_profile_email(access_token)

    try:
        google_sync.store_connection(user_id, refresh_token, email)
    except Exception as exc:
        logger.warning("google.store_connection_failed", error=str(exc))
        return _frontend_redirect("error")

    return _frontend_redirect("connected")


@router.post("/disconnect")
async def google_disconnect(user: dict = Depends(get_current_user)):
    google_sync.clear_connection(user["id"])
    return {"ok": True}
