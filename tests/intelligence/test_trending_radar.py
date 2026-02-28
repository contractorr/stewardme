"""Tests for cross-source trending radar."""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from intelligence.trending_radar import TrendingRadar, _extract_title_terms


@pytest.fixture
def db_path(tmp_path):
    """Create a temp DB with intel_items table seeded."""
    path = tmp_path / "intel.db"
    conn = sqlite3.connect(path)
    conn.execute(
        """
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
            content_hash TEXT
        )
        """
    )
    conn.commit()
    conn.close()
    return path


def _insert_item(
    db_path: Path, source: str, title: str, url: str, tags: str = "", hours_ago: float = 0
):
    scraped_at = (datetime.now() - timedelta(hours=hours_ago)).isoformat()
    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT INTO intel_items (source, title, url, summary, scraped_at, tags) VALUES (?, ?, ?, ?, ?, ?)",
        (source, title, url, f"Summary of {title}", scraped_at, tags),
    )
    conn.commit()
    conn.close()


class TestExtractTitleTerms:
    def test_basic_extraction(self):
        terms = _extract_title_terms("Rust vs Go for WebAssembly")
        assert "rust" in terms
        assert "webassembly" in terms

    def test_stopword_filtering(self):
        terms = _extract_title_terms("The new way to use this tool")
        assert "the" not in terms
        assert "new" not in terms
        assert "way" not in terms
        assert "use" not in terms
        assert "tool" in terms

    def test_hyphenated_terms(self):
        terms = _extract_title_terms("RISC-V meets real-time computing")
        assert "risc-v" in terms
        assert "real-time" in terms

    def test_short_tokens_excluded(self):
        terms = _extract_title_terms("AI is OK for ML")
        # "ai", "is", "ok", "ml" are all < 3 chars or stopwords
        assert "ai" not in terms
        assert "is" not in terms


class TestRecencyScore:
    def test_fresh_item_score_near_one(self, db_path):
        _insert_item(
            db_path, "hackernews", "Rust release", "https://a.com/1", "rust", hours_ago=0.1
        )
        _insert_item(db_path, "reddit", "Rust update", "https://b.com/1", "rust", hours_ago=0.1)
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_sources=2)
        topics = {t["topic"]: t for t in snapshot["topics"]}
        assert "rust" in topics
        assert topics["rust"]["avg_recency"] > 0.9

    def test_old_item_score_near_zero(self, db_path):
        _insert_item(db_path, "hackernews", "Rust old", "https://a.com/2", "rust", hours_ago=167)
        _insert_item(db_path, "reddit", "Rust ancient", "https://b.com/2", "rust", hours_ago=167)
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_sources=2)
        topics = {t["topic"]: t for t in snapshot["topics"]}
        if "rust" in topics:
            assert topics["rust"]["avg_recency"] < 0.02

    def test_midpoint_recency(self, db_path):
        _insert_item(db_path, "hackernews", "Rust mid", "https://a.com/3", "rust", hours_ago=84)
        _insert_item(db_path, "reddit", "Rust mid2", "https://b.com/3", "rust", hours_ago=84)
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_sources=2)
        topics = {t["topic"]: t for t in snapshot["topics"]}
        assert "rust" in topics
        assert 0.4 < topics["rust"]["avg_recency"] < 0.6


class TestCompute:
    def test_cross_source_surfaces(self, db_path):
        """Items from 3 sources with same tag → topic surfaces."""
        for i, src in enumerate(["hackernews", "reddit", "github_trending"]):
            _insert_item(
                db_path, src, f"Kubernetes {src} post", f"https://{src}.com/{i}", "kubernetes"
            )
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_sources=2)
        topics = {t["topic"]: t for t in snapshot["topics"]}
        assert "kubernetes" in topics
        assert topics["kubernetes"]["source_count"] == 3

    def test_single_source_filtered(self, db_path):
        """Items from 1 source only, min_sources=2 → empty."""
        for i in range(5):
            _insert_item(db_path, "hackernews", f"Solana post {i}", f"https://hn.com/{i}", "solana")
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_sources=2)
        topic_names = [t["topic"] for t in snapshot["topics"]]
        assert "solana" not in topic_names

    def test_empty_db(self, db_path):
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_sources=2)
        assert snapshot["topics"] == []
        assert snapshot["total_items_scanned"] == 0

    def test_title_term_matching(self, db_path):
        """Topic discovered via title terms even without tags."""
        _insert_item(db_path, "hackernews", "Mistral releases new model", "https://a.com/m1", "")
        _insert_item(db_path, "reddit", "Mistral AI benchmarks", "https://b.com/m1", "")
        _insert_item(db_path, "arxiv", "Mistral architecture analysis", "https://c.com/m1", "")
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_sources=2)
        topics = {t["topic"]: t for t in snapshot["topics"]}
        assert "mistral" in topics

    def test_max_topics_limit(self, db_path):
        """Respects max_topics."""
        for i in range(20):
            tag = f"topic{i:03d}"
            _insert_item(db_path, "hackernews", f"{tag} hn", f"https://hn.com/{tag}", tag)
            _insert_item(db_path, "reddit", f"{tag} reddit", f"https://reddit.com/{tag}", tag)
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_sources=2, max_topics=5)
        assert len(snapshot["topics"]) == 5

    def test_representative_items_capped(self, db_path):
        """Each topic gets at most 3 representative items."""
        for i in range(10):
            src = ["hackernews", "reddit", "arxiv"][i % 3]
            _insert_item(db_path, src, f"Rust post {i}", f"https://{src}.com/rust{i}", "rust")
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_sources=2)
        topics = {t["topic"]: t for t in snapshot["topics"]}
        assert "rust" in topics
        assert len(topics["rust"]["items"]) <= 3


class TestPersistence:
    def test_refresh_persists(self, db_path):
        _insert_item(db_path, "hackernews", "Go release", "https://a.com/g1", "golang")
        _insert_item(db_path, "reddit", "Go tutorial", "https://b.com/g1", "golang")
        radar = TrendingRadar(db_path)
        radar.refresh(days=7, min_sources=2)

        loaded = radar.load()
        assert loaded is not None
        assert loaded["total_items_scanned"] == 2

    def test_row_cap(self, db_path):
        _insert_item(db_path, "hackernews", "Test", "https://a.com/rc1", "test-topic")
        _insert_item(db_path, "reddit", "Test", "https://b.com/rc1", "test-topic")
        radar = TrendingRadar(db_path)

        for _ in range(25):
            radar.refresh(days=7, min_sources=2)

        conn = sqlite3.connect(db_path)
        count = conn.execute("SELECT COUNT(*) FROM trending_radar").fetchone()[0]
        conn.close()
        assert count <= TrendingRadar.MAX_ROWS

    def test_get_or_compute_cached(self, db_path):
        _insert_item(db_path, "hackernews", "Cache test", "https://a.com/c1", "cache-topic")
        _insert_item(db_path, "reddit", "Cache test", "https://b.com/c1", "cache-topic")
        radar = TrendingRadar(db_path)

        # First call computes and persists
        first = radar.get_or_compute(days=7, min_sources=2)
        assert first["total_items_scanned"] == 2

        # Second call returns cached
        second = radar.get_or_compute(days=7, min_sources=2)
        assert second["computed_at"] == first["computed_at"]

    def test_load_empty_db(self, db_path):
        radar = TrendingRadar(db_path)
        assert radar.load() is None
