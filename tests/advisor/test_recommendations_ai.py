"""Tests for AI capability context injection in recommendations."""

from unittest.mock import Mock

import pytest

from advisor.recommendation_storage import RecommendationStorage
from advisor.recommendations import (
    AI_RELEVANT_CATEGORIES,
    CATEGORY_QUERIES,
    RecommendationEngine,
)


class TestAIRelevantCategories:
    """Test AI relevance detection."""

    def test_entrepreneurial_is_ai_relevant(self):
        assert "entrepreneurial" in AI_RELEVANT_CATEGORIES

    def test_projects_is_ai_relevant(self):
        assert "projects" in AI_RELEVANT_CATEGORIES

    def test_investment_is_ai_relevant(self):
        assert "investment" in AI_RELEVANT_CATEGORIES

    def test_learning_is_ai_relevant(self):
        assert "learning" in AI_RELEVANT_CATEGORIES

    def test_events_not_ai_relevant(self):
        assert "events" not in AI_RELEVANT_CATEGORIES

    def test_career_not_ai_relevant(self):
        assert "career" not in AI_RELEVANT_CATEGORIES


class TestCategoryQueriesEnhanced:
    """Test that AI terms added to relevant category queries."""

    def test_entrepreneurial_has_ai_terms(self):
        q = CATEGORY_QUERIES["entrepreneurial"]
        assert "AI" in q
        assert "automation" in q

    def test_projects_has_ai_terms(self):
        q = CATEGORY_QUERIES["projects"]
        assert "AI" in q
        assert "agents" in q

    def test_investment_has_ai_terms(self):
        q = CATEGORY_QUERIES["investment"]
        assert "AI" in q
        assert "benchmarks" in q

    def test_events_unchanged(self):
        q = CATEGORY_QUERIES["events"]
        assert "AI" not in q


class TestAIContextInjection:
    """Test that AI context is injected for relevant categories only."""

    @pytest.fixture
    def mock_rag(self):
        rag = Mock()
        rag.get_journal_context.return_value = "User interested in AI automation"
        rag.get_intel_context.return_value = "AI tools trending"
        rag.get_profile_context.return_value = ""
        rag.get_ai_capabilities_context.return_value = (
            "AI Capabilities Snapshot: Coding agents solve ~70% of GitHub issues."
        )
        return rag

    @pytest.fixture
    def mock_llm(self):
        def llm_caller(system, prompt, **kwargs):
            return """
### Build AI Code Review SaaS
**Description**: Leverage coding agents for automated PR review
**Why**: AI benchmarks show 70% issue resolution
SCORE: 8.5

**REASONING**
SOURCE: AI capability data showing SWE-bench results
PROFILE_MATCH: Interest in developer tools
CONFIDENCE: 0.8
CAVEATS: Competitive market
"""

        return llm_caller

    @pytest.fixture
    def storage(self, tmp_path):
        return RecommendationStorage(tmp_path / "recs")

    def test_ai_context_injected_for_entrepreneurial(self, mock_rag, mock_llm, storage):
        """Entrepreneurial recs should call get_ai_capabilities_context."""
        engine = RecommendationEngine(
            mock_rag, mock_llm, storage, {"scoring": {"min_threshold": 0.0}}
        )
        engine.generate_category("entrepreneurial", save=False, with_action_plans=False)
        mock_rag.get_ai_capabilities_context.assert_called()

    def test_ai_context_injected_for_projects(self, mock_rag, mock_llm, storage):
        """Projects recs should call get_ai_capabilities_context."""
        engine = RecommendationEngine(
            mock_rag, mock_llm, storage, {"scoring": {"min_threshold": 0.0}}
        )
        engine.generate_category("projects", save=False, with_action_plans=False)
        mock_rag.get_ai_capabilities_context.assert_called()

    def test_ai_context_not_injected_for_events(self, mock_rag, mock_llm, storage):
        """Events recs should NOT call get_ai_capabilities_context."""
        engine = RecommendationEngine(
            mock_rag, mock_llm, storage, {"scoring": {"min_threshold": 0.0}}
        )
        engine.generate_category("events", save=False, with_action_plans=False)
        mock_rag.get_ai_capabilities_context.assert_not_called()

    def test_ai_context_not_injected_for_career(self, mock_rag, mock_llm, storage):
        """Career recs should NOT call get_ai_capabilities_context."""
        engine = RecommendationEngine(
            mock_rag, mock_llm, storage, {"scoring": {"min_threshold": 0.0}}
        )
        engine.generate_category("career", save=False, with_action_plans=False)
        mock_rag.get_ai_capabilities_context.assert_not_called()

    def test_ai_context_failure_falls_back(self, mock_rag, mock_llm, storage):
        """If AI context fails, should fall back to standard prompt."""
        mock_rag.get_ai_capabilities_context.side_effect = Exception("KB unavailable")
        engine = RecommendationEngine(
            mock_rag, mock_llm, storage, {"scoring": {"min_threshold": 0.0}}
        )
        # Should not raise
        recs = engine.generate_category(
            "entrepreneurial", save=False, with_action_plans=False
        )
        assert isinstance(recs, list)
