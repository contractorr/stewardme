"""Records predictions from high-confidence recommendations."""

import json
from datetime import datetime, timedelta

import structlog

from .store import Prediction, PredictionStore

logger = structlog.get_logger()

CATEGORY_HORIZONS = {
    "learning": 90,
    "career": 180,
    "entrepreneurial": 90,
    "investment": 60,
    "events": 30,
    "projects": 60,
}


class PredictionRecorder:
    """Stateless helper — use record_from_recommendation() directly."""

    pass


def record_from_recommendation(rec, store: PredictionStore) -> str | None:
    """Create prediction from a saved recommendation. Returns prediction id or None."""
    if store is None:
        return None
    if rec.score < 7.0:
        return None

    metadata = rec.metadata or {}
    reasoning = metadata.get("reasoning_trace", {})
    confidence = reasoning.get("confidence", 0.5)
    confidence_bucket = metadata.get("confidence", "Medium")
    intel_trigger = metadata.get("intel_trigger", "")
    if isinstance(intel_trigger, str):
        source_intel_ids = json.dumps([intel_trigger] if intel_trigger else [])
    else:
        source_intel_ids = json.dumps(list(intel_trigger))

    horizon_days = CATEGORY_HORIZONS.get(rec.category, 90)
    now = datetime.now()

    claim = f"{rec.title}: {rec.rationale[:200]}" if rec.rationale else rec.title

    prediction = Prediction(
        recommendation_id=rec.id or "",
        category=rec.category,
        claim_text=claim,
        confidence=float(confidence),
        confidence_bucket=str(confidence_bucket),
        source_intel_ids=source_intel_ids,
        created_at=now.isoformat(),
        evaluation_due=(now + timedelta(days=horizon_days)).isoformat(),
    )
    return store.save(prediction)
