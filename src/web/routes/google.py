"""Bring-your-own-credential Gmail + Calendar connection routes.

The user supplies their own read credentials (secret iCal URL for Calendar;
address + app password for Gmail over IMAP). Each is verified before storage
and kept Fernet-encrypted in per-user secrets. No OAuth / no Google app
verification. Google OAuth *sign-in* is unrelated and handled by NextAuth.
"""

import structlog
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from web import google_sync
from web.auth import get_current_user

logger = structlog.get_logger()

router = APIRouter(prefix="/api/google", tags=["google"])


class CalendarConnect(BaseModel):
    ical_url: str


class GmailConnect(BaseModel):
    address: str
    app_password: str


@router.get("/status")
async def google_status(user: dict = Depends(get_current_user)):
    return google_sync.status(user["id"])


@router.put("/calendar")
async def connect_calendar(body: CalendarConnect, user: dict = Depends(get_current_user)):
    try:
        await google_sync.verify_calendar(body.ical_url)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    google_sync.store_calendar(user["id"], body.ical_url)
    return google_sync.status(user["id"])


@router.delete("/calendar")
async def disconnect_calendar(user: dict = Depends(get_current_user)):
    google_sync.clear_calendar(user["id"])
    return google_sync.status(user["id"])


@router.put("/gmail")
async def connect_gmail(body: GmailConnect, user: dict = Depends(get_current_user)):
    try:
        google_sync.verify_gmail(body.address, body.app_password)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    google_sync.store_gmail(user["id"], body.address, body.app_password)
    return google_sync.status(user["id"])


@router.delete("/gmail")
async def disconnect_gmail(user: dict = Depends(get_current_user)):
    google_sync.clear_gmail(user["id"])
    return google_sync.status(user["id"])
