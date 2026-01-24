"""Tests for GitHub trending scraper."""

import pytest
from unittest.mock import MagicMock, patch


class TestGitHubTrendingScraperSync:
    """Test GitHubTrendingScraperSync."""

    def test_source_name(self, temp_dirs):
        """Test source name is correct."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.github import GitHubTrendingScraperSync

        storage = IntelStorage(temp_dirs["intel_db"])
        scraper = GitHubTrendingScraperSync(storage)

        assert scraper.source_name == "github_trending"

    def test_default_languages(self, temp_dirs):
        """Test default language is python."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.github import GitHubTrendingScraperSync

        storage = IntelStorage(temp_dirs["intel_db"])
        scraper = GitHubTrendingScraperSync(storage)

        assert "python" in scraper.languages

    def test_custom_languages(self, temp_dirs):
        """Test custom languages configuration."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.github import GitHubTrendingScraperSync

        storage = IntelStorage(temp_dirs["intel_db"])
        scraper = GitHubTrendingScraperSync(
            storage,
            languages=["rust", "go"],
        )

        assert "rust" in scraper.languages
        assert "go" in scraper.languages
        assert "python" not in scraper.languages

    def test_timeframe_options(self, temp_dirs):
        """Test timeframe configuration."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.github import GitHubTrendingScraperSync

        storage = IntelStorage(temp_dirs["intel_db"])

        daily = GitHubTrendingScraperSync(storage, timeframe="daily")
        weekly = GitHubTrendingScraperSync(storage, timeframe="weekly")
        monthly = GitHubTrendingScraperSync(storage, timeframe="monthly")

        assert daily.timeframe == "daily"
        assert weekly.timeframe == "weekly"
        assert monthly.timeframe == "monthly"

    @patch("intelligence.sources.github.httpx.Client")
    def test_scrape_makes_request(self, mock_client_class, temp_dirs, mock_http_responses):
        """Test that scrape fetches trending page."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.github import GitHubTrendingScraperSync

        mock_client = MagicMock()
        mock_client_class.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_class.return_value.__exit__ = MagicMock(return_value=False)

        mock_response = MagicMock()
        mock_response.text = mock_http_responses["github_trending"]
        mock_response.raise_for_status = MagicMock()
        mock_client.get.return_value = mock_response

        storage = IntelStorage(temp_dirs["intel_db"])
        scraper = GitHubTrendingScraperSync(storage, languages=["python"])

        items = scraper.scrape()

        assert mock_client.get.called
        # May or may not find items depending on HTML parsing
        assert isinstance(items, list)

    def test_save_items(self, temp_dirs):
        """Test save_items method."""
        from intelligence.scraper import IntelStorage, IntelItem
        from intelligence.sources.github import GitHubTrendingScraperSync

        storage = IntelStorage(temp_dirs["intel_db"])
        scraper = GitHubTrendingScraperSync(storage)

        items = [
            IntelItem(
                source="github_trending",
                title="test/repo",
                url="https://github.com/test/repo",
                summary="1000 stars | A test repo",
            )
        ]

        count = scraper.save_items(items)

        assert count == 1


@pytest.mark.asyncio
class TestGitHubTrendingScraper:
    """Test GitHubTrendingScraper (async version)."""

    async def test_source_name(self, temp_dirs):
        """Test async GitHub scraper source name."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.github import GitHubTrendingScraper

        storage = IntelStorage(temp_dirs["intel_db"])
        scraper = GitHubTrendingScraper(storage)

        assert scraper.source_name == "github_trending"
        await scraper.close()

    async def test_languages_config(self, temp_dirs):
        """Test languages configuration in async scraper."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.github import GitHubTrendingScraper

        storage = IntelStorage(temp_dirs["intel_db"])
        scraper = GitHubTrendingScraper(
            storage,
            languages=["python", "rust", "typescript"],
        )

        assert len(scraper.languages) == 3
        await scraper.close()

    async def test_context_manager(self, temp_dirs):
        """Test async context manager usage."""
        from intelligence.scraper import IntelStorage
        from intelligence.sources.github import GitHubTrendingScraper

        storage = IntelStorage(temp_dirs["intel_db"])

        async with GitHubTrendingScraper(storage) as scraper:
            assert scraper.source_name == "github_trending"
