"""SQLite-backed notification read-state store (per-user)."""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path


class NotificationStore:
    """Tracks read state for notifications. Actual notifications are computed on-demand."""

    def __init__(self, data_dir: str | Path):
        self._db_path = Path(data_dir) / "notifications.db"
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self._db_path) as conn:
            conn.execute(
                """CREATE TABLE IF NOT EXISTS read_state (
                    notification_id TEXT PRIMARY KEY,
                    read_at TEXT NOT NULL
                )"""
            )

    def is_read(self, notification_id: str) -> bool:
        with sqlite3.connect(self._db_path) as conn:
            row = conn.execute(
                "SELECT 1 FROM read_state WHERE notification_id = ?", (notification_id,)
            ).fetchone()
            return row is not None

    def mark_read(self, notification_id: str) -> None:
        with sqlite3.connect(self._db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO read_state (notification_id, read_at) VALUES (?, ?)",
                (notification_id, datetime.utcnow().isoformat()),
            )

    def mark_all_read(self, notification_ids: list[str]) -> None:
        now = datetime.utcnow().isoformat()
        with sqlite3.connect(self._db_path) as conn:
            conn.executemany(
                "INSERT OR REPLACE INTO read_state (notification_id, read_at) VALUES (?, ?)",
                [(nid, now) for nid in notification_ids],
            )

    def cleanup_old(self, days: int = 30) -> int:
        cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.execute("DELETE FROM read_state WHERE read_at < ?", (cutoff,))
            return cursor.rowcount
