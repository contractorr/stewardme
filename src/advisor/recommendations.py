"""Recommendation engine with specialized recommenders."""

from abc import ABC, abstractmethod
from typing import Optional

import anthropic
import structlog

from .prompts import PromptTemplates
from .rag import RAGRetriever
from .recommendation_storage import Recommendation, RecommendationStorage
from .scoring import RecommendationScorer

logger = structlog.get_logger()


class BaseRecommender(ABC):
    """Base class for all recommenders."""

    category: str = "general"

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

    @abstractmethod
    def get_prompt(self) -> str:
        """Get the prompt template for this recommender."""
        pass

    @abstractmethod
    def get_context_query(self) -> str:
        """Get the query for retrieving context."""
        pass

    def generate(self, max_items: int = 3, with_action_plans: bool = True) -> list[Recommendation]:
        """Generate recommendations using LLM.

        Args:
            max_items: Max recommendations to generate
            with_action_plans: Generate action plans for high-score recs
        """
        journal_ctx = self.rag.get_journal_context(
            self.get_context_query(),
            max_entries=8,
            max_chars=5000,
        )
        intel_ctx = self.rag.get_intel_context(
            self.get_context_query(),
            max_chars=3000,
        )

        prompt = self.get_prompt().format(
            journal_context=journal_ctx,
            intel_context=intel_ctx,
            max_items=max_items,
        )

        response = self.llm_caller(PromptTemplates.SYSTEM, prompt)
        recs = self._parse_recommendations(response)

        # Generate action plans for top recs (score >= 7.0)
        if with_action_plans:
            for rec in recs:
                if rec.score >= 7.0:
                    try:
                        action_plan = self.generate_action_plan(rec)
                        rec.metadata = rec.metadata or {}
                        rec.metadata["action_plan"] = action_plan
                    except (anthropic.APIError, KeyError, ValueError) as e:
                        logger.warning("Failed to generate action plan", error=str(e))

        return recs

    def _parse_recommendations(self, response: str) -> list[Recommendation]:
        """Parse LLM response into Recommendation objects."""
        recs = []
        current = {}
        lines = response.split("\n")

        for line in lines:
            line = line.strip()
            if line.startswith("### ") or line.startswith("## "):
                if current.get("title"):
                    recs.append(self._build_recommendation(current))
                current = {"title": line.lstrip("#").strip()}
            elif line.startswith("**Why**:") or line.startswith("RATIONALE:"):
                current["rationale"] = line.split(":", 1)[-1].strip()
            elif line.startswith("**Description**:") or line.startswith("DESCRIPTION:"):
                current["description"] = line.split(":", 1)[-1].strip()
            elif line.startswith("RELEVANCE:"):
                current["relevance"] = self._parse_score(line)
            elif line.startswith("URGENCY:"):
                current["urgency"] = self._parse_score(line)
            elif line.startswith("FEASIBILITY:"):
                current["feasibility"] = self._parse_score(line)
            elif line.startswith("IMPACT:"):
                current["impact"] = self._parse_score(line)
            elif current.get("title") and not current.get("description") and line:
                current["description"] = current.get("description", "") + " " + line

        if current.get("title"):
            recs.append(self._build_recommendation(current))

        # Filter by threshold and dedupe
        valid_recs = []
        for rec in recs:
            if self.scorer.passes_threshold(rec.score):
                content_hash = self.scorer.content_hash(rec.title, rec.description)
                if not self.storage.hash_exists(content_hash):
                    rec.embedding_hash = content_hash
                    valid_recs.append(rec)

        return valid_recs

    def _parse_score(self, line: str) -> float:
        try:
            return float(line.split(":")[-1].strip())
        except ValueError:
            return 5.0

    def _build_recommendation(self, data: dict) -> Recommendation:
        score = self.scorer.score(
            relevance=data.get("relevance", 5.0),
            urgency=data.get("urgency", 5.0),
            feasibility=data.get("feasibility", 5.0),
            impact=data.get("impact", 5.0),
            category=self.category,
        )
        return Recommendation(
            category=self.category,
            title=data.get("title", ""),
            description=data.get("description", "").strip(),
            rationale=data.get("rationale", ""),
            score=score,
        )

    def generate_action_plan(self, rec: Recommendation) -> str:
        """Generate detailed action plan for a recommendation."""
        journal_ctx = self.rag.get_journal_context(
            f"{rec.title} {rec.category}",
            max_entries=5,
            max_chars=2000,
        )

        prompt = PromptTemplates.ACTION_PLAN.format(
            title=rec.title,
            category=rec.category,
            description=rec.description,
            rationale=rec.rationale,
            journal_context=journal_ctx,
        )

        return self.llm_caller(PromptTemplates.SYSTEM, prompt, max_tokens=1000)


class LearningRecommender(BaseRecommender):
    """Skills/courses based on career trajectory + trends."""

    category = "learning"

    def get_prompt(self) -> str:
        return PromptTemplates.LEARNING_RECOMMENDATIONS

    def get_context_query(self) -> str:
        return "skills learning goals career development courses"


class CareerRecommender(BaseRecommender):
    """Career moves/pivots analysis."""

    category = "career"

    def get_prompt(self) -> str:
        return PromptTemplates.CAREER_CHANGE_ANALYSIS

    def get_context_query(self) -> str:
        return "career job role position goals ambitions work"


class EntrepreneurialRecommender(BaseRecommender):
    """Startup ideas, side projects, consulting niches."""

    category = "entrepreneurial"

    def get_prompt(self) -> str:
        return PromptTemplates.ENTREPRENEURIAL_OPPORTUNITIES

    def get_context_query(self) -> str:
        return "problems frustrations ideas business startup project"


class InvestmentRecommender(BaseRecommender):
    """Market trends, emerging tech, funding patterns."""

    category = "investment"

    def get_prompt(self) -> str:
        return PromptTemplates.INVESTMENT_OPPORTUNITIES

    def get_context_query(self) -> str:
        return "technology trends funding investment market opportunity"


class RecommendationEngine:
    """Orchestrates all recommenders."""

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

        # Get feedback stats for scoring adjustment
        feedback_stats = storage.get_feedback_stats()

        scoring_config = self.config.get("scoring", {})
        self.scorer = RecommendationScorer(
            min_threshold=scoring_config.get("min_threshold", 6.0),
            similarity_threshold=scoring_config.get("similarity_threshold", 0.85),
            feedback_stats=feedback_stats,
        )

        categories = self.config.get("categories", {})
        self.recommenders = {}

        if categories.get("learning", True):
            self.recommenders["learning"] = LearningRecommender(
                rag, llm_caller, self.scorer, storage
            )
        if categories.get("career", True):
            self.recommenders["career"] = CareerRecommender(
                rag, llm_caller, self.scorer, storage
            )
        if categories.get("entrepreneurial", True):
            self.recommenders["entrepreneurial"] = EntrepreneurialRecommender(
                rag, llm_caller, self.scorer, storage
            )
        if categories.get("investment", True):
            self.recommenders["investment"] = InvestmentRecommender(
                rag, llm_caller, self.scorer, storage
            )

    def generate_category(
        self,
        category: str,
        max_items: int = 3,
        save: bool = True,
        with_action_plans: bool = True,
    ) -> list[Recommendation]:
        """Generate recommendations for a single category."""
        if category not in self.recommenders:
            logger.warning("Unknown category: %s", category)
            return []

        recs = self.recommenders[category].generate(
            max_items=max_items,
            with_action_plans=with_action_plans,
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
        """Generate recommendations for all categories."""
        results = {}
        for category in self.recommenders:
            results[category] = self.generate_category(
                category,
                max_items=max_per_category,
                save=save,
                with_action_plans=with_action_plans,
            )
        return results

    def get_top_recommendations(
        self,
        limit: int = 5,
        min_score: float = 6.0,
    ) -> list[Recommendation]:
        """Get top recommendations across all categories."""
        return self.storage.get_top_by_score(
            min_score=min_score,
            limit=limit,
            exclude_status=["completed", "dismissed"],
        )
