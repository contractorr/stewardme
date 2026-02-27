"""Tests for memory data models."""

from datetime import datetime

from memory.models import FactCategory, FactSource, FactUpdate, StewardFact


class TestFactCategory:
    def test_values(self):
        assert FactCategory.PREFERENCE == "preference"
        assert FactCategory.SKILL == "skill"
        assert FactCategory.CONSTRAINT == "constraint"
        assert FactCategory.PATTERN == "pattern"
        assert FactCategory.CONTEXT == "context"
        assert FactCategory.GOAL_CONTEXT == "goal_context"

    def test_from_string(self):
        assert FactCategory("preference") == FactCategory.PREFERENCE


class TestFactSource:
    def test_values(self):
        assert FactSource.JOURNAL == "journal"
        assert FactSource.FEEDBACK == "feedback"
        assert FactSource.GOAL == "goal"


class TestStewardFact:
    def test_create(self):
        f = StewardFact(
            id="abc123",
            text="User prefers Python",
            category=FactCategory.PREFERENCE,
            source_type=FactSource.JOURNAL,
            source_id="entry-1",
        )
        assert f.id == "abc123"
        assert f.confidence == 0.8
        assert f.superseded_by is None

    def test_defaults(self):
        f = StewardFact(
            id="x",
            text="test",
            category=FactCategory.SKILL,
            source_type=FactSource.PROFILE,
            source_id="p1",
        )
        assert isinstance(f.created_at, datetime)
        assert isinstance(f.updated_at, datetime)


class TestFactUpdate:
    def test_add(self):
        u = FactUpdate(action="ADD", candidate="User likes Rust")
        assert u.action == "ADD"
        assert u.existing_id is None

    def test_update(self):
        u = FactUpdate(
            action="UPDATE", candidate="new text", existing_id="old-id", reasoning="changed"
        )
        assert u.existing_id == "old-id"
