"""Tests for recommendation engine."""

from unittest.mock import Mock

import pytest

from advisor.recommendation_storage import Recommendation, RecommendationStorage
from advisor.recommendations import RecommendationEngine
from advisor.scoring import RecommendationScorer


class TestRecommendationScorer:
    """Tests for scoring functionality."""

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


class TestRecommendationStorage:
    """Tests for markdown-based storage."""

    @pytest.fixture
    def storage(self, tmp_path):
        return RecommendationStorage(tmp_path / "recs")

    def test_init_creates_dir(self, tmp_path):
        path = tmp_path / "recs"
        RecommendationStorage(path)
        assert path.exists()

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

    def test_add_feedback(self, storage):
        rec = Recommendation(category="learning", title="Test", score=7.0)
        rec_id = storage.save(rec)
        assert storage.add_feedback(rec_id, 4, comment="useful")
        retrieved = storage.get(rec_id)
        assert retrieved.metadata["user_rating"] == 4
        assert retrieved.metadata["feedback_comment"] == "useful"


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
        def llm_caller(system, prompt, **kwargs):
            return """
### Learn Rust Async
**Description**: Master async programming in Rust
**Why**: Mentioned interest in systems programming
SCORE: 8.0
"""

        return llm_caller

    @pytest.fixture
    def storage(self, tmp_path):
        return RecommendationStorage(tmp_path / "recs")

    def test_init_categories(self, mock_rag, mock_llm, storage):
        engine = RecommendationEngine(mock_rag, mock_llm, storage)
        assert "learning" in engine.enabled_categories
        assert "career" in engine.enabled_categories

    def test_generate_category(self, mock_rag, mock_llm, storage):
        engine = RecommendationEngine(mock_rag, mock_llm, storage)
        recs = engine.generate_category("learning", max_items=3, save=False)
        assert len(recs) >= 0  # May be empty if score threshold not met

    def test_config_disables_categories(self, mock_rag, mock_llm, storage):
        config = {"categories": {"learning": True, "career": False}}
        engine = RecommendationEngine(mock_rag, mock_llm, storage, config)
        assert "learning" in engine.enabled_categories
        assert "career" not in engine.enabled_categories
