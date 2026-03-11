"""Tests for GitHub repo signal detectors."""

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import pytest

from advisor.signals import SignalDetector, SignalType
from intelligence.github_repos import MonitoredRepo, RepoSnapshot


def _make_repo(name="owner/repo", goal=None):
    return MonitoredRepo(
        id="repo-1",
        user_id="user-1",
        repo_full_name=name,
        html_url=f"https://github.com/{name}",
        linked_goal_path=goal,
    )


def _make_snapshot(
    commits_30d=10,
    pushed_days_ago=5,
    ci_status="success",
    open_issues=3,
    weekly_commits=None,
):
    pushed = (
        datetime.now(timezone.utc) - timedelta(days=pushed_days_ago) if pushed_days_ago else None
    )
    return RepoSnapshot(
        repo_full_name="owner/repo",
        commits_30d=commits_30d,
        open_issues=open_issues,
        ci_status=ci_status,
        pushed_at=pushed,
        weekly_commits=weekly_commits or [5] * 12,
    )


@pytest.fixture
def mock_journal():
    journal = MagicMock()
    journal.list_entries = MagicMock(return_value=[])
    return journal


@pytest.fixture
def mock_repo_store():
    store = MagicMock()
    store.get_all_user_ids_with_repos = MagicMock(return_value=["user-1"])
    store.list_repos = MagicMock(return_value=[_make_repo()])
    return store


class TestRepoStaleDetector:
    def test_stale_repo_fires(self, tmp_path, mock_journal, mock_repo_store):
        mock_repo_store.get_latest_snapshot = MagicMock(
            return_value=_make_snapshot(pushed_days_ago=20)
        )
        detector = SignalDetector(
            mock_journal,
            tmp_path / "intel.db",
            config={"github_monitoring": {"stale_threshold_days": 14}},
            repo_store=mock_repo_store,
        )
        signals = detector._detect_repo_stale()
        assert len(signals) == 1
        assert signals[0].type == SignalType.REPO_STALE

    def test_active_repo_no_signal(self, tmp_path, mock_journal, mock_repo_store):
        mock_repo_store.get_latest_snapshot = MagicMock(
            return_value=_make_snapshot(pushed_days_ago=3)
        )
        detector = SignalDetector(
            mock_journal,
            tmp_path / "intel.db",
            config={"github_monitoring": {"stale_threshold_days": 14}},
            repo_store=mock_repo_store,
        )
        signals = detector._detect_repo_stale()
        assert len(signals) == 0

    def test_goal_linked_higher_severity(self, tmp_path, mock_journal, mock_repo_store):
        mock_repo_store.list_repos = MagicMock(return_value=[_make_repo(goal="goals/build-app.md")])
        mock_repo_store.get_latest_snapshot = MagicMock(
            return_value=_make_snapshot(pushed_days_ago=20)
        )
        detector = SignalDetector(
            mock_journal,
            tmp_path / "intel.db",
            config={"github_monitoring": {"stale_threshold_days": 14}},
            repo_store=mock_repo_store,
        )
        signals = detector._detect_repo_stale()
        assert signals[0].severity == 6  # goal-linked


class TestRepoVelocityDetector:
    def test_velocity_decrease_fires(self, tmp_path, mock_journal, mock_repo_store):
        # Prior 4 weeks: 10/wk, recent 4 weeks: 2/wk → -80%
        wc = [10, 10, 10, 10, 10, 10, 10, 10, 2, 2, 2, 2]
        mock_repo_store.get_latest_snapshot = MagicMock(
            return_value=_make_snapshot(weekly_commits=wc)
        )
        detector = SignalDetector(
            mock_journal,
            tmp_path / "intel.db",
            config={"github_monitoring": {"velocity_change_threshold": 0.5}},
            repo_store=mock_repo_store,
        )
        signals = detector._detect_repo_velocity_change()
        assert len(signals) == 1
        assert "decreased" in signals[0].detail

    def test_velocity_increase_fires(self, tmp_path, mock_journal, mock_repo_store):
        wc = [2, 2, 2, 2, 2, 2, 2, 2, 10, 10, 10, 10]
        mock_repo_store.get_latest_snapshot = MagicMock(
            return_value=_make_snapshot(weekly_commits=wc)
        )
        detector = SignalDetector(
            mock_journal,
            tmp_path / "intel.db",
            config={"github_monitoring": {"velocity_change_threshold": 0.5}},
            repo_store=mock_repo_store,
        )
        signals = detector._detect_repo_velocity_change()
        assert len(signals) == 1
        assert "increased" in signals[0].detail

    def test_steady_no_signal(self, tmp_path, mock_journal, mock_repo_store):
        wc = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
        mock_repo_store.get_latest_snapshot = MagicMock(
            return_value=_make_snapshot(weekly_commits=wc)
        )
        detector = SignalDetector(
            mock_journal,
            tmp_path / "intel.db",
            config={"github_monitoring": {"velocity_change_threshold": 0.5}},
            repo_store=mock_repo_store,
        )
        signals = detector._detect_repo_velocity_change()
        assert len(signals) == 0


class TestRepoIssueSpikeDetector:
    def test_issue_spike_fires(self, tmp_path, mock_journal, mock_repo_store):
        current = _make_snapshot(open_issues=20)
        previous = _make_snapshot(open_issues=5)
        mock_repo_store.get_snapshot_history = MagicMock(return_value=[current, previous])
        detector = SignalDetector(
            mock_journal,
            tmp_path / "intel.db",
            config={"github_monitoring": {}},
            repo_store=mock_repo_store,
        )
        signals = detector._detect_repo_issue_spike()
        assert len(signals) == 1
        assert signals[0].type == SignalType.REPO_ISSUE_SPIKE

    def test_no_spike(self, tmp_path, mock_journal, mock_repo_store):
        current = _make_snapshot(open_issues=6)
        previous = _make_snapshot(open_issues=5)
        mock_repo_store.get_snapshot_history = MagicMock(return_value=[current, previous])
        detector = SignalDetector(
            mock_journal,
            tmp_path / "intel.db",
            config={"github_monitoring": {}},
            repo_store=mock_repo_store,
        )
        signals = detector._detect_repo_issue_spike()
        assert len(signals) == 0


class TestRepoCIFailureDetector:
    def test_ci_failure_fires(self, tmp_path, mock_journal, mock_repo_store):
        mock_repo_store.get_latest_snapshot = MagicMock(
            return_value=_make_snapshot(ci_status="failure")
        )
        detector = SignalDetector(
            mock_journal,
            tmp_path / "intel.db",
            config={"github_monitoring": {}},
            repo_store=mock_repo_store,
        )
        signals = detector._detect_repo_ci_failure()
        assert len(signals) == 1
        assert signals[0].type == SignalType.REPO_CI_FAILURE

    def test_ci_success_no_signal(self, tmp_path, mock_journal, mock_repo_store):
        mock_repo_store.get_latest_snapshot = MagicMock(
            return_value=_make_snapshot(ci_status="success")
        )
        detector = SignalDetector(
            mock_journal,
            tmp_path / "intel.db",
            config={"github_monitoring": {}},
            repo_store=mock_repo_store,
        )
        signals = detector._detect_repo_ci_failure()
        assert len(signals) == 0

    def test_ci_failure_goal_linked_severity(self, tmp_path, mock_journal, mock_repo_store):
        mock_repo_store.list_repos = MagicMock(return_value=[_make_repo(goal="goals/app.md")])
        mock_repo_store.get_latest_snapshot = MagicMock(
            return_value=_make_snapshot(ci_status="failure")
        )
        detector = SignalDetector(
            mock_journal,
            tmp_path / "intel.db",
            config={"github_monitoring": {}},
            repo_store=mock_repo_store,
        )
        signals = detector._detect_repo_ci_failure()
        assert signals[0].severity == 7  # goal-linked higher


class TestDetectAllWithRepoStore:
    def test_repo_detectors_included(self, tmp_path, mock_journal, mock_repo_store):
        mock_repo_store.get_latest_snapshot = MagicMock(
            return_value=_make_snapshot(ci_status="failure")
        )
        mock_repo_store.get_snapshot_history = MagicMock(return_value=[])
        detector = SignalDetector(
            mock_journal,
            tmp_path / "intel.db",
            config={"github_monitoring": {}},
            repo_store=mock_repo_store,
        )
        signals = detector.detect_all()
        repo_signals = [s for s in signals if s.type.value.startswith("repo_")]
        assert len(repo_signals) >= 1

    def test_no_repo_store_no_repo_signals(self, tmp_path, mock_journal):
        detector = SignalDetector(mock_journal, tmp_path / "intel.db", config={}, repo_store=None)
        signals = detector.detect_all()
        repo_signals = [s for s in signals if s.type.value.startswith("repo_")]
        assert len(repo_signals) == 0
