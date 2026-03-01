"""Research routes wrapping src/research/agent.py (per-user)."""

import asyncio

from fastapi import APIRouter, Depends, HTTPException

from web.auth import get_current_user
from web.deps import get_api_key_with_source, get_config, get_user_paths, safe_user_id

router = APIRouter(prefix="/api/research", tags=["research"])


def _get_agent(user_id: str):
    from intelligence.scraper import IntelStorage
    from journal.embeddings import EmbeddingManager
    from journal.storage import JournalStorage
    from research.agent import DeepResearchAgent

    config = get_config()
    paths = get_user_paths(user_id)

    journal_storage = JournalStorage(paths["journal_dir"])
    embeddings = EmbeddingManager(
        paths["chroma_dir"],
        collection_name=f"journal_{safe_user_id(user_id)}",
    )
    intel_storage = IntelStorage(paths["intel_db"])  # shared

    cfg = config.to_dict()

    # Overlay user's tavily_api_key if stored
    from web.deps import get_secret_key
    from web.user_store import get_user_secret

    try:
        tavily_key = get_user_secret(user_id, "tavily_api_key", get_secret_key())
        if tavily_key:
            cfg.setdefault("research", {})["api_key"] = tavily_key
    except Exception:
        pass

    return DeepResearchAgent(
        journal_storage=journal_storage,
        intel_storage=intel_storage,
        embeddings=embeddings,
        config=cfg,
    )


def _check_shared_key(user_id: str):
    """Block deep research for shared-key users — quality too poor on Haiku."""
    _key, source = get_api_key_with_source(user_id)
    if source == "shared":
        raise HTTPException(
            status_code=403,
            detail="Deep research requires your own API key. Add one in Settings to unlock.",
        )


@router.get("/topics")
async def get_topics(user: dict = Depends(get_current_user)):
    _check_shared_key(user["id"])
    try:
        agent = _get_agent(user["id"])
        return await asyncio.to_thread(agent.get_suggested_topics)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/run")
async def run_research(
    topic: str | None = None,
    user: dict = Depends(get_current_user),
):
    _check_shared_key(user["id"])
    try:
        agent = _get_agent(user["id"])
        results = await asyncio.to_thread(agent.run, specific_topic=topic)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
