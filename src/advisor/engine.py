"""LLM orchestration for advice generation."""

import logging
import os
from typing import Optional

from anthropic import Anthropic, APIError, AuthenticationError

from .prompts import PromptTemplates
from .rag import RAGRetriever

logger = logging.getLogger(__name__)


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

    def _call_llm(self, system: str, user_prompt: str, max_tokens: int = 2000) -> str:
        """Make LLM API call."""
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
    ) -> str:
        """Get advice for a question.

        Args:
            question: User's question
            advice_type: general, career, goals, opportunities

        Returns:
            LLM-generated advice
        """
        journal_ctx, intel_ctx = self.rag.get_combined_context(question)

        prompt_template = PromptTemplates.get_prompt(advice_type)
        user_prompt = prompt_template.format(
            journal_context=journal_ctx,
            intel_context=intel_ctx,
            question=question,
        )

        return self._call_llm(PromptTemplates.SYSTEM_BASE, user_prompt)

    def weekly_review(self) -> str:
        """Generate weekly review from recent entries."""
        journal_ctx = self.rag.get_recent_entries(days=7)
        intel_ctx = self.rag.get_intel_context("weekly industry trends", max_chars=2000)

        prompt = PromptTemplates.WEEKLY_REVIEW.format(
            journal_context=journal_ctx,
            intel_context=intel_ctx,
        )

        return self._call_llm(PromptTemplates.SYSTEM_BASE, prompt, max_tokens=1500)

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

        return self._call_llm(PromptTemplates.SYSTEM_BASE, prompt)

    def analyze_goals(self, specific_goal: Optional[str] = None) -> str:
        """Analyze goal progress."""
        query = specific_goal or "goals objectives targets plans"
        journal_ctx = self.rag.get_journal_context(query, max_chars=6000)

        prompt = PromptTemplates.GOAL_ANALYSIS.format(
            journal_context=journal_ctx,
            question=specific_goal or "How am I progressing on my goals?",
        )

        return self._call_llm(PromptTemplates.SYSTEM_BASE, prompt)
