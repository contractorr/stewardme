"""SQLite-backed per-user brief store: brief history, read/dismiss state, config."""

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

VALID_STATUSES = ("unread", "read", "dismissed")


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


class BriefStore:
    """Persists generated briefs and the user's brief configuration."""

    def __init__(self, db_path: str | Path):
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self._db_path) as conn:
            conn.execute(
                """CREATE TABLE IF NOT EXISTS briefs (
                    id TEXT PRIMARY KEY,
                    period_start TEXT NOT NULL,
                    period_end TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'unread'
                        CHECK(status IN ('unread','read','dismissed')),
                    summary TEXT NOT NULL DEFAULT '',
                    sections TEXT NOT NULL DEFAULT '[]',
                    created_at TEXT NOT NULL
                )"""
            )
            conn.execute(
                """CREATE TABLE IF NOT EXISTS config (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )"""
            )

    @staticmethod
    def _row_to_brief(row: sqlite3.Row) -> dict:
        return {
            "id": row["id"],
            "period_start": row["period_start"],
            "period_end": row["period_end"],
            "status": row["status"],
            "summary": row["summary"],
            "sections": json.loads(row["sections"] or "[]"),
            "created_at": row["created_at"],
        }

    def save_brief(
        self,
        summary: str,
        sections: list[dict],
        period_start: str,
        period_end: str,
    ) -> dict:
        brief_id = uuid.uuid4().hex[:12]
        created_at = _utcnow()
        with sqlite3.connect(self._db_path) as conn:
            conn.execute(
                """INSERT INTO briefs
                   (id, period_start, period_end, status, summary, sections, created_at)
                   VALUES (?, ?, ?, 'unread', ?, ?, ?)""",
                (brief_id, period_start, period_end, summary, json.dumps(sections), created_at),
            )
        return {
            "id": brief_id,
            "period_start": period_start,
            "period_end": period_end,
            "status": "unread",
            "summary": summary,
            "sections": sections,
            "created_at": created_at,
        }

    def list_briefs(self, limit: int = 20, include_dismissed: bool = True) -> list[dict]:
        query = "SELECT * FROM briefs"
        if not include_dismissed:
            query += " WHERE status != 'dismissed'"
        query += " ORDER BY created_at DESC LIMIT ?"
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(query, (limit,)).fetchall()
            return [self._row_to_brief(r) for r in rows]

    def get_brief(self, brief_id: str) -> dict | None:
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute("SELECT * FROM briefs WHERE id = ?", (brief_id,)).fetchone()
            return self._row_to_brief(row) if row else None

    def get_latest(self) -> dict | None:
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute("SELECT * FROM briefs ORDER BY created_at DESC LIMIT 1").fetchone()
            return self._row_to_brief(row) if row else None

    def _set_status(self, brief_id: str, status: str) -> bool:
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.execute("UPDATE briefs SET status = ? WHERE id = ?", (status, brief_id))
            return cursor.rowcount > 0

    def mark_read(self, brief_id: str) -> bool:
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.execute(
                "UPDATE briefs SET status = 'read' WHERE id = ? AND status = 'unread'",
                (brief_id,),
            )
            if cursor.rowcount > 0:
                return True
            row = conn.execute("SELECT 1 FROM briefs WHERE id = ?", (brief_id,)).fetchone()
            return row is not None

    def dismiss(self, brief_id: str) -> bool:
        return self._set_status(brief_id, "dismissed")

    def get_config(self) -> dict:
        with sqlite3.connect(self._db_path) as conn:
            row = conn.execute("SELECT value FROM config WHERE key = 'config'").fetchone()
            if not row:
                return {}
            try:
                return json.loads(row[0])
            except (ValueError, TypeError):
                return {}

    def save_config(self, config: dict) -> None:
        with sqlite3.connect(self._db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO config (key, value) VALUES ('config', ?)",
                (json.dumps(config),),
            )

    def recent_custom_topics(self, limit: int = 10) -> list[str]:
        """Titles of custom sections across recent briefs, to avoid topic repeats."""
        topics: list[str] = []
        for brief in self.list_briefs(limit=10):
            for section in brief["sections"]:
                if section.get("kind") == "custom" and section.get("topic"):
                    topics.append(section["topic"])
                elif section.get("kind") == "custom" and section.get("title"):
                    topics.append(section["title"])
                if len(topics) >= limit:
                    return topics
        return topics
