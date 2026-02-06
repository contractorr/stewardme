"""Job scheduling for intelligence gathering."""

import asyncio
import structlog
from pathlib import Path
from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from .scraper import IntelStorage
from .sources import (
    RSSFeedScraper,
    HackerNewsScraper,
    GitHubTrendingScraper,
    ArxivScraper,
    RedditScraper,
    DevToScraper,
    CrunchbaseScraper,
    NewsAPIScraper,
)

logger = structlog.get_logger().bind(source="scheduler")


class IntelScheduler:
    """Manages scheduled intelligence gathering jobs."""

    def __init__(
        self,
        storage: IntelStorage,
        config: Optional[dict] = None,
        journal_storage=None,
        embeddings=None,
        full_config: Optional[dict] = None,
    ):
        self.storage = storage
        self.config = config or {}
        self.journal_storage = journal_storage
        self.embeddings = embeddings
        self.full_config = full_config or {}
        self.scheduler = BackgroundScheduler()
        self._scrapers: list = []
        self._research_agent = None

    def _init_scrapers(self):
        """Initialize async scrapers from config."""
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
            self._scrapers.append(GitHubTrendingScraper(
                self.storage,
                languages=gh_config.get("languages", ["python"]),
                timeframe=gh_config.get("timeframe", "daily"),
            ))

        # arXiv
        arxiv_config = self.config.get("arxiv", {})
        if "arxiv" in enabled or arxiv_config.get("enabled", False):
            self._scrapers.append(ArxivScraper(
                self.storage,
                categories=arxiv_config.get("categories"),
                max_results=arxiv_config.get("max_results", 30),
            ))

        # Reddit
        reddit_config = self.config.get("reddit", {})
        if "reddit" in enabled or reddit_config.get("enabled", False):
            self._scrapers.append(RedditScraper(
                self.storage,
                subreddits=reddit_config.get("subreddits"),
                limit=reddit_config.get("limit", 25),
                timeframe=reddit_config.get("timeframe", "day"),
            ))

        # Dev.to
        devto_config = self.config.get("devto", {})
        if "devto" in enabled or devto_config.get("enabled", False):
            self._scrapers.append(DevToScraper(
                self.storage,
                per_page=devto_config.get("per_page", 30),
                top_period=devto_config.get("top_period", "week"),
            ))

        # Crunchbase (paid)
        cb_config = self.config.get("crunchbase", {})
        if "crunchbase" in enabled or cb_config.get("enabled", False):
            api_key = cb_config.get("api_key")
            if api_key and not api_key.startswith("$"):
                self._scrapers.append(CrunchbaseScraper(
                    self.storage,
                    api_key=api_key,
                    limit=cb_config.get("limit", 30),
                ))

        # NewsAPI (paid)
        news_config = self.config.get("newsapi", {})
        if "newsapi" in enabled or news_config.get("enabled", False):
            api_key = news_config.get("api_key")
            if api_key and not api_key.startswith("$"):
                self._scrapers.append(NewsAPIScraper(
                    self.storage,
                    api_key=api_key,
                    queries=news_config.get("queries"),
                    page_size=news_config.get("page_size", 20),
                    days_back=news_config.get("days_back", 7),
                ))

    async def _run_async(self) -> dict:
        """Run all scrapers concurrently.

        Returns:
            Dict with scraper results {source: new_items_count}
        """
        self._init_scrapers()
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
        tasks = [run_scraper(s) for s in self._scrapers]
        completed = await asyncio.gather(*tasks, return_exceptions=True)

        for result in completed:
            if isinstance(result, tuple):
                name, data = result
                results[name] = data
            elif isinstance(result, Exception):
                results["unknown"] = {"error": str(result)}

        return results

    def run_now(self) -> dict:
        """Run async scrapers from sync context.

        Returns:
            Dict with scraper results {source: new_items_count}
        """
        return asyncio.run(self._run_async())

    def start(self, cron_expr: str = "0 6 * * *"):
        """Start scheduled gathering.

        Args:
            cron_expr: Cron expression for schedule (default: daily 6am)
        """
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

    def _init_research_agent(self):
        """Initialize research agent if configured."""
        research_config = self.full_config.get("research", {})
        if not research_config.get("enabled", False):
            return None

        if not self.journal_storage or not self.embeddings:
            logger.warning("Research agent requires journal_storage and embeddings")
            return None

        try:
            from research.agent import DeepResearchAgent
            return DeepResearchAgent(
                journal_storage=self.journal_storage,
                intel_storage=self.storage,
                embeddings=self.embeddings,
                config=self.full_config,
            )
        except ImportError as e:
            logger.error("Failed to import research agent: %s", e)
            return None

    def run_research_now(self, topic: Optional[str] = None) -> list[dict]:
        """Run deep research immediately.

        Args:
            topic: Optional specific topic to research

        Returns:
            List of research results
        """
        agent = self._init_research_agent()
        if not agent:
            logger.warning("Research agent not available")
            return []

        try:
            return agent.run(specific_topic=topic)
        finally:
            agent.close()

    def get_research_topics(self) -> list[dict]:
        """Get suggested research topics."""
        agent = self._init_research_agent()
        if not agent:
            return []

        try:
            return agent.get_suggested_topics()
        finally:
            agent.close()

    def start_with_research(
        self,
        scrape_cron: str = "0 6 * * *",
        research_cron: str = "0 21 * * 0",
    ):
        """Start scheduler with both scraping and research jobs.

        Args:
            scrape_cron: Cron for intelligence gathering (default: daily 6am)
            research_cron: Cron for deep research (default: Sunday 9pm)
        """
        # Add scraping job
        parts = scrape_cron.split()
        scrape_trigger = CronTrigger(
            minute=parts[0] if len(parts) > 0 else "0",
            hour=parts[1] if len(parts) > 1 else "6",
            day=parts[2] if len(parts) > 2 else "*",
            month=parts[3] if len(parts) > 3 else "*",
            day_of_week=parts[4] if len(parts) > 4 else "*",
        )
        self.scheduler.add_job(
            self.run_now,
            trigger=scrape_trigger,
            id="intel_gather",
            replace_existing=True,
        )

        # Add research job if enabled
        research_config = self.full_config.get("research", {})
        if research_config.get("enabled", False):
            parts = research_cron.split()
            research_trigger = CronTrigger(
                minute=parts[0] if len(parts) > 0 else "0",
                hour=parts[1] if len(parts) > 1 else "21",
                day=parts[2] if len(parts) > 2 else "*",
                month=parts[3] if len(parts) > 3 else "*",
                day_of_week=parts[4] if len(parts) > 4 else "0",
            )
            self.scheduler.add_job(
                self.run_research_now,
                trigger=research_trigger,
                id="deep_research",
                replace_existing=True,
            )
            logger.info("Research job scheduled: %s", research_cron)

        # Add recommendations job if enabled
        rec_config = self.full_config.get("recommendations", {})
        if rec_config.get("enabled", False):
            rec_cron = rec_config.get("delivery", {}).get("schedule", "0 8 * * 0")
            self._add_recommendations_job(rec_cron)

        self.scheduler.start()

    def _add_recommendations_job(self, cron_expr: str):
        """Add weekly recommendations/action brief job."""
        parts = cron_expr.split()
        trigger = CronTrigger(
            minute=parts[0] if len(parts) > 0 else "0",
            hour=parts[1] if len(parts) > 1 else "8",
            day=parts[2] if len(parts) > 2 else "*",
            month=parts[3] if len(parts) > 3 else "*",
            day_of_week=parts[4] if len(parts) > 4 else "0",
        )
        self.scheduler.add_job(
            self.run_recommendations_now,
            trigger=trigger,
            id="weekly_recommendations",
            replace_existing=True,
        )
        logger.info("Recommendations job scheduled: %s", cron_expr)

    def run_recommendations_now(self) -> dict:
        """Run recommendation generation and save action brief.

        Returns:
            Dict with generation results
        """
        rec_config = self.full_config.get("recommendations", {})
        if not rec_config.get("enabled", False):
            logger.warning("Recommendations not enabled")
            return {"error": "not_enabled"}

        if not self.journal_storage:
            logger.warning("Journal storage required for recommendations")
            return {"error": "no_journal_storage"}

        try:
            from advisor.engine import AdvisorEngine
            from advisor.rag import RAGRetriever

            # Build RAG retriever
            from journal import JournalSearch, EmbeddingManager
            paths_config = self.full_config.get("paths", {})
            chroma_dir = Path(paths_config.get("chroma_dir", "~/coach/chroma")).expanduser()
            embeddings = EmbeddingManager(chroma_dir)
            search = JournalSearch(self.journal_storage, embeddings)
            rag = RAGRetriever(search, self.storage.db_path)

            advisor = AdvisorEngine(rag)

            # Get DB path
            rec_db = self.storage.db_path.parent / "recommendations.db"

            # Generate all recommendations
            max_per_cat = rec_config.get("scoring", {}).get("max_per_category", 3)
            recs = advisor.generate_recommendations(
                "all", rec_db, rec_config, max_items=max_per_cat
            )

            # Generate and save action brief
            delivery = rec_config.get("delivery", {})
            if "journal" in delivery.get("methods", ["journal"]):
                advisor.generate_action_brief(
                    rec_db,
                    journal_storage=self.journal_storage,
                    save=True,
                )
                logger.info("Action brief saved to journal")

            return {"recommendations": len(recs), "brief_saved": True}

        except Exception as e:
            logger.error("Failed to generate recommendations: %s", e)
            return {"error": str(e)}
