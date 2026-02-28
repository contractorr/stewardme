"""Tests for feed catalog matching and deduplication logic."""

from web.feed_catalog import (
    FEED_CATALOG,
    MIN_FEEDS,
    feeds_for_categories,
    match_categories_to_profile,
)


def test_match_keywords_ai_ml():
    """Profile mentioning 'machine learning' should match ai_ml."""
    result = match_categories_to_profile(interests=["machine learning"])
    assert "ai_ml" in result


def test_match_keywords_multiple():
    """Multiple profile fields match multiple categories."""
    result = match_categories_to_profile(
        interests=["security"],
        technologies=["kubernetes"],
        languages=["react"],
    )
    assert "security" in result
    assert "devops_cloud" in result
    assert "web_dev" in result


def test_general_tech_always_included():
    """Even with empty profile, general_tech is returned."""
    result = match_categories_to_profile()
    assert result == ["general_tech"]

    result2 = match_categories_to_profile(interests=[], industries=[], technologies=[])
    assert "general_tech" in result2


def test_general_tech_included_with_other_matches():
    """general_tech is appended even when other categories match."""
    result = match_categories_to_profile(interests=["AI"])
    assert "ai_ml" in result
    assert "general_tech" in result


def test_feeds_deduplication():
    """HN appears in multiple categories but only once in output."""
    hn_url = "https://news.ycombinator.com/rss"
    # Both startups_vc and general_tech have HN
    feeds = feeds_for_categories(["startups_vc", "general_tech"])
    hn_feeds = [f for f in feeds if f["url"] == hn_url]
    assert len(hn_feeds) == 1


def test_feeds_for_unknown_category():
    """Unknown category IDs are silently ignored, padded with general_tech."""
    feeds = feeds_for_categories(["nonexistent_category"])
    # general_tech has 4 feeds, all added as padding
    assert len(feeds) == 4
    assert all(f["category_id"] == "general_tech" for f in feeds)


def test_feeds_min_padding():
    """If selected feeds < MIN_FEEDS, pad with general_tech."""
    # security has 3 feeds, which is < MIN_FEEDS
    feeds = feeds_for_categories(["security"])
    assert len(feeds) >= MIN_FEEDS


def test_feeds_no_padding_when_enough():
    """No padding when selected categories already have enough feeds."""
    # Pick categories with many feeds total
    feeds = feeds_for_categories(["ai_ml", "web_dev", "devops_cloud"])
    # Should have at least 9 feeds (4 + 3 + 3), no general_tech padding needed
    assert len(feeds) >= MIN_FEEDS
    # Verify all feeds have required fields
    for f in feeds:
        assert "url" in f
        assert "name" in f
        assert "category_id" in f


def test_catalog_has_expected_categories():
    """Verify catalog structure."""
    ids = {c.id for c in FEED_CATALOG}
    assert "ai_ml" in ids
    assert "general_tech" in ids
    assert "web_dev" in ids
    assert len(FEED_CATALOG) >= 10
    for cat in FEED_CATALOG:
        assert len(cat.feeds) >= 2
        assert cat.label
        assert cat.icon
