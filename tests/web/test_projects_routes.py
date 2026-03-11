"""Tests for projects API routes."""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch


def test_get_issues_returns_normalized_matches(client, auth_headers):
    mocked_results = [
        {
            "title": "Improve auth middleware",
            "url": "https://github.com/acme/app/issues/1",
            "summary": "FastAPI auth cleanup",
            "tags": "python,fastapi,security",
            "source": "github_issues",
            "_match_score": 3,
        },
        {
            "title": "Document CLI flags",
            "url": "https://github.com/acme/app/issues/2",
            "summary": "Improve contributor docs",
            "tags": ["docs", "cli"],
            "source": "github_issues",
            "_match_score": 1,
        },
    ]

    with patch("advisor.projects.get_matching_issues", return_value=mocked_results):
        response = client.get("/api/projects/issues?limit=5&days=7", headers=auth_headers)

    assert response.status_code == 200
    assert response.json() == [
        {
            "title": "Improve auth middleware",
            "url": "https://github.com/acme/app/issues/1",
            "summary": "FastAPI auth cleanup",
            "tags": ["python", "fastapi", "security"],
            "source": "github_issues",
            "match_score": 3,
        },
        {
            "title": "Document CLI flags",
            "url": "https://github.com/acme/app/issues/2",
            "summary": "Improve contributor docs",
            "tags": ["docs", "cli"],
            "source": "github_issues",
            "match_score": 1,
        },
    ]


def test_generate_ideas_requires_api_key(client, auth_headers):
    with patch("web.routes.projects.get_api_key_for_user", return_value=None):
        response = client.post("/api/projects/ideas", headers=auth_headers)

    assert response.status_code == 400
    assert response.json() == {"detail": "No LLM API key configured"}


def test_generate_ideas_uses_provider_messages_contract(client, auth_headers):
    provider = MagicMock()
    provider.generate.return_value = "Idea list"

    def _call_llm(_rag, llm_caller):
        return llm_caller("System prompt", "User prompt", max_tokens=321)

    config = SimpleNamespace(llm=SimpleNamespace(provider="openai", model="gpt-test"))

    with (
        patch("web.routes.projects.get_api_key_for_user", return_value="sk-test"),
        patch("web.routes.projects.get_config", return_value=config),
        patch("journal.storage.JournalStorage"),
        patch("journal.embeddings.EmbeddingManager"),
        patch("journal.fts.JournalFTSIndex"),
        patch("journal.search.JournalSearch"),
        patch("advisor.rag.RAGRetriever"),
        patch("llm.factory.create_llm_provider", return_value=provider),
        patch("web.routes.projects.generate_project_ideas", side_effect=_call_llm),
    ):
        response = client.post("/api/projects/ideas", headers=auth_headers)

    assert response.status_code == 200
    assert response.json() == {"ideas": "Idea list"}
    provider.generate.assert_called_once_with(
        messages=[{"role": "user", "content": "User prompt"}],
        system="System prompt",
        max_tokens=321,
    )
