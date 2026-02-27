"""Journal CRUD routes wrapping src/journal/storage.py (per-user)."""

from pathlib import Path

import structlog
from fastapi import APIRouter, Depends, HTTPException, status

from journal.storage import JournalStorage
from web.auth import get_current_user
from web.deps import get_user_paths
from web.models import JournalCreate, JournalEntry, JournalUpdate, QuickCapture
from web.user_store import log_event

logger = structlog.get_logger()

router = APIRouter(prefix="/api/journal", tags=["journal"])


def _generate_title(content: str, user_id: str) -> str | None:
    """Try to generate an LLM title; returns None on failure."""
    try:
        from journal.titler import generate_title
        from llm import create_cheap_provider
        from web.deps import get_api_key_for_user

        api_key = get_api_key_for_user(user_id)
        if not api_key:
            return None
        llm = create_cheap_provider(api_key=api_key)
        return generate_title(content, llm)
    except Exception:
        logger.debug("title_generation_skipped", user_id=user_id)
        return None


def _get_storage(user_id: str) -> JournalStorage:
    paths = get_user_paths(user_id)
    return JournalStorage(paths["journal_dir"])


def _validate_journal_path(filepath: str, storage: JournalStorage) -> Path:
    """Validate path is inside journal dir (prevent traversal)."""
    resolved = Path(filepath).resolve()
    if not resolved.is_relative_to(storage.journal_dir):
        raise HTTPException(status_code=400, detail="Invalid path")
    if not resolved.exists():
        raise HTTPException(status_code=404, detail="Entry not found")
    return resolved


@router.get("", response_model=list[JournalEntry])
async def list_entries(
    entry_type: str | None = None,
    tag: str | None = None,
    limit: int = 50,
    user: dict = Depends(get_current_user),
):
    storage = _get_storage(user["id"])
    tags = [tag] if tag else None
    entries = storage.list_entries(entry_type=entry_type, tags=tags, limit=limit)
    return [
        JournalEntry(
            path=str(e["path"]),
            title=e["title"],
            type=e["type"],
            created=e.get("created"),
            tags=e.get("tags", []),
            preview=e.get("preview", ""),
        )
        for e in entries
    ]


@router.post("", response_model=JournalEntry, status_code=status.HTTP_201_CREATED)
async def create_entry(
    body: JournalCreate,
    user: dict = Depends(get_current_user),
):
    storage = _get_storage(user["id"])

    title = body.title
    if not title:
        title = _generate_title(body.content, user["id"])

    try:
        filepath = storage.create(
            content=body.content,
            entry_type=body.entry_type,
            title=title,
            tags=body.tags,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    log_event("journal_entry_created", user["id"])

    post = storage.read(filepath)
    return JournalEntry(
        path=str(filepath),
        title=post.get("title", filepath.stem),
        type=post.get("type", "unknown"),
        created=post.get("created"),
        tags=post.get("tags", []),
        content=post.content,
    )


@router.post("/quick", response_model=JournalEntry, status_code=status.HTTP_201_CREATED)
async def quick_capture(
    body: QuickCapture,
    user: dict = Depends(get_current_user),
):
    """Minimal journal entry — auto-title from content, type=quick, embed in ChromaDB."""
    storage = _get_storage(user["id"])
    text = body.content.strip()
    title = _generate_title(text, user["id"])
    if not title:
        title = text[:50].rstrip() + ("..." if len(text) > 50 else "")

    try:
        filepath = storage.create(
            content=text,
            entry_type="quick",
            title=title,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    log_event("journal_entry_created", user["id"])

    # Embed in ChromaDB for RAG
    try:
        paths = get_user_paths(user["id"])
        chroma_dir = paths.get("chroma_dir")
        if chroma_dir:
            from journal.embeddings import EmbeddingManager

            em = EmbeddingManager(chroma_dir)
            em.add_entry(str(filepath), text, {"type": "quick", "title": title})
    except Exception as e:
        logger.warning("quick_capture.embed_failed", error=str(e))

    post = storage.read(filepath)
    return JournalEntry(
        path=str(filepath),
        title=post.get("title", filepath.stem),
        type=post.get("type", "quick"),
        created=post.get("created"),
        tags=post.get("tags", []),
        content=post.content,
    )


@router.get("/{filepath:path}", response_model=JournalEntry)
async def read_entry(
    filepath: str,
    user: dict = Depends(get_current_user),
):
    storage = _get_storage(user["id"])
    resolved = _validate_journal_path(filepath, storage)
    post = storage.read(resolved)
    return JournalEntry(
        path=str(resolved),
        title=post.get("title", resolved.stem),
        type=post.get("type", "unknown"),
        created=post.get("created"),
        tags=post.get("tags", []),
        content=post.content,
    )


@router.put("/{filepath:path}", response_model=JournalEntry)
async def update_entry(
    filepath: str,
    body: JournalUpdate,
    user: dict = Depends(get_current_user),
):
    storage = _get_storage(user["id"])
    resolved = _validate_journal_path(filepath, storage)
    try:
        storage.update(resolved, content=body.content, metadata=body.metadata)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    post = storage.read(resolved)
    return JournalEntry(
        path=str(resolved),
        title=post.get("title", resolved.stem),
        type=post.get("type", "unknown"),
        created=post.get("created"),
        tags=post.get("tags", []),
        content=post.content,
    )


@router.delete("/{filepath:path}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entry(
    filepath: str,
    user: dict = Depends(get_current_user),
):
    storage = _get_storage(user["id"])
    resolved = _validate_journal_path(filepath, storage)
    storage.delete(resolved)
