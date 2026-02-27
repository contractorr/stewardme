"""Heartbeat notification routes — list, dismiss, status."""

import structlog
from fastapi import APIRouter, Depends, HTTPException

from intelligence.heartbeat import ActionBriefStore
from web.auth import get_current_user
from web.deps import get_user_paths
from web.models import HeartbeatNotification, HeartbeatStatus

logger = structlog.get_logger()

router = APIRouter(prefix="/api/heartbeat", tags=["heartbeat"])


def _get_store(user_id: str) -> ActionBriefStore:
    paths = get_user_paths(user_id)
    return ActionBriefStore(paths["intel_db"])


@router.get("/notifications", response_model=list[HeartbeatNotification])
async def get_notifications(
    limit: int = 20,
    user: dict = Depends(get_current_user),
):
    """List active (undismissed) heartbeat notifications."""
    store = _get_store(user["id"])
    rows = store.get_active(limit=limit)
    return [
        HeartbeatNotification(
            id=r.get("id", 0),
            intel_url=r.get("intel_url", ""),
            intel_title=r.get("intel_title", ""),
            intel_summary=r.get("intel_summary") or "",
            relevance=r.get("relevance", 0.0),
            urgency=r.get("urgency", ""),
            suggested_action=r.get("suggested_action", ""),
            reasoning=r.get("reasoning", ""),
            related_goal_id=r.get("related_goal_id"),
            created_at=str(r.get("created_at", "")),
        )
        for r in rows
    ]


@router.post("/notifications/{notification_id}/dismiss")
async def dismiss_notification(
    notification_id: int,
    user: dict = Depends(get_current_user),
):
    """Dismiss a heartbeat notification."""
    store = _get_store(user["id"])
    ok = store.dismiss(notification_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"ok": True}


@router.get("/status", response_model=HeartbeatStatus)
async def get_status(
    user: dict = Depends(get_current_user),
):
    """Get heartbeat status: last run time and active notification count."""
    store = _get_store(user["id"])
    last_run = store.get_last_run_at()
    active = store.get_active(limit=1000)
    return HeartbeatStatus(
        last_run_at=last_run.isoformat() if last_run else None,
        active_count=len(active),
    )
