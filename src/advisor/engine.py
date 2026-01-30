"""LLM orchestration for advice generation."""

import logging
import os
from pathlib import Path
from typing import Optional

from anthropic import Anthropic, APIError, AuthenticationError, RateLimitError

from .prompts import PromptTemplates
from .rag import RAGRetriever

logger = logging.getLogger(__name__)

# Retry decorator for LLM calls
try:
    from cli.retry import llm_retry
    _llm_retry = llm_retry(
        max_attempts=3,
        min_wait=2.0,
        max_wait=30.0,
        exceptions=(RateLimitError, APIError),
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
    """Main advisor engine using Claude API."""

    def __init__(
        self,
        rag: RAGRetriever,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-20250514",
        client: Optional[Anthropic] = None,  # Dependency injection for testing
    ):
        self.rag = rag
        self.model = model

        # Validate API key
        resolved_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not resolved_key and client is None:
            raise APIKeyMissingError(
                "ANTHROPIC_API_KEY not set. Run: export ANTHROPIC_API_KEY=your-key"
            )

        self.client = client or Anthropic(api_key=resolved_key)

    @_llm_retry
    def _call_llm(self, system: str, user_prompt: str, max_tokens: int = 2000) -> str:
        """Make LLM API call with retry on transient errors."""
        try:
            logger.debug("Calling LLM model=%s tokens=%d", self.model, max_tokens)
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system,
                messages=[{"role": "user", "content": user_prompt}],
            )
            return response.content[0].text
        except AuthenticationError as e:
            logger.error("API authentication failed: %s", e)
            raise LLMError("Invalid API key. Check ANTHROPIC_API_KEY.") from e
        except APIError as e:
            logger.error("API call failed: %s", e)
            raise LLMError(f"LLM API error: {e}") from e

    def ask(
        self,
        question: str,
        advice_type: str = "general",
        include_research: bool = True,
    ) -> str:
        """Get advice for a question.

        Args:
            question: User's question
            advice_type: general, career, goals, opportunities
            include_research: Include deep research context

        Returns:
            LLM-generated advice
        """
        journal_ctx, intel_ctx = self.rag.get_combined_context(question)

        # Get research context if available
        research_ctx = ""
        if include_research and hasattr(self.rag, 'get_research_context'):
            research_ctx = self.rag.get_research_context(question)

        has_research = bool(research_ctx.strip())
        prompt_template = PromptTemplates.get_prompt(advice_type, with_research=has_research)

        user_prompt = prompt_template.format(
            journal_context=journal_ctx,
            intel_context=intel_ctx,
            research_context=research_ctx if has_research else "",
            question=question,
        )

        return self._call_llm(PromptTemplates.SYSTEM, user_prompt)

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

        prompt = PromptTemplates.WEEKLY_REVIEW.format(
            journal_context=journal_ctx + stale_goals_ctx,
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

        prompt = PromptTemplates.OPPORTUNITY_DETECTION.format(
            journal_context=journal_ctx,
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

    # === Recommendation Methods ===

    def _get_rec_storage(self, db_path: Path):
        """Lazy init recommendation storage."""
        from .recommendation_storage import RecommendationStorage
        return RecommendationStorage(db_path)

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
