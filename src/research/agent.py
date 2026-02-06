"""Deep research agent orchestrating the full research flow."""

import structlog
from datetime import datetime
from pathlib import Path
from typing import Optional

from journal import JournalStorage, EmbeddingManager
from intelligence.scraper import IntelStorage, IntelItem

from .topics import TopicSelector
from .web_search import WebSearchClient, AsyncWebSearchClient
from .synthesis import ResearchSynthesizer

logger = structlog.get_logger()


class DeepResearchAgent:
    """Orchestrates topic selection, web search, and report generation."""

    def __init__(
        self,
        journal_storage: JournalStorage,
        intel_storage: IntelStorage,
        embeddings: EmbeddingManager,
        config: Optional[dict] = None,
    ):
        self.journal = journal_storage
        self.intel = intel_storage
        self.embeddings = embeddings
        self.config = config or {}

        # Initialize components
        research_config = self.config.get("research", {})

        self.topic_selector = TopicSelector(
            storage=journal_storage,
            max_topics=research_config.get("max_topics_per_week", 2),
            skip_researched_days=research_config.get("skip_if_researched_days", 60),
        )

        self.search_client = WebSearchClient(
            api_key=research_config.get("api_key"),
            provider=research_config.get("api_provider", "tavily"),
            max_results=research_config.get("sources_per_topic", 8),
        )

        self.synthesizer = ResearchSynthesizer(
            model=self.config.get("llm", {}).get("model", "claude-sonnet-4-20250514"),
        )

    def run(self, specific_topic: Optional[str] = None) -> list[dict]:
        """Run deep research on selected or specific topic(s).

        Args:
            specific_topic: Override automatic topic selection

        Returns:
            List of {topic, filepath, success} for each researched topic
        """
        results = []

        if specific_topic:
            topics = [{"topic": specific_topic, "source": "manual", "score": 10, "reason": "User specified"}]
        else:
            # Get topics to research, excluding recently researched
            recent = self.topic_selector.get_recent_research_topics()
            topics = self.topic_selector.get_topics(researched_topics=recent)

        if not topics:
            logger.info("No topics to research")
            return results

        # Get user context for personalization
        user_context = self._get_user_context()

        for topic_info in topics:
            topic = topic_info["topic"]
            logger.info("Researching topic: %s (source: %s)", topic, topic_info["source"])

            try:
                # 1. Web search
                search_results = self.search_client.search(topic)
                if not search_results:
                    logger.warning("No search results for topic: %s", topic)
                    results.append({"topic": topic, "filepath": None, "success": False})
                    continue

                # 2. Synthesize report
                report = self.synthesizer.synthesize(
                    topic=topic,
                    results=search_results,
                    user_context=user_context,
                )

                # 3. Store as journal entry
                filepath = self._store_journal_entry(topic, report, topic_info)

                # 4. Store in intel for hybrid search
                self._store_intel_item(topic, report, search_results)

                # 5. Add to embeddings
                self._add_embeddings(filepath, report)

                results.append({"topic": topic, "filepath": filepath, "success": True})
                logger.info("Research complete for: %s -> %s", topic, filepath)

            except (IOError, ValueError, KeyError) as e:
                logger.error("Research failed for %s: %s", topic, e)
                results.append({"topic": topic, "filepath": None, "success": False, "error": str(e)})

        return results

    def get_suggested_topics(self) -> list[dict]:
        """Get list of suggested research topics without running research."""
        recent = self.topic_selector.get_recent_research_topics()
        return self.topic_selector.get_topics(researched_topics=recent)

    def _get_user_context(self) -> str:
        """Get user context from goals and recent entries."""
        context_parts = []

        # Get goals
        goals = self.journal.list_entries(entry_type="goal", limit=5)
        if goals:
            context_parts.append("GOALS:")
            for g in goals:
                context_parts.append(f"- {g['title']}")

        # Get recent themes from journal
        recent = self.journal.list_entries(limit=10)
        if recent:
            context_parts.append("\nRECENT INTERESTS:")
            tags = set()
            for e in recent:
                tags.update(e.get("tags", []))
            if tags:
                context_parts.append(f"Tags: {', '.join(list(tags)[:10])}")

        return "\n".join(context_parts) if context_parts else ""

    def _store_journal_entry(self, topic: str, report: str, topic_info: dict) -> Path:
        """Store research report as journal entry."""
        return self.journal.create(
            content=report,
            entry_type="research",
            title=f"Research: {topic}",
            tags=["research", "auto", topic_info["source"]],
            metadata={
                "topic": topic,
                "research_source": topic_info["source"],
                "research_reason": topic_info["reason"],
            },
        )

    def _store_intel_item(self, topic: str, report: str, search_results: list) -> None:
        """Store research in intel DB for hybrid search."""
        # Create summary from first part of report
        summary = report[:500] if len(report) > 500 else report

        # Use unique URL based on topic and date
        unique_url = f"research://{topic.lower().replace(' ', '-')}/{datetime.now().strftime('%Y%m%d')}"

        item = IntelItem(
            source="deep_research",
            title=f"Research: {topic}",
            url=unique_url,
            summary=summary,
            content=report,
            published=datetime.now(),
            tags=["research", "auto"],
        )
        self.intel.save(item)

    def _add_embeddings(self, filepath: Path, content: str) -> None:
        """Add research entry to embeddings."""
        self.embeddings.add_entry(
            str(filepath),
            content,
            {"type": "research"},
        )

    def close(self):
        """Clean up resources."""
        self.search_client.close()


class AsyncDeepResearchAgent:
    """Async version of deep research agent."""

    def __init__(
        self,
        journal_storage: JournalStorage,
        intel_storage: IntelStorage,
        embeddings: EmbeddingManager,
        config: Optional[dict] = None,
    ):
        self.journal = journal_storage
        self.intel = intel_storage
        self.embeddings = embeddings
        self.config = config or {}

        research_config = self.config.get("research", {})

        self.topic_selector = TopicSelector(
            storage=journal_storage,
            max_topics=research_config.get("max_topics_per_week", 2),
            skip_researched_days=research_config.get("skip_if_researched_days", 60),
        )

        self.search_client = AsyncWebSearchClient(
            api_key=research_config.get("api_key"),
            provider=research_config.get("api_provider", "tavily"),
            max_results=research_config.get("sources_per_topic", 8),
        )

        self.synthesizer = ResearchSynthesizer(
            model=self.config.get("llm", {}).get("model", "claude-sonnet-4-20250514"),
        )

    async def run(self, specific_topic: Optional[str] = None) -> list[dict]:
        """Async version of research run."""
        results = []

        if specific_topic:
            topics = [{"topic": specific_topic, "source": "manual", "score": 10, "reason": "User specified"}]
        else:
            recent = self.topic_selector.get_recent_research_topics()
            topics = self.topic_selector.get_topics(researched_topics=recent)

        if not topics:
            return results

        user_context = self._get_user_context()

        for topic_info in topics:
            topic = topic_info["topic"]
            try:
                search_results = await self.search_client.search(topic)
                if not search_results:
                    results.append({"topic": topic, "filepath": None, "success": False})
                    continue

                # Synthesis is sync (LLM call)
                report = self.synthesizer.synthesize(
                    topic=topic,
                    results=search_results,
                    user_context=user_context,
                )

                filepath = self._store_journal_entry(topic, report, topic_info)
                self._store_intel_item(topic, report, search_results)
                self._add_embeddings(filepath, report)

                results.append({"topic": topic, "filepath": filepath, "success": True})

            except (IOError, ValueError, KeyError) as e:
                logger.error("Async research failed for %s: %s", topic, e)
                results.append({"topic": topic, "filepath": None, "success": False})

        return results

    def _get_user_context(self) -> str:
        """Get user context (same as sync version)."""
        context_parts = []
        goals = self.journal.list_entries(entry_type="goal", limit=5)
        if goals:
            context_parts.append("GOALS:")
            for g in goals:
                context_parts.append(f"- {g['title']}")
        return "\n".join(context_parts) if context_parts else ""

    def _store_journal_entry(self, topic: str, report: str, topic_info: dict) -> Path:
        """Store research as journal entry."""
        return self.journal.create(
            content=report,
            entry_type="research",
            title=f"Research: {topic}",
            tags=["research", "auto", topic_info["source"]],
            metadata={
                "topic": topic,
                "research_source": topic_info["source"],
            },
        )

    def _store_intel_item(self, topic: str, report: str, search_results: list) -> None:
        """Store in intel DB."""
        summary = report[:500] if len(report) > 500 else report
        unique_url = f"research://{topic.lower().replace(' ', '-')}/{datetime.now().strftime('%Y%m%d')}"

        item = IntelItem(
            source="deep_research",
            title=f"Research: {topic}",
            url=unique_url,
            summary=summary,
            content=report,
            published=datetime.now(),
            tags=["research", "auto"],
        )
        self.intel.save(item)

    def _add_embeddings(self, filepath: Path, content: str) -> None:
        """Add to embeddings."""
        self.embeddings.add_entry(str(filepath), content, {"type": "research"})

    async def close(self):
        """Clean up async resources."""
        await self.search_client.close()
