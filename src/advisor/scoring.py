"""Scoring utilities for recommendations."""

import hashlib


class RecommendationScorer:
    """Score and deduplicate recommendations."""

    def __init__(self, min_threshold: float = 6.0, **_kwargs):
        self.min_threshold = min_threshold

    def passes_threshold(self, score: float) -> bool:
        """Check if score meets minimum threshold."""
        return score >= self.min_threshold

    def content_hash(self, title: str, description: str) -> str:
        """Generate hash for deduplication."""
        content = f"{title.lower().strip()}|{description.lower().strip()}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
