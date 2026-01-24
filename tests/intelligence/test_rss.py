"""Tests for RSS feed scraper."""

import pytest
from unittest.mock import MagicMock, patch


class TestRSSFeedScraper:
    """Test RSSFeedScraper (sync version)."""

    def test_source_name(self, temp_dirs):
        """Test source name extraction from URL."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.rss import RSSFeedScraper

        storage = IntelStorage(temp_dirs["intel_db"])
        scraper = RSSFeedScraper(storage, "https://example.com/feed.xml")

        assert "example" in scraper.source_name

    def test_source_name_custom(self, temp_dirs):
        """Test custom source name."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.rss import RSSFeedScraper

        storage = IntelStorage(temp_dirs["intel_db"])
        scraper = RSSFeedScraper(storage, "https://example.com/feed.xml", name="custom")

        assert scraper.source_name == "rss:custom"

    def test_extract_name_from_url(self, temp_dirs):
        """Test URL name extraction."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.rss import RSSFeedScraper

        storage = IntelStorage(temp_dirs["intel_db"])
        scraper = RSSFeedScraper(storage, "https://www.techcrunch.com/feed/")

        assert "techcrunch" in scraper.source_name

    @patch("intelligence.sources.rss.feedparser.parse")
    def test_scrape_parses_feed(self, mock_parse, temp_dirs):
        """Test that scrape uses feedparser."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.rss import RSSFeedScraper

        mock_entry = MagicMock()
        mock_entry.get.side_effect = lambda k, d=None: {
            "title": "Test Article",
            "link": "https://example.com/article",
        }.get(k, d)
        mock_entry.summary = "Test summary"

        mock_parse.return_value = MagicMock(entries=[mock_entry])

        storage = IntelStorage(temp_dirs["intel_db"])
        scraper = RSSFeedScraper(storage, "https://example.com/feed.xml")

        items = scraper.scrape()

        assert mock_parse.called
        assert len(items) == 1
        assert items[0].title == "Test Article"

    @patch("intelligence.sources.rss.feedparser.parse")
    def test_scrape_limits_entries(self, mock_parse, temp_dirs):
        """Test that scrape limits to 20 entries."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.rss import RSSFeedScraper

        mock_entries = []
        for i in range(30):
            entry = MagicMock()
            entry.get.side_effect = lambda k, d=None, i=i: {
                "title": f"Article {i}",
                "link": f"https://example.com/{i}",
            }.get(k, d)
            entry.summary = f"Summary {i}"
            mock_entries.append(entry)

        mock_parse.return_value = MagicMock(entries=mock_entries)

        storage = IntelStorage(temp_dirs["intel_db"])
        scraper = RSSFeedScraper(storage, "https://example.com/feed.xml")

        items = scraper.scrape()

        assert len(items) == 20

    def test_extract_tags(self, temp_dirs):
        """Test tag extraction from feed entry."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.rss import RSSFeedScraper

        storage = IntelStorage(temp_dirs["intel_db"])
        scraper = RSSFeedScraper(storage, "https://example.com/feed.xml")

        mock_entry = MagicMock()
        mock_tag1 = MagicMock(term="python")
        mock_tag2 = MagicMock(term="programming")
        mock_entry.tags = [mock_tag1, mock_tag2]

        tags = scraper._extract_tags(mock_entry)

        assert "python" in tags
        assert "programming" in tags

    def test_extract_tags_no_tags(self, temp_dirs):
        """Test tag extraction when entry has no tags."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.rss import RSSFeedScraper

        storage = IntelStorage(temp_dirs["intel_db"])
        scraper = RSSFeedScraper(storage, "https://example.com/feed.xml")

        mock_entry = MagicMock(spec=[])  # No tags attribute

        tags = scraper._extract_tags(mock_entry)

        assert tags == []


@pytest.mark.asyncio
class TestAsyncRSSFeedScraper:
    """Test AsyncRSSFeedScraper."""

    async def test_source_name(self, temp_dirs):
        """Test async RSS scraper source name."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.rss import AsyncRSSFeedScraper

        storage = IntelStorage(temp_dirs["intel_db"])
        scraper = AsyncRSSFeedScraper(storage, "https://blog.example.com/rss")

        assert "rss:" in scraper.source_name
        assert "blog" in scraper.source_name
        await scraper.close()

    async def test_custom_name(self, temp_dirs):
        """Test async RSS scraper with custom name."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.rss import AsyncRSSFeedScraper

        storage = IntelStorage(temp_dirs["intel_db"])
        scraper = AsyncRSSFeedScraper(
            storage,
            "https://example.com/feed",
            name="myblog"
        )

        assert scraper.source_name == "rss:myblog"
        await scraper.close()
