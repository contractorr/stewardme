"""Tests for Reddit scraper."""

import pytest

from intelligence.scraper import IntelStorage
from intelligence.sources.reddit import DEFAULT_SUBREDDITS, RedditScraper


class TestRedditScraper:
    @pytest.fixture
    def storage(self, tmp_path):
        return IntelStorage(tmp_path / "test.db")

    def test_source_name(self, storage):
        scraper = RedditScraper(storage)
        assert scraper.source_name == "reddit"

    def test_default_subreddits(self, storage):
        scraper = RedditScraper(storage)
        assert scraper.subreddits == DEFAULT_SUBREDDITS
        assert "cscareerquestions" in scraper.subreddits
        assert "startups" in scraper.subreddits

    def test_custom_subreddits(self, storage):
        scraper = RedditScraper(storage, subreddits=["programming"])
        assert scraper.subreddits == ["programming"]

    def test_timeframe(self, storage):
        scraper = RedditScraper(storage, timeframe="week")
        assert scraper.timeframe == "week"

    def test_user_agent(self, storage):
        scraper = RedditScraper(storage)
        assert "AI-Coach" in scraper.client.headers["User-Agent"]

    @pytest.mark.asyncio
    async def test_context_manager(self, storage):
        async with RedditScraper(storage) as scraper:
            assert scraper.client is not None
