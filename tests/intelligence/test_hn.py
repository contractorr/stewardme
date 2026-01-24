"""Tests for Hacker News scraper."""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from datetime import datetime


class TestHackerNewsScraper:
    """Test HackerNewsScraper (sync version)."""

    def test_source_name(self, temp_dirs):
        """Test source name is correct."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.hn import HackerNewsScraper

        storage = IntelStorage(temp_dirs["intel_db"])
        scraper = HackerNewsScraper(storage)

        assert scraper.source_name == "hackernews"

    def test_detect_tags_ask_hn(self, temp_dirs):
        """Test tag detection for Ask HN posts."""
        from intelligence.utils import detect_hn_tags

        tags = detect_hn_tags("Ask HN: What are the best testing frameworks?")

        assert "ask-hn" in tags

    def test_detect_tags_show_hn(self, temp_dirs):
        """Test tag detection for Show HN posts."""
        from intelligence.utils import detect_hn_tags

        tags = detect_hn_tags("Show HN: My new Python framework")

        assert "show-hn" in tags
        assert "programming" in tags

    def test_detect_tags_topics(self, temp_dirs):
        """Test topic tag detection."""
        from intelligence.utils import detect_hn_tags

        tags = detect_hn_tags("New AI startup raises $50M in funding")

        assert "ai" in tags
        assert "startup" in tags

    @patch("intelligence.sources.hn.httpx.Client")
    def test_scrape_with_mock(self, mock_client_class, temp_dirs, mock_http_responses):
        """Test scraping with mocked HTTP responses."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.hn import HackerNewsScraper

        mock_client = MagicMock()
        mock_client_class.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_class.return_value.__exit__ = MagicMock(return_value=False)

        # Mock responses
        mock_client.get.side_effect = [
            MagicMock(json=MagicMock(return_value=mock_http_responses["hn_topstories"])),
            MagicMock(json=MagicMock(return_value=mock_http_responses["hn_story"])),
            MagicMock(json=MagicMock(return_value=mock_http_responses["hn_story"])),
            MagicMock(json=MagicMock(return_value=mock_http_responses["hn_story"])),
            MagicMock(json=MagicMock(return_value=mock_http_responses["hn_story"])),
            MagicMock(json=MagicMock(return_value=mock_http_responses["hn_story"])),
        ]

        storage = IntelStorage(temp_dirs["intel_db"])
        scraper = HackerNewsScraper(storage, max_stories=5)

        # Override client
        scraper.client = mock_client

        items = scraper.scrape()

        assert len(items) <= 5


@pytest.mark.asyncio
class TestAsyncHackerNewsScraper:
    """Test AsyncHackerNewsScraper."""

    async def test_source_name(self, temp_dirs):
        """Test async scraper source name."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.hn import AsyncHackerNewsScraper

        storage = IntelStorage(temp_dirs["intel_db"])
        scraper = AsyncHackerNewsScraper(storage)

        assert scraper.source_name == "hackernews"
        await scraper.close()

    async def test_detect_tags(self, temp_dirs):
        """Test tag detection in async scraper."""
        from intelligence.utils import detect_hn_tags

        tags = detect_hn_tags("Learning Rust for systems programming")

        assert "programming" in tags
