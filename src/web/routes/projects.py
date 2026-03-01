"""Project discovery routes — matching issues + idea generation."""

import asyncio

import structlog
from fastapi import APIRouter, Depends, HTTPException

from web.auth import get_current_user
from web.deps import get_api_key_for_user, get_config, get_user_paths, safe_user_id

logger = structlog.get_logger()

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("/issues")
async def get_issues(
    limit: int = 20,
    days: int = 14,
    user: dict = Depends(get_current_user),
):
    """Get GitHub issues matching user profile."""
    try:
        from advisor.projects import get_matching_issues
        from intelligence.scraper import IntelStorage

        paths = get_user_paths(user["id"])
        intel = IntelStorage(paths["intel_db"])

        profile = None
        try:
            from profile.storage import ProfileStorage

            ps = ProfileStorage(paths["profile"])
            profile = ps.load()
        except Exception:
            pass

        results = get_matching_issues(intel, profile, limit=limit, days=days)
        # Normalize output
        return [
            {
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "summary": r.get("summary", ""),
                "tags": (
                    r.get("tags", "").split(",")
                    if isinstance(r.get("tags"), str)
                    else r.get("tags", [])
                ),
                "source": r.get("source", ""),
                "match_score": r.get("_match_score", 0),
            }
            for r in results
        ]
    except Exception as e:
        logger.error("projects.issues_error", error=str(e))
        return []


@router.post("/ideas")
async def generate_ideas(
    user: dict = Depends(get_current_user),
):
    """Generate project ideas via LLM."""
    user_id = user["id"]
    config = get_config()
    api_key = get_api_key_for_user(user_id, config.llm.provider)
    if not api_key:
        raise HTTPException(status_code=400, detail="No LLM API key configured")

    try:
        from advisor.projects import ProjectIdeaGenerator
        from advisor.rag import RAGRetriever
        from journal.embeddings import EmbeddingManager
        from journal.fts import JournalFTSIndex
        from journal.search import JournalSearch
        from journal.storage import JournalStorage
        from llm.factory import create_llm_provider

        paths = get_user_paths(user_id)
        journal_storage = JournalStorage(paths["journal_dir"])
        embeddings = EmbeddingManager(
            paths["chroma_dir"],
            collection_name=f"journal_{safe_user_id(user_id)}",
        )
        fts_index = JournalFTSIndex(paths["journal_dir"])
        journal_search = JournalSearch(journal_storage, embeddings, fts_index=fts_index)

        rag = RAGRetriever(
            journal_search=journal_search,
            intel_db_path=paths["intel_db"],
            profile_path=str(paths["profile"]),
        )

        provider = create_llm_provider(
            provider=config.llm.provider,
            api_key=api_key,
            model=config.llm.model,
        )

        def llm_caller(system, prompt, max_tokens=2000):
            return provider.generate(system=system, prompt=prompt, max_tokens=max_tokens)

        gen = ProjectIdeaGenerator(rag, llm_caller)
        ideas = await asyncio.to_thread(gen.generate_ideas)
        return {"ideas": ideas}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("projects.ideas_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
