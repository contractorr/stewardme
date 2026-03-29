"""Helpers for user-authored curriculum storage."""

from __future__ import annotations

import re
import uuid
from pathlib import Path
from typing import Any

import yaml

from storage_paths import get_user_paths

GUIDE_METADATA_FILENAME = "guide.yaml"
_SLUG_RE = re.compile(r"[^a-z0-9]+")


def get_user_curriculum_dirs(user_id: str) -> tuple[Path, Path]:
    """Return active and archived user curriculum roots."""
    paths = get_user_paths(user_id)
    return paths["curriculum_dir"], paths["curriculum_archive_dir"]


def ensure_user_curriculum_dirs(user_id: str) -> tuple[Path, Path]:
    """Create active and archived curriculum roots if missing."""
    active_dir, archive_dir = get_user_curriculum_dirs(user_id)
    active_dir.mkdir(parents=True, exist_ok=True)
    archive_dir.mkdir(parents=True, exist_ok=True)
    return active_dir, archive_dir


def slugify_topic(value: str) -> str:
    normalized = _SLUG_RE.sub("-", value.lower()).strip("-")
    return normalized or "guide"


def build_user_guide_id(topic_or_title: str, *, kind: str = "standalone") -> str:
    """Create a readable, collision-resistant guide id."""
    slug = slugify_topic(topic_or_title)
    suffix = uuid.uuid4().hex[:6]
    prefix = "ext" if kind == "extension" else "user"
    return f"{prefix}-{slug}-{suffix}"


def load_guide_metadata(guide_dir: Path) -> dict[str, Any]:
    """Load optional guide-level metadata from guide.yaml."""
    metadata_path = guide_dir / GUIDE_METADATA_FILENAME
    if not metadata_path.is_file():
        return {}
    try:
        data = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def write_guide_metadata(guide_dir: Path, metadata: dict[str, Any]) -> Path:
    """Write guide-level metadata to guide.yaml."""
    guide_dir.mkdir(parents=True, exist_ok=True)
    metadata_path = guide_dir / GUIDE_METADATA_FILENAME
    metadata_path.write_text(
        yaml.safe_dump(metadata, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )
    return metadata_path
