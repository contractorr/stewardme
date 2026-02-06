"""Tests for goal milestone tracking."""

import pytest
import frontmatter

from advisor.goals import GoalTracker, get_goal_defaults


class TestGoalMilestones:
    """Test milestone CRUD and progress calculation."""

    def _create_goal(self, temp_dirs):
        """Helper to create a goal with storage."""
        from journal.storage import JournalStorage
        storage = JournalStorage(temp_dirs["journal_dir"])
        tracker = GoalTracker(storage)
        path = storage.create(
            content="Learn Kubernetes",
            entry_type="goal",
            title="K8s Goal",
            metadata=get_goal_defaults(),
        )
        return storage, tracker, path

    def test_add_milestone(self, temp_dirs):
        """Add milestone to goal."""
        storage, tracker, path = self._create_goal(temp_dirs)
        assert tracker.add_milestone(path, "Complete pods tutorial")

        post = frontmatter.load(path)
        assert len(post.metadata["milestones"]) == 1
        assert post.metadata["milestones"][0]["title"] == "Complete pods tutorial"
        assert post.metadata["milestones"][0]["completed"] is False

    def test_complete_milestone(self, temp_dirs):
        """Complete a milestone updates status and progress."""
        storage, tracker, path = self._create_goal(temp_dirs)
        tracker.add_milestone(path, "Step 1")
        tracker.add_milestone(path, "Step 2")

        assert tracker.complete_milestone(path, 0)

        post = frontmatter.load(path)
        assert post.metadata["milestones"][0]["completed"] is True
        assert post.metadata["milestones"][0]["completed_at"] is not None
        assert post.metadata["progress"] == 50

    def test_complete_invalid_index(self, temp_dirs):
        """Invalid index returns False."""
        storage, tracker, path = self._create_goal(temp_dirs)
        tracker.add_milestone(path, "Step 1")
        assert not tracker.complete_milestone(path, 5)
        assert not tracker.complete_milestone(path, -1)

    def test_get_progress(self, temp_dirs):
        """Progress calculation is correct."""
        storage, tracker, path = self._create_goal(temp_dirs)
        tracker.add_milestone(path, "A")
        tracker.add_milestone(path, "B")
        tracker.add_milestone(path, "C")
        tracker.complete_milestone(path, 0)

        progress = tracker.get_progress(path)
        assert progress["percent"] == 33
        assert progress["completed"] == 1
        assert progress["total"] == 3

    def test_progress_no_milestones(self, temp_dirs):
        """No milestones returns 0%."""
        storage, tracker, path = self._create_goal(temp_dirs)
        progress = tracker.get_progress(path)
        assert progress["percent"] == 0
        assert progress["total"] == 0

    def test_all_milestones_complete(self, temp_dirs):
        """All complete = 100%."""
        storage, tracker, path = self._create_goal(temp_dirs)
        tracker.add_milestone(path, "Only step")
        tracker.complete_milestone(path, 0)
        progress = tracker.get_progress(path)
        assert progress["percent"] == 100

    def test_frontmatter_compat(self, temp_dirs):
        """Milestones coexist with existing frontmatter."""
        storage, tracker, path = self._create_goal(temp_dirs)
        tracker.add_milestone(path, "Test")

        # Verify other metadata preserved
        post = frontmatter.load(path)
        assert post.metadata.get("status") == "active"
        assert "milestones" in post.metadata
