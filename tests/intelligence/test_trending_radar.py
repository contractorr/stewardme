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
    _source_family,
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
    db_path: Path,
    source: str,
    title: str,
    url: str,
    tags: str = "",
    hours_ago: float = 0,
    published_hours_ago: float | None = None,
):
    scraped_at = (datetime.now() - timedelta(hours=hours_ago)).isoformat()
    published = None
    if published_hours_ago is not None:
        published = (datetime.now() - timedelta(hours=published_hours_ago)).isoformat()
    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT INTO intel_items (source, title, url, summary, scraped_at, tags, published) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (source, title, url, f"Summary of {title}", scraped_at, tags, published),
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
        assert "machine learning" in terms
        assert "learning transforms" in terms
        assert "transforms healthcare" in terms
        assert "healthcare" in terms

    def test_stopword_filtering(self):
        terms = _extract_title_terms("The new way to use this tool")
        assert "the" not in terms
        assert "new" not in terms
        assert "way" not in terms
        assert "use" not in terms
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
        assert "real-time computing" in terms

    def test_short_tokens_excluded(self):
        terms = _extract_title_terms("AI is OK for ML")
        assert len(terms) == 0

    def test_three_char_tokens_excluded(self):
        """Unigrams must be 4+ chars to filter junk like 'won', 'stop'."""
        terms = _extract_title_terms("won the race and got the job")
        assert "won" not in terms
        assert "got" not in terms

    def test_four_char_tokens_included(self):
        terms = _extract_title_terms("Rust and WebAssembly")
        assert "rust" in terms
        assert "webassembly" in terms

    def test_bigram_stopword_filtering(self):
        """Bigrams containing prepositions/articles are dropped."""
        terms = _extract_title_terms("the future of artificial intelligence")
        assert "of artificial" not in terms
        # But "artificial intelligence" should survive
        assert "artificial intelligence" in terms

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


class TestSourceFamily:
    def test_rss_sources_collapse(self):
        assert _source_family("rss:techcrunch") == "rss"
        assert _source_family("rss:ben-evans") == "rss"
        assert _source_family("rss:reddit") == "rss"

    def test_aggregators_collapse(self):
        assert _source_family("hackernews") == "aggregator"
        assert _source_family("producthunt") == "aggregator"

    def test_github_maps(self):
        assert _source_family("github_trending") == "github"

    def test_unknown_source_passthrough(self):
        assert _source_family("arxiv") == "arxiv"


class TestCollocations:
    def test_detect_significant_bigrams(self):
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
    def test_all_recent_items_spread(self):
        """Recent items with time spread get high velocity."""
        now = datetime.now()
        items = [
            {"scraped_at": (now - timedelta(hours=h)).isoformat()}
            for h in range(1, 20)
        ]
        score = _velocity_score(items, now, total_days=7, hot_hours=24)
        assert score > 1.0

    def test_all_old_items(self):
        now = datetime.now()
        # Spread across multiple days so batch detection doesn't trigger
        items = [
            {"scraped_at": (now - timedelta(days=d)).isoformat()}
            for d in range(2, 7)
        ]
        score = _velocity_score(items, now, total_days=7, hot_hours=24)
        assert score == 0.0  # recent_rate is 0

    def test_accelerating_topic(self):
        now = datetime.now()
        items = [
            {"scraped_at": (now - timedelta(days=3)).isoformat()},
            *[{"scraped_at": (now - timedelta(hours=h)).isoformat()} for h in range(5)],
        ]
        score = _velocity_score(items, now, total_days=7, hot_hours=24)
        assert score > 1.0

    def test_capped_at_five(self):
        now = datetime.now()
        # Spread items across hours so batch detection doesn't trigger
        items = [
            {"scraped_at": (now - timedelta(hours=i * 0.1)).isoformat()}
            for i in range(100)
        ]
        score = _velocity_score(items, now, total_days=7, hot_hours=24)
        assert score <= 5.0

    def test_same_batch_returns_neutral(self):
        """Items scraped in same batch (< 2h spread) → velocity 1.0."""
        now = datetime.now()
        items = [
            {"scraped_at": (now - timedelta(minutes=m)).isoformat()}
            for m in range(10)
        ]
        score = _velocity_score(items, now, total_days=7, hot_hours=24)
        assert score == 1.0

    def test_prefers_published_date(self):
        """Uses published date over scraped_at when available."""
        now = datetime.now()
        # All scraped at same time (batch), but published dates are spread
        scraped = (now - timedelta(minutes=5)).isoformat()
        items = [
            {"scraped_at": scraped, "published": (now - timedelta(days=d)).isoformat()}
            for d in range(7)
        ]
        score = _velocity_score(items, now, total_days=7, hot_hours=24)
        # published dates are spread, so batch detection won't trigger on them
        assert score != 1.0


class TestRecencyScore:
    def test_fresh_item_scores_high(self, db_path):
        # Use different source families so they pass min_source_families
        _insert_item(db_path, "hackernews", "Rust release", "https://a.com/1", "rust", hours_ago=1)
        _insert_item(db_path, "rss:news", "Rust update", "https://b.com/1", "rust", hours_ago=12)
        _insert_item(db_path, "github_trending", "Rust trending", "https://c.com/1", "rust", hours_ago=24)
        _insert_item(db_path, "rss:reddit", "Rust reddit", "https://d.com/1", "rust", hours_ago=48)
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_source_families=2, min_items=2)
        topics = {t["topic"]: t for t in snapshot["topics"]}
        assert "rust" in topics
        assert topics["rust"]["velocity"] > 0

    def test_old_item_low_velocity(self, db_path):
        # Spread across days so batch detection doesn't trigger
        _insert_item(db_path, "hackernews", "Rust old", "https://a.com/2", "rust", hours_ago=167)
        _insert_item(db_path, "rss:news", "Rust ancient", "https://b.com/2", "rust", hours_ago=120)
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_source_families=2, min_items=1)
        topics = {t["topic"]: t for t in snapshot["topics"]}
        if "rust" in topics:
            assert topics["rust"]["velocity"] == 0


class TestCompute:
    def test_cross_source_families_surfaces(self, db_path):
        """Items from 3 different source families → topic surfaces."""
        _insert_item(db_path, "hackernews", "Kubernetes HN", "https://hn.com/k1", "kubernetes", 1)
        _insert_item(db_path, "rss:news", "Kubernetes RSS", "https://rss.com/k1", "kubernetes", 12)
        _insert_item(
            db_path, "github_trending", "Kubernetes GH", "https://gh.com/k1", "kubernetes", 24
        )
        _insert_item(db_path, "rss:reddit", "Kubernetes Reddit", "https://rd.com/k1", "kubernetes", 48)
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_source_families=2, min_items=2)
        topics = {t["topic"]: t for t in snapshot["topics"]}
        assert "kubernetes" in topics
        # 3 families: aggregator (HN), rss (rss:news+rss:reddit), github
        assert len(topics["kubernetes"]["source_families"]) == 3

    def test_single_family_filtered(self, db_path):
        """Multiple rss sources are one family — doesn't pass min_source_families=2."""
        for i, src in enumerate(["rss:techcrunch", "rss:reddit", "rss:news", "rss:ben-evans"]):
            _insert_item(db_path, src, f"Solana post {i}", f"https://{src}.com/{i}", "solana")
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_source_families=2, min_items=1)
        topic_names = [t["topic"] for t in snapshot["topics"]]
        assert "solana" not in topic_names

    def test_empty_db(self, db_path):
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_source_families=2)
        assert snapshot["topics"] == []
        assert snapshot["total_items_scanned"] == 0

    def test_min_items_gate(self, db_path):
        """Topics with fewer than min_items are filtered out."""
        # Only 2 items — below min_items=4
        _insert_item(db_path, "hackernews", "Zig news", "https://a.com/z1", "ziglang", 1)
        _insert_item(db_path, "rss:news", "Zig update", "https://b.com/z1", "ziglang", 12)
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_source_families=2, min_items=4)
        topic_names = [t["topic"] for t in snapshot["topics"]]
        assert "ziglang" not in topic_names

    def test_title_phrase_matching(self, db_path):
        """Multi-word phrases discovered from titles."""
        for i, src in enumerate(["hackernews", "rss:news", "github_trending", "rss:reddit"]):
            _insert_item(db_path, src, f"Mistral AI post {i}", f"https://{src}.com/m{i}", "", i * 12)
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_source_families=2, min_items=2)
        topic_names = [t["topic"] for t in snapshot["topics"]]
        assert any("mistral" in t for t in topic_names)

    def test_max_topics_limit(self, db_path):
        """Respects max_topics."""
        for i in range(20):
            tag = f"topic{i:03d}"
            _insert_item(db_path, "hackernews", f"{tag} hn", f"https://hn.com/{tag}", tag, i)
            _insert_item(db_path, "rss:news", f"{tag} rss", f"https://rss.com/{tag}", tag, i + 1)
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_source_families=2, min_items=1, max_topics=5)
        assert len(snapshot["topics"]) == 5

    def test_representative_items_capped(self, db_path):
        """Each topic gets at most 3 representative items."""
        for i in range(10):
            src = ["hackernews", "rss:news", "github_trending"][i % 3]
            _insert_item(db_path, src, f"Rust post {i}", f"https://{src}.com/rust{i}", "rust", i)
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_source_families=2, min_items=1)
        topics = {t["topic"]: t for t in snapshot["topics"]}
        assert "rust" in topics
        assert len(topics["rust"]["items"]) <= 3

    def test_sublinear_tf_dampens_frequency(self, db_path):
        """High-frequency topic doesn't completely dominate scoring."""
        # Topic A: 20 items from 2 families (aggregator, rss)
        for i in range(20):
            src = "hackernews" if i % 2 == 0 else "rss:news"
            _insert_item(db_path, src, f"Alpha post {i}", f"https://{src}.com/alpha{i}", "alpha", i)
        # Topic B: 5 items from 3 families
        for i, src in enumerate(["hackernews", "rss:news", "github_trending", "hackernews", "rss:reddit"]):
            _insert_item(db_path, src, f"Beta post {i}", f"https://{src}.com/beta{i}", "beta", i)
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_source_families=2, min_items=1)
        topics = {t["topic"]: t for t in snapshot["topics"]}
        assert "alpha" in topics and "beta" in topics
        ratio = topics["alpha"]["score"] / topics["beta"]["score"]
        assert ratio < 3.0

    def test_velocity_field_present(self, db_path):
        _insert_item(db_path, "hackernews", "Rust news", "https://a.com/v1", "rust", 1)
        _insert_item(db_path, "rss:news", "Rust update", "https://b.com/v1", "rust", 12)
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_source_families=2, min_items=1)
        for topic in snapshot["topics"]:
            assert "velocity" in topic
            assert "source_families" in topic

    def test_junk_unigrams_filtered(self, db_path):
        """Short junk words like 'won', 'stop', 'life' don't surface as topics."""
        for i, src in enumerate(["hackernews", "rss:news", "github_trending", "rss:reddit"]):
            _insert_item(db_path, src, f"We won the race {i}", f"https://{src}.com/won{i}", "", i * 12)
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_source_families=2, min_items=1)
        topic_names = [t["topic"] for t in snapshot["topics"]]
        assert "won" not in topic_names

    def test_source_families_in_output(self, db_path):
        """Output includes source_families field."""
        _insert_item(db_path, "hackernews", "Docker news", "https://a.com/d1", "docker", 1)
        _insert_item(db_path, "rss:news", "Docker update", "https://b.com/d1", "docker", 12)
        _insert_item(db_path, "github_trending", "Docker trending", "https://c.com/d1", "docker", 24)
        _insert_item(db_path, "rss:reddit", "Docker reddit", "https://d.com/d1", "docker", 48)
        radar = TrendingRadar(db_path)
        snapshot = radar.compute(days=7, min_source_families=2, min_items=2)
        topics = {t["topic"]: t for t in snapshot["topics"]}
        assert "docker" in topics
        assert "source_families" in topics["docker"]
        assert "aggregator" in topics["docker"]["source_families"]


class TestPersistence:
    def test_refresh_persists(self, db_path):
        _insert_item(db_path, "hackernews", "Go release", "https://a.com/g1", "golang", 1)
        _insert_item(db_path, "rss:news", "Go tutorial", "https://b.com/g1", "golang", 12)
        radar = TrendingRadar(db_path)
        radar.refresh(days=7, min_source_families=2, min_items=1)

        loaded = radar.load()
        assert loaded is not None
        assert loaded["total_items_scanned"] == 2

    def test_row_cap(self, db_path):
        _insert_item(db_path, "hackernews", "Test", "https://a.com/rc1", "test-topic", 1)
        _insert_item(db_path, "rss:news", "Test", "https://b.com/rc1", "test-topic", 12)
        radar = TrendingRadar(db_path)

        for _ in range(25):
            radar.refresh(days=7, min_source_families=2, min_items=1)

        conn = sqlite3.connect(db_path)
        count = conn.execute("SELECT COUNT(*) FROM trending_radar").fetchone()[0]
        conn.close()
        assert count <= TrendingRadar.MAX_ROWS

    def test_get_or_compute_cached(self, db_path):
        _insert_item(db_path, "hackernews", "Cache test", "https://a.com/c1", "cache-topic", 1)
        _insert_item(db_path, "rss:news", "Cache test", "https://b.com/c1", "cache-topic", 12)
        radar = TrendingRadar(db_path)

        first = radar.get_or_compute(days=7, min_source_families=2, min_items=1)
        assert first["total_items_scanned"] == 2

        second = radar.get_or_compute(days=7, min_source_families=2, min_items=1)
        assert second["computed_at"] == first["computed_at"]

    def test_load_empty_db(self, db_path):
        radar = TrendingRadar(db_path)
        assert radar.load() is None
