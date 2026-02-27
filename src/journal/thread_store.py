"""SQLite-backed storage for journal thread groupings."""

import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import structlog

from db import wal_connect

logger = structlog.get_logger()


@dataclass
class Thread:
    id: str
    label: str
    created_at: datetime
    updated_at: datetime
    entry_count: int = 0
    status: str = "active"


@dataclass
class ThreadEntry:
    entry_id: str
    thread_id: str
    added_at: datetime
    similarity: float
    entry_date: datetime


class ThreadStore:
    """SQLite persistence for thread groupings."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with wal_connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS journal_threads (
                    id TEXT PRIMARY KEY,
                    label TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT NOT NULL DEFAULT 'active'
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS thread_entries (
                    thread_id TEXT NOT NULL,
                    entry_id TEXT NOT NULL,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    similarity REAL NOT NULL,
                    entry_date TIMESTAMP NOT NULL,
                    PRIMARY KEY (thread_id, entry_id),
                    FOREIGN KEY (thread_id) REFERENCES journal_threads(id)
                )
            """)
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_thread_entries_entry ON thread_entries(entry_id)"
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_threads_status ON journal_threads(status)")

    async def create_thread(self, label: str) -> Thread:
        thread_id = uuid.uuid4().hex[:16]
        now = datetime.now()
        with wal_connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO journal_threads (id, label, created_at, updated_at, status) VALUES (?, ?, ?, ?, ?)",
                (thread_id, label, now.isoformat(), now.isoformat(), "active"),
            )
        return Thread(
            id=thread_id,
            label=label,
            created_at=now,
            updated_at=now,
            entry_count=0,
            status="active",
        )

    async def add_entry(
        self,
        thread_id: str,
        entry_id: str,
        similarity: float,
        entry_date: datetime,
    ) -> None:
        now = datetime.now()
        with wal_connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO thread_entries (thread_id, entry_id, added_at, similarity, entry_date) VALUES (?, ?, ?, ?, ?)",
                (thread_id, entry_id, now.isoformat(), similarity, entry_date.isoformat()),
            )
            conn.execute(
                "UPDATE journal_threads SET updated_at = ? WHERE id = ?",
                (now.isoformat(), thread_id),
            )

    async def get_thread(self, thread_id: str) -> Thread | None:
        with wal_connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM journal_threads WHERE id = ?", (thread_id,)
            ).fetchone()
            if not row:
                return None
            count = conn.execute(
                "SELECT COUNT(*) FROM thread_entries WHERE thread_id = ?", (thread_id,)
            ).fetchone()[0]
        return self._row_to_thread(row, count)

    async def get_threads_for_entry(self, entry_id: str) -> list[Thread]:
        with wal_connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """SELECT t.*, COUNT(te2.entry_id) as entry_count
                   FROM thread_entries te
                   JOIN journal_threads t ON t.id = te.thread_id
                   LEFT JOIN thread_entries te2 ON te2.thread_id = t.id
                   WHERE te.entry_id = ?
                   GROUP BY t.id""",
                (entry_id,),
            ).fetchall()
        return [self._row_to_thread(r, r["entry_count"]) for r in rows]

    async def get_active_threads(self, min_entries: int = 2) -> list[Thread]:
        with wal_connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """SELECT t.*, COUNT(te.entry_id) as entry_count
                   FROM journal_threads t
                   JOIN thread_entries te ON te.thread_id = t.id
                   WHERE t.status = 'active'
                   GROUP BY t.id
                   HAVING COUNT(te.entry_id) >= ?
                   ORDER BY t.updated_at DESC""",
                (min_entries,),
            ).fetchall()
        return [self._row_to_thread(r, r["entry_count"]) for r in rows]

    async def get_thread_entries(self, thread_id: str) -> list[ThreadEntry]:
        with wal_connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM thread_entries WHERE thread_id = ? ORDER BY entry_date ASC",
                (thread_id,),
            ).fetchall()
        return [self._row_to_thread_entry(r) for r in rows]

    async def update_label(self, thread_id: str, label: str) -> None:
        with wal_connect(self.db_path) as conn:
            conn.execute(
                "UPDATE journal_threads SET label = ? WHERE id = ?",
                (label, thread_id),
            )

    async def clear_all(self) -> None:
        """Delete all threads and entries. Used by reindex."""
        with wal_connect(self.db_path) as conn:
            conn.execute("DELETE FROM thread_entries")
            conn.execute("DELETE FROM journal_threads")

    @staticmethod
    def _row_to_thread(row: sqlite3.Row, entry_count: int) -> Thread:
        d = dict(row)
        return Thread(
            id=d["id"],
            label=d["label"],
            created_at=datetime.fromisoformat(d["created_at"]),
            updated_at=datetime.fromisoformat(d["updated_at"]),
            entry_count=entry_count,
            status=d["status"],
        )

    @staticmethod
    def _row_to_thread_entry(row: sqlite3.Row) -> ThreadEntry:
        d = dict(row)
        return ThreadEntry(
            entry_id=d["entry_id"],
            thread_id=d["thread_id"],
            added_at=datetime.fromisoformat(d["added_at"]),
            similarity=d["similarity"],
            entry_date=datetime.fromisoformat(d["entry_date"]),
        )
