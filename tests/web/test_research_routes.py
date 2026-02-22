"""Tests for research API routes (topics, run)."""

from unittest.mock import MagicMock, patch

_AGENT_PATCH = "web.routes.research._get_agent"


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
