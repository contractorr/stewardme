"""Job scheduling for intelligence gathering."""

import asyncio
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

import structlog
import structlog.contextvars
from apscheduler.events import EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from observability import metrics

from .scraper import IntelStorage
from .sources import (
    ArxivScraper,
    EventScraper,
    GitHubIssuesScraper,
    GitHubTrendingScraper,
    HackerNewsScraper,
    RedditScraper,
    RSSFeedScraper,
)

logger = structlog.get_logger().bind(source="scheduler")


def _is_rate_limit_error(e: Exception) -> bool:
    """Check if exception is a rate limit / HTTP 429 error."""
    msg = str(e).lower()
    if "429" in msg or "rate limit" in msg or "too many requests" in msg:
        return True
    # Check for aiohttp/httpx response status attribute
    status = getattr(e, "status", None) or getattr(e, "status_code", None)
    return status == 429


def _parse_cron(expr: str, defaults: Optional[dict] = None) -> CronTrigger:
    """Parse cron expression string into CronTrigger.

    Args:
        expr: 5-field cron expression (min hour day month dow)
        defaults: Optional dict of default values for missing fields
    """
    d = defaults or {"minute": "0", "hour": "6", "day": "*", "month": "*", "day_of_week": "*"}
    parts = expr.split()
    return CronTrigger(
        minute=parts[0] if len(parts) > 0 else d.get("minute", "0"),
        hour=parts[1] if len(parts) > 1 else d.get("hour", "6"),
        day=parts[2] if len(parts) > 2 else d.get("day", "*"),
        month=parts[3] if len(parts) > 3 else d.get("month", "*"),
        day_of_week=parts[4] if len(parts) > 4 else d.get("day_of_week", "*"),
    )


class ResearchRunner:
    """Handles deep research agent initialization and execution."""

    def __init__(self, storage: IntelStorage, journal_storage, embeddings, config: dict):
        self.storage = storage
        self.journal_storage = journal_storage
        self.embeddings = embeddings
        self.config = config

    def _init_agent(self):
        """Initialize research agent if configured."""
        research_config = self.config.get("research", {})
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
                config=self.config,
            )
        except ImportError as e:
            logger.error("Failed to import research agent: %s", e)
            return None

    def run(self, topic: Optional[str] = None) -> list[dict]:
        """Run deep research immediately."""
        agent = self._init_agent()
        if not agent:
            logger.warning("Research agent not available")
            return []

        try:
            return agent.run(specific_topic=topic)
        finally:
            agent.close()

    def get_topics(self) -> list[dict]:
        """Get suggested research topics."""
        agent = self._init_agent()
        if not agent:
            return []

        try:
            return agent.get_suggested_topics()
        finally:
            agent.close()


class RecommendationRunner:
    """Handles recommendation generation and action brief saving."""

    def __init__(self, storage: IntelStorage, journal_storage, config: dict):
        self.storage = storage
        self.journal_storage = journal_storage
        self.config = config

    def run(self) -> dict:
        """Generate recommendations and save action brief."""
        rec_config = self.config.get("recommendations", {})
        if not rec_config.get("enabled", False):
            logger.warning("Recommendations not enabled")
            return {"error": "not_enabled"}

        if not self.journal_storage:
            logger.warning("Journal storage required for recommendations")
            return {"error": "no_journal_storage"}

        try:
            from advisor.engine import AdvisorEngine
            from advisor.rag import RAGRetriever
            from journal import EmbeddingManager, JournalSearch

            paths_config = self.config.get("paths", {})
            chroma_dir = Path(paths_config.get("chroma_dir", "~/coach/chroma")).expanduser()
            embeddings = EmbeddingManager(chroma_dir)
            search = JournalSearch(self.journal_storage, embeddings)
            rag = RAGRetriever(search, self.storage.db_path)

            advisor = AdvisorEngine(rag)

            rec_db = self.storage.db_path.parent / "recommendations"

            max_per_cat = rec_config.get("scoring", {}).get("max_per_category", 3)
            recs = advisor.generate_recommendations(
                "all", rec_db, rec_config, max_items=max_per_cat
            )

            delivery = rec_config.get("delivery", {})
            brief_text = None
            if "journal" in delivery.get("methods", ["journal"]):
                brief_text = advisor.generate_action_brief(
                    rec_db,
                    journal_storage=self.journal_storage,
                    save=True,
                )
                logger.info("Action brief saved to journal")

            # Send email digest if configured
            if brief_text and "email" in delivery.get("methods", []):
                try:
                    from cli.email_digest import send_digest
                    send_digest(
                        subject="AI Coach - Weekly Action Brief",
                        body_markdown=brief_text,
                        config=self.config,
                    )
                except Exception as e:
                    logger.warning("Email digest failed", error=str(e))

            return {"recommendations": len(recs), "brief_saved": True}

        except Exception as e:
            logger.error("Failed to generate recommendations: %s", e)
            return {"error": str(e)}


class IntelScheduler:
    """Manages scheduled intelligence gathering jobs. Delegates research/recs to runners."""

    def __init__(
        self,
        storage: IntelStorage,
        config: Optional[dict] = None,
        journal_storage=None,
        embeddings=None,
        full_config: Optional[dict] = None,
        on_error: Optional[Callable] = None,
    ):
        self.storage = storage
        self.config = config or {}
        self.journal_storage = journal_storage
        self.embeddings = embeddings
        self.full_config = full_config or {}
        self.on_error = on_error
        self.scheduler = BackgroundScheduler()
        self._scrapers: list = []

        # Init rate limit notifier if full config available
        if self.full_config.get("email", {}).get("enabled", False):
            try:
                from cli.config_models import CoachConfig
                from cli.rate_limit_notifier import get_notifier, init_notifier
                if get_notifier() is None:
                    cm = CoachConfig.from_dict(dict(self.full_config))
                    init_notifier(cm)
            except Exception:
                pass

        self._research = ResearchRunner(
            storage, journal_storage, embeddings, self.full_config
        )
        self._recommendations = RecommendationRunner(
            storage, journal_storage, self.full_config
        )

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

        # Events (confs.tech + RSS)
        events_config = self.full_config.get("events", {})
        if events_config.get("enabled", False):
            # Load profile for location filter
            location = ""
            if events_config.get("location_filter", False):
                try:
                    from profile.storage import ProfileStorage
                    profile_path = self.full_config.get("profile", {}).get("path", "~/coach/profile.yaml")
                    ps = ProfileStorage(profile_path)
                    p = ps.load()
                    if p:
                        location = p.location
                except Exception:
                    pass
            self._scrapers.append(EventScraper(
                self.storage,
                topics=events_config.get("topics"),
                location_filter=location,
                rss_feeds=events_config.get("rss_feeds", []),
            ))

        # GitHub Issues (good-first-issue / help-wanted)
        gh_issues_config = self.full_config.get("projects", {}).get("github_issues", {})
        if gh_issues_config.get("enabled", False):
            langs = gh_issues_config.get("languages")
            if not langs:
                try:
                    from profile.storage import ProfileStorage
                    profile_path = self.full_config.get("profile", {}).get("path", "~/coach/profile.yaml")
                    ps = ProfileStorage(profile_path)
                    p = ps.load()
                    if p:
                        langs = p.languages_frameworks[:5]
                except Exception:
                    pass
            self._scrapers.append(GitHubIssuesScraper(
                self.storage,
                languages=langs or ["python"],
                labels=gh_issues_config.get("labels", ["good-first-issue", "help-wanted"]),
                token=gh_issues_config.get("token"),
            ))


    async def _run_async(self) -> dict:
        """Run all scrapers concurrently."""
        # Generate correlation ID and bind to structlog
        run_id = uuid.uuid4().hex[:8]
        structlog.contextvars.bind_contextvars(run_id=run_id)

        try:
            self._init_scrapers()
            results = {}

            async def run_scraper(scraper):
                try:
                    with metrics.timer("scrape_duration"):
                        items = await asyncio.wait_for(scraper.scrape(), timeout=60.0)
                        new_count = await scraper.save_items(items)

                    metrics.counter("scraper_success")
                    metrics.counter("scraper_items_new", new_count)

                    return scraper.source_name, {
                        "scraped": len(items),
                        "new": new_count,
                    }
                except asyncio.TimeoutError:
                    metrics.counter("scraper_failure")
                    return scraper.source_name, {"error": "timeout"}
                except Exception as e:
                    if _is_rate_limit_error(e):
                        from cli.rate_limit_notifier import get_notifier
                        n = get_notifier()
                        if n:
                            n.notify(scraper.source_name, str(e))
                    logger.warning("scraper_failed", source=scraper.source_name, error=str(e), error_type=type(e).__name__)
                    metrics.counter("scraper_failure")
                    return scraper.source_name, {"error": str(e)}
                finally:
                    await scraper.close()

            tasks = [run_scraper(s) for s in self._scrapers]
            completed = await asyncio.gather(*tasks, return_exceptions=True)

            for result in completed:
                if isinstance(result, tuple):
                    name, data = result
                    results[name] = data
                elif isinstance(result, Exception):
                    logger.warning("scraper_gather_exception", error=str(result), error_type=type(result).__name__)
                    metrics.counter("scraper_failure")
                    results["unknown"] = {"error": str(result)}

            return results
        finally:
            structlog.contextvars.unbind_contextvars("run_id")

    def run_now(self) -> dict:
        """Run async scrapers from sync context."""
        return asyncio.run(self._run_async())

    def _default_error_handler(self, event):
        """Default error handler for APScheduler job failures."""
        logger.error(
            "job_error",
            job_id=event.job_id,
            exception=str(event.exception),
            traceback=event.traceback,
        )

        # Write status file
        status_path = Path("~/.coach/last_run_status.json").expanduser()
        status_path.parent.mkdir(parents=True, exist_ok=True)
        status_data = {
            "status": "error",
            "job_id": event.job_id,
            "error": str(event.exception),
            "timestamp": datetime.now().isoformat(),
        }
        status_path.write_text(json.dumps(status_data, indent=2))

        # Call custom handler if provided
        if self.on_error:
            try:
                self.on_error(event)
            except Exception as e:
                logger.error("Error in custom on_error callback: %s", e)

    def start(self, cron_expr: str = "0 6 * * *"):
        """Start scheduled gathering."""
        trigger = _parse_cron(cron_expr)
        self.scheduler.add_job(
            self.run_now,
            trigger=trigger,
            id="intel_gather",
            replace_existing=True,
        )
        self.scheduler.add_listener(self._default_error_handler, EVENT_JOB_ERROR)
        self.scheduler.start()

    def stop(self):
        """Stop scheduler."""
        self.scheduler.shutdown()

    # Delegate research methods
    def run_research_now(self, topic: Optional[str] = None) -> list[dict]:
        """Run deep research immediately."""
        return self._research.run(topic=topic)

    def get_research_topics(self) -> list[dict]:
        """Get suggested research topics."""
        return self._research.get_topics()

    # Delegate recommendation methods
    def run_recommendations_now(self) -> dict:
        """Run recommendation generation and save action brief."""
        return self._recommendations.run()

    def start_with_research(
        self,
        scrape_cron: str = "0 6 * * *",
        research_cron: str = "0 21 * * 0",
    ):
        """Start scheduler with both scraping and research jobs."""
        # Add scraping job
        scrape_trigger = _parse_cron(scrape_cron)
        self.scheduler.add_job(
            self.run_now,
            trigger=scrape_trigger,
            id="intel_gather",
            replace_existing=True,
        )

        # Add research job if enabled
        research_config = self.full_config.get("research", {})
        if research_config.get("enabled", False):
            research_trigger = _parse_cron(
                research_cron,
                defaults={"minute": "0", "hour": "21", "day": "*", "month": "*", "day_of_week": "0"},
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

        self.scheduler.add_listener(self._default_error_handler, EVENT_JOB_ERROR)
        self.scheduler.start()

    def _add_recommendations_job(self, cron_expr: str):
        """Add weekly recommendations/action brief job."""
        trigger = _parse_cron(
            cron_expr,
            defaults={"minute": "0", "hour": "8", "day": "*", "month": "*", "day_of_week": "0"},
        )
        self.scheduler.add_job(
            self.run_recommendations_now,
            trigger=trigger,
            id="weekly_recommendations",
            replace_existing=True,
        )
        logger.info("Recommendations job scheduled: %s", cron_expr)
