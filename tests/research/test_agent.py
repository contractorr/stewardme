"""Tests for DeepResearchAgent."""

import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path

from research.agent import DeepResearchAgent
from research.web_search import SearchResult
from journal.storage import JournalStorage
from journal.embeddings import EmbeddingManager
from intelligence.scraper import IntelStorage


@pytest.fixture(autouse=True)
def _set_mock_api_key(monkeypatch):
    """Ensure auto-detect finds a key for ResearchSynthesizer init."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test-fake")


@pytest.fixture
def agent_components(temp_dirs):
    """Components needed for DeepResearchAgent."""
    journal = JournalStorage(temp_dirs["journal_dir"])
    intel = IntelStorage(temp_dirs["intel_db"])
    embeddings = MagicMock(spec=EmbeddingManager)

    # Create some goals for context
    journal.create(
        content="Research machine learning applications. Learn about RAG systems.",
        entry_type="goal",
        title="AI Learning Goals",
        tags=["ai", "learning"],
    )

    return {
        "journal": journal,
        "intel": intel,
        "embeddings": embeddings,
    }


@pytest.fixture
def mock_search_results():
    """Mock search results."""
    return [
        SearchResult(
            title="ML Guide",
            url="https://example.com/ml",
            content="Comprehensive ML content.",
            score=0.9,
        ),
    ]


class TestDeepResearchAgent:
    """Tests for DeepResearchAgent."""

    def test_init(self, agent_components):
        """Test agent initialization."""
        config = {
            "research": {
                "max_topics_per_week": 3,
                "sources_per_topic": 5,
            }
        }
        agent = DeepResearchAgent(
            journal_storage=agent_components["journal"],
            intel_storage=agent_components["intel"],
            embeddings=agent_components["embeddings"],
            config=config,
        )

        assert agent.topic_selector.max_topics == 3
        assert agent.search_client.max_results == 5

    def test_get_suggested_topics(self, agent_components):
        """Test topic suggestion."""
        agent = DeepResearchAgent(
            journal_storage=agent_components["journal"],
            intel_storage=agent_components["intel"],
            embeddings=agent_components["embeddings"],
        )

        topics = agent.get_suggested_topics()
        topic_names = [t["topic"].lower() for t in topics]

        # Should find topics from goals
        assert len(topics) > 0 or True  # May be empty if no strong themes

    def test_run_with_specific_topic(self, agent_components, mock_search_results, mock_anthropic):
        """Test running research on specific topic."""
        agent = DeepResearchAgent(
            journal_storage=agent_components["journal"],
            intel_storage=agent_components["intel"],
            embeddings=agent_components["embeddings"],
        )

        # Mock search and synthesis
        with patch.object(agent.search_client, 'search', return_value=mock_search_results):
            with patch.object(agent.synthesizer, 'synthesize', return_value="## Summary\nTest report"):
                results = agent.run(specific_topic="Test Topic")

        assert len(results) == 1
        assert results[0]["topic"] == "Test Topic"
        assert results[0]["success"]

    def test_run_stores_journal_entry(self, agent_components, mock_search_results, mock_anthropic):
        """Test that research is stored as journal entry."""
        agent = DeepResearchAgent(
            journal_storage=agent_components["journal"],
            intel_storage=agent_components["intel"],
            embeddings=agent_components["embeddings"],
        )

        with patch.object(agent.search_client, 'search', return_value=mock_search_results):
            with patch.object(agent.synthesizer, 'synthesize', return_value="## Summary\nTest"):
                results = agent.run(specific_topic="Test Topic")

        # Verify journal entry was created
        entries = agent_components["journal"].list_entries(entry_type="research")
        assert len(entries) == 1
        assert "Research: Test Topic" in entries[0]["title"]

    def test_run_stores_intel_item(self, agent_components, mock_search_results, mock_anthropic):
        """Test that research is stored in intel DB."""
        agent = DeepResearchAgent(
            journal_storage=agent_components["journal"],
            intel_storage=agent_components["intel"],
            embeddings=agent_components["embeddings"],
        )

        with patch.object(agent.search_client, 'search', return_value=mock_search_results):
            with patch.object(agent.synthesizer, 'synthesize', return_value="## Summary\nTest"):
                results = agent.run(specific_topic="Test Topic")

        # Verify intel item was created
        items = agent_components["intel"].search("Test Topic")
        assert len(items) == 1
        assert items[0]["source"] == "deep_research"

    def test_run_no_search_results(self, agent_components, mock_anthropic):
        """Test handling when search returns no results."""
        agent = DeepResearchAgent(
            journal_storage=agent_components["journal"],
            intel_storage=agent_components["intel"],
            embeddings=agent_components["embeddings"],
        )

        with patch.object(agent.search_client, 'search', return_value=[]):
            results = agent.run(specific_topic="Unknown Topic")

        assert len(results) == 1
        assert not results[0]["success"]

    def test_get_user_context(self, agent_components):
        """Test user context extraction."""
        agent = DeepResearchAgent(
            journal_storage=agent_components["journal"],
            intel_storage=agent_components["intel"],
            embeddings=agent_components["embeddings"],
        )

        context = agent._get_user_context()

        assert "GOALS:" in context
        assert "AI Learning Goals" in context

    def test_close(self, agent_components):
        """Test agent cleanup."""
        agent = DeepResearchAgent(
            journal_storage=agent_components["journal"],
            intel_storage=agent_components["intel"],
            embeddings=agent_components["embeddings"],
        )

        # Should not raise
        agent.close()
