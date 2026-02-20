"""Advisor routes wrapping AdvisorEngine (per-user)."""

from fastapi import APIRouter, Depends, HTTPException

from web.auth import get_current_user
from web.deps import get_api_key_for_user, get_config, get_user_paths
from web.models import AdvisorAsk, AdvisorResponse

router = APIRouter(prefix="/api/advisor", tags=["advisor"])


def _get_engine(user_id: str):
    from advisor.engine import AdvisorEngine
    from advisor.rag import RAGRetriever
    from intelligence.scraper import IntelStorage
    from journal.embeddings import EmbeddingManager
    from journal.storage import JournalStorage

    config = get_config()
    paths = get_user_paths(user_id)

    journal_storage = JournalStorage(paths["journal_dir"])
    embeddings = EmbeddingManager(
        paths["chroma_dir"],
        collection_name=f"journal_{user_id}",
    )
    intel_storage = IntelStorage(paths["intel_db"])  # shared

    rag = RAGRetriever(
        journal_storage=journal_storage,
        embedding_manager=embeddings,
        intel_storage=intel_storage,
        config=config.to_dict(),
    )

    api_key = get_api_key_for_user(user_id, config.llm.provider)
    return AdvisorEngine(
        rag=rag,
        api_key=api_key,
        model=config.llm.model,
        provider=config.llm.provider,
    )


@router.post("/ask", response_model=AdvisorResponse)
async def ask_advisor(
    body: AdvisorAsk,
    user: dict = Depends(get_current_user),
):
    try:
        engine = _get_engine(user["id"])
        answer = engine.ask(body.question, advice_type=body.advice_type)
        return AdvisorResponse(answer=answer, advice_type=body.advice_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
