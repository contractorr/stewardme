"""Daily briefing routes — aggregates signals, patterns, recommendations, stale goals."""

from pathlib import Path

import structlog
from fastapi import APIRouter, Depends, HTTPException, Query

from advisor.goals import GoalTracker
from advisor.patterns import PatternDetector
from advisor.recommendation_storage import RecommendationStorage
from advisor.signals import SignalStore
from journal.storage import JournalStorage
from web.auth import get_current_user
from web.deps import get_user_paths
from web.models import (
    BriefingGoal,
    BriefingPattern,
    BriefingRecommendation,
    BriefingResponse,
    BriefingSignal,
)
from web.user_store import get_feedback_count

logger = structlog.get_logger()

router = APIRouter(prefix="/api/briefing", tags=["briefing"])


def _get_storage(user_id: str) -> JournalStorage:
    paths = get_user_paths(user_id)
    return JournalStorage(paths["journal_dir"])


@router.get("", response_model=BriefingResponse)
async def get_briefing(
    min_signal_severity: int = Query(default=3, ge=1, le=10),
    max_signals: int = Query(default=10, ge=1, le=50),
    max_recommendations: int = Query(default=5, ge=1, le=20),
    user: dict = Depends(get_current_user),
):
    paths = get_user_paths(user["id"])
    storage = _get_storage(user["id"])
    db_path = paths["intel_db"]

    # Signals
    signals: list[dict] = []
    try:
        store = SignalStore(db_path)
        signals = store.get_active(min_severity=min_signal_severity, limit=max_signals)
    except Exception as e:
        logger.warning("briefing.signals_error", error=str(e))

    # Patterns
    patterns: list[dict] = []
    try:
        embeddings = None
        chroma_dir = paths.get("chroma_dir")
        if chroma_dir and Path(chroma_dir).exists():
            try:
                from journal import EmbeddingManager

                embeddings = EmbeddingManager(chroma_dir)
            except Exception:
                pass
        detector = PatternDetector(storage, embeddings=embeddings)
        raw_patterns = detector.detect_all()
        patterns = [
            {
                "type": p.type,
                "confidence": p.confidence,
                "summary": p.summary,
                "evidence": p.evidence,
                "coaching_prompt": p.coaching_prompt,
            }
            for p in raw_patterns
        ]
    except Exception as e:
        logger.warning("briefing.patterns_error", error=str(e))

    # Recommendations
    recommendations: list[dict] = []
    try:
        rec_dir = paths.get("recommendations_dir")
        if rec_dir:
            rec_storage = RecommendationStorage(rec_dir)
            recs = rec_storage.get_top_by_score(limit=max_recommendations)
            for r in recs:
                meta = r.metadata or {}
                critic = None
                if any(meta.get(k) for k in ("confidence", "critic_challenge", "missing_context")):
                    critic = {
                        "confidence": meta.get("confidence", "Medium"),
                        "confidence_rationale": meta.get("confidence_rationale", ""),
                        "critic_challenge": meta.get("critic_challenge", ""),
                        "missing_context": meta.get("missing_context", ""),
                        "alternative": meta.get("alternative"),
                        "intel_contradictions": meta.get("intel_contradictions"),
                    }
                recommendations.append({
                    "id": r.id or "",
                    "category": r.category,
                    "title": r.title,
                    "description": r.description[:200] if r.description else "",
                    "score": r.score,
                    "status": r.status,
                    "reasoning_trace": meta.get("reasoning_trace"),
                    "critic": critic,
                })
    except Exception as e:
        logger.warning("briefing.recommendations_error", error=str(e))

    # Stale goals
    stale_goals: list[dict] = []
    try:
        tracker = GoalTracker(storage)
        raw_stale = tracker.get_stale_goals()
        stale_goals = [
            {
                "path": str(g["path"]),
                "title": g["title"],
                "status": g["status"],
                "days_since_check": g.get("days_since_check") or 0,
            }
            for g in raw_stale
        ]
    except Exception as e:
        logger.warning("briefing.stale_goals_error", error=str(e))

    has_data = bool(signals or patterns or recommendations or stale_goals)

    # Adaptation count — how many feedback events the user has given
    adaptation_count = 0
    try:
        adaptation_count = get_feedback_count(user["id"])
    except Exception:
        pass

    return BriefingResponse(
        signals=[BriefingSignal(**s) for s in signals],
        patterns=[BriefingPattern(**p) for p in patterns],
        recommendations=[BriefingRecommendation(**r) for r in recommendations],
        stale_goals=[BriefingGoal(**g) for g in stale_goals],
        has_data=has_data,
        adaptation_count=adaptation_count,
    )


@router.post("/signals/{signal_id}/acknowledge")
async def acknowledge_signal(
    signal_id: int,
    user: dict = Depends(get_current_user),
):
    paths = get_user_paths(user["id"])
    try:
        store = SignalStore(paths["intel_db"])
        ok = store.acknowledge(signal_id)
        if not ok:
            raise HTTPException(status_code=404, detail="Signal not found")
        return {"ok": True}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("briefing.acknowledge_error", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to acknowledge signal")
