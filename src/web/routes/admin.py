"""Admin analytics routes."""

from fastapi import APIRouter, Depends, Query

from web.auth import get_admin_user
from web.user_store import get_usage_stats

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/stats")
async def get_stats(
    days: int = Query(default=30, ge=1, le=365),
    user: dict = Depends(get_admin_user),
):
    return get_usage_stats(days=days)
