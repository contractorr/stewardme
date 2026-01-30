"""Tests for Dev.to scraper."""

import pytest
from intelligence.scraper import IntelStorage
from intelligence.sources.devto import DevToScraper


class TestDevToScraper:
    @pytest.fixture
    def storage(self, tmp_path):
        return IntelStorage(tmp_path / "test.db")

    def test_source_name(self, storage):
        scraper = DevToScraper(storage)
        assert scraper.source_name == "devto"

    def test_default_config(self, storage):
        scraper = DevToScraper(storage)
        assert scraper.per_page == 30
        assert scraper.top_period == "week"

    def test_custom_config(self, storage):
        scraper = DevToScraper(storage, per_page=10, top_period="month")
        assert scraper.per_page == 10
        assert scraper.top_period == "month"

    @pytest.mark.asyncio
    async def test_context_manager(self, storage):
        async with DevToScraper(storage) as scraper:
            assert scraper.client is not None
