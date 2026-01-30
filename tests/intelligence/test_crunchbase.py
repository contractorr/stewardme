"""Tests for Crunchbase scraper."""

import pytest
from intelligence.scraper import IntelStorage
from intelligence.sources.crunchbase import CrunchbaseScraper


class TestCrunchbaseScraper:
    @pytest.fixture
    def storage(self, tmp_path):
        return IntelStorage(tmp_path / "test.db")

    def test_source_name(self, storage):
        scraper = CrunchbaseScraper(storage, api_key="test_key")
        assert scraper.source_name == "crunchbase"

    def test_api_key_header(self, storage):
        scraper = CrunchbaseScraper(storage, api_key="test_key")
        assert scraper.client.headers["X-cb-user-key"] == "test_key"

    def test_default_limit(self, storage):
        scraper = CrunchbaseScraper(storage, api_key="test_key")
        assert scraper.limit == 30

    def test_custom_limit(self, storage):
        scraper = CrunchbaseScraper(storage, api_key="test_key", limit=50)
        assert scraper.limit == 50

    @pytest.mark.asyncio
    async def test_context_manager(self, storage):
        async with CrunchbaseScraper(storage, api_key="test") as scraper:
            assert scraper.client is not None
