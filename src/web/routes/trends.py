"""Mood + topic trend routes."""

import structlog
from fastapi import APIRouter, Depends, HTTPException

from web.auth import get_current_user
from web.deps import get_user_paths

logger = structlog.get_logger()

router = APIRouter(prefix="/api/trends", tags=["trends"])


@router.get("/mood")
async def get_mood(
    days: int = 30,
    user: dict = Depends(get_current_user),
):
    """Mood timeline from journal sentiment analysis."""
    try:
        from journal.sentiment import get_mood_history
        from journal.storage import JournalStorage

        paths = get_user_paths(user["id"])
        storage = JournalStorage(paths["journal_dir"])
        return get_mood_history(storage, days=days)
    except Exception as e:
        logger.error("trends.mood_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/topics")
async def get_topics(
    days: int = 90,
    window: str = "weekly",
    user: dict = Depends(get_current_user),
):
    """Topic trends via embedding clustering."""
    try:
        from journal.embeddings import EmbeddingManager
        from journal.search import JournalSearch
        from journal.storage import JournalStorage
        from journal.trends import TrendDetector

        paths = get_user_paths(user["id"])
        storage = JournalStorage(paths["journal_dir"])

        try:
            embeddings = EmbeddingManager(
                paths["chroma_dir"],
                collection_name=f"journal_{user['id']}",
            )
        except Exception:
            return []

        search = JournalSearch(storage, embeddings)
        detector = TrendDetector(search)
        return detector.detect_trends(days=days, window=window)
    except Exception as e:
        logger.error("trends.topics_error", error=str(e))
        return []
