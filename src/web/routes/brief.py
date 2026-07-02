"""Configurable brief routes: latest, generate, history, read/dismiss, config."""

import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query

from web.auth import get_current_user
from web.brief_models import BriefConfig, BriefLatestResponse, BriefResponse
from web.brief_store import BriefStore

router = APIRouter(prefix="/api/brief", tags=["brief"])


def _get_store(user_id: str) -> BriefStore:
    from web.deps import get_user_paths

    return BriefStore(get_user_paths(user_id)["briefs_db"])


def _load_config(store: BriefStore) -> BriefConfig:
    raw = store.get_config()
    try:
        return BriefConfig(**raw)
    except Exception:
        return BriefConfig()


def _should_generate(store: BriefStore, config: BriefConfig) -> bool:
    if not config.enabled:
        return False
    latest = store.get_latest()
    if latest is None:
        return True
    try:
        created = datetime.fromisoformat(latest["created_at"].replace("Z", "+00:00"))
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
    except (KeyError, ValueError):
        return True
    age = datetime.now(timezone.utc) - created
    return age >= timedelta(hours=config.min_interval_hours)


@router.get("/latest", response_model=BriefLatestResponse)
async def get_latest_brief(user: dict = Depends(get_current_user)):
    store = _get_store(user["id"])
    config = _load_config(store)
    latest = store.get_latest()
    return BriefLatestResponse(
        brief=BriefResponse(**latest) if latest else None,
        should_generate=_should_generate(store, config),
    )


@router.post("/generate", response_model=BriefResponse)
async def generate_brief_endpoint(
    force: bool = Query(False),
    user: dict = Depends(get_current_user),
):
    from web.brief_generator import generate_brief

    store = _get_store(user["id"])
    config = _load_config(store)
    if not force and not _should_generate(store, config):
        latest = store.get_latest()
        if latest:
            return BriefResponse(**latest)
    brief = generate_brief(user["id"], config, store)
    return BriefResponse(**brief)


@router.get("", response_model=list[BriefResponse])
async def list_briefs(
    limit: int = Query(20, ge=1, le=50),
    include_dismissed: bool = Query(True),
    user: dict = Depends(get_current_user),
):
    store = _get_store(user["id"])
    return [
        BriefResponse(**brief)
        for brief in store.list_briefs(limit=limit, include_dismissed=include_dismissed)
    ]


@router.post("/{brief_id}/read")
async def mark_brief_read(brief_id: str, user: dict = Depends(get_current_user)):
    store = _get_store(user["id"])
    if not store.mark_read(brief_id):
        raise HTTPException(status_code=404, detail="Brief not found")
    return {"ok": True}


@router.post("/{brief_id}/dismiss")
async def dismiss_brief(brief_id: str, user: dict = Depends(get_current_user)):
    store = _get_store(user["id"])
    if not store.dismiss(brief_id):
        raise HTTPException(status_code=404, detail="Brief not found")
    return {"ok": True}


@router.get("/config", response_model=BriefConfig)
async def get_brief_config(user: dict = Depends(get_current_user)):
    return _load_config(_get_store(user["id"]))


@router.put("/config", response_model=BriefConfig)
async def update_brief_config(
    config: BriefConfig,
    user: dict = Depends(get_current_user),
):
    for section in config.custom_sections:
        if not section.id:
            section.id = uuid.uuid4().hex[:8]
    store = _get_store(user["id"])
    store.save_config(config.model_dump())
    return config
