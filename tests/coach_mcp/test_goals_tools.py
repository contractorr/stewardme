"""Tests for goals MCP tools."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

import coach_mcp.bootstrap


@pytest.fixture
def mock_components(tmp_path):
    journal_dir = tmp_path / "journal"
    journal_dir.mkdir()

    storage = MagicMock()
    storage.journal_dir = journal_dir
    embeddings = MagicMock()

    components = {
        "config": {},
        "config_model": MagicMock(),
        "paths": {"journal_dir": journal_dir},
        "storage": storage,
        "embeddings": embeddings,
        "search": MagicMock(),
        "intel_storage": MagicMock(),
        "intel_search": MagicMock(),
        "rag": MagicMock(),
        "advisor": None,
    }
    coach_mcp.bootstrap._components = components
    yield components


def test_list_goals(mock_components):
    """goals_list should return goals with progress."""
    from coach_mcp.tools.goals import _list_goals

    goal_path = Path("/tmp/journal/goal-test.md")

    with patch("coach_mcp.tools.goals._get_tracker") as mock_get:
        tracker = MagicMock()
        mock_get.return_value = tracker
        tracker.get_goals.return_value = [
            {
                "path": goal_path,
                "title": "Learn Rust",
                "status": "active",
                "created": "2024-01-01",
                "last_checked": "2024-01-10",
                "check_in_days": 14,
                "days_since_check": 5,
                "is_stale": False,
                "tags": ["learning"],
                "content": "Goal content",
            }
        ]
        tracker.get_progress.return_value = {
            "percent": 50,
            "completed": 1,
            "total": 2,
            "milestones": [],
        }

        result = _list_goals({"include_inactive": False})
        assert result["count"] == 1
        assert result["goals"][0]["title"] == "Learn Rust"
        assert result["goals"][0]["progress"]["percent"] == 50


def test_check_in(mock_components):
    """goals_check_in should delegate to tracker."""
    from coach_mcp.tools.goals import _check_in

    with patch("coach_mcp.tools.goals._get_tracker") as mock_get:
        tracker = MagicMock()
        mock_get.return_value = tracker
        tracker.check_in_goal.return_value = True

        result = _check_in({"goal_path": "/tmp/goal.md", "notes": "On track"})
        assert result["success"] is True
        tracker.check_in_goal.assert_called_once_with(Path("/tmp/goal.md"), notes="On track")


def test_update_status(mock_components):
    """goals_update_status should delegate to tracker."""
    from coach_mcp.tools.goals import _update_status

    with patch("coach_mcp.tools.goals._get_tracker") as mock_get:
        tracker = MagicMock()
        mock_get.return_value = tracker
        tracker.update_goal_status.return_value = True

        result = _update_status({"goal_path": "/tmp/goal.md", "status": "completed"})
        assert result["success"] is True
        assert result["status"] == "completed"


def test_add_milestone(mock_components):
    """goals_add_milestone should delegate to tracker and return progress."""
    from coach_mcp.tools.goals import _add_milestone

    with patch("coach_mcp.tools.goals._get_tracker") as mock_get:
        tracker = MagicMock()
        mock_get.return_value = tracker
        tracker.add_milestone.return_value = True
        tracker.get_progress.return_value = {"percent": 0, "completed": 0, "total": 1}

        result = _add_milestone({"goal_path": "/tmp/goal.md", "title": "Chapter 1"})
        assert result["success"] is True
        assert result["progress"]["total"] == 1


def test_complete_milestone(mock_components):
    """goals_complete_milestone should delegate to tracker."""
    from coach_mcp.tools.goals import _complete_milestone

    with patch("coach_mcp.tools.goals._get_tracker") as mock_get:
        tracker = MagicMock()
        mock_get.return_value = tracker
        tracker.complete_milestone.return_value = True
        tracker.get_progress.return_value = {"percent": 100, "completed": 1, "total": 1}

        result = _complete_milestone({"goal_path": "/tmp/goal.md", "milestone_index": 0})
        assert result["success"] is True
        assert result["progress"]["percent"] == 100
