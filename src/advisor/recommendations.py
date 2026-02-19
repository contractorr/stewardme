"""Unified recommendation engine."""

from typing import Optional

import structlog

from llm import LLMError

from .prompts import PromptTemplates
from .rag import RAGRetriever
from .recommendation_storage import Recommendation, RecommendationStorage
from .scoring import RecommendationScorer

logger = structlog.get_logger()

# Context queries per category
CATEGORY_QUERIES = {
    "learning": "skills learning goals career development courses",
    "career": "career job role position goals ambitions work",
    "entrepreneurial": "problems frustrations ideas business startup project",
    "investment": "technology trends funding investment market opportunity",
    "events": "conference meetup workshop event speaking cfp",
    "projects": "open source contribution project coding side-project",
}


class Recommender:
    """Single unified recommender that works across all categories."""

    def __init__(
        self,
        rag: RAGRetriever,
        llm_caller,
        scorer: RecommendationScorer,
        storage: RecommendationStorage,
    ):
        self.rag = rag
        self.llm_caller = llm_caller
        self.scorer = scorer
        self.storage = storage

    def generate(
        self,
        category: str,
        max_items: int = 3,
        with_action_plans: bool = True,
    ) -> list[Recommendation]:
        """Generate recommendations for a category."""
        # Check for sparse data
        try:
            all_entries = self.rag.search.storage.list_entries(limit=5)
            if len(all_entries) < 5:
                logger.info("Sparse journal data (%d entries), skipping recommendations", len(all_entries))
                return []
        except Exception:
            pass

        context_query = CATEGORY_QUERIES.get(category, category)

        journal_ctx = self.rag.get_journal_context(
            context_query, max_entries=8, max_chars=5000,
        )
        intel_ctx = self.rag.get_intel_context(context_query, max_chars=3000)

        prompt = PromptTemplates.UNIFIED_RECOMMENDATIONS.format(
            category=category,
            journal_context=journal_ctx,
            intel_context=intel_ctx,
            max_items=max_items,
        )

        response = self.llm_caller(PromptTemplates.SYSTEM, prompt)
        recs = self._parse_recommendations(response, category)

        if with_action_plans:
            for rec in recs:
                if rec.score >= 7.0:
                    try:
                        action_plan = self._generate_action_plan(rec)
                        rec.metadata = rec.metadata or {}
                        rec.metadata["action_plan"] = action_plan
                    except (LLMError, KeyError, ValueError) as e:
                        logger.warning("Failed to generate action plan", error=str(e))

        return recs

    def _parse_recommendations(self, response: str, category: str) -> list[Recommendation]:
        """Parse LLM response into Recommendation objects."""
        recs = []
        current: dict = {}

        for line in response.split("\n"):
            line = line.strip()
            if line.startswith("### ") or line.startswith("## "):
                if current.get("title"):
                    recs.append(self._build_recommendation(current, category))
                current = {"title": line.lstrip("#").strip()}
            elif line.startswith("**Why**:") or line.startswith("RATIONALE:"):
                current["rationale"] = line.split(":", 1)[-1].strip()
            elif line.startswith("**Description**:") or line.startswith("DESCRIPTION:"):
                current["description"] = line.split(":", 1)[-1].strip()
            elif line.startswith("SCORE:"):
                try:
                    current["score"] = min(10.0, max(0.0, float(line.split(":")[-1].strip())))
                except ValueError:
                    current["score"] = 5.0
            elif current.get("title") and not current.get("description") and line:
                current["description"] = current.get("description", "") + " " + line

        if current.get("title"):
            recs.append(self._build_recommendation(current, category))

        # Filter by threshold and dedupe
        valid = []
        for rec in recs:
            if self.scorer.passes_threshold(rec.score):
                content_hash = self.scorer.content_hash(rec.title, rec.description)
                if not self.storage.hash_exists(content_hash):
                    rec.embedding_hash = content_hash
                    valid.append(rec)

        return valid

    def _build_recommendation(self, data: dict, category: str) -> Recommendation:
        return Recommendation(
            category=category,
            title=data.get("title", ""),
            description=data.get("description", "").strip(),
            rationale=data.get("rationale", ""),
            score=data.get("score", 5.0),
        )

    def _generate_action_plan(self, rec: Recommendation) -> str:
        journal_ctx = self.rag.get_journal_context(
            f"{rec.title} {rec.category}", max_entries=5, max_chars=2000,
        )
        prompt = PromptTemplates.ACTION_PLAN.format(
            title=rec.title,
            category=rec.category,
            description=rec.description,
            rationale=rec.rationale,
            journal_context=journal_ctx,
        )
        return self.llm_caller(PromptTemplates.SYSTEM, prompt, max_tokens=1000)


class RecommendationEngine:
    """Orchestrates recommendation generation."""

    def __init__(
        self,
        rag: RAGRetriever,
        llm_caller,
        storage: RecommendationStorage,
        config: Optional[dict] = None,
    ):
        self.rag = rag
        self.llm_caller = llm_caller
        self.storage = storage
        self.config = config or {}

        scoring_config = self.config.get("scoring", {})
        self.scorer = RecommendationScorer(
            min_threshold=scoring_config.get("min_threshold", 6.0),
        )

        self.recommender = Recommender(rag, llm_caller, self.scorer, storage)

        # Determine enabled categories
        categories = self.config.get("categories", {})
        self.enabled_categories = [
            cat for cat in CATEGORY_QUERIES
            if categories.get(cat, True)
        ]

    def generate_category(
        self,
        category: str,
        max_items: int = 3,
        save: bool = True,
        with_action_plans: bool = True,
    ) -> list[Recommendation]:
        """Generate recommendations for a single category."""
        if category not in CATEGORY_QUERIES:
            logger.warning("Unknown category: %s", category)
            return []

        recs = self.recommender.generate(
            category, max_items=max_items, with_action_plans=with_action_plans,
        )

        if save:
            for rec in recs:
                rec.id = self.storage.save(rec)

        return recs

    def generate_all(
        self,
        max_per_category: int = 3,
        save: bool = True,
        with_action_plans: bool = True,
    ) -> dict[str, list[Recommendation]]:
        """Generate recommendations for all enabled categories."""
        results = {}
        for category in self.enabled_categories:
            results[category] = self.generate_category(
                category, max_items=max_per_category,
                save=save, with_action_plans=with_action_plans,
            )
        return results

    def get_top_recommendations(
        self, limit: int = 5, min_score: float = 6.0,
    ) -> list[Recommendation]:
        """Get top recommendations across all categories."""
        return self.storage.get_top_by_score(
            min_score=min_score, limit=limit,
            exclude_status=["completed", "dismissed"],
        )
