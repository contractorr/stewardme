"""Tests for intelligence scraper and storage."""

import pytest
from datetime import datetime


class TestIntelStorage:
    """Test IntelStorage SQLite operations."""

    def test_init_creates_db(self, temp_dirs):
        """Test that initialization creates database."""
        from intelligence.scraper import IntelStorage

        storage = IntelStorage(temp_dirs["intel_db"])

        assert temp_dirs["intel_db"].exists()

    def test_save_item(self, temp_dirs):
        """Test saving an intel item."""
        from intelligence.scraper import IntelStorage, IntelItem

        storage = IntelStorage(temp_dirs["intel_db"])

        item = IntelItem(
            source="test",
            title="Test Article",
            url="https://example.com/test",
            summary="Test summary",
        )

        result = storage.save(item)

        assert result is True

    def test_save_duplicate_url_ignored(self, temp_dirs):
        """Test that duplicate URLs are ignored."""
        from intelligence.scraper import IntelStorage, IntelItem

        storage = IntelStorage(temp_dirs["intel_db"])

        item = IntelItem(
            source="test",
            title="Original Title",
            url="https://example.com/unique",
            summary="Original summary",
        )

        first = storage.save(item)
        second = storage.save(item)  # Same URL

        assert first is True
        assert second is False

    def test_get_recent(self, populated_intel):
        """Test getting recent items."""
        items = populated_intel.get_recent(days=7)

        assert len(items) >= 3

    def test_get_recent_with_limit(self, populated_intel):
        """Test get_recent respects limit."""
        items = populated_intel.get_recent(days=7, limit=1)

        assert len(items) == 1

    def test_search(self, populated_intel):
        """Test keyword search."""
        results = populated_intel.search("AI")

        assert len(results) >= 1
        assert any("AI" in r["title"] or "AI" in r["summary"] for r in results)

    def test_search_no_results(self, populated_intel):
        """Test search with no matches."""
        results = populated_intel.search("xyznonexistent")

        assert len(results) == 0

    def test_tags_stored_correctly(self, temp_dirs):
        """Test that tags are stored and retrieved."""
        from intelligence.scraper import IntelStorage, IntelItem

        storage = IntelStorage(temp_dirs["intel_db"])

        item = IntelItem(
            source="test",
            title="Tagged Item",
            url="https://example.com/tagged",
            summary="Has tags",
            tags=["python", "ai", "testing"],
        )

        storage.save(item)
        results = storage.search("Tagged")

        assert len(results) >= 1
        assert "python" in results[0]["tags"]


class TestIntelItem:
    """Test IntelItem dataclass."""

    def test_create_minimal(self):
        """Test creating item with minimal fields."""
        from intelligence.scraper import IntelItem

        item = IntelItem(
            source="test",
            title="Title",
            url="https://example.com",
            summary="Summary",
        )

        assert item.source == "test"
        assert item.content is None
        assert item.tags is None

    def test_create_full(self):
        """Test creating item with all fields."""
        from intelligence.scraper import IntelItem

        item = IntelItem(
            source="hackernews",
            title="Full Item",
            url="https://example.com/full",
            summary="Full summary",
            content="Full content body",
            published=datetime.now(),
            tags=["tag1", "tag2"],
        )

        assert item.content == "Full content body"
        assert len(item.tags) == 2
