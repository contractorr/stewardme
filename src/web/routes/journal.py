"""Journal CRUD routes wrapping src/journal/storage.py."""

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status

from journal.storage import JournalStorage
from web.auth import get_current_user
from web.deps import get_coach_paths
from web.models import JournalCreate, JournalEntry, JournalUpdate

router = APIRouter(prefix="/api/journal", tags=["journal"])


def _get_storage() -> JournalStorage:
    paths = get_coach_paths()
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
    storage = _get_storage()
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
    storage = _get_storage()
    try:
        filepath = storage.create(
            content=body.content,
            entry_type=body.entry_type,
            title=body.title,
            tags=body.tags,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    post = storage.read(filepath)
    return JournalEntry(
        path=str(filepath),
        title=post.get("title", filepath.stem),
        type=post.get("type", "unknown"),
        created=post.get("created"),
        tags=post.get("tags", []),
        content=post.content,
    )


@router.get("/{filepath:path}", response_model=JournalEntry)
async def read_entry(
    filepath: str,
    user: dict = Depends(get_current_user),
):
    storage = _get_storage()
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
    storage = _get_storage()
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
    storage = _get_storage()
    resolved = _validate_journal_path(filepath, storage)
    storage.delete(resolved)
