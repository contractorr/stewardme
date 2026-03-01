"""Intelligence feed routes."""

from urllib.parse import urlparse

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from intelligence.scraper import IntelStorage
from web.auth import get_current_user
from web.deps import get_coach_paths, get_config
from web.user_store import (
    add_user_rss_feed,
    get_user_rss_feeds,
    remove_user_rss_feed,
)

router = APIRouter(prefix="/api/intel", tags=["intel"])


class RSSFeedAdd(BaseModel):
    url: str
    name: str | None = None


class RSSFeedRemove(BaseModel):
    url: str


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


@router.get("/rss-feeds")
async def list_rss_feeds(user: dict = Depends(get_current_user)):
    """List user's custom RSS feeds."""
    return get_user_rss_feeds(user["id"])


@router.post("/rss-feeds")
async def add_rss_feed(body: RSSFeedAdd, user: dict = Depends(get_current_user)):
    """Validate and add an RSS feed."""
    parsed = urlparse(body.url)
    if parsed.scheme not in ("http", "https"):
        raise HTTPException(status_code=400, detail="URL must be http or https")

    # Validate feed is reachable and looks like RSS/Atom
    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            resp = await client.get(body.url, headers={"User-Agent": "CoachBot/1.0"})
            resp.raise_for_status()
            snippet = resp.text[:2048].lower()
            if "<rss" not in snippet and "<feed" not in snippet and "<channel" not in snippet:
                raise HTTPException(
                    status_code=400,
                    detail="URL does not appear to be a valid RSS/Atom feed",
                )
    except httpx.HTTPError as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch feed: {e}")

    feed = add_user_rss_feed(user["id"], body.url, body.name, added_by="user")
    return feed


@router.delete("/rss-feeds")
async def delete_rss_feed(body: RSSFeedRemove, user: dict = Depends(get_current_user)):
    """Remove a user's RSS feed."""
    removed = remove_user_rss_feed(user["id"], body.url)
    if not removed:
        raise HTTPException(status_code=404, detail="Feed not found")
    return {"ok": True}


@router.get("/trending")
async def get_trending(user: dict = Depends(get_current_user)):
    """Get cross-source trending topics."""
    from intelligence.trending_radar import TrendingRadar

    paths = get_coach_paths()
    config = get_config()
    tr_config = config.to_dict().get("trending_radar", {})

    radar = TrendingRadar(paths["intel_db"])
    snapshot = radar.load()
    if not snapshot:
        # Try to create a cheap LLM provider for better trending analysis
        llm = _get_cheap_llm(user["id"])
        snapshot = radar.refresh(
            llm=llm,
            days=tr_config.get("days", 7),
            min_source_families=tr_config.get("min_source_families", tr_config.get("min_sources", 2)),
            min_items=tr_config.get("min_items", 4),
            max_topics=tr_config.get("max_topics", 10),
        )
    return snapshot


def _get_cheap_llm(user_id: str):
    """Try to create a cheap LLM provider from user's key or env. Returns None on failure."""
    try:
        from llm import create_cheap_provider
        from web.deps import get_secret_key
        from web.user_store import get_user_secret

        fernet_key = get_secret_key()
        api_key = get_user_secret(user_id, "llm_api_key", fernet_key)
        provider_name = get_user_secret(user_id, "llm_provider", fernet_key) or "auto"
        if api_key:
            return create_cheap_provider(provider=provider_name, api_key=api_key)
        # Fall back to env-based provider
        return create_cheap_provider()
    except Exception:
        return None


@router.post("/scrape")
async def scrape_now(user: dict = Depends(get_current_user)):
    """Trigger immediate scrape of all sources."""
    try:
        from intelligence.scheduler import IntelScheduler
        from intelligence.sources import RSSFeedScraper
        from journal.embeddings import EmbeddingManager
        from journal.storage import JournalStorage
        from web.user_store import get_all_user_rss_feeds

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

        # Merge user-added RSS feeds
        config_urls = set(config.to_dict().get("sources", {}).get("rss_feeds", []))
        for feed in get_all_user_rss_feeds():
            if feed["url"] not in config_urls:
                scheduler._scrapers.append(
                    RSSFeedScraper(storage, feed["url"], name=feed.get("name"))
                )

        result = await scheduler._run_async()
        return {"status": "completed", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
