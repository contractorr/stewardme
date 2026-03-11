"""Tests for GitHubRepoPoller."""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest

from intelligence.github_repo_poller import GitHubRepoPoller
from intelligence.github_repos import MonitoredRepo, RepoSnapshot


@pytest.fixture
def mock_client():
    client = AsyncMock()
    client.get_repo_stats = AsyncMock(
        return_value=RepoSnapshot(
            repo_full_name="owner/repo",
            commits_30d=10,
            open_issues=2,
            ci_status="success",
            pushed_at=datetime.now(timezone.utc) - timedelta(days=3),
            weekly_commits=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        )
    )
    return client


@pytest.fixture
def mock_store():
    store = MagicMock()
    store.save_snapshot = MagicMock()
    store.update_poll_tier = MagicMock()
    return store


@pytest.fixture
def poller(mock_client, mock_store):
    return GitHubRepoPoller(mock_client, mock_store)


def _make_repo(name="owner/repo", tier="moderate", goal=None):
    return MonitoredRepo(
        id="repo-1",
        user_id="user-1",
        repo_full_name=name,
        html_url=f"https://github.com/{name}",
        poll_tier=tier,
        linked_goal_path=goal,
    )


class TestPollOne:
    @pytest.mark.asyncio
    async def test_poll_one_success(self, poller, mock_store):
        repo = _make_repo()
        snapshot = await poller._poll_one(repo)
        assert snapshot.commits_30d == 10
        mock_store.save_snapshot.assert_called_once()

    @pytest.mark.asyncio
    async def test_poll_one_not_found(self, poller, mock_client):
        mock_client.get_repo_stats = AsyncMock(return_value=None)
        repo = _make_repo()
        with pytest.raises(ValueError, match="not found"):
            await poller._poll_one(repo)


class TestPollUserRepos:
    @pytest.mark.asyncio
    async def test_poll_user_repos(self, poller, mock_store):
        mock_store.get_repos_due_for_poll = MagicMock(return_value=[_make_repo()])
        snapshots = await poller.poll_user_repos("user-1")
        assert len(snapshots) == 1

    @pytest.mark.asyncio
    async def test_poll_empty(self, poller, mock_store):
        mock_store.get_repos_due_for_poll = MagicMock(return_value=[])
        snapshots = await poller.poll_user_repos("user-1")
        assert snapshots == []


class TestComputeTier:
    def test_active(self):
        snap = RepoSnapshot(
            repo_full_name="x/y",
            pushed_at=datetime.now(timezone.utc) - timedelta(days=2),
        )
        assert GitHubRepoPoller._compute_tier(snap) == "active"

    def test_moderate(self):
        snap = RepoSnapshot(
            repo_full_name="x/y",
            pushed_at=datetime.now(timezone.utc) - timedelta(days=15),
        )
        assert GitHubRepoPoller._compute_tier(snap) == "moderate"

    def test_stale(self):
        snap = RepoSnapshot(
            repo_full_name="x/y",
            pushed_at=datetime.now(timezone.utc) - timedelta(days=60),
        )
        assert GitHubRepoPoller._compute_tier(snap) == "stale"

    def test_no_pushed_at(self):
        snap = RepoSnapshot(repo_full_name="x/y", pushed_at=None)
        assert GitHubRepoPoller._compute_tier(snap) == "stale"
