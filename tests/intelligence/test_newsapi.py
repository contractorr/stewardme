"""Tests for NewsAPI scraper."""

import pytest
from intelligence.scraper import IntelStorage
from intelligence.sources.newsapi import NewsAPIScraper, DEFAULT_QUERIES


class TestNewsAPIScraper:
    @pytest.fixture
    def storage(self, tmp_path):
        return IntelStorage(tmp_path / "test.db")

    def test_source_name(self, storage):
        scraper = NewsAPIScraper(storage, api_key="test_key")
        assert scraper.source_name == "newsapi"

    def test_default_queries(self, storage):
        scraper = NewsAPIScraper(storage, api_key="test_key")
        assert scraper.queries == DEFAULT_QUERIES
        assert "startup funding" in scraper.queries

    def test_custom_queries(self, storage):
        scraper = NewsAPIScraper(storage, api_key="test_key", queries=["AI"])
        assert scraper.queries == ["AI"]

    def test_page_size(self, storage):
        scraper = NewsAPIScraper(storage, api_key="test_key", page_size=50)
        assert scraper.page_size == 50

    def test_days_back(self, storage):
        scraper = NewsAPIScraper(storage, api_key="test_key", days_back=3)
        assert scraper.days_back == 3

    @pytest.mark.asyncio
    async def test_context_manager(self, storage):
        async with NewsAPIScraper(storage, api_key="test") as scraper:
            assert scraper.client is not None
