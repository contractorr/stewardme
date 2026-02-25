"""Topic trend routes."""

import asyncio

import structlog
from fastapi import APIRouter, Depends

from web.auth import get_current_user
from web.deps import get_user_paths, safe_user_id

logger = structlog.get_logger()

router = APIRouter(prefix="/api/trends", tags=["trends"])


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
                collection_name=f"journal_{safe_user_id(user['id'])}",
            )
        except Exception:
            return []

        search = JournalSearch(storage, embeddings)
        detector = TrendDetector(search)
        return await asyncio.to_thread(detector.detect_trends, days=days, window=window)
    except Exception as e:
        logger.error("trends.topics_error", error=str(e))
        return []
