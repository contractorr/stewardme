"""SQLite persistence for monitored repos and health snapshots."""

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

import structlog

from db import wal_connect

from .github_repos import MonitoredRepo, RepoSnapshot

logger = structlog.get_logger()


class GitHubRepoStore:
    """Monitored repos + snapshots in intel.db."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path).expanduser()
        self._init_db()

    def _init_db(self) -> None:
        with wal_connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS monitored_repos (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    repo_full_name TEXT NOT NULL,
                    html_url TEXT NOT NULL,
                    is_private INTEGER DEFAULT 0,
                    linked_goal_path TEXT,
                    poll_tier TEXT DEFAULT 'moderate',
                    last_polled_at TIMESTAMP,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, repo_full_name)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS repo_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    repo_id TEXT NOT NULL REFERENCES monitored_repos(id) ON DELETE CASCADE,
                    snapshot_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    commits_30d INTEGER,
                    open_issues INTEGER,
                    open_prs INTEGER,
                    latest_release TEXT,
                    ci_status TEXT,
                    contributors_30d INTEGER,
                    pushed_at TIMESTAMP,
                    weekly_commits_json TEXT
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_snapshots_repo_date
                ON repo_snapshots(repo_id, snapshot_at)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_monitored_repos_user
                ON monitored_repos(user_id)
            """)
            # Enable foreign key enforcement for cascade delete
            conn.execute("PRAGMA foreign_keys = ON")

    def add_repo(
        self,
        user_id: str,
        repo_full_name: str,
        html_url: str,
        is_private: bool = False,
        linked_goal_path: str | None = None,
    ) -> str:
        repo_id = uuid.uuid4().hex
        with wal_connect(self.db_path) as conn:
            try:
                conn.execute(
                    """INSERT INTO monitored_repos
                       (id, user_id, repo_full_name, html_url, is_private, linked_goal_path)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (repo_id, user_id, repo_full_name, html_url, int(is_private), linked_goal_path),
                )
            except sqlite3.IntegrityError:
                raise ValueError(f"Repo {repo_full_name} already monitored")
        return repo_id

    def remove_repo(self, user_id: str, repo_id: str) -> bool:
        with wal_connect(self.db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.execute(
                "DELETE FROM monitored_repos WHERE id = ? AND user_id = ?",
                (repo_id, user_id),
            )
            return cursor.rowcount > 0

    def list_repos(self, user_id: str) -> list[MonitoredRepo]:
        with wal_connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM monitored_repos WHERE user_id = ? ORDER BY added_at DESC",
                (user_id,),
            ).fetchall()
        return [self._row_to_monitored_repo(row) for row in rows]

    def get_repo(self, user_id: str, repo_id: str) -> MonitoredRepo | None:
        with wal_connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM monitored_repos WHERE id = ? AND user_id = ?",
                (repo_id, user_id),
            ).fetchone()
        return self._row_to_monitored_repo(row) if row else None

    def link_goal(self, repo_id: str, goal_path: str) -> None:
        with wal_connect(self.db_path) as conn:
            conn.execute(
                "UPDATE monitored_repos SET linked_goal_path = ? WHERE id = ?",
                (goal_path, repo_id),
            )

    def unlink_goal(self, repo_id: str) -> None:
        with wal_connect(self.db_path) as conn:
            conn.execute(
                "UPDATE monitored_repos SET linked_goal_path = NULL WHERE id = ?",
                (repo_id,),
            )

    def save_snapshot(self, repo_id: str, snapshot: RepoSnapshot) -> None:
        weekly_json = json.dumps(snapshot.weekly_commits) if snapshot.weekly_commits else "[]"
        pushed_str = snapshot.pushed_at.isoformat() if snapshot.pushed_at else None
        with wal_connect(self.db_path) as conn:
            conn.execute(
                """INSERT INTO repo_snapshots
                   (repo_id, snapshot_at, commits_30d, open_issues, open_prs,
                    latest_release, ci_status, contributors_30d, pushed_at, weekly_commits_json)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    repo_id,
                    snapshot.snapshot_at.isoformat(),
                    snapshot.commits_30d,
                    snapshot.open_issues,
                    snapshot.open_prs,
                    snapshot.latest_release,
                    snapshot.ci_status,
                    snapshot.contributors_30d,
                    pushed_str,
                    weekly_json,
                ),
            )
            conn.execute(
                "UPDATE monitored_repos SET last_polled_at = ? WHERE id = ?",
                (datetime.now(timezone.utc).isoformat(), repo_id),
            )

    def get_latest_snapshot(self, repo_id: str) -> RepoSnapshot | None:
        with wal_connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                """SELECT * FROM repo_snapshots
                   WHERE repo_id = ? ORDER BY snapshot_at DESC LIMIT 1""",
                (repo_id,),
            ).fetchone()
        return self._row_to_snapshot(row) if row else None

    def get_snapshot_history(self, repo_id: str, days: int = 90) -> list[RepoSnapshot]:
        with wal_connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """SELECT * FROM repo_snapshots
                   WHERE repo_id = ? AND snapshot_at > datetime('now', ?)
                   ORDER BY snapshot_at DESC""",
                (repo_id, f"-{days} days"),
            ).fetchall()
        return [self._row_to_snapshot(row) for row in rows]

    def get_repos_due_for_poll(self, user_id: str) -> list[MonitoredRepo]:
        """Return repos whose last_polled_at exceeds their tier cadence."""
        with wal_connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """SELECT * FROM monitored_repos WHERE user_id = ?
                   AND (
                       last_polled_at IS NULL
                       OR (poll_tier = 'active' AND last_polled_at < datetime('now', '-1 day'))
                       OR (poll_tier = 'moderate' AND last_polled_at < datetime('now', '-3 days'))
                       OR (poll_tier = 'stale' AND last_polled_at < datetime('now', '-7 days'))
                   )""",
                (user_id,),
            ).fetchall()
        return [self._row_to_monitored_repo(row) for row in rows]

    def get_all_user_ids_with_repos(self) -> list[str]:
        """Return distinct user IDs that have monitored repos."""
        with wal_connect(self.db_path) as conn:
            rows = conn.execute("SELECT DISTINCT user_id FROM monitored_repos").fetchall()
        return [row[0] for row in rows]

    def update_poll_tier(self, repo_id: str, tier: str) -> None:
        with wal_connect(self.db_path) as conn:
            conn.execute(
                "UPDATE monitored_repos SET poll_tier = ? WHERE id = ?",
                (tier, repo_id),
            )

    def prune_snapshots(self, max_age_days: int = 90) -> int:
        with wal_connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM repo_snapshots WHERE snapshot_at < datetime('now', ?)",
                (f"-{max_age_days} days",),
            )
            return cursor.rowcount

    @staticmethod
    def _row_to_monitored_repo(row: sqlite3.Row) -> MonitoredRepo:
        return MonitoredRepo(
            id=row["id"],
            user_id=row["user_id"],
            repo_full_name=row["repo_full_name"],
            html_url=row["html_url"],
            is_private=bool(row["is_private"]),
            linked_goal_path=row["linked_goal_path"],
            poll_tier=row["poll_tier"] or "moderate",
            last_polled_at=row["last_polled_at"],
            added_at=row["added_at"],
        )

    @staticmethod
    def _row_to_snapshot(row: sqlite3.Row) -> RepoSnapshot:
        weekly = []
        if row["weekly_commits_json"]:
            try:
                weekly = json.loads(row["weekly_commits_json"])
            except (json.JSONDecodeError, TypeError):
                pass
        pushed_at = None
        if row["pushed_at"]:
            try:
                pushed_at = datetime.fromisoformat(str(row["pushed_at"]))
            except (ValueError, TypeError):
                pass
        snapshot_at = datetime.now(timezone.utc)
        if row["snapshot_at"]:
            try:
                snapshot_at = datetime.fromisoformat(str(row["snapshot_at"]))
            except (ValueError, TypeError):
                pass
        return RepoSnapshot(
            repo_full_name="",  # not stored in snapshot table
            snapshot_at=snapshot_at,
            commits_30d=row["commits_30d"] or 0,
            open_issues=row["open_issues"] or 0,
            open_prs=row["open_prs"] or 0,
            latest_release=row["latest_release"],
            ci_status=row["ci_status"] or "none",
            contributors_30d=row["contributors_30d"] or 0,
            pushed_at=pushed_at,
            weekly_commits=weekly,
        )
