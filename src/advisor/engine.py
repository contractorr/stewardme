"""LLM orchestration for advice generation."""

from pathlib import Path
from typing import Optional

import structlog

from llm import LLMError as BaseLLMError
from llm import LLMRateLimitError, create_llm_provider

from .prompts import PromptTemplates
from .rag import RAGRetriever

logger = structlog.get_logger()

# Retry decorator for LLM calls
try:
    from cli.retry import llm_retry
    _llm_retry = llm_retry(
        max_attempts=3,
        min_wait=2.0,
        max_wait=30.0,
        exceptions=(LLMRateLimitError, BaseLLMError),
    )
except ImportError:
    def _llm_retry(func):
        return func


class AdvisorError(Exception):
    """Base exception for advisor errors."""
    pass


class APIKeyMissingError(AdvisorError):
    """Raised when API key is not configured."""
    pass


class LLMError(AdvisorError):
    """Raised when LLM call fails."""
    pass


class AdvisorEngine:
    """Main advisor engine using pluggable LLM providers."""

    def __init__(
        self,
        rag: RAGRetriever,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        provider: Optional[str] = None,
        client=None,  # Dependency injection for testing
        use_tools: bool = False,
        components: Optional[dict] = None,
    ):
        self.rag = rag
        self.model = model
        self.use_tools = use_tools

        try:
            self.llm = create_llm_provider(
                provider=provider,
                api_key=api_key,
                model=model,
                client=client,
            )
        except BaseLLMError as e:
            raise APIKeyMissingError(str(e)) from e

        self._orchestrator = None
        if use_tools and components:
            from .agentic import AgenticOrchestrator
            from .tools import ToolRegistry

            registry = ToolRegistry(components)
            self._orchestrator = AgenticOrchestrator(
                llm=self.llm,
                registry=registry,
                system_prompt=PromptTemplates.AGENTIC_SYSTEM,
            )

    @_llm_retry
    def _call_llm(self, system: str, user_prompt: str, max_tokens: int = 2000, conversation_history: list[dict] | None = None) -> str:
        """Make LLM API call with retry on transient errors."""
        try:
            logger.debug("Calling LLM provider=%s tokens=%d", self.llm.provider_name, max_tokens)
            messages = list(conversation_history or [])
            messages.append({"role": "user", "content": user_prompt})
            return self.llm.generate(
                messages=messages,
                system=system,
                max_tokens=max_tokens,
            )
        except BaseLLMError as e:
            if isinstance(e, LLMRateLimitError):
                from cli.rate_limit_notifier import get_notifier
                n = get_notifier()
                if n:
                    n.notify(self.llm.provider_name, str(e))
            logger.error("LLM call failed: %s", e)
            raise LLMError(str(e)) from e

    def ask(
        self,
        question: str,
        advice_type: str = "general",
        include_research: bool = True,
        conversation_history: list[dict] | None = None,
    ) -> str:
        """Get advice for a question.

        Args:
            question: User's question
            advice_type: general, career, goals, opportunities
            include_research: Include deep research context
            conversation_history: Prior conversation messages for context

        Returns:
            LLM-generated advice
        """
        # Agentic mode: LLM decides what to look up via tool calls
        if self._orchestrator:
            return self._orchestrator.run(question, conversation_history=conversation_history)

        # Classic RAG mode: single-shot retrieval + LLM call
        journal_ctx, intel_ctx = self.rag.get_combined_context(question)
        profile_ctx = self.rag.get_profile_context()

        # Get research context if available
        research_ctx = ""
        if include_research and hasattr(self.rag, 'get_research_context'):
            research_ctx = self.rag.get_research_context(question)

        has_research = bool(research_ctx.strip())
        prompt_template = PromptTemplates.get_prompt(advice_type, with_research=has_research)

        user_prompt = prompt_template.format(
            journal_context=profile_ctx + journal_ctx,
            intel_context=intel_ctx,
            research_context=research_ctx if has_research else "",
            question=question,
        )

        return self._call_llm(PromptTemplates.SYSTEM, user_prompt, conversation_history=conversation_history)

    def weekly_review(self, journal_storage=None) -> str:
        """Generate weekly review from recent entries.

        Args:
            journal_storage: Optional storage for stale goal detection
        """
        journal_ctx = self.rag.get_recent_entries(days=7)
        intel_ctx = self.rag.get_intel_context("weekly industry trends", max_chars=2000)

        # Add stale goals warning if storage provided
        stale_goals_ctx = ""
        if journal_storage:
            from .goals import GoalTracker
            tracker = GoalTracker(journal_storage)
            stale = tracker.get_stale_goals()
            if stale:
                stale_goals_ctx = "\n\nSTALE GOALS NEEDING ATTENTION:\n"
                for g in stale[:5]:
                    stale_goals_ctx += f"- {g['title']} (last check: {g.get('days_since_check', '?')} days ago)\n"

        profile_ctx = self.rag.get_profile_context()
        prompt = PromptTemplates.WEEKLY_REVIEW.format(
            journal_context=profile_ctx + journal_ctx + stale_goals_ctx,
            intel_context=intel_ctx,
        )

        return self._call_llm(PromptTemplates.SYSTEM, prompt, max_tokens=1500)

    def detect_opportunities(self) -> str:
        """Identify opportunities based on profile and trends."""
        # Use broad query to get diverse journal context
        journal_ctx = self.rag.get_journal_context(
            "skills interests goals projects work",
            max_entries=8,
            max_chars=5000,
        )
        intel_ctx = self.rag.get_intel_context(
            "opportunities trends hiring funding",
            max_chars=3000,
        )

        profile_ctx = self.rag.get_profile_context()
        prompt = PromptTemplates.OPPORTUNITY_DETECTION.format(
            journal_context=profile_ctx + journal_ctx,
            intel_context=intel_ctx,
        )

        return self._call_llm(PromptTemplates.SYSTEM, prompt)

    def analyze_goals(self, specific_goal: Optional[str] = None) -> str:
        """Analyze goal progress."""
        query = specific_goal or "goals objectives targets plans"
        journal_ctx = self.rag.get_journal_context(query, max_chars=6000)

        prompt = PromptTemplates.GOAL_ANALYSIS.format(
            journal_context=journal_ctx,
            question=specific_goal or "How am I progressing on my goals?",
        )

        return self._call_llm(PromptTemplates.SYSTEM, prompt)

    # === Skill & Learning Methods ===

    def analyze_skill_gaps(self) -> str:
        """Analyze skill gaps between current state and aspirations."""
        from .skills import SkillGapAnalyzer
        analyzer = SkillGapAnalyzer(self.rag, self._call_llm)
        return analyzer.analyze()

    def generate_learning_path(
        self,
        skill: str,
        lp_dir: str | Path = "~/coach/learning_paths",
        current_level: int = 1,
        target_level: int = 4,
    ) -> Path:
        """Generate a structured learning path for a skill."""
        from .learning_paths import LearningPathGenerator, LearningPathStorage
        storage = LearningPathStorage(lp_dir)
        generator = LearningPathGenerator(self.rag, self._call_llm, storage)
        return generator.generate(skill, current_level=current_level, target_level=target_level)

    # === Recommendation Methods ===

    def _get_rec_storage(self, rec_path: Path):
        """Lazy init recommendation storage."""
        from .recommendation_storage import RecommendationStorage
        return RecommendationStorage(rec_path)

    def _get_rec_engine(self, db_path: Path, config: Optional[dict] = None):
        """Lazy init recommendation engine."""
        from .recommendations import RecommendationEngine
        storage = self._get_rec_storage(db_path)
        return RecommendationEngine(
            rag=self.rag,
            llm_caller=self._call_llm,
            storage=storage,
            config=config,
        )

    def generate_recommendations(
        self,
        category: str,
        db_path: Path,
        config: Optional[dict] = None,
        max_items: int = 3,
    ) -> list:
        """Generate recommendations for a category.

        Args:
            category: learning, career, entrepreneurial, investment, or all
            db_path: Path to recommendations database
            config: Recommendation config
            max_items: Max items per category

        Returns:
            List of Recommendation objects
        """
        engine = self._get_rec_engine(db_path, config)

        if category == "all":
            results = engine.generate_all(max_per_category=max_items)
            # Flatten to single list
            all_recs = []
            for recs in results.values():
                all_recs.extend(recs)
            return sorted(all_recs, key=lambda r: r.score, reverse=True)
        else:
            return engine.generate_category(category, max_items=max_items)

    def generate_action_brief(
        self,
        db_path: Path,
        journal_storage=None,
        max_items: int = 5,
        min_score: float = 6.0,
        save: bool = False,
    ) -> str:
        """Generate weekly action brief.

        Args:
            db_path: Path to recommendations database
            journal_storage: Optional storage to save brief
            max_items: Max recommendations to include
            min_score: Minimum score threshold
            save: Save as journal entry

        Returns:
            Action brief markdown
        """
        from .action_brief import ActionBriefGenerator
        storage = self._get_rec_storage(db_path)
        generator = ActionBriefGenerator(
            rag=self.rag,
            llm_caller=self._call_llm,
            rec_storage=storage,
            journal_storage=journal_storage,
        )

        if save and journal_storage:
            filepath = generator.generate_and_save(
                max_items=max_items,
                min_score=min_score,
            )
            logger.info("Saved action brief to %s", filepath)

        return generator.generate(max_items=max_items, min_score=min_score)
