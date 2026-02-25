"""SQLite-backed context cache with TTL for RAG retrieval results."""

import hashlib
import json
import time

from db import wal_connect


class ContextCache:
    """Cache RAG context payloads in SQLite with TTL."""

    def __init__(self, db_path, default_ttl: int = 86400):
        self.db_path = db_path
        self.default_ttl = default_ttl
        self._init_db()

    def _init_db(self):
        with wal_connect(self.db_path) as conn:
            conn.execute(
                """CREATE TABLE IF NOT EXISTS context_cache (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    created_at REAL NOT NULL
                )"""
            )

    def get(self, cache_key: str) -> str | None:
        """Return cached value if not expired, else None."""
        with wal_connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT value, created_at FROM context_cache WHERE key = ?",
                (cache_key,),
            ).fetchone()
        if row is None:
            return None
        value, created_at = row
        if time.time() - created_at > self.default_ttl:
            self._delete(cache_key)
            return None
        return value

    def set(self, cache_key: str, value: str):
        """Upsert cache entry with current timestamp."""
        with wal_connect(self.db_path) as conn:
            conn.execute(
                """INSERT INTO context_cache (key, value, created_at)
                   VALUES (?, ?, ?)
                   ON CONFLICT(key) DO UPDATE SET value=excluded.value, created_at=excluded.created_at""",
                (cache_key, value, time.time()),
            )

    def make_key(self, context_type: str, query: str, **params) -> str:
        """SHA256 hash of context_type + query + sorted params."""
        payload = json.dumps({"type": context_type, "query": query, **params}, sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()

    def clear_expired(self):
        """Delete entries older than TTL."""
        cutoff = time.time() - self.default_ttl
        with wal_connect(self.db_path) as conn:
            conn.execute("DELETE FROM context_cache WHERE created_at < ?", (cutoff,))

    def _delete(self, cache_key: str):
        with wal_connect(self.db_path) as conn:
            conn.execute("DELETE FROM context_cache WHERE key = ?", (cache_key,))
