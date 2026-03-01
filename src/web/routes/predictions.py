"""Prediction ledger routes — list, stats, review."""

from typing import Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from predictions.store import PredictionStore
from web.auth import get_current_user
from web.deps import get_user_paths

logger = structlog.get_logger()

router = APIRouter(prefix="/api/predictions", tags=["predictions"])


class OutcomeBody(BaseModel):
    outcome: str
    notes: Optional[str] = None


def _get_store(user_id: str) -> PredictionStore:
    paths = get_user_paths(user_id)
    return PredictionStore(paths["intel_db"])


@router.get("")
async def list_predictions(
    status: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = Query(default=20, ge=1, le=100),
    user: dict = Depends(get_current_user),
):
    store = _get_store(user["id"])
    return store.get_all(category=category, outcome=status, limit=limit)


@router.get("/stats")
async def prediction_stats(
    user: dict = Depends(get_current_user),
):
    store = _get_store(user["id"])
    return store.get_stats()


@router.get("/review")
async def predictions_review(
    user: dict = Depends(get_current_user),
):
    store = _get_store(user["id"])
    return store.get_review_due(limit=3)


@router.post("/{prediction_id}/review")
async def record_outcome(
    prediction_id: str,
    body: OutcomeBody,
    user: dict = Depends(get_current_user),
):
    if body.outcome not in ("confirmed", "rejected", "expired", "skipped"):
        raise HTTPException(status_code=400, detail="Invalid outcome")
    store = _get_store(user["id"])
    ok = store.record_outcome(prediction_id, body.outcome, body.notes)
    return {"ok": ok}
