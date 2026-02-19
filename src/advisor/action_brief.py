"""Weekly action brief generator — includes events, learning, and projects."""

from datetime import datetime
from pathlib import Path
from typing import Optional

import structlog

from .prompts import PromptTemplates
from .rag import RAGRetriever
from .recommendation_storage import Recommendation, RecommendationStorage

logger = structlog.get_logger()


class ActionBriefGenerator:
    """Generate weekly action briefs from recommendations + events + learning + projects."""

    def __init__(
        self,
        rag: RAGRetriever,
        llm_caller,
        rec_storage: RecommendationStorage,
        journal_storage=None,
        config: Optional[dict] = None,
    ):
        self.rag = rag
        self.llm_caller = llm_caller
        self.rec_storage = rec_storage
        self.journal_storage = journal_storage
        self.config = config or {}

    def generate(
        self,
        max_items: int = 5,
        min_score: float = 6.0,
    ) -> str:
        """Generate weekly action brief with events, learning, and projects.

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
        profile_ctx = self.rag.get_profile_context()
        intel_ctx = self.rag.get_intel_context("trends opportunities news", max_chars=2000)

        # Gather extra sections
        events_section = self._get_events_section()
        learning_section = self._get_learning_section()
        projects_section = self._get_projects_section()

        extra_context = ""
        if events_section:
            extra_context += f"\n\nTIME-SENSITIVE EVENTS:\n{events_section}"
        if learning_section:
            extra_context += f"\n\nACTIVE LEARNING PATHS:\n{learning_section}"
        if projects_section:
            extra_context += f"\n\nNEW PROJECT OPPORTUNITIES:\n{projects_section}"

        prompt = PromptTemplates.WEEKLY_ACTION_BRIEF.format(
            journal_context=profile_ctx + journal_ctx,
            intel_context=intel_ctx + extra_context,
            recommendations=rec_text,
            date=datetime.now().strftime("%b %d, %Y"),
        )

        return self.llm_caller(PromptTemplates.SYSTEM, prompt)

    def generate_and_save(
        self,
        max_items: int = 5,
        min_score: float = 6.0,
    ) -> Optional[Path]:
        """Generate brief and save as journal entry."""
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
        lines = []
        for i, rec in enumerate(recs, 1):
            lines.append(f"{i}. [{rec.category.upper()}] {rec.title}")
            lines.append(f"   Score: {rec.score:.1f}")
            lines.append(f"   {rec.description[:200]}")
            if rec.rationale:
                lines.append(f"   Rationale: {rec.rationale[:150]}")
            lines.append("")
        return "\n".join(lines)

    def _get_events_section(self) -> str:
        """Get upcoming events for the brief."""
        try:
            from advisor.events import get_upcoming_events
            from intelligence.scraper import IntelStorage

            intel_db = Path(self.config.get("paths", {}).get("intel_db", "~/coach/intel.db")).expanduser()
            if not intel_db.exists():
                return ""

            storage = IntelStorage(intel_db)

            profile = None
            try:
                from profile.storage import ProfileStorage
                profile_path = self.config.get("profile", {}).get("path", "~/coach/profile.yaml")
                ps = ProfileStorage(profile_path)
                profile = ps.load()
            except Exception:
                pass

            events = get_upcoming_events(storage, profile=profile, days=30, limit=5, min_score=5.0)
            if not events:
                return ""

            lines = []
            for e in events:
                meta = e.get("_metadata", {})
                date = meta.get("event_date", "?")[:10]
                cfp = f" (CFP: {meta['cfp_deadline'][:10]})" if meta.get("cfp_deadline") else ""
                lines.append(f"- {e['title']} — {date}{cfp}")
            return "\n".join(lines)
        except Exception as exc:
            logger.debug("events_section_skipped", error=str(exc))
            return ""

    def _get_learning_section(self) -> str:
        """Get active learning path status for the brief."""
        try:
            from advisor.learning_paths import LearningPathStorage
            lp_dir = self.config.get("learning_paths", {}).get("dir", "~/coach/learning_paths")
            storage = LearningPathStorage(lp_dir)
            active = storage.list_paths(status="active")
            if not active:
                return ""

            lines = []
            for p in active[:3]:
                lines.append(f"- {p['skill']}: {p['completed_modules']}/{p['total_modules']} modules ({p['progress']}%)")
            return "\n".join(lines)
        except Exception as exc:
            logger.debug("learning_section_skipped", error=str(exc))
            return ""

    def _get_projects_section(self) -> str:
        """Get new project opportunities for the brief."""
        try:
            from intelligence.scraper import IntelStorage
            intel_db = Path(self.config.get("paths", {}).get("intel_db", "~/coach/intel.db")).expanduser()
            if not intel_db.exists():
                return ""

            storage = IntelStorage(intel_db)
            items = storage.get_recent(days=7, limit=50)
            issues = [i for i in items if i.get("source") == "github_issues"][:5]
            if not issues:
                return ""

            lines = []
            for i in issues:
                lines.append(f"- {i['title'][:60]} ({i.get('url', '')})")
            return "\n".join(lines)
        except Exception as exc:
            logger.debug("projects_section_skipped", error=str(exc))
            return ""

    def _generate_empty_brief(self) -> str:
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
