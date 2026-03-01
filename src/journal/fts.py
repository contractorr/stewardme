"""FTS5 full-text search index for journal entries."""

import re
import sqlite3
from pathlib import Path
from typing import Optional

import structlog

from db import wal_connect

logger = structlog.get_logger()


class JournalFTSIndex:
    """SQLite FTS5 index for journal entries.

    Stores at ``<journal_dir>/../journal.db`` (sibling of journal/ dir).
    """

    def __init__(self, journal_dir: str | Path):
        journal_dir = Path(journal_dir).expanduser()
        self.db_path = journal_dir.parent / "journal.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with wal_connect(self.db_path) as conn:
            conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS journal_fts USING fts5(
                    path UNINDEXED,
                    title,
                    entry_type UNINDEXED,
                    content,
                    tags,
                    tokenize='porter unicode61'
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS journal_fts_meta (
                    path TEXT PRIMARY KEY,
                    mtime REAL NOT NULL
                )
            """)

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def upsert(self, path: str, title: str, entry_type: str, content: str, tags: str, mtime: float):
        """Insert or replace an entry in the FTS index."""
        with wal_connect(self.db_path) as conn:
            # Delete old row if exists (FTS5 has no UPDATE)
            conn.execute("DELETE FROM journal_fts WHERE path = ?", (path,))
            conn.execute(
                "INSERT INTO journal_fts(path, title, entry_type, content, tags) VALUES (?, ?, ?, ?, ?)",
                (path, title, entry_type, content, tags),
            )
            conn.execute(
                "INSERT OR REPLACE INTO journal_fts_meta(path, mtime) VALUES (?, ?)",
                (path, mtime),
            )

    def delete(self, path: str):
        """Remove an entry from the FTS index."""
        with wal_connect(self.db_path) as conn:
            conn.execute("DELETE FROM journal_fts WHERE path = ?", (path,))
            conn.execute("DELETE FROM journal_fts_meta WHERE path = ?", (path,))

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(
        self,
        query: str,
        limit: int = 20,
        entry_type: Optional[str] = None,
    ) -> list[dict]:
        """BM25-ranked full-text search.

        Returns list of dicts with keys: path, title, entry_type, tags, rank.
        """
        fts_query = self._to_fts5_query(query)
        if not fts_query:
            return []

        sql = """
            SELECT path, title, entry_type, tags, bm25(journal_fts) AS rank
            FROM journal_fts
            WHERE journal_fts MATCH ?
        """
        params: list = [fts_query]

        if entry_type:
            sql += " AND entry_type = ?"
            params.append(entry_type)

        sql += " ORDER BY rank LIMIT ?"
        params.append(limit)

        try:
            with wal_connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(sql, params).fetchall()
                return [dict(r) for r in rows]
        except sqlite3.OperationalError as e:
            logger.warning("journal_fts_search_error", error=str(e))
            return []

    # ------------------------------------------------------------------
    # Sync
    # ------------------------------------------------------------------

    def sync_from_storage(self, entries: list[dict]) -> tuple[int, int]:
        """Incremental sync from journal storage entries.

        Args:
            entries: list of dicts with keys ``id`` (path str), ``content``, ``metadata``.
                     Same shape as ``JournalStorage.get_all_content()``.

        Returns:
            (added_or_updated, deleted) counts.
        """
        updated = 0
        deleted = 0

        current_paths = set()

        with wal_connect(self.db_path) as conn:
            # Build mtime cache
            existing = {
                row[0]: row[1]
                for row in conn.execute("SELECT path, mtime FROM journal_fts_meta").fetchall()
            }

        for entry in entries:
            path_str = entry["id"]
            current_paths.add(path_str)
            p = Path(path_str)
            if not p.exists():
                continue

            mtime = p.stat().st_mtime
            if path_str in existing and existing[path_str] == mtime:
                continue  # unchanged

            meta = entry.get("metadata", {})
            title = meta.get("title", p.stem)
            entry_type = meta.get("type", "")
            tags_list = meta.get("tags", [])
            tags = ", ".join(tags_list) if isinstance(tags_list, list) else str(tags_list or "")

            self.upsert(path_str, title, entry_type, entry["content"], tags, mtime)
            updated += 1

        # Remove entries no longer on disk
        stale = set(existing.keys()) - current_paths
        for path_str in stale:
            self.delete(path_str)
            deleted += 1

        return updated, deleted

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _to_fts5_query(query: str) -> str:
        """Convert user query to FTS5 MATCH expression.

        Splits into tokens, appends ``*`` for prefix matching, implicit AND.
        """
        tokens = re.findall(r"[\w]+", query.lower())
        if not tokens:
            return ""
        return " ".join(f"{t}*" for t in tokens)
