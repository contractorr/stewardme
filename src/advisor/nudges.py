"""Behavioral nudges — lightweight checks surfaced during CLI interactions."""

from datetime import datetime, timedelta
from typing import Optional

import structlog

logger = structlog.get_logger()


class NudgeEngine:
    """Generate contextual nudges based on user activity."""

    def __init__(
        self,
        journal_storage=None,
        profile_storage=None,
        lp_storage=None,
        config: Optional[dict] = None,
    ):
        self.journal_storage = journal_storage
        self.profile_storage = profile_storage
        self.lp_storage = lp_storage
        self.config = config or {}

    def get_nudges(self, max_nudges: int = 3) -> list[str]:
        """Run all nudge checks, return list of nudge messages."""
        nudges = []

        nudges.extend(self._check_profile_stale())
        nudges.extend(self._check_stale_goals())
        nudges.extend(self._check_learning_stalled())
        nudges.extend(self._check_journal_streak())

        return nudges[:max_nudges]

    def _check_profile_stale(self) -> list[str]:
        if not self.profile_storage:
            return []
        try:
            profile = self.profile_storage.load()
            if not profile:
                return [
                    "No profile set up yet. Run `coach profile update` to get personalized advice."
                ]
            refresh_days = self.config.get("profile", {}).get("interview_refresh_days", 90)
            if profile.is_stale(refresh_days):
                return [
                    f"Profile is >{refresh_days} days old. Run `coach profile update` to refresh."
                ]
        except Exception:
            pass
        return []

    def _check_stale_goals(self) -> list[str]:
        if not self.journal_storage:
            return []
        try:
            from advisor.goals import GoalTracker

            tracker = GoalTracker(self.journal_storage)
            stale = tracker.get_stale_goals(days=14)
            if stale:
                top = stale[0]
                return [
                    f'Haven\'t checked in on "{top["title"]}" in {top.get("days_since_check", "14+")} days.'
                ]
        except Exception:
            pass
        return []

    def _check_learning_stalled(self) -> list[str]:
        if not self.lp_storage:
            return []
        try:
            active = self.lp_storage.list_paths(status="active")
            for path in active:
                updated = path.get("updated_at") or path.get("created_at", "")
                if updated:
                    try:
                        updated_dt = datetime.fromisoformat(updated)
                        if (datetime.now() - updated_dt).days > 14:
                            return [
                                f'Learning path "{path["skill"]}" hasn\'t progressed in 2+ weeks. Run `coach learn next`.'
                            ]
                    except ValueError:
                        pass
        except Exception:
            pass
        return []

    def _check_journal_streak(self) -> list[str]:
        if not self.journal_storage:
            return []
        try:
            entries = self.journal_storage.list_entries(limit=30)
            if not entries:
                return ["No journal entries yet. Start with `coach journal add`."]

            now = datetime.now()
            week_ago = now - timedelta(days=7)
            recent = [
                e
                for e in entries
                if e.get("created")
                and datetime.fromisoformat(e["created"].replace("Z", "+00:00")).replace(tzinfo=None)
                > week_ago
            ]

            if len(recent) >= 5:
                return [f"{len(recent)} entries this week — solid streak!"]
            elif len(recent) == 0:
                return ["No journal entries in 7 days. Quick reflection? `coach journal add`"]
        except Exception:
            pass
        return []


def get_nudges_for_cli(config: dict, components: dict, max_nudges: int = 2) -> list[str]:
    """Convenience function for CLI commands to get nudges."""
    profile_storage = None
    try:
        from profile.storage import ProfileStorage

        profile_path = config.get("profile", {}).get("path", "~/coach/profile.yaml")
        profile_storage = ProfileStorage(profile_path)
    except Exception:
        pass

    lp_storage = None
    try:
        from advisor.learning_paths import LearningPathStorage

        lp_dir = config.get("learning_paths", {}).get("dir", "~/coach/learning_paths")
        lp_storage = LearningPathStorage(lp_dir)
    except Exception:
        pass

    engine = NudgeEngine(
        journal_storage=components.get("storage"),
        profile_storage=profile_storage,
        lp_storage=lp_storage,
        config=config,
    )
    return engine.get_nudges(max_nudges)
