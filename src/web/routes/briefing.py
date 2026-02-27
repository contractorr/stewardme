"""Daily briefing routes — aggregates signals, patterns, recommendations, stale goals."""

import asyncio
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
    GoalIntelMatch,
)
from web.models import (
    DailyBrief as DailyBriefModel,
)
from web.models import (
    DailyBriefItem as DailyBriefItemModel,
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
        raw_patterns = await asyncio.to_thread(detector.detect_all)
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
                recommendations.append(
                    {
                        "id": r.id or "",
                        "category": r.category,
                        "title": r.title,
                        "description": r.description[:200] if r.description else "",
                        "score": r.score,
                        "status": r.status,
                        "reasoning_trace": meta.get("reasoning_trace"),
                        "critic": critic,
                    }
                )
    except Exception as e:
        logger.warning("briefing.recommendations_error", error=str(e))

    # Goals
    stale_goals: list[dict] = []
    all_goals: list[dict] = []
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
        raw_all = tracker.get_goals(include_inactive=False)
        all_goals = [
            {
                "path": str(g["path"]),
                "title": g["title"],
                "status": g["status"],
                "days_since_check": g.get("days_since_check") or 0,
            }
            for g in raw_all
        ]
    except Exception as e:
        logger.warning("briefing.goals_error", error=str(e))

    # Goal-intel matches
    goal_intel_matches: list[dict] = []
    try:
        from intelligence.goal_intel_match import GoalIntelMatchStore

        match_store = GoalIntelMatchStore(db_path)
        goal_paths = [g["path"] for g in all_goals]
        if goal_paths:
            goal_intel_matches = match_store.get_matches(goal_paths=goal_paths, limit=20)
    except Exception as e:
        logger.warning("briefing.goal_intel_matches_error", error=str(e))

    has_data = bool(
        signals or patterns or recommendations or stale_goals or all_goals or goal_intel_matches
    )

    # Adaptation count — how many feedback events the user has given
    adaptation_count = 0
    try:
        adaptation_count = get_feedback_count(user["id"])
    except Exception:
        pass

    # Daily brief
    daily_brief = None
    try:
        from profile.storage import ProfileStorage

        from advisor.daily_brief import DailyBriefBuilder
        from advisor.learning_paths import LearningPathStorage

        weekly_hours = 5
        profile_path = paths.get("profile")
        if profile_path and Path(profile_path).exists():
            prof = ProfileStorage(profile_path).load()
            if prof and hasattr(prof, "weekly_hours_available"):
                weekly_hours = prof.weekly_hours_available or 5

        learning_paths_list: list[dict] = []
        lp_dir = paths.get("learning_paths_dir")
        if lp_dir and Path(lp_dir).exists():
            learning_paths_list = LearningPathStorage(lp_dir).list_paths(status="active")

        rec_list = recommendations  # already gathered above

        brief_data = DailyBriefBuilder().build(
            stale_goals=stale_goals,
            recommendations=rec_list,
            learning_paths=learning_paths_list,
            all_goals=all_goals,
            weekly_hours=weekly_hours,
            intel_matches=goal_intel_matches,
        )
        daily_brief = DailyBriefModel(
            items=[
                DailyBriefItemModel(
                    kind=item.kind,
                    title=item.title,
                    description=item.description,
                    time_minutes=item.time_minutes,
                    action=item.action,
                    priority=item.priority,
                )
                for item in brief_data.items
            ],
            budget_minutes=brief_data.budget_minutes,
            used_minutes=brief_data.used_minutes,
            generated_at=brief_data.generated_at,
        )
    except Exception as e:
        logger.warning("briefing.daily_brief_error", error=str(e))

    return BriefingResponse(
        signals=[BriefingSignal(**s) for s in signals],
        patterns=[BriefingPattern(**p) for p in patterns],
        recommendations=[BriefingRecommendation(**r) for r in recommendations],
        stale_goals=[BriefingGoal(**g) for g in stale_goals],
        goals=[BriefingGoal(**g) for g in all_goals],
        has_data=has_data,
        adaptation_count=adaptation_count,
        daily_brief=daily_brief,
        goal_intel_matches=[GoalIntelMatch(**m) for m in goal_intel_matches],
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
