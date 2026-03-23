"""Compute notification candidates on-demand from existing data sources."""

import structlog

from web.notification_store import NotificationStore

logger = structlog.get_logger()


def _due_review_notification(user_id: str) -> list[dict]:
    """Single notification if there are due curriculum reviews."""
    try:
        from pathlib import Path

        from curriculum.store import CurriculumStore
        from web.deps import get_user_paths

        paths = get_user_paths(user_id)
        store = CurriculumStore(Path(paths["data_dir"]) / "curriculum.db")
        count = store.count_due_reviews(user_id)
        if count > 0:
            return [
                {
                    "id": "due_reviews",
                    "type": "due_reviews",
                    "title": f"{count} review{'s' if count != 1 else ''} due",
                    "body": "Spaced repetition reviews are waiting for you.",
                    "action_url": "/learn/review",
                }
            ]
    except Exception as exc:
        logger.debug("notification.due_reviews_failed", error=str(exc))
    return []


def _stale_goal_notifications(user_id: str) -> list[dict]:
    """One notification per stale goal."""
    try:
        from advisor.goals import GoalTracker
        from journal.storage import JournalStorage
        from web.deps import get_user_paths

        paths = get_user_paths(user_id)
        storage = JournalStorage(paths["journal_dir"])
        tracker = GoalTracker(storage)
        stale = [g for g in tracker.get_goals() if g.get("is_stale")]
        return [
            {
                "id": f"stale_goal:{g.get('path', g.get('title', ''))}",
                "type": "stale_goal",
                "title": f"Goal needs attention: {g.get('title', 'Untitled')}",
                "body": f"No check-in for {g.get('days_since_check', '?')} days.",
                "action_url": "/goals",
            }
            for g in stale[:5]
        ]
    except Exception as exc:
        logger.debug("notification.stale_goals_failed", error=str(exc))
    return []


def compute_notifications(user_id: str, store: NotificationStore) -> list[dict]:
    """Compute all notification candidates, annotate with read state."""
    candidates: list[dict] = []
    candidates.extend(_due_review_notification(user_id))
    candidates.extend(_stale_goal_notifications(user_id))

    for n in candidates:
        n["read"] = store.is_read(n["id"])

    return candidates
