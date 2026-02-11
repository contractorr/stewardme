"""Goal tracking and check-in management."""

from datetime import datetime
from pathlib import Path
from typing import Optional

import frontmatter
import structlog

from shared_types import GoalStatus

logger = structlog.get_logger()


class GoalTracker:
    """Track goals and detect stale ones needing attention."""

    DEFAULT_CHECK_IN_DAYS = 14

    def __init__(self, journal_storage):
        self.storage = journal_storage

    def get_goals(self, include_inactive: bool = False) -> list[dict]:
        """Get all goals with their metadata.

        Args:
            include_inactive: Include completed/paused/abandoned goals

        Returns:
            List of goal entries with staleness info
        """
        entries = self.storage.list_entries(entry_type="goal", limit=100)
        goals = []

        for entry in entries:
            try:
                post = frontmatter.load(entry["path"])
                meta = dict(post.metadata)

                status = meta.get("status", "active")
                if not include_inactive and status in (GoalStatus.COMPLETED, GoalStatus.ABANDONED):
                    continue

                last_checked = meta.get("last_checked", meta.get("created"))
                check_in_days = meta.get("check_in_days", self.DEFAULT_CHECK_IN_DAYS)

                # Calculate staleness
                days_since = self._days_since(last_checked)
                is_stale = days_since >= check_in_days if days_since else False

                goals.append({
                    "path": entry["path"],
                    "title": meta.get("title", "Untitled Goal"),
                    "status": status,
                    "created": meta.get("created"),
                    "last_checked": last_checked,
                    "check_in_days": check_in_days,
                    "days_since_check": days_since,
                    "is_stale": is_stale,
                    "tags": meta.get("tags", []),
                    "content": post.content[:200] if post.content else "",
                })
            except (OSError, ValueError) as e:
                logger.debug("Failed to load goal entry", error=str(e))
                continue

        return sorted(goals, key=lambda g: (not g["is_stale"], g.get("days_since_check") or 0), reverse=True)

    def get_stale_goals(self, days_threshold: Optional[int] = None) -> list[dict]:
        """Get goals that haven't been checked in recently.

        Args:
            days_threshold: Override default threshold

        Returns:
            List of stale goals
        """
        threshold = days_threshold or self.DEFAULT_CHECK_IN_DAYS
        all_goals = self.get_goals(include_inactive=False)

        return [
            g for g in all_goals
            if g.get("days_since_check", 0) >= threshold
        ]

    def check_in_goal(
        self,
        goal_path: Path,
        notes: Optional[str] = None,
    ) -> bool:
        """Record a check-in for a goal.

        Args:
            goal_path: Path to goal file
            notes: Optional check-in notes

        Returns:
            True if successful
        """
        try:
            post = frontmatter.load(goal_path)
            now = datetime.now().isoformat()

            # Update last_checked
            post["last_checked"] = now

            # Append notes to content if provided
            if notes:
                check_in_entry = f"\n\n---\n**Check-in {now[:10]}**: {notes}"
                post.content = (post.content or "") + check_in_entry

            with open(goal_path, "w") as f:
                f.write(frontmatter.dumps(post))

            return True
        except (OSError, ValueError) as e:
            logger.debug("Failed to check in goal", error=str(e))
            return False

    def update_goal_status(
        self,
        goal_path: Path,
        status: str,
    ) -> bool:
        """Update goal status.

        Args:
            goal_path: Path to goal file
            status: New status (active, paused, completed, abandoned)

        Returns:
            True if successful
        """
        valid = tuple(GoalStatus)
        if status not in valid:
            return False

        try:
            post = frontmatter.load(goal_path)
            post["status"] = status
            post["status_updated"] = datetime.now().isoformat()

            with open(goal_path, "w") as f:
                f.write(frontmatter.dumps(post))

            return True
        except (OSError, ValueError) as e:
            logger.debug("Failed to update goal status", error=str(e))
            return False

    def add_milestone(self, goal_path: Path, title: str) -> bool:
        """Append a milestone to goal's frontmatter.

        Args:
            goal_path: Path to goal file
            title: Milestone title

        Returns:
            True if successful
        """
        try:
            post = frontmatter.load(goal_path)
            milestones = post.metadata.get("milestones", [])
            milestones.append({
                "title": title,
                "completed": False,
                "completed_at": None,
            })
            post["milestones"] = milestones
            post["progress"] = self._calc_progress(milestones)

            with open(goal_path, "w") as f:
                f.write(frontmatter.dumps(post))
            return True
        except (OSError, ValueError) as e:
            logger.debug("Failed to add milestone", error=str(e))
            return False

    def complete_milestone(self, goal_path: Path, milestone_index: int) -> bool:
        """Mark a milestone as completed.

        Args:
            goal_path: Path to goal file
            milestone_index: 0-based index of milestone

        Returns:
            True if successful
        """
        try:
            post = frontmatter.load(goal_path)
            milestones = post.metadata.get("milestones", [])

            if milestone_index < 0 or milestone_index >= len(milestones):
                return False

            milestones[milestone_index]["completed"] = True
            milestones[milestone_index]["completed_at"] = datetime.now().isoformat()
            post["milestones"] = milestones
            post["progress"] = self._calc_progress(milestones)

            with open(goal_path, "w") as f:
                f.write(frontmatter.dumps(post))
            return True
        except (OSError, ValueError) as e:
            logger.debug("Failed to complete milestone", error=str(e))
            return False

    def get_progress(self, goal_path: Path) -> dict:
        """Get progress info for a goal.

        Returns:
            Dict with percent, completed, total, milestones list
        """
        try:
            post = frontmatter.load(goal_path)
            milestones = post.metadata.get("milestones", [])
            completed = sum(1 for m in milestones if m.get("completed"))
            total = len(milestones)
            percent = int((completed / total * 100) if total > 0 else 0)

            return {
                "percent": percent,
                "completed": completed,
                "total": total,
                "milestones": milestones,
            }
        except (OSError, ValueError):
            return {"percent": 0, "completed": 0, "total": 0, "milestones": []}

    @staticmethod
    def _calc_progress(milestones: list) -> int:
        """Calculate progress percentage from milestones."""
        if not milestones:
            return 0
        completed = sum(1 for m in milestones if m.get("completed"))
        return int(completed / len(milestones) * 100)

    def _days_since(self, iso_date: Optional[str]) -> Optional[int]:
        """Calculate days since ISO date string."""
        if not iso_date:
            return None
        try:
            dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
            if dt.tzinfo:
                dt = dt.replace(tzinfo=None)
            return (datetime.now() - dt).days
        except (OSError, ValueError) as e:
            logger.debug("Failed to parse date", error=str(e))
            return None


def get_goal_defaults() -> dict:
    """Get default metadata for new goal entries."""
    return {
        "status": str(GoalStatus.ACTIVE),
        "last_checked": datetime.now().isoformat(),
        "check_in_days": 14,
    }
