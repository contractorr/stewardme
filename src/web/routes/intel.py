"""Intelligence feed routes."""

from fastapi import APIRouter, Depends, HTTPException, Query

from intelligence.scraper import IntelStorage
from web.auth import get_current_user
from web.deps import get_coach_paths, get_config

router = APIRouter(prefix="/api/intel", tags=["intel"])


def _get_storage() -> IntelStorage:
    paths = get_coach_paths()
    return IntelStorage(paths["intel_db"])


@router.get("/recent")
async def get_recent(
    days: int = Query(default=7, ge=1, le=90),
    limit: int = Query(default=50, ge=1, le=200),
    user: dict = Depends(get_current_user),
):
    storage = _get_storage()
    return storage.get_recent(days=days, limit=limit)


@router.get("/search")
async def search_intel(
    q: str = Query(..., max_length=500),
    limit: int = Query(default=20, ge=1, le=100),
    user: dict = Depends(get_current_user),
):
    storage = _get_storage()
    return storage.search(q, limit=limit)


@router.get("/health")
async def get_health(user: dict = Depends(get_current_user)):
    """Get scraper health status for all sources."""
    from intelligence.health import ScraperHealthTracker

    paths = get_coach_paths()
    tracker = ScraperHealthTracker(paths["intel_db"])
    return {"scrapers": tracker.get_all_health()}


@router.post("/scrape")
async def scrape_now(user: dict = Depends(get_current_user)):
    """Trigger immediate scrape of all sources."""
    try:
        from intelligence.scheduler import IntelScheduler
        from journal.embeddings import EmbeddingManager
        from journal.storage import JournalStorage

        config = get_config()
        paths = get_coach_paths()
        storage = _get_storage()
        journal_storage = JournalStorage(paths["journal_dir"])
        embeddings = EmbeddingManager(paths["chroma_dir"])

        scheduler = IntelScheduler(
            storage=storage,
            config=config.to_dict().get("sources", {}),
            journal_storage=journal_storage,
            embeddings=embeddings,
            full_config=config.to_dict(),
        )
        result = await scheduler._run_async()
        return {"status": "completed", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
