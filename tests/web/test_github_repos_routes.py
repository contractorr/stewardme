"""Tests for GitHub repo monitoring routes."""

from unittest.mock import MagicMock, patch


class TestMonitorRepo:
    def test_monitor_repo(self, client, auth_headers):
        with patch("web.routes.github_repos.get_github_repo_store") as mock_store_fn:
            store = MagicMock()
            store.add_repo.return_value = "repo-123"
            store.get_repo.return_value = MagicMock(
                id="repo-123",
                repo_full_name="owner/myrepo",
                html_url="https://github.com/owner/myrepo",
                is_private=False,
                linked_goal_path=None,
                poll_tier="moderate",
                last_polled_at=None,
                added_at="2026-03-11",
            )
            store.get_latest_snapshot.return_value = None
            mock_store_fn.return_value = store

            res = client.post(
                "/api/github/repos/monitor",
                headers=auth_headers,
                json={"repo_full_name": "owner/myrepo"},
            )
            assert res.status_code == 201
            assert res.json()["repo_full_name"] == "owner/myrepo"

    def test_monitor_duplicate_409(self, client, auth_headers):
        with patch("web.routes.github_repos.get_github_repo_store") as mock_store_fn:
            store = MagicMock()
            store.add_repo.side_effect = ValueError("already monitored")
            mock_store_fn.return_value = store

            res = client.post(
                "/api/github/repos/monitor",
                headers=auth_headers,
                json={"repo_full_name": "owner/myrepo"},
            )
            assert res.status_code == 409

    def test_monitor_invalid_name_400(self, client, auth_headers):
        res = client.post(
            "/api/github/repos/monitor",
            headers=auth_headers,
            json={"repo_full_name": "../evil/path"},
        )
        assert res.status_code == 422  # pydantic pattern validation


class TestUnmonitorRepo:
    def test_unmonitor(self, client, auth_headers):
        with patch("web.routes.github_repos.get_github_repo_store") as mock_store_fn:
            store = MagicMock()
            store.remove_repo.return_value = True
            mock_store_fn.return_value = store

            res = client.delete(
                "/api/github/repos/monitor/repo-123",
                headers=auth_headers,
            )
            assert res.status_code == 204

    def test_unmonitor_not_found(self, client, auth_headers):
        with patch("web.routes.github_repos.get_github_repo_store") as mock_store_fn:
            store = MagicMock()
            store.remove_repo.return_value = False
            mock_store_fn.return_value = store

            res = client.delete(
                "/api/github/repos/monitor/nonexistent",
                headers=auth_headers,
            )
            assert res.status_code == 404


class TestListMonitored:
    def test_list_empty(self, client, auth_headers):
        with patch("web.routes.github_repos.get_github_repo_store") as mock_store_fn:
            store = MagicMock()
            store.list_repos.return_value = []
            mock_store_fn.return_value = store

            res = client.get("/api/github/repos/monitored", headers=auth_headers)
            assert res.status_code == 200
            assert res.json() == []


class TestUserIsolation:
    def test_user_b_cannot_see_user_a_repos(self, client, auth_headers, auth_headers_b):
        with patch("web.routes.github_repos.get_github_repo_store") as mock_store_fn:
            store = MagicMock()

            def list_repos_side_effect(user_id):
                if user_id == "user-123":
                    return [
                        MagicMock(
                            id="r1",
                            repo_full_name="owner/secret",
                            html_url="url",
                            is_private=True,
                            linked_goal_path=None,
                            poll_tier="moderate",
                            last_polled_at=None,
                            added_at="2026-03-11",
                        )
                    ]
                return []

            store.list_repos.side_effect = list_repos_side_effect
            store.get_latest_snapshot.return_value = None
            mock_store_fn.return_value = store

            # User A sees their repo
            res_a = client.get("/api/github/repos/monitored", headers=auth_headers)
            assert res_a.status_code == 200
            assert len(res_a.json()) == 1

            # User B sees nothing
            res_b = client.get("/api/github/repos/monitored", headers=auth_headers_b)
            assert res_b.status_code == 200
            assert len(res_b.json()) == 0


class TestLinkGoal:
    def test_link_goal(self, client, auth_headers):
        with patch("web.routes.github_repos.get_github_repo_store") as mock_store_fn:
            store = MagicMock()
            repo_mock = MagicMock(
                id="r1",
                repo_full_name="owner/repo",
                html_url="url",
                is_private=False,
                linked_goal_path="goals/my-goal.md",
                poll_tier="moderate",
                last_polled_at=None,
                added_at="2026-03-11",
            )
            store.get_repo.return_value = repo_mock
            store.get_latest_snapshot.return_value = None
            mock_store_fn.return_value = store

            res = client.patch(
                "/api/github/repos/monitor/r1/link",
                headers=auth_headers,
                json={"goal_path": "goals/my-goal.md"},
            )
            assert res.status_code == 200
            store.link_goal.assert_called_once()

    def test_link_goal_repo_not_found(self, client, auth_headers):
        with patch("web.routes.github_repos.get_github_repo_store") as mock_store_fn:
            store = MagicMock()
            store.get_repo.return_value = None
            mock_store_fn.return_value = store

            res = client.patch(
                "/api/github/repos/monitor/bad-id/link",
                headers=auth_headers,
                json={"goal_path": "goals/my-goal.md"},
            )
            assert res.status_code == 404
