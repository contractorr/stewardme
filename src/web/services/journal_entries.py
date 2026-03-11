"""Shared journal-entry validation helpers for web routes."""

from pathlib import Path

from fastapi import HTTPException
from journal.storage import JournalStorage
from web.deps import get_user_paths


def resolve_journal_entry(filepath: str, user_id: str) -> tuple[Path, object]:
    """Resolve a user journal entry path and load its frontmatter post."""
    paths = get_user_paths(user_id)
    journal_dir = Path(paths["journal_dir"]).resolve()
    entry_path = Path(filepath)
    if not entry_path.is_absolute():
        entry_path = journal_dir / entry_path

    resolved = entry_path.resolve()
    if not resolved.is_relative_to(journal_dir):
        raise HTTPException(status_code=400, detail="Invalid path")
    if not resolved.exists():
        raise HTTPException(status_code=404, detail="Entry not found")

    storage = JournalStorage(journal_dir)
    try:
        return resolved, storage.read(resolved)
    except (OSError, ValueError):
        raise HTTPException(status_code=400, detail="Invalid journal entry")


def resolve_goal_entry(filepath: str, user_id: str) -> tuple[Path, object]:
    """Resolve a journal entry and ensure it is a goal."""
    try:
        resolved, post = resolve_journal_entry(filepath, user_id)
    except HTTPException as exc:
        if exc.status_code == 404:
            raise HTTPException(status_code=404, detail="Goal not found")
        raise
    if post.get("type") != "goal":
        raise HTTPException(status_code=404, detail="Goal not found")
    return resolved, post
