"""Engagement tracking routes."""

import structlog
from fastapi import APIRouter, Depends

from web.auth import get_current_user
from web.models import EngagementEvent, EngagementStats
from web.user_store import get_engagement_stats, log_engagement, log_event

logger = structlog.get_logger()

router = APIRouter(prefix="/api/engagement", tags=["engagement"])


@router.post("", status_code=201)
async def post_engagement(
    body: EngagementEvent,
    user: dict = Depends(get_current_user),
):
    logger.info(
        "engagement.event",
        user_id=user["id"],
        event_type=body.event_type,
        target_type=body.target_type,
        target_id=body.target_id,
    )
    log_engagement(
        user_id=user["id"],
        event_type=body.event_type,
        target_type=body.target_type,
        target_id=body.target_id,
        metadata=body.metadata,
    )
    if body.event_type in ("feedback_useful", "feedback_irrelevant"):
        log_event(
            "recommendation_feedback",
            user["id"],
            {
                "category": (body.metadata or {}).get("category", ""),
                "score": 1 if body.event_type == "feedback_useful" else -1,
            },
        )
    return {"ok": True}


@router.get("/stats", response_model=EngagementStats)
async def engagement_stats(
    user: dict = Depends(get_current_user),
):
    stats = get_engagement_stats(user["id"])
    return EngagementStats(**stats)
