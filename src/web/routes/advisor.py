"""Advisor routes wrapping AdvisorEngine (per-user)."""

import asyncio
import json
import time
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.responses import StreamingResponse

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
from web.deps import get_api_key_for_user, get_config, get_user_paths, safe_user_id
from web.models import (
    AdvisorAsk,
    AdvisorResponse,
    ConversationDetail,
    ConversationListItem,
    ConversationMessage,
)
from web.user_store import log_event

router = APIRouter(prefix="/api/advisor", tags=["advisor"])

MAX_HISTORY_CHARS = 64_000  # ~16k tokens


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
        collection_name=f"journal_{safe_user_id(user_id)}",
    )
    intel_storage = IntelStorage(paths["intel_db"])  # shared
    journal_search = JournalSearch(journal_storage, embeddings)

    users_db = Path.home() / "coach" / "users.db"
    rag = RAGRetriever(
        journal_search=journal_search,
        intel_db_path=paths["intel_db"],
        profile_path=str(paths["profile"]),
        users_db_path=users_db,
        user_id=user_id,
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
            "user_id": user_id,
        }

    return AdvisorEngine(
        rag=rag,
        api_key=api_key,
        model=config.llm.model,
        provider=config.llm.provider,
        use_tools=use_tools,
        components=components,
    )


def _trim_history(messages: list[dict], max_chars: int = MAX_HISTORY_CHARS) -> list[dict]:
    """Keep most recent messages that fit within max_chars."""
    total = 0
    trimmed = []
    for msg in reversed(messages):
        total += len(msg.get("content", ""))
        if total > max_chars:
            break
        trimmed.append(msg)
    trimmed.reverse()
    return trimmed


@router.post("/ask", response_model=AdvisorResponse)
async def ask_advisor(
    body: AdvisorAsk,
    use_tools: bool = Query(True),
    user: dict = Depends(get_current_user),
):
    try:
        user_id = user["id"]
        conv_id = body.conversation_id

        # Create or validate conversation
        if not conv_id:
            title = body.question[:80].strip() or "New conversation"
            conv_id = create_conversation(user_id, title)
        elif not conversation_belongs_to(conv_id, user_id):
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Load history
        history_rows = get_messages(conv_id, limit=20)
        history = _trim_history(
            [{"role": m["role"], "content": m["content"]} for m in history_rows]
        )

        # Save user message
        add_message(conv_id, "user", body.question)

        engine = _get_engine(user_id, use_tools=use_tools)
        start = time.monotonic()
        answer = await asyncio.to_thread(
            engine.ask,
            body.question,
            advice_type=body.advice_type,
            conversation_history=history or None,
        )

        # Save assistant response
        add_message(conv_id, "assistant", answer)
        log_event("chat_query", user_id, {"latency_ms": int((time.monotonic() - start) * 1000)})

        return AdvisorResponse(answer=answer, advice_type=body.advice_type, conversation_id=conv_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask/stream")
async def ask_advisor_stream(
    body: AdvisorAsk,
    use_tools: bool = Query(True),
    user: dict = Depends(get_current_user),
):
    """SSE streaming version of /ask — emits tool_start/tool_done/answer events."""
    user_id = user["id"]
    conv_id = body.conversation_id

    # Create or validate conversation
    if not conv_id:
        title = body.question[:80].strip() or "New conversation"
        conv_id = create_conversation(user_id, title)
    elif not conversation_belongs_to(conv_id, user_id):
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Load history
    history_rows = get_messages(conv_id, limit=20)
    history = _trim_history([{"role": m["role"], "content": m["content"]} for m in history_rows])

    # Save user message
    add_message(conv_id, "user", body.question)

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
            start = time.monotonic()
            answer = await loop.run_in_executor(
                None,
                lambda: engine.ask(
                    body.question,
                    advice_type=body.advice_type,
                    conversation_history=history or None,
                    event_callback=_event_callback,
                ),
            )
            # Save assistant response
            add_message(conv_id, "assistant", answer)
            log_event("chat_query", user_id, {"latency_ms": int((time.monotonic() - start) * 1000)})
            # Only emit answer if agentic callback didn't already send one
            if not answer_sent:
                queue.put_nowait(
                    {
                        "type": "answer",
                        "content": answer,
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
