"""Tests for AdvisorEngine."""

from unittest.mock import MagicMock, patch
import pytest

from advisor.engine import AdvisorEngine, APIKeyMissingError, LLMError


@pytest.fixture
def mock_rag():
    rag = MagicMock()
    rag.get_combined_context.return_value = ("journal ctx", "intel ctx")
    rag.get_recent_entries.return_value = "recent entries"
    rag.get_intel_context.return_value = "intel context"
    rag.get_journal_context.return_value = "journal context"
    rag.get_research_context.return_value = ""
    return rag


@pytest.fixture
def mock_client():
    client = MagicMock()
    resp = MagicMock()
    resp.content = [MagicMock(text="Mocked LLM response")]
    client.messages.create.return_value = resp
    return client


@pytest.fixture
def engine(mock_rag, mock_client):
    return AdvisorEngine(rag=mock_rag, client=mock_client)


class TestAdvisorEngine:
    def test_init_requires_api_key(self, mock_rag):
        with pytest.raises(APIKeyMissingError):
            AdvisorEngine(rag=mock_rag, api_key=None)

    def test_init_with_client(self, mock_rag, mock_client):
        engine = AdvisorEngine(rag=mock_rag, client=mock_client)
        assert engine.client is mock_client

    def test_ask_general(self, engine, mock_client):
        result = engine.ask("What should I learn?")
        assert result == "Mocked LLM response"
        mock_client.messages.create.assert_called_once()

    def test_ask_career(self, engine, mock_client):
        result = engine.ask("Career advice?", advice_type="career")
        assert isinstance(result, str)
        assert mock_client.messages.create.called

    def test_ask_includes_research_context(self, engine, mock_rag):
        mock_rag.get_research_context.return_value = "research data here"
        engine.ask("test", include_research=True)
        mock_rag.get_research_context.assert_called()

    def test_ask_skips_research_when_disabled(self, engine, mock_rag):
        engine.ask("test", include_research=False)
        mock_rag.get_research_context.assert_not_called()

    def test_weekly_review(self, engine, mock_client):
        result = engine.weekly_review()
        assert isinstance(result, str)
        assert mock_client.messages.create.called

    def test_weekly_review_with_stale_goals(self, engine, mock_client, populated_journal):
        result = engine.weekly_review(journal_storage=populated_journal["storage"])
        assert isinstance(result, str)

    def test_detect_opportunities(self, engine, mock_client):
        result = engine.detect_opportunities()
        assert isinstance(result, str)
        assert mock_client.messages.create.called

    def test_analyze_goals(self, engine, mock_client):
        result = engine.analyze_goals()
        assert isinstance(result, str)

    def test_analyze_goals_specific(self, engine, mock_client):
        result = engine.analyze_goals(specific_goal="Learn Rust")
        assert isinstance(result, str)

    def test_llm_auth_error(self, mock_rag):
        from anthropic import AuthenticationError
        client = MagicMock()
        client.messages.create.side_effect = AuthenticationError(
            message="bad key", response=MagicMock(status_code=401), body={}
        )
        engine = AdvisorEngine(rag=mock_rag, client=client)
        with pytest.raises(LLMError, match="Invalid API key"):
            engine.ask("test")

    def test_generate_recommendations(self, engine, tmp_path):
        db_path = tmp_path / "recs.db"
        recs = engine.generate_recommendations("learning", db_path)
        assert isinstance(recs, list)

    def test_generate_action_brief(self, engine, tmp_path):
        db_path = tmp_path / "recs.db"
        brief = engine.generate_action_brief(db_path)
        assert isinstance(brief, str)
