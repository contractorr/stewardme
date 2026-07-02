"""SQLite persistence for polished notes."""

import json
import uuid
from datetime import datetime
from pathlib import Path

import structlog

from db import ensure_schema_version, wal_connect

from .models import Note
from .polisher import PolishResult

logger = structlog.get_logger()

SCHEMA_VERSION = 1


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


class NotesStore:
    """Per-user SQLite store for the note polish workflow."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with wal_connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    title TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL DEFAULT 'pending',
                    original_text TEXT,
                    polished_markdown TEXT NOT NULL DEFAULT '',
                    polished_html TEXT NOT NULL DEFAULT '',
                    diff TEXT NOT NULL DEFAULT '',
                    corrections TEXT NOT NULL DEFAULT '[]',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    accepted_at TIMESTAMP
                )
            """)
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_notes_user ON notes(user_id, status, created_at)"
            )
            ensure_schema_version(conn, SCHEMA_VERSION)
            conn.commit()

    def create_pending(
        self,
        user_id: str,
        title: str,
        original_text: str,
        result: PolishResult,
        html: str,
    ) -> Note:
        note_id = uuid.uuid4().hex
        now = datetime.utcnow()
        with wal_connect(self.db_path) as conn:
            conn.execute(
                """INSERT INTO notes
                   (id, user_id, title, status, original_text, polished_markdown,
                    polished_html, diff, corrections, created_at)
                   VALUES (?, ?, ?, 'pending', ?, ?, ?, ?, ?, ?)""",
                (
                    note_id,
                    user_id,
                    title,
                    original_text,
                    result.polished_markdown,
                    html,
                    result.diff,
                    json.dumps(result.corrections),
                    now.isoformat(),
                ),
            )
            conn.commit()
        return Note(
            id=note_id,
            user_id=user_id,
            title=title,
            status="pending",
            original_text=original_text,
            polished_markdown=result.polished_markdown,
            polished_html=html,
            diff=result.diff,
            corrections=result.corrections,
            created_at=now,
        )

    def list_notes(self, user_id: str, status: str | None = None, limit: int = 100) -> list[Note]:
        """List notes without body payloads (title/status/dates only)."""
        with wal_connect(self.db_path, row_factory=True) as conn:
            query = "SELECT id, user_id, title, status, created_at, accepted_at FROM notes WHERE user_id = ?"
            params: list[object] = [user_id]
            if status:
                query += " AND status = ?"
                params.append(status)
            query += " ORDER BY created_at DESC LIMIT ?"
            params.append(limit)
            rows = conn.execute(query, tuple(params)).fetchall()
            return [self._row_to_note(dict(row)) for row in rows]

    def get_note(self, user_id: str, note_id: str) -> Note | None:
        with wal_connect(self.db_path, row_factory=True) as conn:
            row = conn.execute(
                "SELECT * FROM notes WHERE user_id = ? AND id = ?", (user_id, note_id)
            ).fetchone()
            return self._row_to_note(dict(row)) if row else None

    def accept(self, user_id: str, note_id: str) -> Note | None:
        """Accept the polish: keep the HTML, discard the original input for good."""
        note = self.get_note(user_id, note_id)
        if note is None:
            return None
        if note.status == "accepted":
            return note
        now = datetime.utcnow()
        with wal_connect(self.db_path) as conn:
            conn.execute(
                """UPDATE notes SET status = 'accepted', original_text = NULL,
                   diff = '', accepted_at = ? WHERE user_id = ? AND id = ?""",
                (now.isoformat(), user_id, note_id),
            )
            conn.commit()
        return self.get_note(user_id, note_id)

    def delete(self, user_id: str, note_id: str) -> bool:
        with wal_connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM notes WHERE user_id = ? AND id = ?", (user_id, note_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def _row_to_note(row: dict) -> Note:
        try:
            corrections = json.loads(row.get("corrections") or "[]")
        except json.JSONDecodeError:
            corrections = []
        return Note(
            id=row["id"],
            user_id=row["user_id"],
            title=row.get("title", ""),
            status=row.get("status", "pending"),
            original_text=row.get("original_text"),
            polished_markdown=row.get("polished_markdown", ""),
            polished_html=row.get("polished_html", ""),
            diff=row.get("diff", ""),
            corrections=corrections if isinstance(corrections, list) else [],
            created_at=_parse_dt(row.get("created_at")),
            accepted_at=_parse_dt(row.get("accepted_at")),
        )
