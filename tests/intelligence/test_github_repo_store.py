"""Tests for GitHubRepoStore."""

import pytest

from intelligence.github_repo_store import GitHubRepoStore
from intelligence.github_repos import RepoSnapshot


@pytest.fixture
def store(tmp_path):
    return GitHubRepoStore(tmp_path / "intel.db")


class TestAddRemoveRepos:
    def test_add_and_list(self, store):
        repo_id = store.add_repo("user-1", "owner/repo", "https://github.com/owner/repo")
        repos = store.list_repos("user-1")
        assert len(repos) == 1
        assert repos[0].repo_full_name == "owner/repo"
        assert repos[0].id == repo_id

    def test_add_duplicate_raises(self, store):
        store.add_repo("user-1", "owner/repo", "https://github.com/owner/repo")
        with pytest.raises(ValueError, match="already monitored"):
            store.add_repo("user-1", "owner/repo", "https://github.com/owner/repo")

    def test_remove_repo(self, store):
        repo_id = store.add_repo("user-1", "owner/repo", "https://github.com/owner/repo")
        assert store.remove_repo("user-1", repo_id)
        assert store.list_repos("user-1") == []

    def test_remove_wrong_user(self, store):
        repo_id = store.add_repo("user-1", "owner/repo", "https://github.com/owner/repo")
        assert not store.remove_repo("user-2", repo_id)

    def test_user_isolation(self, store):
        store.add_repo("user-1", "owner/repo1", "https://github.com/owner/repo1")
        store.add_repo("user-2", "owner/repo2", "https://github.com/owner/repo2")
        assert len(store.list_repos("user-1")) == 1
        assert store.list_repos("user-1")[0].repo_full_name == "owner/repo1"

    def test_private_flag(self, store):
        store.add_repo("user-1", "owner/repo", "https://github.com/owner/repo", is_private=True)
        repos = store.list_repos("user-1")
        assert repos[0].is_private is True


class TestGoalLinking:
    def test_link_and_unlink(self, store):
        repo_id = store.add_repo("user-1", "owner/repo", "https://github.com/owner/repo")
        store.link_goal(repo_id, "goals/my-goal.md")
        repo = store.get_repo("user-1", repo_id)
        assert repo.linked_goal_path == "goals/my-goal.md"

        store.unlink_goal(repo_id)
        repo = store.get_repo("user-1", repo_id)
        assert repo.linked_goal_path is None


class TestSnapshots:
    def test_save_and_get_latest(self, store):
        repo_id = store.add_repo("user-1", "owner/repo", "https://github.com/owner/repo")
        snapshot = RepoSnapshot(
            repo_full_name="owner/repo",
            commits_30d=42,
            open_issues=5,
            open_prs=3,
            ci_status="success",
            weekly_commits=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        )
        store.save_snapshot(repo_id, snapshot)
        latest = store.get_latest_snapshot(repo_id)
        assert latest is not None
        assert latest.commits_30d == 42
        assert latest.open_issues == 5
        assert latest.weekly_commits == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    def test_snapshot_history(self, store):
        repo_id = store.add_repo("user-1", "owner/repo", "https://github.com/owner/repo")
        for i in range(3):
            snapshot = RepoSnapshot(repo_full_name="owner/repo", commits_30d=i * 10)
            store.save_snapshot(repo_id, snapshot)
        history = store.get_snapshot_history(repo_id, days=90)
        assert len(history) == 3

    def test_prune_snapshots(self, store):
        repo_id = store.add_repo("user-1", "owner/repo", "https://github.com/owner/repo")
        snapshot = RepoSnapshot(repo_full_name="owner/repo", commits_30d=10)
        store.save_snapshot(repo_id, snapshot)
        # Recent snapshot should not be pruned
        pruned = store.prune_snapshots(max_age_days=90)
        assert pruned == 0

    def test_cascade_delete(self, store):
        repo_id = store.add_repo("user-1", "owner/repo", "https://github.com/owner/repo")
        snapshot = RepoSnapshot(repo_full_name="owner/repo", commits_30d=10)
        store.save_snapshot(repo_id, snapshot)
        assert store.get_latest_snapshot(repo_id) is not None
        store.remove_repo("user-1", repo_id)
        assert store.get_latest_snapshot(repo_id) is None


class TestPollTier:
    def test_get_repos_due_for_poll_new(self, store):
        """New repos (never polled) should always be due."""
        store.add_repo("user-1", "owner/repo", "https://github.com/owner/repo")
        due = store.get_repos_due_for_poll("user-1")
        assert len(due) == 1

    def test_update_poll_tier(self, store):
        repo_id = store.add_repo("user-1", "owner/repo", "https://github.com/owner/repo")
        store.update_poll_tier(repo_id, "active")
        repo = store.get_repo("user-1", repo_id)
        assert repo.poll_tier == "active"

    def test_get_all_user_ids(self, store):
        store.add_repo("user-1", "owner/repo1", "url1")
        store.add_repo("user-2", "owner/repo2", "url2")
        ids = store.get_all_user_ids_with_repos()
        assert set(ids) == {"user-1", "user-2"}
