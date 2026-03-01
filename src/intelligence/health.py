"""Scraper health tracking with exponential backoff."""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

import structlog

from db import wal_connect

logger = structlog.get_logger().bind(source="scraper_health")

_MAX_BACKOFF_SECONDS = 3600

_RSS_FEED_HEALTH_DDL = """
CREATE TABLE IF NOT EXISTS rss_feed_health (
    feed_url TEXT PRIMARY KEY,
    last_attempt_at TIMESTAMP,
    last_success_at TIMESTAMP,
    consecutive_errors INTEGER DEFAULT 0,
    total_attempts INTEGER DEFAULT 0,
    total_errors INTEGER DEFAULT 0,
    last_error TEXT
)
"""


class ScraperHealthTracker:
    """Track scraper health and manage backoff for failing sources."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path).expanduser()

    def record_success(
        self,
        source: str,
        items_scraped: int = 0,
        items_new: int = 0,
        duration_s: float | None = None,
        items_deduped: int = 0,
    ) -> None:
        """Record successful scrape: reset errors, clear backoff, store metrics."""
        now = datetime.utcnow().isoformat()
        with wal_connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO scraper_health (source, last_run_at, last_success_at,
                    consecutive_errors, total_runs, total_errors, last_error, backoff_until,
                    last_items_scraped, last_items_new, last_duration_seconds, last_items_deduped)
                VALUES (?, ?, ?, 0, 1, 0, NULL, NULL, ?, ?, ?, ?)
                ON CONFLICT(source) DO UPDATE SET
                    last_run_at = ?,
                    last_success_at = ?,
                    consecutive_errors = 0,
                    total_runs = total_runs + 1,
                    last_error = NULL,
                    backoff_until = NULL,
                    last_items_scraped = ?,
                    last_items_new = ?,
                    last_duration_seconds = ?,
                    last_items_deduped = ?
                """,
                (
                    source,
                    now,
                    now,
                    items_scraped,
                    items_new,
                    duration_s,
                    items_deduped,
                    now,
                    now,
                    items_scraped,
                    items_new,
                    duration_s,
                    items_deduped,
                ),
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
                (
                    source,
                    now_iso,
                    error_truncated,
                    backoff_until,
                    now_iso,
                    error_truncated,
                    backoff_until,
                ),
            )
            if new_errors >= 3:
                logger.warning(
                    "scraper_consecutive_failures",
                    source=source,
                    count=new_errors,
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
            rows = conn.execute("SELECT * FROM scraper_health ORDER BY source").fetchall()
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

    def get_health_summary(self) -> list[dict]:
        """Return health with computed status and error_rate per source."""
        now = datetime.utcnow().isoformat()
        rows = self.get_all_health()
        for r in rows:
            errs = r.get("consecutive_errors", 0) or 0
            if r.get("backoff_until") and r["backoff_until"] > now:
                r["status"] = "backoff"
            elif errs >= 3:
                r["status"] = "failing"
            elif errs >= 1:
                r["status"] = "degraded"
            else:
                r["status"] = "healthy"
            total = r.get("total_runs", 0) or 0
            total_err = r.get("total_errors", 0) or 0
            r["error_rate"] = round(total_err / total * 100, 1) if total else 0.0
        return rows


class RSSFeedHealthTracker:
    """Per-feed health tracking for individual RSS feed URLs."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path).expanduser()
        with wal_connect(self.db_path) as conn:
            conn.execute(_RSS_FEED_HEALTH_DDL)

    def record_success(self, feed_url: str) -> None:
        now = datetime.utcnow().isoformat()
        with wal_connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO rss_feed_health
                    (feed_url, last_attempt_at, last_success_at,
                     consecutive_errors, total_attempts, total_errors, last_error)
                VALUES (?, ?, ?, 0, 1, 0, NULL)
                ON CONFLICT(feed_url) DO UPDATE SET
                    last_attempt_at = ?,
                    last_success_at = ?,
                    consecutive_errors = 0,
                    total_attempts = total_attempts + 1,
                    last_error = NULL
                """,
                (feed_url, now, now, now, now),
            )

    def record_failure(self, feed_url: str, error: str) -> None:
        now = datetime.utcnow().isoformat()
        error_truncated = error[:500]
        with wal_connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO rss_feed_health
                    (feed_url, last_attempt_at, last_success_at,
                     consecutive_errors, total_attempts, total_errors, last_error)
                VALUES (?, ?, NULL, 1, 1, 1, ?)
                ON CONFLICT(feed_url) DO UPDATE SET
                    last_attempt_at = ?,
                    consecutive_errors = consecutive_errors + 1,
                    total_attempts = total_attempts + 1,
                    total_errors = total_errors + 1,
                    last_error = ?
                """,
                (feed_url, now, error_truncated, now, error_truncated),
            )

    def get_all_health(self) -> list[dict]:
        with wal_connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT * FROM rss_feed_health ORDER BY feed_url").fetchall()
            return [dict(r) for r in rows]

    def get_feed_health(self, feed_url: str) -> dict | None:
        with wal_connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM rss_feed_health WHERE feed_url = ?",
                (feed_url,),
            ).fetchone()
            return dict(row) if row else None
