"""Tests for journal embeddings operations."""



class TestEmbeddingManager:
    """Test EmbeddingManager vector operations."""

    def test_init_creates_collection(self, temp_dirs):
        """Test that initialization creates ChromaDB collection."""
        from journal.embeddings import EmbeddingManager

        manager = EmbeddingManager(temp_dirs["chroma_dir"])

        assert manager.collection is not None
        assert manager.count() >= 0

    def test_add_entry(self, temp_dirs):
        """Test adding an entry to vector store."""
        from journal.embeddings import EmbeddingManager

        manager = EmbeddingManager(temp_dirs["chroma_dir"])
        initial_count = manager.count()

        manager.add_entry(
            entry_id="test-1",
            content="This is a test entry about programming.",
            metadata={"type": "note"},
        )

        assert manager.count() == initial_count + 1

    def test_add_entry_upsert(self, temp_dirs):
        """Test that add_entry upserts existing entries."""
        from journal.embeddings import EmbeddingManager

        manager = EmbeddingManager(temp_dirs["chroma_dir"])

        manager.add_entry("test-1", "Original content")
        count_after_add = manager.count()

        manager.add_entry("test-1", "Updated content")

        assert manager.count() == count_after_add  # No duplicate

    def test_remove_entry(self, temp_dirs):
        """Test removing an entry from vector store."""
        from journal.embeddings import EmbeddingManager

        manager = EmbeddingManager(temp_dirs["chroma_dir"])

        manager.add_entry("test-remove", "Content to remove")
        count_after_add = manager.count()

        manager.remove_entry("test-remove")

        assert manager.count() == count_after_add - 1

    def test_remove_nonexistent_no_error(self, temp_dirs):
        """Test that removing non-existent entry doesn't raise."""
        from journal.embeddings import EmbeddingManager

        manager = EmbeddingManager(temp_dirs["chroma_dir"])

        # Should not raise
        manager.remove_entry("nonexistent-id")

    def test_query_returns_results(self, temp_dirs):
        """Test querying returns relevant results."""
        from journal.embeddings import EmbeddingManager

        manager = EmbeddingManager(temp_dirs["chroma_dir"])

        manager.add_entry("prog-1", "Python programming is fun and powerful.")
        manager.add_entry("cooking-1", "Baking bread requires patience and flour.")

        results = manager.query("coding in python", n_results=2)

        assert len(results) >= 1
        assert results[0]["id"] == "prog-1"  # Programming entry should rank higher

    def test_query_with_filter(self, temp_dirs):
        """Test querying with metadata filter."""
        from journal.embeddings import EmbeddingManager

        manager = EmbeddingManager(temp_dirs["chroma_dir"])

        manager.add_entry("note-1", "A note about work", {"type": "note"})
        manager.add_entry("goal-1", "A goal about work", {"type": "goal"})

        results = manager.query("work", n_results=5, where={"type": "goal"})

        for result in results:
            if result["metadata"]:
                assert result["metadata"].get("type") == "goal"

    def test_sync_from_storage(self, temp_dirs):
        """Test syncing from storage entries."""
        from journal.embeddings import EmbeddingManager

        manager = EmbeddingManager(temp_dirs["chroma_dir"])

        entries = [
            {"id": "sync-1", "content": "First synced entry"},
            {"id": "sync-2", "content": "Second synced entry"},
        ]

        added, removed = manager.sync_from_storage(entries)

        assert added == 2
        assert manager.count() >= 2

    def test_sync_removes_deleted(self, temp_dirs):
        """Test that sync removes entries not in storage."""
        from journal.embeddings import EmbeddingManager

        manager = EmbeddingManager(temp_dirs["chroma_dir"])

        # Add initial entries
        manager.add_entry("keep-1", "Keep this")
        manager.add_entry("delete-1", "Delete this")

        # Sync with only one entry
        added, removed = manager.sync_from_storage([
            {"id": "keep-1", "content": "Keep this"},
        ])

        assert removed == 1
