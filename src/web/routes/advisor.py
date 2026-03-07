"""Advisor routes wrapping AdvisorEngine (per-user)."""

import asyncio
import json

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.responses import StreamingResponse

from services.advice import (
    ConversationNotFoundError,
    finish_conversation_turn,
    run_advice,
    start_conversation_turn,
)
from web.auth import get_current_user
from web.conversation_store import (
    add_message,
    conversation_belongs_to,
    create_conversation,
    delete_conversation,
    get_conversation,
    get_messages,
    list_conversations,
)
from web.deps import (
    SHARED_LLM_MODEL,
    enforce_shared_key_usage_limit,
    get_api_key_with_source,
    get_config,
    get_intel_storage,
    get_memory_store,
    get_profile_path,
    get_thread_store,
    get_user_paths,
    safe_user_id,
)
from web.models import (
    AdvisorAsk,
    AdvisorResponse,
    ConversationDetail,
    ConversationListItem,
    ConversationMessage,
)
from web.user_store import get_default_db_path, log_event

router = APIRouter(prefix="/api/advisor", tags=["advisor"])



def _get_engine(user_id: str, use_tools: bool = False):
    from advisor.engine import AdvisorEngine
    from advisor.rag import RAGRetriever
    from journal.embeddings import EmbeddingManager
    from journal.fts import JournalFTSIndex
    from journal.search import JournalSearch
    from journal.storage import JournalStorage

    config = get_config()
    paths = get_user_paths(user_id)

    journal_storage = JournalStorage(paths["journal_dir"])
    embeddings = EmbeddingManager(
        paths["chroma_dir"],
        collection_name=f"journal_{safe_user_id(user_id)}",
    )
    intel_storage = get_intel_storage()
    fts_index = JournalFTSIndex(paths["journal_dir"])
    journal_search = JournalSearch(journal_storage, embeddings, fts_index=fts_index)

    # Per-user memory + thread stores for cross-conversation continuity
    fact_store = None
    thread_store = None
    memory_config = None
    if config.memory.enabled:
        fact_store = get_memory_store(user_id)
        memory_config = {
            "max_context_facts": config.memory.max_context_facts,
            "high_confidence_threshold": config.memory.high_confidence_threshold,
        }
    if config.threads.enabled:
        thread_store = get_thread_store(user_id)

    users_db = get_default_db_path()
    rag = RAGRetriever(
        journal_search=journal_search,
        intel_db_path=paths["intel_db"],
        profile_path=str(get_profile_path(user_id)),
        users_db_path=users_db,
        user_id=user_id,
        fact_store=fact_store,
        memory_config=memory_config,
        thread_store=thread_store,
    )

    api_key, source = get_api_key_with_source(user_id)
    is_shared = source == "shared"

    # Shared key: force Haiku, disable agentic mode
    model = SHARED_LLM_MODEL if is_shared else config.llm.model
    effective_use_tools = False if is_shared else use_tools

    # Build per-user components dict for agentic mode
    components = None
    if effective_use_tools:
        components = {
            "storage": journal_storage,
            "embeddings": embeddings,
            "intel_storage": intel_storage,
            "rag": rag,
            "profile_path": str(get_profile_path(user_id)),
            "recommendations_dir": paths["recommendations_dir"],
            "user_id": user_id,
        }

    rag_config = {"structured_profile": True, "xml_delimiters": True}
    if config.memory.enabled:
        rag_config["inject_memory"] = True
    if config.threads.enabled:
        rag_config["inject_recurring_thoughts"] = True

    return AdvisorEngine(
        rag=rag,
        api_key=api_key,
        model=model,
        provider=config.llm.provider,
        use_tools=effective_use_tools,
        components=components,
        rag_config=rag_config,
    )


@router.post("/ask", response_model=AdvisorResponse)
async def ask_advisor(
    body: AdvisorAsk,
    use_tools: bool = Query(True),
    user: dict = Depends(get_current_user),
    _rate_limit: None = Depends(enforce_shared_key_usage_limit),
):
    try:
        user_id = user["id"]
        conv_id, history = start_conversation_turn(
            user_id=user_id,
            conversation_id=body.conversation_id,
            question=body.question,
            create_conversation_fn=create_conversation,
            conversation_belongs_to_fn=conversation_belongs_to,
            get_messages_fn=get_messages,
            add_message_fn=add_message,
        )

        engine = _get_engine(user_id, use_tools=use_tools)
        result = await asyncio.to_thread(
            run_advice,
            engine,
            body.question,
            advice_type=body.advice_type,
            conversation_history=history or None,
        )

        finish_conversation_turn(
            conv_id=conv_id,
            user_id=user_id,
            answer=result["answer"],
            latency_ms=result["latency_ms"],
            add_message_fn=add_message,
            log_event_fn=log_event,
        )

        return AdvisorResponse(answer=result["answer"], advice_type=body.advice_type, conversation_id=conv_id)
    except ConversationNotFoundError:
        raise HTTPException(status_code=404, detail="Conversation not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask/stream")
async def ask_advisor_stream(
    body: AdvisorAsk,
    use_tools: bool = Query(True),
    user: dict = Depends(get_current_user),
    _rate_limit: None = Depends(enforce_shared_key_usage_limit),
):
    """SSE streaming version of /ask — emits tool_start/tool_done/answer events."""
    user_id = user["id"]

    try:
        conv_id, history = start_conversation_turn(
            user_id=user_id,
            conversation_id=body.conversation_id,
            question=body.question,
            create_conversation_fn=create_conversation,
            conversation_belongs_to_fn=conversation_belongs_to,
            get_messages_fn=get_messages,
            add_message_fn=add_message,
        )
    except ConversationNotFoundError:
        raise HTTPException(status_code=404, detail="Conversation not found")

    queue: asyncio.Queue[dict | None] = asyncio.Queue()

    answer_sent = False

    def _event_callback(event: dict):
        nonlocal answer_sent
        if event.get("type") == "answer":
            answer_sent = True
        queue.put_nowait(event)

    async def _run_engine():
        try:
            engine = _get_engine(user_id, use_tools=use_tools)
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: run_advice(
                    engine,
                    body.question,
                    advice_type=body.advice_type,
                    conversation_history=history or None,
                    event_callback=_event_callback,
                ),
            )
            finish_conversation_turn(
                conv_id=conv_id,
                user_id=user_id,
                answer=result["answer"],
                latency_ms=result["latency_ms"],
                add_message_fn=add_message,
                log_event_fn=log_event,
            )
            # Only emit answer if agentic callback didn't already send one
            if not answer_sent:
                queue.put_nowait(
                    {
                        "type": "answer",
                        "content": result["answer"],
                        "conversation_id": conv_id,
                        "advice_type": body.advice_type,
                    }
                )
        except Exception as exc:
            queue.put_nowait({"type": "error", "detail": str(exc)})
        finally:
            queue.put_nowait(None)  # sentinel

    async def _sse_generator():
        task = asyncio.create_task(_run_engine())
        try:
            while True:
                event = await queue.get()
                if event is None:
                    break
                # Enrich answer events with conversation metadata
                if event.get("type") == "answer":
                    event.setdefault("conversation_id", conv_id)
                    event.setdefault("advice_type", body.advice_type)
                yield f"data: {json.dumps(event)}\n\n"
        finally:
            task.cancel()

    return StreamingResponse(_sse_generator(), media_type="text/event-stream")


@router.get("/conversations", response_model=list[ConversationListItem])
async def list_user_conversations(
    user: dict = Depends(get_current_user),
):
    rows = list_conversations(user["id"])
    return [ConversationListItem(**r) for r in rows]


@router.get("/conversations/{conv_id}", response_model=ConversationDetail)
async def get_user_conversation(
    conv_id: str,
    user: dict = Depends(get_current_user),
):
    conv = get_conversation(conv_id, user["id"])
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return ConversationDetail(
        id=conv["id"],
        title=conv["title"],
        messages=[ConversationMessage(**m) for m in conv["messages"]],
    )


@router.delete("/conversations/{conv_id}")
async def delete_user_conversation(
    conv_id: str,
    user: dict = Depends(get_current_user),
):
    deleted = delete_conversation(conv_id, user["id"])
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"ok": True}
