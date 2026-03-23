"""Full user data export endpoint."""

import json
from datetime import datetime
from pathlib import Path

import structlog
from fastapi import APIRouter, Depends
from starlette.responses import Response

from web.auth import get_current_user
from web.deps import get_memory_store, get_profile_storage, get_user_paths

logger = structlog.get_logger()

router = APIRouter(prefix="/api/export", tags=["export"])


def _export_journal(user_id: str) -> list[dict]:
    try:
        import frontmatter

        paths = get_user_paths(user_id)
        journal_dir = Path(paths["journal_dir"])
        if not journal_dir.exists():
            return []
        entries = []
        for f in sorted(journal_dir.glob("*.md")):
            try:
                post = frontmatter.load(f)
                entries.append(
                    {
                        "filename": f.name,
                        "metadata": {k: str(v) for k, v in post.metadata.items()},
                        "content": post.content,
                    }
                )
            except Exception:
                continue
        return entries
    except Exception:
        return []


def _export_memory(user_id: str) -> list[dict]:
    try:
        store = get_memory_store(user_id)
        facts = store.get_all_active()
        return [
            {
                "id": str(getattr(f, "id", "")),
                "category": getattr(f, "category", ""),
                "content": getattr(f, "content", ""),
                "confidence": getattr(f, "confidence", 0),
                "source": getattr(f, "source", ""),
                "created_at": str(getattr(f, "created_at", "")),
            }
            for f in facts
        ]
    except Exception:
        return []


def _export_goals(user_id: str) -> list[dict]:
    try:
        from advisor.goals import GoalTracker
        from journal.storage import JournalStorage

        paths = get_user_paths(user_id)
        storage = JournalStorage(paths["journal_dir"])
        tracker = GoalTracker(storage)
        return tracker.get_goals(include_inactive=True)
    except Exception:
        return []


def _export_curriculum(user_id: str) -> dict:
    try:
        from curriculum.store import CurriculumStore

        paths = get_user_paths(user_id)
        store = CurriculumStore(Path(paths["data_dir"]) / "curriculum.db")
        stats = store.get_stats(user_id)
        enrollments = store.get_enrollments(user_id)
        return {
            "stats": stats.model_dump() if hasattr(stats, "model_dump") else {},
            "enrollments": enrollments,
        }
    except Exception:
        return {}


def _export_profile(user_id: str) -> dict:
    try:
        storage = get_profile_storage(user_id)
        profile = storage.load()
        if profile and hasattr(profile, "model_dump"):
            return profile.model_dump()
        return {}
    except Exception:
        return {}


@router.get("")
async def export_user_data(user: dict = Depends(get_current_user)):
    user_id = user["id"]
    data = {
        "exported_at": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "journal": _export_journal(user_id),
        "memory": _export_memory(user_id),
        "goals": _export_goals(user_id),
        "curriculum": _export_curriculum(user_id),
        "profile": _export_profile(user_id),
    }
    content = json.dumps(data, indent=2, default=str)
    return Response(
        content=content,
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=coach_export.json"},
    )
