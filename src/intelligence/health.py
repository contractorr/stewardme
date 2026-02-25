"""Scraper health tracking with exponential backoff."""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

import structlog

from db import wal_connect

logger = structlog.get_logger().bind(source="scraper_health")

_MAX_BACKOFF_SECONDS = 3600


class ScraperHealthTracker:
    """Track scraper health and manage backoff for failing sources."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path).expanduser()

    def record_success(self, source: str) -> None:
        """Record successful scrape: reset errors, clear backoff."""
        now = datetime.utcnow().isoformat()
        with wal_connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO scraper_health (source, last_run_at, last_success_at,
                    consecutive_errors, total_runs, total_errors, last_error, backoff_until)
                VALUES (?, ?, ?, 0, 1, 0, NULL, NULL)
                ON CONFLICT(source) DO UPDATE SET
                    last_run_at = ?,
                    last_success_at = ?,
                    consecutive_errors = 0,
                    total_runs = total_runs + 1,
                    last_error = NULL,
                    backoff_until = NULL
                """,
                (source, now, now, now, now),
            )

    def record_failure(self, source: str, error: str) -> None:
        """Record failed scrape: increment errors, compute backoff."""
        now = datetime.utcnow()
        error_truncated = error[:500]
        now_iso = now.isoformat()

        with wal_connect(self.db_path) as conn:
            # Get current consecutive_errors to compute backoff
            row = conn.execute(
                "SELECT consecutive_errors FROM scraper_health WHERE source = ?",
                (source,),
            ).fetchone()
            prev_errors = row[0] if row else 0
            new_errors = prev_errors + 1
            backoff_secs = min(2**new_errors * 60, _MAX_BACKOFF_SECONDS)
            backoff_until = (now + timedelta(seconds=backoff_secs)).isoformat()

            conn.execute(
                """
                INSERT INTO scraper_health (source, last_run_at, last_success_at,
                    consecutive_errors, total_runs, total_errors, last_error, backoff_until)
                VALUES (?, ?, NULL, 1, 1, 1, ?, ?)
                ON CONFLICT(source) DO UPDATE SET
                    last_run_at = ?,
                    consecutive_errors = consecutive_errors + 1,
                    total_runs = total_runs + 1,
                    total_errors = total_errors + 1,
                    last_error = ?,
                    backoff_until = ?
                """,
                (source, now_iso, error_truncated, backoff_until,
                 now_iso, error_truncated, backoff_until),
            )
            logger.info(
                "scraper_backoff",
                source=source,
                consecutive_errors=new_errors,
                backoff_seconds=backoff_secs,
            )

    def should_skip(self, source: str) -> bool:
        """Return True if source is in backoff period."""
        now = datetime.utcnow().isoformat()
        with wal_connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT backoff_until FROM scraper_health WHERE source = ?",
                (source,),
            ).fetchone()
            if not row or not row[0]:
                return False
            return row[0] > now

    def get_all_health(self) -> list[dict]:
        """Return health status for all tracked sources."""
        with wal_connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM scraper_health ORDER BY source"
            ).fetchall()
            return [dict(r) for r in rows]

    def get_source_health(self, source: str) -> dict | None:
        """Return health status for a single source."""
        with wal_connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM scraper_health WHERE source = ?",
                (source,),
            ).fetchone()
            return dict(row) if row else None
