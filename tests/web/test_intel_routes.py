"""Tests for intel API routes (search, recent, scrape)."""

from unittest.mock import MagicMock, patch


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
    mock_scheduler.run_now.return_value = {"sources": 3}
    with (
        patch("web.routes.intel._get_storage", return_value=MagicMock()),
        patch("intelligence.scheduler.IntelScheduler", return_value=mock_scheduler),
        patch("journal.storage.JournalStorage"),
        patch("journal.embeddings.EmbeddingManager"),
    ):
        res = client.post("/api/intel/scrape", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["status"] == "completed"
