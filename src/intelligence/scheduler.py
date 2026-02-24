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
    AICapabilitiesScraper,
    ArxivScraper,
    EventScraper,
    GitHubIssuesScraper,
    GitHubTrendingScraper,
    GooglePatentsScraper,
    HackerNewsScraper,
    ProductHuntScraper,
    RedditScraper,
    RSSFeedScraper,
    YCJobsScraper,
)

logger = structlog.get_logger().bind(source="scheduler")


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

        self._research = ResearchRunner(storage, journal_storage, embeddings, self.full_config)
        self._recommendations = RecommendationRunner(storage, journal_storage, self.full_config)

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
            self._scrapers.append(
                GitHubTrendingScraper(
                    self.storage,
                    languages=gh_config.get("languages", ["python"]),
                    timeframe=gh_config.get("timeframe", "daily"),
                )
            )

        # arXiv
        arxiv_config = self.config.get("arxiv", {})
        if "arxiv" in enabled or arxiv_config.get("enabled", False):
            self._scrapers.append(
                ArxivScraper(
                    self.storage,
                    categories=arxiv_config.get("categories"),
                    max_results=arxiv_config.get("max_results", 30),
                )
            )

        # Reddit
        reddit_config = self.config.get("reddit", {})
        if "reddit" in enabled or reddit_config.get("enabled", False):
            self._scrapers.append(
                RedditScraper(
                    self.storage,
                    subreddits=reddit_config.get("subreddits"),
                    limit=reddit_config.get("limit", 25),
                    timeframe=reddit_config.get("timeframe", "day"),
                )
            )

        # Events (confs.tech + RSS)
        events_config = self.full_config.get("events", {})
        if events_config.get("enabled", False):
            # Load profile for location filter
            location = ""
            if events_config.get("location_filter", False):
                try:
                    from profile.storage import ProfileStorage

                    profile_path = self.full_config.get("profile", {}).get(
                        "path", "~/coach/profile.yaml"
                    )
                    ps = ProfileStorage(profile_path)
                    p = ps.load()
                    if p:
                        location = p.location
                except Exception:
                    pass
            self._scrapers.append(
                EventScraper(
                    self.storage,
                    topics=events_config.get("topics"),
                    location_filter=location,
                    rss_feeds=events_config.get("rss_feeds", []),
                )
            )

        # Product Hunt
        ph_config = self.config.get("producthunt", {})
        if "producthunt" in enabled or ph_config.get("enabled", False):
            self._scrapers.append(
                ProductHuntScraper(
                    self.storage,
                    max_items=ph_config.get("max_items", 20),
                )
            )

        # YC Jobs
        yc_config = self.config.get("yc_jobs", {})
        if "yc_jobs" in enabled or yc_config.get("enabled", False):
            self._scrapers.append(
                YCJobsScraper(
                    self.storage,
                    max_items=yc_config.get("max_items", 30),
                )
            )

        # Google Patents
        patents_config = self.config.get("google_patents", {})
        if "google_patents" in enabled or patents_config.get("enabled", False):
            self._scrapers.append(
                GooglePatentsScraper(
                    self.storage,
                    feeds=patents_config.get("feeds"),
                    max_per_feed=patents_config.get("max_per_feed", 15),
                )
            )

        # AI Capabilities (METR, Chatbot Arena, HELM)
        ai_cap_config = self.config.get("ai_capabilities", {})
        if "ai_capabilities" in enabled or ai_cap_config.get("enabled", False):
            self._scrapers.append(
                AICapabilitiesScraper(
                    self.storage,
                    sources=ai_cap_config.get("sources", ["metr", "chatbot_arena", "helm"]),
                    max_items_per_source=ai_cap_config.get("max_items_per_source", 10),
                )
            )

        # GitHub Issues (good-first-issue / help-wanted)
        gh_issues_config = self.full_config.get("projects", {}).get("github_issues", {})
        if gh_issues_config.get("enabled", False):
            langs = gh_issues_config.get("languages")
            if not langs:
                try:
                    from profile.storage import ProfileStorage

                    profile_path = self.full_config.get("profile", {}).get(
                        "path", "~/coach/profile.yaml"
                    )
                    ps = ProfileStorage(profile_path)
                    p = ps.load()
                    if p:
                        langs = p.languages_frameworks[:5]
                except Exception:
                    pass
            self._scrapers.append(
                GitHubIssuesScraper(
                    self.storage,
                    languages=langs or ["python"],
                    labels=gh_issues_config.get("labels", ["good-first-issue", "help-wanted"]),
                    token=gh_issues_config.get("token"),
                )
            )

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
                    logger.warning(
                        "scraper_failed",
                        source=scraper.source_name,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
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
                    logger.warning(
                        "scraper_gather_exception",
                        error=str(result),
                        error_type=type(result).__name__,
                    )
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

    # --- Signal detection + autonomous actions ---

    def run_signal_detection(self) -> list:
        """Run signal detection across all data sources."""
        if not self.journal_storage:
            logger.warning("Signal detection requires journal_storage")
            return []
        try:
            from advisor.signals import SignalDetector

            db_path = self.storage.db_path
            detector = SignalDetector(self.journal_storage, db_path, self.full_config)
            signals = detector.detect_all()
            logger.info("signal_detection_complete", count=len(signals))
            return signals
        except Exception as e:
            logger.error("signal_detection_failed", error=str(e))
            return []

    def run_autonomous_actions(self) -> list:
        """Run autonomous actions based on current signals."""
        if not self.journal_storage:
            logger.warning("Autonomous actions require journal_storage")
            return []
        try:
            from advisor.autonomous import AutonomousActionEngine
            from advisor.signals import SignalStore

            db_path = self.storage.db_path
            store = SignalStore(db_path)
            active_signals = store.get_active(limit=20)

            # Reconstruct Signal objects from stored data
            from advisor.signals import Signal, SignalType

            signals = []
            for s in active_signals:
                try:
                    signals.append(
                        Signal(
                            type=SignalType(s["type"]),
                            severity=s["severity"],
                            title=s["title"],
                            detail=s.get("detail", ""),
                            suggested_actions=s.get("suggested_actions", []),
                            evidence=s.get("evidence", []),
                        )
                    )
                except (ValueError, KeyError):
                    continue

            engine = AutonomousActionEngine(
                self.journal_storage, db_path, self.full_config, self.embeddings
            )
            results = engine.process_signals(signals)
            logger.info("autonomous_actions_complete", count=len(results))
            return results
        except Exception as e:
            logger.error("autonomous_actions_failed", error=str(e))
            return []

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
                defaults={
                    "minute": "0",
                    "hour": "21",
                    "day": "*",
                    "month": "*",
                    "day_of_week": "0",
                },
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

        # Add signal detection + autonomous actions if agent enabled
        agent_config = self.full_config.get("agent", {})
        if agent_config.get("enabled", False):
            signal_cron = agent_config.get("signals", {}).get("schedule", "0 9 * * *")
            signal_trigger = _parse_cron(signal_cron)
            self.scheduler.add_job(
                self.run_signal_detection,
                trigger=signal_trigger,
                id="signal_detection",
                replace_existing=True,
            )
            logger.info("Signal detection job scheduled: %s", signal_cron)

            # Autonomous actions run 1 hour after signal detection
            auto_trigger = _parse_cron(
                "0 10 * * *",
                defaults={
                    "minute": "0",
                    "hour": "10",
                    "day": "*",
                    "month": "*",
                    "day_of_week": "*",
                },
            )
            self.scheduler.add_job(
                self.run_autonomous_actions,
                trigger=auto_trigger,
                id="autonomous_actions",
                replace_existing=True,
            )
            logger.info("Autonomous actions job scheduled")

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
