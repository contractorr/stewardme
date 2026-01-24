"""Job scheduling for intelligence gathering."""

import asyncio
from pathlib import Path
from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from .scraper import IntelStorage
from .sources import (
    RSSFeedScraper,
    HackerNewsScraper,
    AsyncRSSFeedScraper,
    AsyncHackerNewsScraper,
    GitHubTrendingScraper,
    GitHubTrendingScraperSync,
)


class IntelScheduler:
    """Manages scheduled intelligence gathering jobs."""

    def __init__(self, storage: IntelStorage, config: Optional[dict] = None):
        self.storage = storage
        self.config = config or {}
        self.scheduler = BackgroundScheduler()
        self._scrapers: list = []
        self._async_scrapers: list = []

    def _init_scrapers(self):
        """Initialize sync scrapers from config."""
        self._scrapers = []

        enabled = self.config.get("enabled", ["hn_top", "rss_feeds"])

        if "hn_top" in enabled:
            self._scrapers.append(HackerNewsScraper(self.storage))

        if "rss_feeds" in enabled:
            for url in self.config.get("rss_feeds", []):
                self._scrapers.append(RSSFeedScraper(self.storage, url))

        if "custom_blogs" in enabled:
            for url in self.config.get("custom_blogs", []):
                self._scrapers.append(RSSFeedScraper(self.storage, url))

        # GitHub trending
        gh_config = self.config.get("github_trending", {})
        if gh_config.get("enabled", False):
            self._scrapers.append(GitHubTrendingScraperSync(
                self.storage,
                languages=gh_config.get("languages", ["python"]),
                timeframe=gh_config.get("timeframe", "daily"),
            ))

    def _init_async_scrapers(self):
        """Initialize async scrapers from config."""
        self._async_scrapers = []

        enabled = self.config.get("enabled", ["hn_top", "rss_feeds"])

        if "hn_top" in enabled:
            self._async_scrapers.append(AsyncHackerNewsScraper(self.storage))

        if "rss_feeds" in enabled:
            for url in self.config.get("rss_feeds", []):
                self._async_scrapers.append(AsyncRSSFeedScraper(self.storage, url))

        if "custom_blogs" in enabled:
            for url in self.config.get("custom_blogs", []):
                self._async_scrapers.append(AsyncRSSFeedScraper(self.storage, url))

        # GitHub trending
        gh_config = self.config.get("github_trending", {})
        if gh_config.get("enabled", False):
            self._async_scrapers.append(GitHubTrendingScraper(
                self.storage,
                languages=gh_config.get("languages", ["python"]),
                timeframe=gh_config.get("timeframe", "daily"),
            ))

    def run_now(self) -> dict:
        """Run all scrapers immediately (sync version).

        Returns:
            Dict with scraper results {source: new_items_count}
        """
        self._init_scrapers()
        results = {}

        for scraper in self._scrapers:
            try:
                items = scraper.scrape()
                new_count = scraper.save_items(items)
                results[scraper.source_name] = {
                    "scraped": len(items),
                    "new": new_count,
                }
            except Exception as e:
                results[scraper.source_name] = {"error": str(e)}

        return results

    async def run_now_async(self) -> dict:
        """Run all scrapers concurrently.

        Returns:
            Dict with scraper results {source: new_items_count}
        """
        self._init_async_scrapers()
        results = {}

        async def run_scraper(scraper):
            """Run single scraper with timeout."""
            try:
                items = await asyncio.wait_for(scraper.scrape(), timeout=60.0)
                new_count = await scraper.save_items(items)
                return scraper.source_name, {
                    "scraped": len(items),
                    "new": new_count,
                }
            except asyncio.TimeoutError:
                return scraper.source_name, {"error": "timeout"}
            except Exception as e:
                return scraper.source_name, {"error": str(e)}
            finally:
                await scraper.close()

        # Run all scrapers concurrently
        tasks = [run_scraper(s) for s in self._async_scrapers]
        completed = await asyncio.gather(*tasks, return_exceptions=True)

        for result in completed:
            if isinstance(result, tuple):
                name, data = result
                results[name] = data
            elif isinstance(result, Exception):
                results["unknown"] = {"error": str(result)}

        return results

    def run_now_fast(self) -> dict:
        """Run async scrapers from sync context."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Already in async context, use sync version
                return self.run_now()
            return loop.run_until_complete(self.run_now_async())
        except RuntimeError:
            # No event loop, create new one
            return asyncio.run(self.run_now_async())

    def start(self, cron_expr: str = "0 6 * * *"):
        """Start scheduled gathering.

        Args:
            cron_expr: Cron expression for schedule (default: daily 6am)
        """
        self._init_scrapers()

        parts = cron_expr.split()
        trigger = CronTrigger(
            minute=parts[0] if len(parts) > 0 else "0",
            hour=parts[1] if len(parts) > 1 else "6",
            day=parts[2] if len(parts) > 2 else "*",
            month=parts[3] if len(parts) > 3 else "*",
            day_of_week=parts[4] if len(parts) > 4 else "*",
        )

        self.scheduler.add_job(
            self.run_now,
            trigger=trigger,
            id="intel_gather",
            replace_existing=True,
        )

        self.scheduler.start()

    def stop(self):
        """Stop scheduler."""
        self.scheduler.shutdown()
