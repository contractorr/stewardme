"""Advisor routes wrapping AdvisorEngine."""

from fastapi import APIRouter, Depends, HTTPException

from web.auth import get_current_user
from web.deps import get_api_key_for_provider, get_coach_paths, get_config
from web.models import AdvisorAsk, AdvisorResponse

router = APIRouter(prefix="/api/advisor", tags=["advisor"])


def _get_engine():
    from advisor.engine import AdvisorEngine
    from advisor.rag import RAGRetriever
    from intelligence.scraper import IntelStorage
    from journal.embeddings import EmbeddingManager
    from journal.storage import JournalStorage

    config = get_config()
    paths = get_coach_paths()

    journal_storage = JournalStorage(paths["journal_dir"])
    embeddings = EmbeddingManager(paths["chroma_dir"], journal_storage)
    intel_storage = IntelStorage(paths["intel_db"])

    rag = RAGRetriever(
        journal_storage=journal_storage,
        embedding_manager=embeddings,
        intel_storage=intel_storage,
        config=config.to_dict(),
    )

    api_key = get_api_key_for_provider(config.llm.provider)
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
        engine = _get_engine()
        answer = engine.ask(body.question, advice_type=body.advice_type)
        return AdvisorResponse(answer=answer, advice_type=body.advice_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
