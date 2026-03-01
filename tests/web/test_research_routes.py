"""Tests for research API routes (topics, run)."""

from unittest.mock import MagicMock, patch

_AGENT_PATCH = "web.routes.research._get_agent"
_AGENT_CLASS = "research.agent.DeepResearchAgent"


def test_get_topics(client, auth_headers):
    mock_agent = MagicMock()
    mock_agent.get_suggested_topics.return_value = [
        {"topic": "AI Safety", "source": "journal", "score": 0.9, "reason": "Mentioned often"},
    ]
    with patch(_AGENT_PATCH, return_value=mock_agent):
        res = client.get("/api/research/topics", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["topic"] == "AI Safety"


def test_get_topics_empty(client, auth_headers):
    mock_agent = MagicMock()
    mock_agent.get_suggested_topics.return_value = []
    with patch(_AGENT_PATCH, return_value=mock_agent):
        res = client.get("/api/research/topics", headers=auth_headers)
    assert res.status_code == 200
    assert res.json() == []


def test_run_research(client, auth_headers):
    mock_agent = MagicMock()
    mock_agent.run.return_value = [{"topic": "Rust", "report": "Rust is great"}]
    with patch(_AGENT_PATCH, return_value=mock_agent):
        res = client.post("/api/research/run?topic=Rust", headers=auth_headers)
    assert res.status_code == 200
    assert "results" in res.json()
    mock_agent.run.assert_called_once_with(specific_topic="Rust")


def test_run_research_no_topic(client, auth_headers):
    mock_agent = MagicMock()
    mock_agent.run.return_value = []
    with patch(_AGENT_PATCH, return_value=mock_agent):
        res = client.post("/api/research/run", headers=auth_headers)
    assert res.status_code == 200
    mock_agent.run.assert_called_once_with(specific_topic=None)


def test_get_agent_injects_user_tavily_key(client, auth_headers, secret_key):
    """User's stored tavily_api_key flows into DeepResearchAgent config."""
    captured_config = {}
    mock_agent = MagicMock()
    mock_agent.get_suggested_topics.return_value = []

    class FakeAgent:
        def __init__(self, **kwargs):
            captured_config.update(kwargs.get("config", {}))
            # Proxy all attribute access to mock_agent
            self.__dict__.update(mock_agent.__dict__)

        def get_suggested_topics(self):
            return mock_agent.get_suggested_topics()

    with (
        patch(_AGENT_CLASS, FakeAgent),
        patch("journal.storage.JournalStorage"),
        patch("journal.embeddings.EmbeddingManager"),
        patch("intelligence.scraper.IntelStorage"),
        patch(
            "web.user_store.get_user_secret",
            return_value="tvly-test-key-456",
        ),
        patch("web.deps.get_secret_key", return_value=secret_key),
    ):
        res = client.get("/api/research/topics", headers=auth_headers)
    assert res.status_code == 200
    assert captured_config.get("research", {}).get("api_key") == "tvly-test-key-456"


def test_get_agent_works_without_tavily_key(client, auth_headers):
    """Agent still constructed when user has no stored tavily key."""
    mock_agent = MagicMock()
    mock_agent.get_suggested_topics.return_value = []
    with patch(_AGENT_PATCH, return_value=mock_agent):
        res = client.get("/api/research/topics", headers=auth_headers)
    assert res.status_code == 200
