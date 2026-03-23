"""Notification routes — list, count, mark-read."""

from fastapi import APIRouter, Depends, Query

from web.auth import get_current_user
from web.notification_store import NotificationStore

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


def _get_store(user_id: str) -> NotificationStore:
    from web.deps import get_user_paths

    paths = get_user_paths(user_id)
    return NotificationStore(paths["data_dir"])


@router.get("")
async def list_notifications(
    limit: int = Query(20, ge=1, le=100),
    unread_only: bool = Query(False),
    user: dict = Depends(get_current_user),
):
    from web.notification_sources import compute_notifications

    store = _get_store(user["id"])
    notifications = compute_notifications(user["id"], store)
    if unread_only:
        notifications = [n for n in notifications if not n["read"]]
    return notifications[:limit]


@router.get("/count")
async def notification_count(user: dict = Depends(get_current_user)):
    from web.notification_sources import compute_notifications

    store = _get_store(user["id"])
    notifications = compute_notifications(user["id"], store)
    unread = sum(1 for n in notifications if not n["read"])
    return {"unread": unread}


@router.post("/{notification_id}/read")
async def mark_read(notification_id: str, user: dict = Depends(get_current_user)):
    store = _get_store(user["id"])
    store.mark_read(notification_id)
    return {"ok": True}


@router.post("/read-all")
async def mark_all_read(user: dict = Depends(get_current_user)):
    from web.notification_sources import compute_notifications

    store = _get_store(user["id"])
    notifications = compute_notifications(user["id"], store)
    for n in notifications:
        if not n["read"]:
            store.mark_read(n["id"])
    return {"ok": True}
