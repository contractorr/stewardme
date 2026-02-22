"""Autonomous action engine — executes actions triggered by signals without user prompting."""

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import structlog

from advisor.signals import Signal, SignalType

logger = structlog.get_logger()


@dataclass
class ActionResult:
    action_type: str
    signal_id: Optional[int]
    success: bool
    detail: str


class ActionLog:
    """SQLite persistence for autonomous action audit trail."""

    def __init__(self, db_path: Path):
        self.db_path = Path(db_path).expanduser()
        self._init_table()

    def _init_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS action_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action_type TEXT NOT NULL,
                    signal_id INTEGER,
                    context_json TEXT,
                    result_json TEXT,
                    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_action_type ON action_log(action_type)
            """)

    def log(self, result: ActionResult, context: Optional[dict] = None) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """INSERT INTO action_log (action_type, signal_id, context_json, result_json)
                VALUES (?, ?, ?, ?)""",
                (
                    result.action_type,
                    result.signal_id,
                    json.dumps(context or {}),
                    json.dumps({"success": result.success, "detail": result.detail}),
                ),
            )
            return cursor.lastrowid

    def count_today(self) -> int:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT COUNT(*) FROM action_log WHERE date(executed_at) = date('now')"
            ).fetchone()
            return row[0] if row else 0

    def has_recent_action(self, action_type: str, signal_title: str, hours: int = 24) -> bool:
        """Check if a similar action was taken recently to prevent duplicates."""
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                """SELECT 1 FROM action_log
                WHERE action_type = ?
                AND context_json LIKE ?
                AND executed_at >= datetime('now', ?)
                LIMIT 1""",
                (action_type, f"%{signal_title[:50]}%", f"-{hours} hours"),
            ).fetchone()
            return row is not None


class AutonomousActionEngine:
    """Execute autonomous actions based on detected signals."""

    def __init__(
        self,
        journal_storage,
        db_path: Path,
        config: Optional[dict] = None,
        embeddings=None,
    ):
        self.storage = journal_storage
        self.db_path = Path(db_path).expanduser()
        self.config = config or {}
        self.embeddings = embeddings
        self.agent_config = self.config.get("agent", {}).get("autonomous", {})
        self.action_log = ActionLog(self.db_path)

    def process_signals(self, signals: list[Signal]) -> list[ActionResult]:
        """Execute autonomous actions based on detected signals."""
        max_actions = self.agent_config.get("max_actions_per_day", 5)
        if self.action_log.count_today() >= max_actions:
            logger.info("max_daily_actions_reached", max=max_actions)
            return []

        results = []
        handlers = {
            SignalType.RESEARCH_TRIGGER: self._handle_research_trigger,
            SignalType.GOAL_COMPLETE_CANDIDATE: self._handle_goal_complete,
            SignalType.TOPIC_EMERGENCE: self._handle_topic_emergence,
            SignalType.GOAL_STALE: self._handle_stale_goal_reminder,
            SignalType.DEADLINE_URGENT: self._handle_deadline_urgent,
        }

        for signal in signals:
            if self.action_log.count_today() >= max_actions:
                break

            handler = handlers.get(signal.type)
            if not handler:
                continue

            # Check for recent duplicate action
            if self.action_log.has_recent_action(signal.type.value, signal.title):
                continue

            try:
                result = handler(signal)
                if result:
                    self.action_log.log(result, {"signal_title": signal.title})
                    results.append(result)
            except Exception as e:
                logger.warning("autonomous_action_error", signal=signal.type.value, error=str(e))

        return results

    def _handle_research_trigger(self, signal: Signal) -> Optional[ActionResult]:
        """Queue deep research on a frequently mentioned topic."""
        if not self.agent_config.get("auto_research", True):
            return None

        # Extract topic from signal title
        topic = signal.title.replace("Research opportunity: ", "")
        try:
            from intelligence.scheduler import ResearchRunner
            from intelligence.scraper import IntelStorage

            intel = IntelStorage(self.db_path)
            runner = ResearchRunner(intel, self.storage, self.embeddings, self.config)
            reports = runner.run(topic=topic)
            return ActionResult(
                action_type=signal.type.value,
                signal_id=None,
                success=bool(reports),
                detail=f"Queued research on '{topic}': {len(reports)} report(s)",
            )
        except Exception as e:
            return ActionResult(
                action_type=signal.type.value,
                signal_id=None,
                success=False,
                detail=f"Research failed for '{topic}': {e}",
            )

    def _handle_goal_complete(self, signal: Signal) -> Optional[ActionResult]:
        """Mark goal as completed when all milestones done."""
        from advisor.goals import GoalTracker

        tracker = GoalTracker(self.storage)
        # Extract path from evidence
        if not signal.evidence:
            return None
        goal_path = Path(signal.evidence[0])
        if not goal_path.exists():
            return None

        ok = tracker.update_goal_status(goal_path, "completed")
        if ok:
            # Create celebration entry
            goal_title = signal.title.replace("Goal ready to complete: ", "")
            self.storage.create(
                content=f"## Goal Completed: {goal_title}\n\nAll milestones achieved! Time to celebrate this accomplishment and set the next challenge.",
                entry_type="insight",
                title=f"Goal completed: {goal_title}",
                tags=["goal-complete", "celebration"],
            )
        return ActionResult(
            action_type=signal.type.value,
            signal_id=None,
            success=ok,
            detail=f"Goal marked completed: {signal.evidence[0]}"
            if ok
            else "Failed to update goal",
        )

    def _handle_topic_emergence(self, signal: Signal) -> Optional[ActionResult]:
        """Create draft goal suggestion as insight entry."""
        if not self.agent_config.get("auto_goal_suggestions", True):
            return None

        topic = signal.title.replace("Emerging topic: ", "")
        filepath = self.storage.create(
            content=(
                f"## Emerging Topic: {topic}\n\n"
                f"{signal.detail}\n\n"
                "### Suggested next steps\n"
                + "\n".join(f"- {a}" for a in signal.suggested_actions)
                + "\n\n*Auto-generated insight from signal detection.*"
            ),
            entry_type="insight",
            title=f"Emerging topic: {topic}",
            tags=["auto-insight", "topic-emergence"],
        )
        return ActionResult(
            action_type=signal.type.value,
            signal_id=None,
            success=bool(filepath),
            detail=f"Created insight entry for emerging topic '{topic}'",
        )

    def _handle_stale_goal_reminder(self, signal: Signal) -> Optional[ActionResult]:
        """Create check-in reminder entry for stale goals."""
        if not self.agent_config.get("auto_check_in_reminders", True):
            return None

        goal_title = signal.title.replace("Goal stale: ", "")
        filepath = self.storage.create(
            content=(
                f"## Check-in Reminder: {goal_title}\n\n"
                f"{signal.detail}\n\n"
                "Take a moment to review this goal:\n"
                "- Is it still relevant?\n"
                "- What progress have you made?\n"
                "- What's blocking you?\n\n"
                "*Auto-generated reminder from signal detection.*"
            ),
            entry_type="note",
            title=f"Reminder: check in on {goal_title}",
            tags=["auto-reminder", "goal-check-in"],
        )
        return ActionResult(
            action_type=signal.type.value,
            signal_id=None,
            success=bool(filepath),
            detail=f"Created check-in reminder for '{goal_title}'",
        )

    def _handle_deadline_urgent(self, signal: Signal) -> Optional[ActionResult]:
        """Bump recommendation priority for urgent deadlines (metadata-only action)."""
        # This is a lightweight metadata action — just log that we flagged it
        return ActionResult(
            action_type=signal.type.value,
            signal_id=None,
            success=True,
            detail=f"Flagged urgent deadline: {signal.title}",
        )
