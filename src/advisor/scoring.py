"""Multi-factor scoring for recommendations."""

import hashlib
from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class ScoringWeights:
    """Configurable weights for scoring factors."""
    relevance: float = 0.4
    urgency: float = 0.2
    feasibility: float = 0.2
    impact: float = 0.2


class RecommendationScorer:
    """Score and deduplicate recommendations."""

    def __init__(
        self,
        weights: Optional[ScoringWeights] = None,
        min_threshold: float = 6.0,
        similarity_threshold: float = 0.85,
        feedback_stats: Optional[dict] = None,
    ):
        self.weights = weights or ScoringWeights()
        self.min_threshold = min_threshold
        self.similarity_threshold = similarity_threshold
        self.feedback_stats = feedback_stats or {}

    def score(
        self,
        relevance: float,
        urgency: float,
        feasibility: float,
        impact: float,
        category: Optional[str] = None,
    ) -> float:
        """Calculate weighted score (0-10 scale).

        Args:
            relevance: How relevant to user's goals/interests (0-10)
            urgency: Time-sensitivity (0-10)
            feasibility: How achievable given user's context (0-10)
            impact: Potential value/outcome (0-10)
            category: Optional category for feedback adjustment

        Returns:
            Weighted score adjusted by historical feedback
        """
        base_score = (
            self.weights.relevance * relevance +
            self.weights.urgency * urgency +
            self.weights.feasibility * feasibility +
            self.weights.impact * impact
        )

        # Apply feedback adjustment: final = base * (1 + 0.1 * (avg_rating - 3))
        avg_rating = 3.0
        if category and self.feedback_stats.get("by_category", {}).get(category):
            avg_rating = self.feedback_stats["by_category"][category]["avg_rating"]
        elif self.feedback_stats.get("avg_rating"):
            avg_rating = self.feedback_stats["avg_rating"]

        feedback_multiplier = 1 + 0.1 * (avg_rating - 3)
        return base_score * feedback_multiplier

    def passes_threshold(self, score: float) -> bool:
        """Check if score meets minimum threshold."""
        return score >= self.min_threshold

    def content_hash(self, title: str, description: str) -> str:
        """Generate hash for deduplication."""
        content = f"{title.lower().strip()}|{description.lower().strip()}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def cosine_similarity(self, vec1: list[float], vec2: list[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if not vec1 or not vec2:
            return 0.0
        a = np.array(vec1)
        b = np.array(vec2)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))

    def is_duplicate(
        self,
        embedding: list[float],
        existing_embeddings: list[list[float]],
    ) -> bool:
        """Check if recommendation is similar to existing ones."""
        for existing in existing_embeddings:
            if self.cosine_similarity(embedding, existing) >= self.similarity_threshold:
                return True
        return False


def parse_llm_scores(response: str) -> dict[str, float]:
    """Parse LLM response for scoring factors.

    Expected format in response:
    RELEVANCE: 8.5
    URGENCY: 6.0
    FEASIBILITY: 7.5
    IMPACT: 9.0
    """
    scores = {}
    for line in response.split("\n"):
        line = line.strip().upper()
        for factor in ["RELEVANCE", "URGENCY", "FEASIBILITY", "IMPACT"]:
            if line.startswith(f"{factor}:"):
                try:
                    val = float(line.split(":")[-1].strip())
                    scores[factor.lower()] = min(10.0, max(0.0, val))
                except ValueError:
                    pass
    return scores
