"""Research routes wrapping src/research/agent.py."""

from fastapi import APIRouter, Depends, HTTPException

from web.auth import get_current_user
from web.deps import get_coach_paths, get_config

router = APIRouter(prefix="/api/research", tags=["research"])


def _get_agent():
    from intelligence.scraper import IntelStorage
    from journal.embeddings import EmbeddingManager
    from journal.storage import JournalStorage
    from research.agent import DeepResearchAgent

    config = get_config()
    paths = get_coach_paths()

    journal_storage = JournalStorage(paths["journal_dir"])
    embeddings = EmbeddingManager(paths["chroma_dir"], journal_storage)
    intel_storage = IntelStorage(paths["intel_db"])

    return DeepResearchAgent(
        journal_storage=journal_storage,
        intel_storage=intel_storage,
        embeddings=embeddings,
        config=config.to_dict(),
    )


@router.get("/topics")
async def get_topics(user: dict = Depends(get_current_user)):
    try:
        agent = _get_agent()
        return agent.get_suggested_topics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/run")
async def run_research(
    topic: str | None = None,
    user: dict = Depends(get_current_user),
):
    try:
        agent = _get_agent()
        results = agent.run(specific_topic=topic)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
