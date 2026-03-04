"""Tests for eval/intel.py — intel scraping quality evaluation."""

import sqlite3
from datetime import datetime, timedelta

import pytest

from eval.intel import (
    IntelEvalReport,
    _measure_content_quality,
    _measure_dedup,
    _measure_freshness,
    _measure_reliability,
    _measure_source_diversity,
    run_intel_eval,
)


@pytest.fixture
def intel_db(tmp_path):
    """Create a seeded intel.db for testing."""
    db_path = tmp_path / "intel.db"
    conn = sqlite3.connect(str(db_path))
    conn.execute("""
        CREATE TABLE intel_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            summary TEXT,
            content TEXT,
            published TIMESTAMP,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            tags TEXT,
            content_hash TEXT,
            duplicate_of INTEGER
        )
    """)
    conn.execute("""
        CREATE TABLE scraper_health (
            source TEXT PRIMARY KEY,
            last_run_at TIMESTAMP,
            last_success_at TIMESTAMP,
            consecutive_errors INTEGER DEFAULT 0,
            total_runs INTEGER DEFAULT 0,
            total_errors INTEGER DEFAULT 0,
            last_error TEXT,
            backoff_until TIMESTAMP,
            last_items_scraped INTEGER DEFAULT 0,
            last_items_new INTEGER DEFAULT 0,
            last_duration_seconds REAL,
            last_items_deduped INTEGER DEFAULT 0
        )
    """)

    now = datetime.utcnow()

    # Insert items from different sources, some fresh, some stale
    items = [
        (
            "hackernews",
            "AI Agents",
            "https://hn.com/1",
            "Summary about AI",
            now.isoformat(),
            "ai,agents",
            None,
        ),
        (
            "hackernews",
            "Rust Release",
            "https://hn.com/2",
            "Rust 2.0",
            (now - timedelta(days=2)).isoformat(),
            "rust",
            None,
        ),
        (
            "github_trending",
            "New Framework",
            "https://gh.com/1",
            "A framework",
            now.isoformat(),
            "",
            None,
        ),
        (
            "rss:blog",
            "Old Post",
            "https://blog.com/1",
            "Ancient post",
            (now - timedelta(days=30)).isoformat(),
            None,
            None,
        ),
        (
            "reddit",
            "Discussion",
            "https://reddit.com/1",
            None,
            (now - timedelta(days=1)).isoformat(),
            "python,ml",
            None,
        ),
        (
            "hackernews",
            "Duplicate",
            "https://hn.com/3",
            "Dup content",
            now.isoformat(),
            "ai",
            1,
        ),  # duplicate_of=1
    ]
    for source, title, url, summary, scraped_at, tags, dup in items:
        conn.execute(
            "INSERT INTO intel_items (source, title, url, summary, scraped_at, tags, duplicate_of) VALUES (?,?,?,?,?,?,?)",
            (source, title, url, summary, scraped_at, tags, dup),
        )

    # Insert scraper health
    health = [
        ("hackernews", now.isoformat(), now.isoformat(), 0, 10, 0, None, None, 20, 15, 1.5, 5),
        ("github_trending", now.isoformat(), now.isoformat(), 0, 5, 1, None, None, 10, 8, 2.0, 2),
        (
            "reddit",
            now.isoformat(),
            None,
            4,
            8,
            4,
            "timeout",
            (now + timedelta(hours=1)).isoformat(),
            0,
            0,
            None,
            0,
        ),
    ]
    for row in health:
        conn.execute(
            """INSERT INTO scraper_health
            (source, last_run_at, last_success_at, consecutive_errors, total_runs, total_errors,
             last_error, backoff_until, last_items_scraped, last_items_new, last_duration_seconds, last_items_deduped)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            row,
        )

    conn.commit()
    conn.close()
    return db_path


class TestMeasureFreshness:
    def test_with_data(self, intel_db):
        conn = sqlite3.connect(str(intel_db))
        result = _measure_freshness(conn, days=7)
        conn.close()
        assert result["total_items"] == 6
        assert 0 < result["pct_fresh"] <= 1.0
        assert result["staleness_p50_days"] is not None
        assert "buckets" in result

    def test_empty_db(self, tmp_path):
        db = tmp_path / "empty.db"
        conn = sqlite3.connect(str(db))
        conn.execute("CREATE TABLE intel_items (id INTEGER PRIMARY KEY, scraped_at TEXT)")
        result = _measure_freshness(conn, days=7)
        conn.close()
        assert result["total_items"] == 0
        assert result["pct_fresh"] == 0.0


class TestMeasureSourceDiversity:
    def test_with_data(self, intel_db):
        conn = sqlite3.connect(str(intel_db))
        result = _measure_source_diversity(conn)
        conn.close()
        assert result["unique_sources"] == 4  # hackernews, github_trending, rss:blog, reddit
        assert result["unique_families"] >= 3  # aggregator, github, rss, reddit
        assert 0 <= result["gini"] <= 1.0
        assert "hackernews" in result["per_source"]


class TestMeasureDedup:
    def test_with_data(self, intel_db):
        conn = sqlite3.connect(str(intel_db))
        result = _measure_dedup(conn)
        conn.close()
        assert result["duplicate_of_count"] == 1
        assert result["total_items"] == 6
        assert result["overall_dedup_ratio"] > 0
        assert "hackernews" in result["per_source"]


class TestMeasureReliability:
    def test_with_data(self, intel_db):
        conn = sqlite3.connect(str(intel_db))
        result = _measure_reliability(conn)
        conn.close()
        assert len(result["sources"]) == 3
        # hackernews=healthy, github_trending=healthy(0 consec errs), reddit=backoff
        statuses = {s["source"]: s["status"] for s in result["sources"]}
        assert statuses["hackernews"] == "healthy"
        assert statuses["reddit"] == "backoff"
        assert result["healthy_scraper_pct"] > 0


class TestMeasureContentQuality:
    def test_with_data(self, intel_db):
        conn = sqlite3.connect(str(intel_db))
        result = _measure_content_quality(conn)
        conn.close()
        assert result["avg_summary_len"] > 0
        assert 0 <= result["pct_has_tags"] <= 1.0
        assert result["pct_valid_url"] == 1.0  # all URLs start with https://


class TestRunIntelEval:
    def test_full_run(self, intel_db):
        report = run_intel_eval(intel_db)
        assert isinstance(report, IntelEvalReport)
        assert "passed" in report.summary
        assert report.freshness["total_items"] == 6

    def test_threshold_failure(self, intel_db):
        # Very strict thresholds
        report = run_intel_eval(intel_db, thresholds={"pct_fresh_min": 0.99})
        assert report.summary["passed"] is False
        assert len(report.summary["failures"]) > 0

    def test_to_dict(self, intel_db):
        report = run_intel_eval(intel_db)
        d = report.to_dict()
        assert "freshness" in d
        assert "summary" in d
