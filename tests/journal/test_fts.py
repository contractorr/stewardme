"""Tests for journal FTS5 full-text search."""

import sqlite3


class TestJournalFTSIndex:
    """Unit tests for JournalFTSIndex."""

    def test_init_creates_db(self, tmp_path):
        from journal.fts import JournalFTSIndex

        journal_dir = tmp_path / "journal"
        journal_dir.mkdir()
        idx = JournalFTSIndex(journal_dir)

        assert idx.db_path.exists()
        # Verify FTS table exists
        with sqlite3.connect(str(idx.db_path)) as conn:
            tables = [
                r[0]
                for r in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                ).fetchall()
            ]
            assert "journal_fts" in tables
            assert "journal_fts_meta" in tables

    def test_upsert_and_search(self, tmp_path):
        from journal.fts import JournalFTSIndex

        journal_dir = tmp_path / "journal"
        journal_dir.mkdir()
        idx = JournalFTSIndex(journal_dir)

        idx.upsert(
            "/fake/path.md",
            "Rust Programming",
            "reflection",
            "Learning Rust ownership model",
            "rust, programming",
            1.0,
        )

        results = idx.search("rust")
        assert len(results) == 1
        assert results[0]["title"] == "Rust Programming"

    def test_search_empty_query(self, tmp_path):
        from journal.fts import JournalFTSIndex

        journal_dir = tmp_path / "journal"
        journal_dir.mkdir()
        idx = JournalFTSIndex(journal_dir)

        results = idx.search("")
        assert results == []

    def test_search_no_matches(self, tmp_path):
        from journal.fts import JournalFTSIndex

        journal_dir = tmp_path / "journal"
        journal_dir.mkdir()
        idx = JournalFTSIndex(journal_dir)

        idx.upsert("/fake/a.md", "Python Tips", "note", "Python tricks", "python", 1.0)

        results = idx.search("nonexistent_xyzzy")
        assert results == []

    def test_bm25_rank_is_negative(self, tmp_path):
        """BM25 scores from FTS5 are negative (lower = better match)."""
        from journal.fts import JournalFTSIndex

        journal_dir = tmp_path / "journal"
        journal_dir.mkdir()
        idx = JournalFTSIndex(journal_dir)

        idx.upsert("/a.md", "Rust", "note", "Rust Rust Rust", "rust", 1.0)
        results = idx.search("rust")
        assert len(results) == 1
        assert results[0]["rank"] < 0

    def test_stemming(self, tmp_path):
        """Porter stemmer: 'testing' matches 'test*'."""
        from journal.fts import JournalFTSIndex

        journal_dir = tmp_path / "journal"
        journal_dir.mkdir()
        idx = JournalFTSIndex(journal_dir)

        idx.upsert("/a.md", "Testing Guide", "note", "Testing best practices", "testing", 1.0)

        results = idx.search("test")
        assert len(results) >= 1

    def test_prefix_matching(self, tmp_path):
        """Prefix matching: 'prog*' matches 'programming'."""
        from journal.fts import JournalFTSIndex

        journal_dir = tmp_path / "journal"
        journal_dir.mkdir()
        idx = JournalFTSIndex(journal_dir)

        idx.upsert("/a.md", "Programming", "note", "programming in Python", "python", 1.0)

        results = idx.search("prog")
        assert len(results) >= 1

    def test_delete(self, tmp_path):
        from journal.fts import JournalFTSIndex

        journal_dir = tmp_path / "journal"
        journal_dir.mkdir()
        idx = JournalFTSIndex(journal_dir)

        idx.upsert("/a.md", "To Delete", "note", "content", "", 1.0)
        assert len(idx.search("delete")) == 1

        idx.delete("/a.md")
        assert len(idx.search("delete")) == 0

    def test_upsert_replaces_old_row(self, tmp_path):
        from journal.fts import JournalFTSIndex

        journal_dir = tmp_path / "journal"
        journal_dir.mkdir()
        idx = JournalFTSIndex(journal_dir)

        idx.upsert("/a.md", "Old Title", "note", "old content", "", 1.0)
        idx.upsert("/a.md", "New Title", "note", "new content", "", 2.0)

        results = idx.search("new")
        assert len(results) == 1
        assert results[0]["title"] == "New Title"

        results = idx.search("old")
        assert len(results) == 0

    def test_entry_type_filter(self, tmp_path):
        from journal.fts import JournalFTSIndex

        journal_dir = tmp_path / "journal"
        journal_dir.mkdir()
        idx = JournalFTSIndex(journal_dir)

        idx.upsert("/a.md", "Goal Entry", "goal", "learn rust", "rust", 1.0)
        idx.upsert("/b.md", "Note Entry", "note", "learn rust too", "rust", 1.0)

        all_results = idx.search("rust")
        assert len(all_results) == 2

        goals_only = idx.search("rust", entry_type="goal")
        assert len(goals_only) == 1
        assert goals_only[0]["entry_type"] == "goal"

    def test_to_fts5_query(self):
        from journal.fts import JournalFTSIndex

        assert JournalFTSIndex._to_fts5_query("rust programming") == "rust* programming*"
        assert JournalFTSIndex._to_fts5_query("") == ""
        assert JournalFTSIndex._to_fts5_query("AI") == "ai*"

    def test_sync_from_storage(self, populated_journal, tmp_path):
        """sync_from_storage indexes entries from JournalStorage.get_all_content()."""
        from journal.fts import JournalFTSIndex

        storage = populated_journal["storage"]
        entries = storage.get_all_content()

        journal_dir = tmp_path / "fts_journal"
        journal_dir.mkdir()
        idx = JournalFTSIndex(journal_dir)

        updated, deleted = idx.sync_from_storage(entries)
        assert updated >= 3  # sample entries
        assert deleted == 0

        # Second sync should be no-op (unchanged mtime)
        updated2, deleted2 = idx.sync_from_storage(entries)
        assert updated2 == 0
        assert deleted2 == 0

    def test_sync_removes_deleted_files(self, populated_journal, tmp_path):
        """sync_from_storage removes entries for files no longer on disk."""
        from journal.fts import JournalFTSIndex

        storage = populated_journal["storage"]
        entries = storage.get_all_content()

        journal_dir = tmp_path / "fts_journal2"
        journal_dir.mkdir()
        idx = JournalFTSIndex(journal_dir)

        idx.sync_from_storage(entries)

        # Remove one entry from the list (simulating file deletion)
        reduced = entries[1:]
        updated, deleted = idx.sync_from_storage(reduced)
        assert deleted == 1


class TestJournalSearchFTSIntegration:
    """Integration: JournalSearch.keyword_search routes through FTS."""

    def test_keyword_search_uses_fts(self, populated_journal, tmp_path):
        from journal.fts import JournalFTSIndex
        from journal.search import JournalSearch

        storage = populated_journal["storage"]
        idx = JournalFTSIndex(storage.journal_dir)

        search = JournalSearch(storage, embeddings=None, fts_index=idx)

        # Sync FTS
        entries = storage.get_all_content()
        idx.sync_from_storage(entries)

        results = search.keyword_search("Rust")
        assert len(results) >= 1
        assert any("Rust" in r.get("content", "") or "Rust" in r.get("title", "") for r in results)

    def test_keyword_search_fallback_without_fts(self, populated_journal):
        """Without FTS index, falls back to in-memory scan."""
        from journal.search import JournalSearch

        storage = populated_journal["storage"]
        search = JournalSearch(storage, embeddings=None, fts_index=None)

        results = search.keyword_search("Rust")
        assert len(results) >= 1

    def test_hybrid_search_with_fts(self, populated_journal, temp_dirs):
        """hybrid_search works when FTS is wired in."""
        from journal.embeddings import EmbeddingManager
        from journal.fts import JournalFTSIndex
        from journal.search import JournalSearch

        storage = populated_journal["storage"]
        embeddings = EmbeddingManager(temp_dirs["chroma_dir"])
        idx = JournalFTSIndex(storage.journal_dir)

        search = JournalSearch(storage, embeddings, fts_index=idx)

        # Sync both
        entries = storage.get_all_content()
        idx.sync_from_storage(entries)
        search.sync_embeddings()

        results = search.hybrid_search("Rust programming")
        assert len(results) >= 1
