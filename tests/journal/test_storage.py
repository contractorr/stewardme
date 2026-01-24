"""Tests for journal storage operations."""

import pytest
from datetime import datetime


class TestJournalStorage:
    """Test JournalStorage CRUD operations."""

    def test_create_entry(self, temp_dirs):
        """Test creating a new journal entry."""
        from journal.storage import JournalStorage

        storage = JournalStorage(temp_dirs["journal_dir"])

        path = storage.create(
            content="Test entry content",
            entry_type="reflection",
            title="Test Title",
            tags=["test", "unit"],
        )

        assert path is not None
        assert (temp_dirs["journal_dir"] / path).exists()

    def test_create_generates_filename(self, temp_dirs):
        """Test that create generates proper filename."""
        from journal.storage import JournalStorage

        storage = JournalStorage(temp_dirs["journal_dir"])

        path = storage.create(
            content="Test content",
            entry_type="goal",
        )

        assert "goal" in path.lower() or path.endswith(".md")

    def test_read_entry(self, populated_journal):
        """Test reading an existing entry."""
        storage = populated_journal["storage"]
        path = populated_journal["paths"][0]

        post = storage.read(path)

        assert post is not None
        assert post.content is not None
        assert "reflection" in str(post.metadata.get("type", ""))

    def test_read_nonexistent_returns_none(self, temp_dirs):
        """Test reading non-existent entry returns None."""
        from journal.storage import JournalStorage

        storage = JournalStorage(temp_dirs["journal_dir"])

        post = storage.read("nonexistent.md")

        assert post is None

    def test_update_entry(self, populated_journal):
        """Test updating an existing entry."""
        storage = populated_journal["storage"]
        path = populated_journal["paths"][0]

        result = storage.update(path, content="Updated content")

        assert result is True
        post = storage.read(path)
        assert "Updated content" in post.content

    def test_delete_entry(self, populated_journal):
        """Test deleting an entry."""
        storage = populated_journal["storage"]
        path = populated_journal["paths"][0]

        result = storage.delete(path)

        assert result is True
        post = storage.read(path)
        assert post is None

    def test_list_entries(self, populated_journal):
        """Test listing all entries."""
        storage = populated_journal["storage"]

        entries = storage.list_entries()

        assert len(entries) >= 3  # At least our sample entries

    def test_list_entries_with_limit(self, populated_journal):
        """Test listing with limit."""
        storage = populated_journal["storage"]

        entries = storage.list_entries(limit=1)

        assert len(entries) == 1

    def test_frontmatter_preserved(self, temp_dirs):
        """Test that YAML frontmatter is preserved."""
        from journal.storage import JournalStorage

        storage = JournalStorage(temp_dirs["journal_dir"])

        path = storage.create(
            content="Content with metadata",
            entry_type="insight",
            title="Frontmatter Test",
            tags=["meta", "test"],
        )

        post = storage.read(path)

        assert post.metadata.get("type") == "insight"
        assert post.metadata.get("title") == "Frontmatter Test"
        assert "meta" in post.metadata.get("tags", [])

    def test_duplicate_title_handling(self, temp_dirs):
        """Test that duplicate titles create unique files."""
        from journal.storage import JournalStorage

        storage = JournalStorage(temp_dirs["journal_dir"])

        path1 = storage.create(content="First", entry_type="note", title="Same Title")
        path2 = storage.create(content="Second", entry_type="note", title="Same Title")

        assert path1 != path2
        assert storage.read(path1) is not None
        assert storage.read(path2) is not None

    def test_get_all_content(self, populated_journal):
        """Test getting all content for embedding."""
        storage = populated_journal["storage"]

        entries = storage.get_all_content()

        assert len(entries) >= 3
        for entry in entries:
            assert "id" in entry
            assert "content" in entry
