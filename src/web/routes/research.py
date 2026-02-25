"""Research routes wrapping src/research/agent.py (per-user)."""

import asyncio

from fastapi import APIRouter, Depends, HTTPException

from web.auth import get_current_user
from web.deps import get_config, get_user_paths, safe_user_id

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

    return DeepResearchAgent(
        journal_storage=journal_storage,
        intel_storage=intel_storage,
        embeddings=embeddings,
        config=config.to_dict(),
    )


@router.get("/topics")
async def get_topics(user: dict = Depends(get_current_user)):
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
    try:
        agent = _get_agent(user["id"])
        results = await asyncio.to_thread(agent.run, specific_topic=topic)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
