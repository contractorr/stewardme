"""Tests for cross-source trending radar."""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from intelligence.trending_radar import (
    STOPWORDS,
    TrendingRadar,
    _detect_collocations,
    _extract_title_terms,
    _velocity_score,
)


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
    def test_phrase_extraction(self):
        terms = _extract_title_terms("Rust vs Go for WebAssembly")
        # "vs" and "for" are stopwords, so we get two phrases
        assert "rust" in terms
        assert "webassembly" in terms

    def test_multi_word_phrase(self):
        terms = _extract_title_terms("Machine learning transforms healthcare")
        assert "machine learning" in terms  # bigram from adjacent non-stopwords
        assert "learning transforms" in terms
        assert "transforms healthcare" in terms
        assert "healthcare" in terms

    def test_stopword_filtering(self):
        terms = _extract_title_terms("The new way to use this tool")
        assert "the" not in terms
        assert "new" not in terms
        assert "way" not in terms
        assert "use" not in terms
        # "tool" is now a stopword
        assert len(terms) == 0

    def test_expanded_stopwords(self):
        """Words that used to slip through are now filtered."""
        terms = _extract_title_terms("Your code career data open free")
        assert "your" not in terms
        assert "code" not in terms
        assert "career" not in terms
        assert "data" not in terms
        assert "open" not in terms
        assert "free" not in terms

    def test_hyphenated_terms(self):
        terms = _extract_title_terms("RISC-V meets real-time computing")
        assert "risc-v" in terms
        assert "real-time" in terms
        assert "computing" in terms
        assert "real-time computing" in terms  # bigram

    def test_short_tokens_excluded(self):
        terms = _extract_title_terms("AI is OK for ML")
        # "ai", "ok", "ml" are all < 3 chars, "is"/"for" are stopwords
        assert len(terms) == 0

    def test_adjacent_non_stopwords_form_phrase(self):
        terms = _extract_title_terms("Google DeepMind releases Gemini Pro")
        assert "google deepmind" in terms or "gemini pro" in terms


class TestStopwords:
    def test_your_is_stopword(self):
        assert "your" in STOPWORDS

    def test_code_is_stopword(self):
        assert "code" in STOPWORDS

    def test_career_is_stopword(self):
        assert "career" in STOPWORDS

    def test_domain_terms_not_stopwords(self):
        """Actual tech topics should not be in stopwords."""
        for term in ["kubernetes", "rust", "python", "docker", "llm", "transformer"]:
            assert term not in STOPWORDS


class TestCollocations:
    def test_detect_significant_bigrams(self):
        # Repeat "machine learning" across many titles to make it statistically significant
        titles = [
            "Machine learning for healthcare",
            "Machine learning in production",
            "Machine learning benchmarks",
            "Machine learning infrastructure",
            "Deep learning vs machine learning",
            "Machine learning ops best practices",
            "Advances in machine learning",
            "Machine learning at scale",
        ]
        collocations = _detect_collocations(titles, threshold=10.0)
        assert "machine learning" in collocations

    def test_no_collocations_on_sparse_data(self):
        titles = ["Rust release", "Go update", "Python news"]
        collocations = _detect_collocations(titles, threshold=15.0)
        assert len(collocations) == 0

    def test_empty_titles(self):
        assert _detect_collocations([], threshold=15.0) == {}


class TestVelocityScore:
    def test_all_recent_items(self):
        now = datetime.now()
        items = [{"scraped_at": (now - timedelta(hours=2)).isoformat()} for _ in range(5)]
        score = _velocity_score(items, now, total_days=7, hot_hours=24)
        # All items in recent window, no baseline → brand-new boost
        assert score > 1.0

    def test_all_old_items(self):
        now = datetime.now()
        items = [{"scraped_at": (now - timedelta(days=4)).isoformat()} for _ in range(5)]
        score = _velocity_score(items, now, total_days=7, hot_hours=24)
        # All items in baseline, none recent → velocity < 1
        assert score == 0.0  # recent_rate is 0

    def test_accelerating_topic(self):
        now = datetime.now()
        # 1 old mention, 5 recent mentions
        items = [
            {"scraped_at": (now - timedelta(days=3)).isoformat()},
            *[{"scraped_at": (now - timedelta(hours=h)).isoformat()} for h in range(5)],
        ]
        score = _velocity_score(items, now, total_days=7, hot_hours=24)
        assert score > 1.0  # accelerating

    def test_capped_at_five(self):
        now = datetime.now()
        items = [{"scraped_at": (now - timedelta(minutes=10)).isoformat()} for _ in range(100)]
        score = _velocity_score(items, now, total_days=7, hot_hours=24)
        assert score <= 5.0


class TestRecencyScore:
    def test_fresh_item_scores_high(self, db_path):
        _insert_item(
            db_path, "hackernews", "Rust release", "https://a.com/1", "rust", hours_ago=0.1
        )
        _insert_item(db_path, "reddit", "Rust update", "https://b.com/1", "rust", hours_ago=0.1)
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_sources=2)
        topics = {t["topic"]: t for t in snapshot["topics"]}
        assert "rust" in topics
        # Velocity should be high for items just added
        assert topics["rust"]["velocity"] > 0

    def test_old_item_low_velocity(self, db_path):
        _insert_item(db_path, "hackernews", "Rust old", "https://a.com/2", "rust", hours_ago=167)
        _insert_item(db_path, "reddit", "Rust ancient", "https://b.com/2", "rust", hours_ago=167)
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_sources=2)
        topics = {t["topic"]: t for t in snapshot["topics"]}
        if "rust" in topics:
            assert topics["rust"]["velocity"] == 0


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

    def test_title_phrase_matching(self, db_path):
        """Multi-word phrases discovered from titles."""
        _insert_item(db_path, "hackernews", "Mistral AI releases new model", "https://a.com/m1", "")
        _insert_item(
            db_path, "reddit", "Mistral AI benchmarks show promise", "https://b.com/m1", ""
        )
        _insert_item(db_path, "arxiv", "Mistral AI architecture analysis", "https://c.com/m1", "")
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_sources=2)
        topic_names = [t["topic"] for t in snapshot["topics"]]
        # Should surface "mistral" (possibly as part of a phrase)
        assert any("mistral" in t for t in topic_names)

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

    def test_sublinear_tf_dampens_frequency(self, db_path):
        """High-frequency topic doesn't completely dominate scoring."""
        # Topic A: 20 items from 2 sources
        for i in range(20):
            src = "hackernews" if i % 2 == 0 else "reddit"
            _insert_item(db_path, src, f"Alpha post {i}", f"https://{src}.com/alpha{i}", "alpha")
        # Topic B: 5 items from 3 sources
        for i, src in enumerate(["hackernews", "reddit", "arxiv", "hackernews", "reddit"]):
            _insert_item(db_path, src, f"Beta post {i}", f"https://{src}.com/beta{i}", "beta")
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_sources=2)
        topics = {t["topic"]: t for t in snapshot["topics"]}
        assert "alpha" in topics and "beta" in topics
        # With sublinear TF, alpha shouldn't be 4x beta's score despite 4x the items
        ratio = topics["alpha"]["score"] / topics["beta"]["score"]
        assert ratio < 3.0  # sublinear dampening

    def test_velocity_field_present(self, db_path):
        """Topics include velocity field instead of avg_recency."""
        _insert_item(db_path, "hackernews", "Rust news", "https://a.com/v1", "rust")
        _insert_item(db_path, "reddit", "Rust update", "https://b.com/v1", "rust")
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_sources=2)
        for topic in snapshot["topics"]:
            assert "velocity" in topic
            assert "avg_recency" not in topic


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
