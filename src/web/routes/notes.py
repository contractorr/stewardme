"""Note polish routes — messy text in, reviewed + sanitized HTML out."""

import asyncio
from pathlib import Path

import structlog
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from llm import LLMError, create_llm_provider
from notes.models import Note
from notes.polisher import MAX_NOTE_CHARS, NotePolisher, NotePolishError
from notes.rendering import markdown_to_html, sanitize_html
from notes.store import NotesStore
from web.auth import get_current_user
from web.deps import (
    SHARED_LLM_MODEL,
    enforce_shared_key_usage_limit,
    get_config,
    get_user_paths,
    resolve_llm_credentials_for_user,
)
from web.user_store import log_event

logger = structlog.get_logger()
router = APIRouter(prefix="/api/notes", tags=["notes"])


# --- Request/response schemas (route-local; web/models.py is a guarded hotspot) ---


class NotePolishRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=MAX_NOTE_CHARS)
    title: str = Field(default="", max_length=200)


class NoteCorrection(BaseModel):
    type: str = "rewording"
    original: str = ""
    corrected: str = ""
    reason: str = ""


class NoteSummaryResponse(BaseModel):
    id: str
    title: str = ""
    status: str = "pending"
    created_at: str | None = None
    accepted_at: str | None = None


class NoteResponse(NoteSummaryResponse):
    original_text: str | None = None
    polished_markdown: str = ""
    polished_html: str = ""
    diff: str = ""
    corrections: list[NoteCorrection] = Field(default_factory=list)


def _get_store(user_id: str) -> NotesStore:
    paths = get_user_paths(user_id)
    return NotesStore(Path(paths["data_dir"]) / "notes.db")


def _build_polisher(user_id: str) -> NotePolisher:
    provider_name, api_key, source = resolve_llm_credentials_for_user(user_id)
    if not api_key:
        raise HTTPException(status_code=400, detail="No LLM API key configured")
    config = get_config()
    model = SHARED_LLM_MODEL if source == "shared" else config.llm.model
    try:
        llm = create_llm_provider(
            provider=provider_name or config.llm.provider, api_key=api_key, model=model
        )
    except LLMError as exc:
        logger.warning("notes.llm_init_failed", user_id=user_id, error=str(exc))
        raise HTTPException(status_code=503, detail="Note polishing is currently unavailable.")
    return NotePolisher(llm)


def _shape_summary(note: Note) -> NoteSummaryResponse:
    return NoteSummaryResponse(
        id=note.id,
        title=note.title,
        status=note.status,
        created_at=note.created_at.isoformat() if note.created_at else None,
        accepted_at=note.accepted_at.isoformat() if note.accepted_at else None,
    )


def _shape_note(note: Note) -> NoteResponse:
    return NoteResponse(
        **_shape_summary(note).model_dump(),
        original_text=note.original_text if note.status == "pending" else None,
        polished_markdown=note.polished_markdown,
        polished_html=note.polished_html,
        diff=note.diff,
        corrections=note.corrections,
    )


@router.post(
    "/polish",
    response_model=NoteResponse,
    status_code=201,
    dependencies=[Depends(enforce_shared_key_usage_limit)],
)
async def polish_note(payload: NotePolishRequest, user: dict = Depends(get_current_user)):
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=422, detail="Note text is empty")

    polisher = _build_polisher(user["id"])
    try:
        result = await asyncio.to_thread(polisher.polish, text)
    except NotePolishError as exc:
        raise HTTPException(status_code=502, detail=f"{exc}. Please try again.")
    except LLMError as exc:
        logger.warning("notes.polish_failed", user_id=user["id"], error=str(exc))
        raise HTTPException(status_code=502, detail="Polishing failed. Please try again.")

    html = sanitize_html(markdown_to_html(result.polished_markdown))
    title = payload.title.strip() or _derive_title(result.polished_markdown)

    store = _get_store(user["id"])
    note = store.create_pending(user["id"], title, text, result, html)
    log_event(user["id"], "note_polished", {"note_id": note.id, "chars": len(text)})
    return _shape_note(note)


@router.get("", response_model=list[NoteSummaryResponse])
async def list_notes(
    status: str | None = Query(default=None, pattern="^(pending|accepted)$"),
    user: dict = Depends(get_current_user),
):
    store = _get_store(user["id"])
    return [_shape_summary(note) for note in store.list_notes(user["id"], status=status)]


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: str, user: dict = Depends(get_current_user)):
    store = _get_store(user["id"])
    note = store.get_note(user["id"], note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return _shape_note(note)


@router.post("/{note_id}/accept", response_model=NoteResponse)
async def accept_note(note_id: str, user: dict = Depends(get_current_user)):
    store = _get_store(user["id"])
    note = store.accept(user["id"], note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    log_event(user["id"], "note_accepted", {"note_id": note_id})
    return _shape_note(note)


@router.post("/{note_id}/discard", status_code=204)
async def discard_note(note_id: str, user: dict = Depends(get_current_user)):
    store = _get_store(user["id"])
    if not store.delete(user["id"], note_id):
        raise HTTPException(status_code=404, detail="Note not found")
    log_event(user["id"], "note_discarded", {"note_id": note_id})


def _derive_title(markdown: str) -> str:
    for line in markdown.splitlines():
        stripped = line.strip().lstrip("#").strip()
        if stripped:
            return stripped[:80]
    return "Untitled note"
