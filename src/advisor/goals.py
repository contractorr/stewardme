"""Goal tracking and check-in management."""

from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import frontmatter


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
                if not include_inactive and status in ("completed", "abandoned"):
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
            except Exception:
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
        except Exception:
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
        valid = ("active", "paused", "completed", "abandoned")
        if status not in valid:
            return False

        try:
            post = frontmatter.load(goal_path)
            post["status"] = status
            post["status_updated"] = datetime.now().isoformat()

            with open(goal_path, "w") as f:
                f.write(frontmatter.dumps(post))

            return True
        except Exception:
            return False

    def _days_since(self, iso_date: Optional[str]) -> Optional[int]:
        """Calculate days since ISO date string."""
        if not iso_date:
            return None
        try:
            dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
            if dt.tzinfo:
                dt = dt.replace(tzinfo=None)
            return (datetime.now() - dt).days
        except Exception:
            return None


def get_goal_defaults() -> dict:
    """Get default metadata for new goal entries."""
    return {
        "status": "active",
        "last_checked": datetime.now().isoformat(),
        "check_in_days": 14,
    }
