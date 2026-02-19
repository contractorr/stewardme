"""Skill gap analyzer — identifies gaps between current skills and aspirations."""

import structlog

from .prompts import PromptTemplates
from .rag import RAGRetriever

logger = structlog.get_logger()


class SkillGapAnalyzer:
    """Analyze skill gaps between current state and aspirational roles."""

    def __init__(self, rag: RAGRetriever, llm_caller):
        self.rag = rag
        self.llm_caller = llm_caller

    def analyze(self) -> str:
        """Run skill gap analysis using profile + journal context.

        Returns:
            Formatted skill gap analysis markdown
        """
        profile_ctx = self.rag.get_profile_context()
        journal_ctx = self.rag.get_journal_context(
            "skills goals career aspirations learning",
            max_entries=8,
            max_chars=4000,
        )

        prompt = PromptTemplates.SKILL_GAP_ANALYSIS.format(
            profile_context=profile_ctx,
            journal_context=journal_ctx,
        )

        return self.llm_caller(PromptTemplates.SYSTEM, prompt, max_tokens=2000)
