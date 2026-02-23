"""Profile view/edit API routes."""

from profile.storage import ProfileStorage, Skill

import structlog
from fastapi import APIRouter, Depends, HTTPException

from journal.embeddings import EmbeddingManager
from web.auth import get_current_user
from web.deps import get_user_paths
from web.models import ProfileResponse, ProfileUpdate

logger = structlog.get_logger()

router = APIRouter(prefix="/api/profile", tags=["profile"])


def _embed_profile(user_id: str, profile) -> None:
    """Re-embed profile in ChromaDB after update."""
    try:
        paths = get_user_paths(user_id)
        em = EmbeddingManager(paths["chroma_dir"], collection_name="profile")
        parts = [profile.summary()]
        if profile.goals_short_term:
            parts.append(f"Short-term goals: {profile.goals_short_term}")
        if profile.goals_long_term:
            parts.append(f"Long-term vision: {profile.goals_long_term}")
        if profile.fears_risks:
            parts.append("Concerns: " + ", ".join(profile.fears_risks))
        if profile.active_projects:
            parts.append("Active projects: " + ", ".join(profile.active_projects))
        text = "\n".join(parts)
        em.add_entry(f"profile:{user_id}", text, {"type": "profile", "user_id": user_id})
    except Exception as e:
        logger.warning("profile.embed_failed", error=str(e))


@router.get("", response_model=ProfileResponse)
async def get_profile(user: dict = Depends(get_current_user)):
    paths = get_user_paths(user["id"])
    storage = ProfileStorage(paths["profile"])
    profile = storage.load()
    if not profile:
        return ProfileResponse()

    data = profile.model_dump()
    data["career_stage"] = str(data["career_stage"])
    data["skills"] = [{"name": s["name"], "proficiency": s["proficiency"]} for s in data["skills"]]
    data["summary"] = profile.summary()
    data["is_stale"] = profile.is_stale()
    return ProfileResponse(**data)


@router.patch("")
async def update_profile(
    body: ProfileUpdate,
    user: dict = Depends(get_current_user),
):
    paths = get_user_paths(user["id"])
    storage = ProfileStorage(paths["profile"])
    profile = storage.get_or_empty()

    updates = body.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    for field, value in updates.items():
        if field == "skills" and isinstance(value, list):
            value = [Skill(**s) if isinstance(s, dict) else s for s in value]
        if not hasattr(profile, field):
            raise HTTPException(status_code=400, detail=f"Unknown field: {field}")
        setattr(profile, field, value)

    storage.save(profile)
    _embed_profile(user["id"], profile)

    return {"ok": True, "updated_fields": list(updates.keys())}
