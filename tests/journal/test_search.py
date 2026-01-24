"""Tests for journal search operations."""

import pytest


class TestJournalSearch:
    """Test JournalSearch semantic and keyword search."""

    def test_init_with_storage(self, populated_journal, temp_dirs):
        """Test initialization with journal storage."""
        from journal.search import JournalSearch
        from journal.embeddings import EmbeddingManager

        embeddings = EmbeddingManager(temp_dirs["chroma_dir"])
        search = JournalSearch(
            storage=populated_journal["storage"],
            embedding_manager=embeddings,
        )

        assert search.storage is not None
        assert search.embeddings is not None

    def test_semantic_search(self, populated_journal, temp_dirs):
        """Test semantic search returns relevant results."""
        from journal.search import JournalSearch
        from journal.embeddings import EmbeddingManager

        embeddings = EmbeddingManager(temp_dirs["chroma_dir"])
        search = JournalSearch(
            storage=populated_journal["storage"],
            embedding_manager=embeddings,
        )

        # Sync embeddings first
        search.sync_embeddings()

        results = search.semantic_search("AI and programming")

        assert len(results) >= 1

    def test_keyword_search(self, populated_journal, temp_dirs):
        """Test keyword search finds matching entries."""
        from journal.search import JournalSearch

        search = JournalSearch(
            storage=populated_journal["storage"],
            embedding_manager=None,
        )

        results = search.keyword_search("Rust")

        assert len(results) >= 1
        assert any("Rust" in r.get("content", "") or "Rust" in r.get("title", "") for r in results)

    def test_keyword_search_no_results(self, populated_journal, temp_dirs):
        """Test keyword search with no matches."""
        from journal.search import JournalSearch

        search = JournalSearch(
            storage=populated_journal["storage"],
            embedding_manager=None,
        )

        results = search.keyword_search("xyznonexistent123")

        assert len(results) == 0

    def test_get_context_for_query(self, populated_journal, temp_dirs):
        """Test getting formatted context for RAG."""
        from journal.search import JournalSearch
        from journal.embeddings import EmbeddingManager

        embeddings = EmbeddingManager(temp_dirs["chroma_dir"])
        search = JournalSearch(
            storage=populated_journal["storage"],
            embedding_manager=embeddings,
        )
        search.sync_embeddings()

        context = search.get_context_for_query("career and goals")

        assert isinstance(context, str)
        assert len(context) > 0

    def test_context_respects_char_limit(self, populated_journal, temp_dirs):
        """Test that context respects character limit."""
        from journal.search import JournalSearch

        search = JournalSearch(
            storage=populated_journal["storage"],
            embedding_manager=None,
        )

        context = search.get_context_for_query("test", max_chars=100)

        assert len(context) <= 150  # Some buffer for formatting

    def test_sync_embeddings(self, populated_journal, temp_dirs):
        """Test syncing embeddings from storage."""
        from journal.search import JournalSearch
        from journal.embeddings import EmbeddingManager

        embeddings = EmbeddingManager(temp_dirs["chroma_dir"])
        search = JournalSearch(
            storage=populated_journal["storage"],
            embedding_manager=embeddings,
        )

        added, removed = search.sync_embeddings()

        assert added >= 3  # Our sample entries
        assert embeddings.count() >= 3

    def test_fallback_to_keyword_without_embeddings(self, populated_journal):
        """Test that search falls back to keyword without embeddings."""
        from journal.search import JournalSearch

        search = JournalSearch(
            storage=populated_journal["storage"],
            embedding_manager=None,
        )

        # Should not raise, falls back to keyword search
        results = search.semantic_search("programming")

        assert isinstance(results, list)
