"""Embedding model versioning for ChromaDB collection names.

Derives a short filesystem-safe tag from the active embedding function so that
switching models targets a new collection file automatically.
"""

from __future__ import annotations

import re
from pathlib import Path

import structlog

logger = structlog.get_logger()

EMBEDDING_SCHEMA_VERSION = 1

_ALIASES: dict[str, str] = {
    "gemini-embedding-2-preview": "gemini2",
    "text-embedding-3-small": "oai3s",
    "text-embedding-3-large": "oai3l",
    "simple-hash-fallback": "hash",
    "all-MiniLM-L6-v2": "minilm6",
}


def model_tag(embedding_fn) -> str:
    """Derive short filesystem-safe tag from an embedding function."""
    raw = getattr(embedding_fn, "_model", None)
    if raw is None:
        name_attr = getattr(embedding_fn, "name", None)
        if callable(name_attr):
            raw = name_attr()
        elif isinstance(name_attr, str):
            raw = name_attr
        else:
            raw = "unknown"
    return _ALIASES.get(raw, _sanitize(raw))


def _sanitize(name: str) -> str:
    """Lowercase, replace non-alnum with _, truncate to 16 chars."""
    return re.sub(r"[^a-z0-9]", "_", name.lower().strip())[:16].strip("_")


def versioned_name(base: str, embedding_fn, user_id: str | None = None) -> str:
    """Build a versioned collection name.

    Format: ``{base}_v{schema}_{tag}`` with optional ``_{safe_uid}`` suffix.
    """
    tag = model_tag(embedding_fn)
    name = f"{base}_v{EMBEDDING_SCHEMA_VERSION}_{tag}"
    if user_id:
        from storage_paths import safe_user_id

        name = f"{name}_{safe_user_id(user_id)}"
    return name


def auto_migrate_collection(base_dir: Path, old_name: str, new_name: str) -> bool:
    """Rename an unversioned LocalCollection JSON file to the versioned name.

    Returns True if migration happened, False otherwise. This is O(1) — no
    re-embedding required when the underlying model hasn't changed.
    """
    old_path = Path(base_dir) / f"{old_name}.json"
    new_path = Path(base_dir) / f"{new_name}.json"
    if old_path.exists() and not new_path.exists():
        try:
            old_path.rename(new_path)
            logger.info(
                "collection_auto_migrated",
                old=old_name,
                new=new_name,
                dir=str(base_dir),
            )
            return True
        except OSError as e:
            logger.warning("collection_auto_migrate_failed", error=str(e))
    return False
