"""Weekly action brief generator."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from .prompts import PromptTemplates
from .recommendation_storage import Recommendation, RecommendationStorage
from .rag import RAGRetriever

logger = logging.getLogger(__name__)


class ActionBriefGenerator:
    """Generate weekly action briefs from recommendations."""

    def __init__(
        self,
        rag: RAGRetriever,
        llm_caller,
        rec_storage: RecommendationStorage,
        journal_storage=None,
    ):
        self.rag = rag
        self.llm_caller = llm_caller
        self.rec_storage = rec_storage
        self.journal_storage = journal_storage

    def generate(
        self,
        max_items: int = 5,
        min_score: float = 6.0,
    ) -> str:
        """Generate weekly action brief.

        Args:
            max_items: Max recommendations to include
            min_score: Minimum score threshold

        Returns:
            Formatted action brief markdown
        """
        # Get top recommendations
        recs = self.rec_storage.get_top_by_score(
            min_score=min_score,
            limit=max_items,
            exclude_status=["completed", "dismissed"],
        )

        if not recs:
            return self._generate_empty_brief()

        # Format recommendations for prompt
        rec_text = self._format_recommendations(recs)

        # Get context
        journal_ctx = self.rag.get_recent_entries(days=7)
        intel_ctx = self.rag.get_intel_context(
            "trends opportunities news",
            max_chars=2000,
        )

        prompt = PromptTemplates.WEEKLY_ACTION_BRIEF.format(
            journal_context=journal_ctx,
            intel_context=intel_ctx,
            recommendations=rec_text,
            date=datetime.now().strftime("%b %d, %Y"),
        )

        return self.llm_caller(PromptTemplates.SYSTEM, prompt)

    def generate_and_save(
        self,
        max_items: int = 5,
        min_score: float = 6.0,
    ) -> Optional[Path]:
        """Generate brief and save as journal entry.

        Returns:
            Path to saved entry or None
        """
        if not self.journal_storage:
            logger.warning("Journal storage not configured, cannot save brief")
            return None

        brief = self.generate(max_items=max_items, min_score=min_score)

        filepath = self.journal_storage.create(
            content=brief,
            entry_type="action_brief",
            title=f"Action Brief - {datetime.now().strftime('%Y-%m-%d')}",
            tags=["action_brief", "weekly", "recommendations"],
        )

        return filepath

    def _format_recommendations(self, recs: list[Recommendation]) -> str:
        """Format recommendations for prompt context."""
        lines = []
        for i, rec in enumerate(recs, 1):
            lines.append(f"{i}. [{rec.category.upper()}] {rec.title}")
            lines.append(f"   Score: {rec.score:.1f}")
            lines.append(f"   {rec.description[:200]}")
            if rec.rationale:
                lines.append(f"   Rationale: {rec.rationale[:150]}")
            lines.append("")
        return "\n".join(lines)

    def _generate_empty_brief(self) -> str:
        """Generate brief when no recommendations exist."""
        date = datetime.now().strftime("%b %d, %Y")
        return f"""# Weekly Action Brief - {date}

## No Priority Actions This Week

No recommendations meet the threshold. Consider:
- Adding more journal entries about your goals and challenges
- Running `coach recommend all` to generate new recommendations
- Lowering the score threshold in config

## Reflection Prompts
- What's the most important thing you could work on this week?
- What opportunity have you been putting off?
- What skill would unlock the most value for you right now?
"""
