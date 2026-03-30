"""Coverage for lower-effort intelligence scrapers."""

import asyncio
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest


class FeedEntry(dict):
    """Minimal feed entry with both dict and attribute access."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc


def _http_status_error(url: str, status_code: int = 500) -> httpx.HTTPStatusError:
    request = httpx.Request("GET", url)
    response = httpx.Response(status_code, request=request)
    return httpx.HTTPStatusError("boom", request=request, response=response)


@pytest.fixture
def storage():
    return MagicMock(name="intel_storage")


@pytest.mark.asyncio
class TestEventScraperCoverage:
    async def test_scrape_confs_tech_success_and_ignores_fetch_errors(self, storage):
        from intelligence.sources.events import EventScraper

        scraper = EventScraper(storage, topics=["python"])
        response = MagicMock(status_code=200)
        response.json.return_value = [
            {
                "name": "PyCon US",
                "url": "https://pycon.org",
                "city": "Pittsburgh",
                "country": "USA",
                "startDate": "2026-04-15",
            }
        ]
        scraper.client.get = AsyncMock(side_effect=[response, RuntimeError("network boom")])

        items = await scraper._scrape_confs_tech()

        assert len(items) == 1
        assert items[0].title == "PyCon US"
        assert "event" in items[0].tags
        await scraper.close()

    async def test_scrape_rss_events_non_200_returns_empty(self, storage):
        from intelligence.sources.events import EventScraper

        scraper = EventScraper(storage)
        scraper.client.get = AsyncMock(return_value=MagicMock(status_code=503))

        items = await scraper._scrape_rss_events("https://example.com/feed.xml")

        assert items == []
        await scraper.close()


@pytest.mark.asyncio
class TestGitHubIssuesScraperCoverage:
    async def test_search_issues_success(self, storage):
        from intelligence.sources.github_issues import GitHubIssuesScraper

        scraper = GitHubIssuesScraper(
            storage,
            languages=["python"],
            labels=["good-first-issue"],
        )
        response = MagicMock(status_code=200)
        response.raise_for_status = MagicMock()
        response.json.return_value = {
            "items": [
                {
                    "title": "Add tests",
                    "html_url": "https://github.com/acme/repo/issues/1",
                    "body": "Would love more coverage.",
                    "repository_url": "https://api.github.com/repos/acme/repo",
                    "labels": [{"name": "good-first-issue"}, {"name": "testing"}],
                    "created_at": "2026-03-01T12:00:00Z",
                    "comments": 3,
                }
            ]
        }
        scraper.client.get = AsyncMock(return_value=response)

        items = await scraper._search_issues("python", "good-first-issue")

        assert len(items) == 1
        assert items[0].source == "github_issues"
        assert items[0].title == "Add tests"
        assert "python" in items[0].tags
        assert "good-first-issue" in items[0].tags
        await scraper.close()

    async def test_search_issues_rate_limited_returns_empty(self, storage):
        from intelligence.sources.github_issues import GitHubIssuesScraper

        scraper = GitHubIssuesScraper(storage)
        scraper.client.get = AsyncMock(return_value=MagicMock(status_code=403))

        items = await scraper._search_issues("python", "good-first-issue")

        assert items == []
        await scraper.close()


@pytest.mark.asyncio
class TestGooglePatentsScraperCoverage:
    async def test_source_name(self, storage):
        from intelligence.sources.google_patents import GooglePatentsScraper

        scraper = GooglePatentsScraper(storage)

        assert scraper.source_name == "google_patents"
        await scraper.close()

    async def test_scrape_feed_success(self, storage):
        from intelligence.sources.google_patents import GooglePatentsScraper

        scraper = GooglePatentsScraper(storage, feeds=["https://example.com/patents.xml"])
        response = MagicMock()
        response.text = "<rss />"
        response.raise_for_status = MagicMock()
        scraper.client.get = AsyncMock(return_value=response)
        feed = MagicMock(
            entries=[
                FeedEntry(
                    title="AI accelerator architecture",
                    link="https://patents.google.com/patent/US123",
                    summary="<p>New accelerator for ML workloads.</p>",
                    published_parsed=(2026, 3, 1, 0, 0, 0, 0, 0, 0),
                )
            ]
        )

        with patch("intelligence.sources.google_patents.feedparser.parse", return_value=feed):
            items = await scraper._scrape_feed("https://example.com/patents.xml")

        assert len(items) == 1
        assert items[0].source == "google_patents"
        assert items[0].summary == "New accelerator for ML workloads."
        assert "patent" in items[0].tags
        await scraper.close()

    async def test_scrape_feed_error_returns_empty(self, storage):
        from intelligence.sources.google_patents import GooglePatentsScraper

        scraper = GooglePatentsScraper(storage, feeds=["https://example.com/patents.xml"])
        response = MagicMock()
        response.raise_for_status.side_effect = _http_status_error(
            "https://example.com/patents.xml"
        )
        scraper.client.get = AsyncMock(return_value=response)

        items = await scraper._scrape_feed("https://example.com/patents.xml")

        assert items == []
        await scraper.close()


@pytest.mark.asyncio
class TestProductHuntScraperCoverage:
    async def test_source_name(self, storage):
        from intelligence.sources.producthunt import ProductHuntScraper

        scraper = ProductHuntScraper(storage)

        assert scraper.source_name == "producthunt"
        await scraper.close()

    async def test_scrape_success(self, storage):
        from intelligence.sources.producthunt import ProductHuntScraper

        scraper = ProductHuntScraper(storage, feed_url="https://example.com/feed.xml")
        response = MagicMock()
        response.text = "<rss />"
        response.raise_for_status = MagicMock()
        scraper.client.get = AsyncMock(return_value=response)
        feed = MagicMock(
            entries=[
                FeedEntry(
                    title="Agent Console",
                    link="https://example.com/agent-console",
                    summary="<p>Launches AI workflows.</p>",
                    published_parsed=(2026, 3, 2, 0, 0, 0, 0, 0, 0),
                )
            ]
        )

        with patch("intelligence.sources.producthunt.feedparser.parse", return_value=feed):
            items = await scraper.scrape()

        assert len(items) == 1
        assert items[0].source == "producthunt"
        assert items[0].summary == "Launches AI workflows."
        assert "product-launch" in items[0].tags
        await scraper.close()

    async def test_scrape_error_returns_empty(self, storage):
        from intelligence.sources.producthunt import ProductHuntScraper

        scraper = ProductHuntScraper(storage, feed_url="https://example.com/feed.xml")
        response = MagicMock()
        response.raise_for_status.side_effect = _http_status_error("https://example.com/feed.xml")
        scraper.client.get = AsyncMock(return_value=response)

        items = await scraper.scrape()

        assert items == []
        await scraper.close()


@pytest.mark.asyncio
class TestYCJobsScraperCoverage:
    async def test_source_name(self, storage):
        from intelligence.sources.yc_jobs import YCJobsScraper

        scraper = YCJobsScraper(storage)

        assert scraper.source_name == "yc_jobs"
        await scraper.close()

    async def test_scrape_success(self, storage):
        from intelligence.sources.yc_jobs import YCJobsScraper

        scraper = YCJobsScraper(storage, max_items=1, concurrency=1)
        ids_response = MagicMock()
        ids_response.raise_for_status = MagicMock()
        ids_response.json.return_value = [123]
        job_response = MagicMock()
        job_response.raise_for_status = MagicMock()
        job_response.json.return_value = {
            "title": "Hiring founding engineer",
            "text": "<p>Work on Rust and Python systems.</p>",
            "time": int(datetime(2026, 3, 3, tzinfo=timezone.utc).timestamp()),
            "url": "https://jobs.example.com/founding-engineer",
        }
        scraper.client.get = AsyncMock(side_effect=[ids_response, job_response])

        items = await scraper.scrape()

        assert len(items) == 1
        assert items[0].source == "yc_jobs"
        assert items[0].summary == "Work on Rust and Python systems."
        assert "hiring" in items[0].tags
        await scraper.close()

    async def test_fetch_job_error_returns_none(self, storage):
        from intelligence.sources.yc_jobs import YCJobsScraper

        scraper = YCJobsScraper(storage)
        scraper.client.get = AsyncMock(
            side_effect=httpx.RequestError(
                "boom",
                request=httpx.Request("GET", "https://hacker-news.firebaseio.com/v0/item/1.json"),
            )
        )

        item = await scraper._fetch_job(asyncio.Semaphore(1), 1)

        assert item is None
        await scraper.close()
