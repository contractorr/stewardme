"""Tests for ResearchSynthesizer."""

import pytest
from unittest.mock import MagicMock, patch

from research.synthesis import ResearchSynthesizer
from research.web_search import SearchResult


@pytest.fixture
def mock_claude_client():
    """Mock Claude client."""
    mock = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="""## Summary
Test research summary.

## Key Insights
- Insight 1
- Insight 2

## Relevance to Your Goals
This relates to your learning goals.

## Sources
- Source 1

## Next Steps
- Action 1
""")]
    mock.messages.create.return_value = mock_response
    return mock


@pytest.fixture
def sample_search_results():
    """Sample search results for testing."""
    return [
        SearchResult(
            title="Article 1",
            url="https://example.com/1",
            content="Content about machine learning.",
            score=0.9,
        ),
        SearchResult(
            title="Article 2",
            url="https://example.com/2",
            content="More content about AI.",
            score=0.8,
        ),
    ]


class TestResearchSynthesizer:
    """Tests for ResearchSynthesizer."""

    def test_synthesize_with_results(self, mock_claude_client, sample_search_results):
        """Test synthesis generates report."""
        synth = ResearchSynthesizer(client=mock_claude_client)
        report = synth.synthesize(
            topic="Machine Learning",
            results=sample_search_results,
            user_context="Learning AI",
        )

        assert "## Summary" in report
        assert "## Key Insights" in report
        mock_claude_client.messages.create.assert_called_once()

    def test_synthesize_empty_results(self, mock_claude_client):
        """Test synthesis with no results."""
        synth = ResearchSynthesizer(client=mock_claude_client)
        report = synth.synthesize(topic="Unknown Topic", results=[])

        assert "No sources found" in report
        mock_claude_client.messages.create.assert_not_called()

    def test_synthesize_with_user_context(self, mock_claude_client, sample_search_results):
        """Test that user context is included in prompt."""
        synth = ResearchSynthesizer(client=mock_claude_client)
        synth.synthesize(
            topic="Test",
            results=sample_search_results,
            user_context="My goal is to learn Rust",
        )

        call_args = mock_claude_client.messages.create.call_args
        prompt = call_args.kwargs["messages"][0]["content"]
        assert "My goal is to learn Rust" in prompt

    def test_format_sources(self, mock_claude_client, sample_search_results):
        """Test source formatting."""
        synth = ResearchSynthesizer(client=mock_claude_client)
        formatted = synth._format_sources(sample_search_results)

        assert "[Source 1]" in formatted
        assert "[Source 2]" in formatted
        assert "Article 1" in formatted
        assert "https://example.com/1" in formatted

    def test_fallback_report_on_api_error(self, sample_search_results):
        """Test fallback report when API fails."""
        mock_client = MagicMock()
        from anthropic import APIError
        mock_client.messages.create.side_effect = APIError("API Error", request=MagicMock(), body=None)

        synth = ResearchSynthesizer(client=mock_client)
        report = synth.synthesize(topic="Test", results=sample_search_results)

        assert "synthesis unavailable" in report.lower()
        assert "Article 1" in report
