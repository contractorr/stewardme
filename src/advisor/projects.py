"""Project opportunity engine — open-source matching + side-project ideas."""

import structlog

from .prompts import PromptTemplates
from .rag import RAGRetriever

logger = structlog.get_logger()


def get_matching_issues(
    intel_storage,
    profile=None,
    limit: int = 20,
    days: int = 14,
) -> list[dict]:
    """Get GitHub issues matching user's profile skills.

    Args:
        intel_storage: IntelStorage instance
        profile: Optional UserProfile for skill matching
        limit: Max results
        days: Lookback window
    """
    items = intel_storage.get_recent(days=days, limit=100)
    issues = [i for i in items if i.get("source") == "github_issues"]

    if profile:
        # Score by skill match
        profile_langs = set(t.lower() for t in profile.languages_frameworks)
        profile_skills = set(s.name.lower() for s in profile.skills)
        all_keywords = profile_langs | profile_skills

        scored = []
        for issue in issues:
            tags = set(
                t.strip().lower()
                for t in (issue.get("tags", "").split(",") if isinstance(issue.get("tags"), str) else issue.get("tags", []))
            )
            summary_lower = issue.get("summary", "").lower()
            score = sum(1 for kw in all_keywords if kw in tags or kw in summary_lower)
            issue["_match_score"] = score
            scored.append(issue)

        scored.sort(key=lambda i: i["_match_score"], reverse=True)
        return scored[:limit]

    return issues[:limit]


class ProjectIdeaGenerator:
    """Generate side-project ideas from journal pain points."""

    def __init__(self, rag: RAGRetriever, llm_caller):
        self.rag = rag
        self.llm_caller = llm_caller

    def generate_ideas(self) -> str:
        """Generate side-project ideas from journal context."""
        profile_ctx = self.rag.get_profile_context()
        journal_ctx = self.rag.get_journal_context(
            "frustration problem idea project build wish annoying",
            max_entries=10,
            max_chars=5000,
        )

        prompt = PromptTemplates.SIDE_PROJECT_IDEAS.format(
            profile_context=profile_ctx,
            journal_context=journal_ctx,
        )

        return self.llm_caller(PromptTemplates.SYSTEM, prompt, max_tokens=2000)
