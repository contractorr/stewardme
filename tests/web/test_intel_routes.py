"""Tests for intel API routes (search, recent, scrape, trending, rss-feeds health)."""

from unittest.mock import AsyncMock, MagicMock, patch


def test_get_recent_empty(client, auth_headers):
    mock_storage = MagicMock()
    mock_storage.get_recent.return_value = []
    with patch("web.routes.intel._get_storage", return_value=mock_storage):
        res = client.get("/api/intel/recent", headers=auth_headers)
    assert res.status_code == 200
    assert res.json() == []


def test_get_recent_with_items(client, auth_headers):
    mock_storage = MagicMock()
    mock_storage.get_recent.return_value = [
        {
            "source": "hackernews",
            "title": "AI Breakthrough",
            "url": "https://example.com",
            "summary": "Big news",
        },
    ]
    with patch("web.routes.intel._get_storage", return_value=mock_storage):
        res = client.get("/api/intel/recent?days=3&limit=10", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["title"] == "AI Breakthrough"
    mock_storage.get_recent.assert_called_once_with(days=3, limit=10)


def test_search(client, auth_headers):
    mock_storage = MagicMock()
    mock_storage.search.return_value = [
        {"source": "reddit", "title": "Rust tips", "url": "https://r.com", "summary": "Tips"},
    ]
    with patch("web.routes.intel._get_storage", return_value=mock_storage):
        res = client.get("/api/intel/search?q=rust&limit=5", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.json()) == 1
    mock_storage.search.assert_called_once_with("rust", limit=5)


def test_scrape_trigger(client, auth_headers):
    mock_scheduler = MagicMock()
    mock_scheduler._run_async = AsyncMock(return_value={"sources": 3})
    with (
        patch("web.routes.intel._get_storage", return_value=MagicMock()),
        patch("intelligence.scheduler.IntelScheduler", return_value=mock_scheduler),
        patch("journal.storage.JournalStorage"),
        patch("journal.embeddings.EmbeddingManager"),
    ):
        res = client.post("/api/intel/scrape", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["status"] == "completed"


def test_trending_returns_personalized_flag(client, auth_headers):
    """Trending endpoint adds personalized flag to snapshot."""
    mock_snapshot = {
        "computed_at": "2026-01-01T00:00:00",
        "days": 7,
        "total_items_scanned": 10,
        "topics": [
            {
                "topic": "rust",
                "score": 0.5,
                "item_count": 4,
                "source_count": 2,
                "sources": ["hackernews", "rss:news"],
                "velocity": 1.5,
                "items": [
                    {
                        "id": 1,
                        "title": "Rust 2.0",
                        "url": "https://a.com",
                        "source": "hackernews",
                        "summary": "new",
                    },
                ],
            },
        ],
    }
    mock_radar = MagicMock()
    mock_radar.load.return_value = mock_snapshot

    with (
        patch(
            "intelligence.trending_radar.TrendingRadar",
            return_value=mock_radar,
        ),
        patch(
            "web.routes.intel._personalize_trending",
            return_value={**mock_snapshot, "personalized": False},
        ),
    ):
        res = client.get("/api/intel/trending", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert "personalized" in data


def test_scrape_injects_user_github_token(client, auth_headers, secret_key):
    """User's stored github_token flows into scheduler full_config."""
    captured = {}
    real_init_called = False

    class FakeScheduler:
        def __init__(self, **kwargs):
            nonlocal real_init_called
            real_init_called = True
            captured.update(kwargs)
            self._scrapers = []

        async def _run_async(self):
            return {"sources": 0}

    with (
        patch("web.routes.intel._get_storage", return_value=MagicMock()),
        patch("intelligence.scheduler.IntelScheduler", FakeScheduler),
        patch("journal.storage.JournalStorage"),
        patch("journal.embeddings.EmbeddingManager"),
        patch(
            "web.user_store.get_user_secret",
            return_value="ghp_test_token_123",
        ),
        patch("web.deps.get_secret_key", return_value=secret_key),
    ):
        res = client.post("/api/intel/scrape", headers=auth_headers)
    assert res.status_code == 200
    assert real_init_called
    token = captured["full_config"]["projects"]["github_issues"]["token"]
    assert token == "ghp_test_token_123"


def test_scrape_works_without_github_token(client, auth_headers):
    """Scrape still works when user has no stored github_token."""
    mock_scheduler = MagicMock()
    mock_scheduler._run_async = AsyncMock(return_value={"sources": 0})
    with (
        patch("web.routes.intel._get_storage", return_value=MagicMock()),
        patch("intelligence.scheduler.IntelScheduler", return_value=mock_scheduler),
        patch("journal.storage.JournalStorage"),
        patch("journal.embeddings.EmbeddingManager"),
        patch("web.user_store.get_user_secret", return_value=None),
        patch("web.deps.get_secret_key", return_value="fake-key"),
    ):
        res = client.post("/api/intel/scrape", headers=auth_headers)
    assert res.status_code == 200


def test_rss_feeds_includes_health(client, auth_headers):
    """RSS feeds endpoint attaches per-feed health data."""
    mock_feeds = [{"url": "https://a.com/rss", "name": "A"}]
    mock_health = [
        {"feed_url": "https://a.com/rss", "consecutive_errors": 0, "total_attempts": 5},
    ]

    mock_fht = MagicMock()
    mock_fht.get_all_health.return_value = mock_health

    with (
        patch("web.routes.intel.get_user_rss_feeds", return_value=mock_feeds),
        patch(
            "intelligence.health.RSSFeedHealthTracker",
            return_value=mock_fht,
        ),
    ):
        res = client.get("/api/intel/rss-feeds", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["health"]["feed_url"] == "https://a.com/rss"
