"""Learning path CRUD + generation routes."""

import structlog
from fastapi import APIRouter, Depends, HTTPException

from web.auth import get_current_user
from web.deps import get_api_key_for_user, get_config, get_user_paths, safe_user_id
from web.models import LearningGenerate, LearningProgress

logger = structlog.get_logger()

router = APIRouter(prefix="/api/learning", tags=["learning"])


def _get_storage(user_id: str):
    from advisor.learning_paths import LearningPathStorage

    paths = get_user_paths(user_id)
    return LearningPathStorage(paths["learning_paths_dir"])


@router.get("")
async def list_paths(
    status: str | None = None,
    user: dict = Depends(get_current_user),
):
    storage = _get_storage(user["id"])
    return storage.list_paths(status=status)


@router.get("/{path_id}")
async def get_path(
    path_id: str,
    user: dict = Depends(get_current_user),
):
    storage = _get_storage(user["id"])
    result = storage.get(path_id)
    if not result:
        raise HTTPException(status_code=404, detail="Learning path not found")
    return result


@router.post("/{path_id}/progress")
async def update_progress(
    path_id: str,
    body: LearningProgress,
    user: dict = Depends(get_current_user),
):
    storage = _get_storage(user["id"])
    ok = storage.update_progress(path_id, body.completed_modules)
    if not ok:
        raise HTTPException(status_code=404, detail="Learning path not found")
    return {"ok": True}


@router.post("/generate")
async def generate_path(
    body: LearningGenerate,
    user: dict = Depends(get_current_user),
):
    """Generate a new learning path via LLM."""
    user_id = user["id"]
    config = get_config()
    api_key = get_api_key_for_user(user_id, config.llm.provider)
    if not api_key:
        raise HTTPException(status_code=400, detail="No LLM API key configured")

    try:
        from advisor.learning_paths import LearningPathGenerator
        from advisor.rag import RAGRetriever
        from journal.embeddings import EmbeddingManager
        from journal.search import JournalSearch
        from journal.storage import JournalStorage
        from llm.factory import create_provider

        paths = get_user_paths(user_id)
        journal_storage = JournalStorage(paths["journal_dir"])
        embeddings = EmbeddingManager(
            paths["chroma_dir"],
            collection_name=f"journal_{safe_user_id(user_id)}",
        )
        journal_search = JournalSearch(journal_storage, embeddings)

        rag = RAGRetriever(
            journal_search=journal_search,
            intel_db_path=paths["intel_db"],
            profile_path=str(paths["profile"]),
        )

        provider = create_provider(
            provider=config.llm.provider,
            api_key=api_key,
            model=config.llm.model,
        )

        def llm_caller(system, prompt, max_tokens=2000):
            return provider.generate(system=system, prompt=prompt, max_tokens=max_tokens)

        storage = _get_storage(user_id)
        gen = LearningPathGenerator(rag, llm_caller, storage)
        filepath = gen.generate(
            body.skill,
            current_level=body.current_level,
            target_level=body.target_level,
        )

        # Return the created path
        result = storage.get(filepath.stem.split("_")[-1])
        if not result:
            # Fallback: read latest
            paths_list = storage.list_paths()
            result = paths_list[0] if paths_list else {"id": "", "skill": body.skill}

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error("learning.generate_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
