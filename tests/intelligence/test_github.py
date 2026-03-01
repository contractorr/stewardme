"""Tests for GitHub trending scraper."""

import pytest


@pytest.mark.asyncio
class TestGitHubTrendingScraper:
    """Test GitHubTrendingScraper (async)."""

    async def test_source_name(self, temp_dirs):
        """Test source name is correct."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.github import GitHubTrendingScraper

        storage = IntelStorage(temp_dirs["intel_db"])
        scraper = GitHubTrendingScraper(storage)

        assert scraper.source_name == "github_trending"
        await scraper.close()

    async def test_default_languages(self, temp_dirs):
        """Test default language is python."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.github import GitHubTrendingScraper

        storage = IntelStorage(temp_dirs["intel_db"])
        scraper = GitHubTrendingScraper(storage)

        assert "python" in scraper.languages
        await scraper.close()

    async def test_custom_languages(self, temp_dirs):
        """Test custom languages configuration."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.github import GitHubTrendingScraper

        storage = IntelStorage(temp_dirs["intel_db"])
        scraper = GitHubTrendingScraper(
            storage,
            languages=["rust", "go"],
        )

        assert "rust" in scraper.languages
        assert "go" in scraper.languages
        assert "python" not in scraper.languages
        await scraper.close()

    async def test_timeframe_options(self, temp_dirs):
        """Test timeframe configuration."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.github import GitHubTrendingScraper

        storage = IntelStorage(temp_dirs["intel_db"])

        daily = GitHubTrendingScraper(storage, timeframe="daily")
        weekly = GitHubTrendingScraper(storage, timeframe="weekly")
        monthly = GitHubTrendingScraper(storage, timeframe="monthly")

        assert daily.timeframe == "daily"
        assert weekly.timeframe == "weekly"
        assert monthly.timeframe == "monthly"

        await daily.close()
        await weekly.close()
        await monthly.close()

    async def test_save_items(self, temp_dirs):
        """Test save_items method."""
        from intelligence.scraper import IntelItem, IntelStorage
        from intelligence.sources.github import GitHubTrendingScraper

        storage = IntelStorage(temp_dirs["intel_db"])
        scraper = GitHubTrendingScraper(storage)

        items = [
            IntelItem(
                source="github_trending",
                title="test/repo",
                url="https://github.com/test/repo",
                summary="1000 stars | A test repo",
            )
        ]

        new_count, deduped_count = await scraper.save_items(items)

        assert new_count == 1
        await scraper.close()

    async def test_context_manager(self, temp_dirs):
        """Test async context manager usage."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.github import GitHubTrendingScraper

        storage = IntelStorage(temp_dirs["intel_db"])

        async with GitHubTrendingScraper(storage) as scraper:
            assert scraper.source_name == "github_trending"
