"""Research report synthesis using LLM."""

import os
from typing import Optional

import structlog
from anthropic import Anthropic, APIError

from cli.retry import llm_retry

from .web_search import SearchResult

logger = structlog.get_logger()


class ResearchSynthesizer:
    """Synthesizes research reports from web search results."""

    SYSTEM_PROMPT = """You are a research assistant that synthesizes information from multiple sources into actionable research reports.

Your reports should be:
- Concise but comprehensive
- Focused on practical insights
- Well-structured with clear sections
- Honest about limitations or conflicting information"""

    SYNTHESIS_PROMPT = """Synthesize a research report on "{topic}" based on these sources:

{sources}

USER CONTEXT (their goals/interests):
{user_context}

Generate a research report with these sections:
## Summary
(2-3 sentence overview)

## Key Insights
(Bullet points of the most important findings)

## Relevance to Your Goals
(How this connects to the user's stated interests/goals)

## Sources
(List sources with brief descriptions)

## Next Steps
(2-3 actionable recommendations)

Be specific and practical. Cite sources when making claims."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-20250514",
        client: Optional[Anthropic] = None,
    ):
        resolved_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = client or Anthropic(api_key=resolved_key)
        self.model = model

    @llm_retry(exceptions=(APIError,))
    def synthesize(
        self,
        topic: str,
        results: list[SearchResult],
        user_context: str = "",
        max_tokens: int = 2000,
    ) -> str:
        """Generate research report from search results.

        Args:
            topic: Research topic
            results: Web search results
            user_context: User's goals/interests for personalization
            max_tokens: Max tokens for response

        Returns:
            Markdown-formatted research report
        """
        if not results:
            return self._empty_report(topic)

        # Format sources for prompt
        sources_text = self._format_sources(results)

        prompt = self.SYNTHESIS_PROMPT.format(
            topic=topic,
            sources=sources_text,
            user_context=user_context or "No specific context provided.",
        )

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=self.SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        except APIError as e:
            logger.error("LLM synthesis failed: %s", e)
            return self._fallback_report(topic, results)

    def _format_sources(self, results: list[SearchResult]) -> str:
        """Format search results for the prompt."""
        parts = []
        for i, r in enumerate(results, 1):
            parts.append(f"[Source {i}] {r.title}\nURL: {r.url}\nContent: {r.content}\n")
        return "\n".join(parts)

    def _empty_report(self, topic: str) -> str:
        """Generate report when no sources found."""
        return f"""## Summary
No sources found for "{topic}". This may be due to search API limitations or an overly specific query.

## Key Insights
- Unable to gather information at this time

## Next Steps
- Try a more general search term
- Check if TAVILY_API_KEY is configured correctly
- Research this topic manually"""

    def _fallback_report(self, topic: str, results: list[SearchResult]) -> str:
        """Generate basic report when LLM fails."""
        sources = "\n".join(f"- [{r.title}]({r.url})" for r in results[:5])
        return f"""## Summary
Research gathered on "{topic}" but synthesis unavailable due to API error.

## Sources Found
{sources}

## Next Steps
- Review sources manually
- Retry research later"""
