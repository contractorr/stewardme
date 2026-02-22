"""Advisor routes wrapping AdvisorEngine (per-user)."""

from fastapi import APIRouter, Depends, HTTPException, Query

from web.auth import get_current_user
from web.deps import get_api_key_for_user, get_config, get_user_paths
from web.models import AdvisorAsk, AdvisorResponse

router = APIRouter(prefix="/api/advisor", tags=["advisor"])


def _get_engine(user_id: str, use_tools: bool = False):
    from advisor.engine import AdvisorEngine
    from advisor.rag import RAGRetriever
    from intelligence.scraper import IntelStorage
    from journal.embeddings import EmbeddingManager
    from journal.search import JournalSearch
    from journal.storage import JournalStorage

    config = get_config()
    paths = get_user_paths(user_id)

    journal_storage = JournalStorage(paths["journal_dir"])
    embeddings = EmbeddingManager(
        paths["chroma_dir"],
        collection_name=f"journal_{user_id}",
    )
    intel_storage = IntelStorage(paths["intel_db"])  # shared
    journal_search = JournalSearch(journal_storage, embeddings)

    rag = RAGRetriever(
        journal_search=journal_search,
        intel_db_path=paths["intel_db"],
        profile_path=str(paths["profile"]),
    )

    api_key = get_api_key_for_user(user_id, config.llm.provider)

    # Build per-user components dict for agentic mode
    components = None
    if use_tools:
        components = {
            "storage": journal_storage,
            "embeddings": embeddings,
            "intel_storage": intel_storage,
            "rag": rag,
            "profile_path": str(paths["profile"]),
            "recommendations_dir": paths["recommendations_dir"],
        }

    return AdvisorEngine(
        rag=rag,
        api_key=api_key,
        model=config.llm.model,
        provider=config.llm.provider,
        use_tools=use_tools,
        components=components,
    )


@router.post("/ask", response_model=AdvisorResponse)
async def ask_advisor(
    body: AdvisorAsk,
    use_tools: bool = Query(False),
    user: dict = Depends(get_current_user),
):
    try:
        engine = _get_engine(user["id"], use_tools=use_tools)
        answer = engine.ask(body.question, advice_type=body.advice_type)
        return AdvisorResponse(answer=answer, advice_type=body.advice_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
