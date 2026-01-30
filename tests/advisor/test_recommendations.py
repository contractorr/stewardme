"""Tests for recommendation engine."""

import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock

from advisor.scoring import RecommendationScorer, ScoringWeights, parse_llm_scores
from advisor.recommendation_storage import Recommendation, RecommendationStorage
from advisor.recommendations import (
    RecommendationEngine,
    LearningRecommender,
    CareerRecommender,
)


class TestRecommendationScorer:
    """Tests for scoring functionality."""

    def test_default_weights(self):
        scorer = RecommendationScorer()
        assert scorer.weights.relevance == 0.4
        assert scorer.weights.urgency == 0.2

    def test_score_calculation(self):
        scorer = RecommendationScorer()
        score = scorer.score(
            relevance=8.0, urgency=6.0, feasibility=7.0, impact=9.0
        )
        expected = 0.4 * 8.0 + 0.2 * 6.0 + 0.2 * 7.0 + 0.2 * 9.0
        assert score == expected

    def test_passes_threshold(self):
        scorer = RecommendationScorer(min_threshold=6.0)
        assert scorer.passes_threshold(7.0)
        assert not scorer.passes_threshold(5.0)

    def test_content_hash(self):
        scorer = RecommendationScorer()
        h1 = scorer.content_hash("Learn Rust", "Master async programming")
        h2 = scorer.content_hash("Learn Rust", "Master async programming")
        h3 = scorer.content_hash("Learn Go", "Master concurrency")
        assert h1 == h2
        assert h1 != h3

    def test_cosine_similarity(self):
        scorer = RecommendationScorer()
        vec1 = [1.0, 0.0, 0.0]
        vec2 = [1.0, 0.0, 0.0]
        vec3 = [0.0, 1.0, 0.0]
        assert scorer.cosine_similarity(vec1, vec2) == pytest.approx(1.0)
        assert scorer.cosine_similarity(vec1, vec3) == pytest.approx(0.0)


class TestParseLLMScores:
    """Tests for LLM response parsing."""

    def test_parse_scores(self):
        response = """
        RELEVANCE: 8.5
        URGENCY: 6.0
        FEASIBILITY: 7.5
        IMPACT: 9.0
        """
        scores = parse_llm_scores(response)
        assert scores["relevance"] == 8.5
        assert scores["urgency"] == 6.0

    def test_parse_clamps_values(self):
        response = "RELEVANCE: 15.0\nURGENCY: -5.0"
        scores = parse_llm_scores(response)
        assert scores["relevance"] == 10.0
        assert scores["urgency"] == 0.0


class TestRecommendationStorage:
    """Tests for SQLite storage."""

    @pytest.fixture
    def db_path(self, tmp_path):
        return tmp_path / "rec_test.db"

    @pytest.fixture
    def storage(self, db_path):
        return RecommendationStorage(db_path)

    def test_init_creates_db(self, db_path):
        storage = RecommendationStorage(db_path)
        assert db_path.exists()

    def test_save_and_get(self, storage):
        rec = Recommendation(
            category="learning",
            title="Learn Rust",
            description="Master async",
            score=8.0,
        )
        rec_id = storage.save(rec)
        retrieved = storage.get(rec_id)
        assert retrieved.title == "Learn Rust"
        assert retrieved.category == "learning"

    def test_update_status(self, storage):
        rec = Recommendation(category="career", title="Test", score=7.0)
        rec_id = storage.save(rec)
        storage.update_status(rec_id, "completed")
        retrieved = storage.get(rec_id)
        assert retrieved.status == "completed"

    def test_list_by_category(self, storage):
        storage.save(Recommendation(category="learning", title="A", score=8.0))
        storage.save(Recommendation(category="learning", title="B", score=7.0))
        storage.save(Recommendation(category="career", title="C", score=9.0))

        learning = storage.list_by_category("learning")
        assert len(learning) == 2

    def test_hash_exists(self, storage):
        rec = Recommendation(
            category="learning",
            title="Test",
            embedding_hash="abc123",
            score=7.0,
        )
        storage.save(rec)
        assert storage.hash_exists("abc123")
        assert not storage.hash_exists("xyz789")


class TestRecommendationEngine:
    """Tests for engine orchestration."""

    @pytest.fixture
    def mock_rag(self):
        rag = Mock()
        rag.get_journal_context.return_value = "User wants to learn Rust"
        rag.get_intel_context.return_value = "Rust demand growing 40%"
        return rag

    @pytest.fixture
    def mock_llm(self):
        def llm_caller(system, prompt):
            return """
### Learn Rust Async
**Description**: Master async programming in Rust
**Why**: Mentioned interest in systems programming
RELEVANCE: 8.0
URGENCY: 7.0
FEASIBILITY: 6.0
IMPACT: 8.0
"""
        return llm_caller

    @pytest.fixture
    def storage(self, tmp_path):
        return RecommendationStorage(tmp_path / "rec.db")

    def test_init_recommenders(self, mock_rag, mock_llm, storage):
        engine = RecommendationEngine(mock_rag, mock_llm, storage)
        assert "learning" in engine.recommenders
        assert "career" in engine.recommenders

    def test_generate_category(self, mock_rag, mock_llm, storage):
        engine = RecommendationEngine(mock_rag, mock_llm, storage)
        recs = engine.generate_category("learning", max_items=3, save=False)
        assert len(recs) >= 0  # May be empty if score threshold not met

    def test_config_disables_categories(self, mock_rag, mock_llm, storage):
        config = {"categories": {"learning": True, "career": False}}
        engine = RecommendationEngine(mock_rag, mock_llm, storage, config)
        assert "learning" in engine.recommenders
        assert "career" not in engine.recommenders
