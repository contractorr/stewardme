"""Tests for GitHubRepoClient."""

import httpx
import pytest

from intelligence.github_repos import GitHubRepoClient


@pytest.fixture
def mock_transport():
    """Create a mock httpx transport."""
    return httpx.MockTransport(lambda request: httpx.Response(200, json=[]))


class TestGitHubRepoClient:
    @pytest.mark.asyncio
    async def test_list_user_repos_success(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                200,
                json=[
                    {
                        "id": 1,
                        "name": "myrepo",
                        "full_name": "user/myrepo",
                        "private": False,
                        "archived": False,
                        "default_branch": "main",
                        "pushed_at": "2026-03-01T00:00:00Z",
                        "open_issues_count": 3,
                        "language": "Python",
                        "html_url": "https://github.com/user/myrepo",
                    }
                ],
                headers={"X-RateLimit-Remaining": "4999"},
            )

        transport = httpx.MockTransport(handler)
        client = GitHubRepoClient(token="test-token")
        client._client = httpx.AsyncClient(transport=transport, base_url="https://api.github.com")
        try:
            repos = await client.list_user_repos("user")
            assert len(repos) == 1
            assert repos[0].full_name == "user/myrepo"
            assert repos[0].language == "Python"
        finally:
            await client.close()

    @pytest.mark.asyncio
    async def test_list_user_repos_404(self):
        transport = httpx.MockTransport(lambda r: httpx.Response(404))
        client = GitHubRepoClient()
        client._client = httpx.AsyncClient(transport=transport, base_url="https://api.github.com")
        try:
            repos = await client.list_user_repos("nonexistent")
            assert repos == []
        finally:
            await client.close()

    @pytest.mark.asyncio
    async def test_list_user_repos_403_rate_limit(self):
        transport = httpx.MockTransport(lambda r: httpx.Response(403))
        client = GitHubRepoClient()
        client._client = httpx.AsyncClient(transport=transport, base_url="https://api.github.com")
        try:
            repos = await client.list_user_repos("user")
            assert repos == []
        finally:
            await client.close()

    @pytest.mark.asyncio
    async def test_get_commit_activity(self):
        weekly = list(range(52))

        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={"all": weekly, "owner": weekly})

        transport = httpx.MockTransport(handler)
        client = GitHubRepoClient(token="test")
        client._client = httpx.AsyncClient(transport=transport, base_url="https://api.github.com")
        try:
            result = await client.get_commit_activity("owner", "repo")
            assert len(result) == 12
            assert result == weekly[-12:]
        finally:
            await client.close()

    @pytest.mark.asyncio
    async def test_get_commit_activity_202(self):
        """202 means stats computing — return empty."""
        transport = httpx.MockTransport(lambda r: httpx.Response(202))
        client = GitHubRepoClient()
        client._client = httpx.AsyncClient(transport=transport, base_url="https://api.github.com")
        try:
            result = await client.get_commit_activity("owner", "repo")
            assert result == []
        finally:
            await client.close()

    @pytest.mark.asyncio
    async def test_get_ci_status_success(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                200,
                json={
                    "workflow_runs": [
                        {
                            "conclusion": "success",
                            "updated_at": "2026-03-01T00:00:00Z",
                            "name": "CI",
                        }
                    ]
                },
            )

        transport = httpx.MockTransport(handler)
        client = GitHubRepoClient(token="test")
        client._client = httpx.AsyncClient(transport=transport, base_url="https://api.github.com")
        try:
            ci = await client.get_ci_status("owner", "repo", "main")
            assert ci.state == "success"
            assert ci.workflow_name == "CI"
        finally:
            await client.close()

    @pytest.mark.asyncio
    async def test_get_ci_status_no_runs(self):
        transport = httpx.MockTransport(lambda r: httpx.Response(200, json={"workflow_runs": []}))
        client = GitHubRepoClient()
        client._client = httpx.AsyncClient(transport=transport, base_url="https://api.github.com")
        try:
            ci = await client.get_ci_status("owner", "repo", "main")
            assert ci.state == "none"
        finally:
            await client.close()

    @pytest.mark.asyncio
    async def test_rate_limit_tracking(self):
        transport = httpx.MockTransport(
            lambda r: httpx.Response(
                200,
                json=[],
                headers={"X-RateLimit-Remaining": "50"},
            )
        )
        client = GitHubRepoClient(token="test")
        client._client = httpx.AsyncClient(transport=transport, base_url="https://api.github.com")
        try:
            await client.list_user_repos("user")
            assert client._rate_limited is True
            assert client._rate_limit_remaining == 50
        finally:
            await client.close()
