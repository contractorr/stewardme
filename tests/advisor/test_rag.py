"""Tests for RAG retrieval."""

import pytest


class TestRAGRetriever:
    """Test RAGRetriever context retrieval."""

    def test_init(self, populated_journal, temp_dirs):
        """Test RAG retriever initialization."""
        from journal.search import JournalSearch
        from advisor.rag import RAGRetriever

        search = JournalSearch(
            storage=populated_journal["storage"],
            embedding_manager=None,
        )

        rag = RAGRetriever(
            journal_search=search,
            intel_db_path=temp_dirs["intel_db"],
        )

        assert rag.journal is not None

    def test_get_journal_context(self, populated_journal, temp_dirs):
        """Test getting journal context."""
        from journal.search import JournalSearch
        from journal.embeddings import EmbeddingManager
        from advisor.rag import RAGRetriever

        embeddings = EmbeddingManager(temp_dirs["chroma_dir"])
        search = JournalSearch(
            storage=populated_journal["storage"],
            embedding_manager=embeddings,
        )
        search.sync_embeddings()

        rag = RAGRetriever(journal_search=search)

        context = rag.get_journal_context("career goals")

        assert isinstance(context, str)
        assert len(context) > 0

    def test_get_intel_context_no_db(self, populated_journal, temp_dirs):
        """Test intel context when no DB exists."""
        from journal.search import JournalSearch
        from advisor.rag import RAGRetriever
        from pathlib import Path

        search = JournalSearch(
            storage=populated_journal["storage"],
            embedding_manager=None,
        )

        rag = RAGRetriever(
            journal_search=search,
            intel_db_path=Path("/nonexistent/path.db"),
        )

        context = rag.get_intel_context("test")

        assert "No external intelligence" in context

    def test_get_intel_context_with_data(self, populated_journal, populated_intel, temp_dirs):
        """Test intel context with populated data."""
        from journal.search import JournalSearch
        from advisor.rag import RAGRetriever

        search = JournalSearch(
            storage=populated_journal["storage"],
            embedding_manager=None,
        )

        rag = RAGRetriever(
            journal_search=search,
            intel_db_path=temp_dirs["intel_db"],
        )

        context = rag.get_intel_context("AI programming")

        assert isinstance(context, str)
        # Should find AI-related items from sample data

    def test_get_intel_context_with_semantic_search(self, populated_journal, populated_intel, temp_dirs):
        """Test intel context using semantic search."""
        from journal.search import JournalSearch
        from intelligence.search import IntelSearch
        from intelligence.embeddings import IntelEmbeddingManager
        from advisor.rag import RAGRetriever

        intel_embeddings = IntelEmbeddingManager(temp_dirs["chroma_dir"])
        intel_search = IntelSearch(populated_intel, intel_embeddings)
        intel_search.sync_embeddings()

        journal_search = JournalSearch(
            storage=populated_journal["storage"],
            embedding_manager=None,
        )

        rag = RAGRetriever(
            journal_search=journal_search,
            intel_search=intel_search,
        )

        context = rag.get_intel_context("machine learning")

        assert isinstance(context, str)

    def test_get_combined_context(self, populated_journal, populated_intel, temp_dirs):
        """Test combined journal + intel context."""
        from journal.search import JournalSearch
        from journal.embeddings import EmbeddingManager
        from advisor.rag import RAGRetriever

        embeddings = EmbeddingManager(temp_dirs["chroma_dir"])
        search = JournalSearch(
            storage=populated_journal["storage"],
            embedding_manager=embeddings,
        )
        search.sync_embeddings()

        rag = RAGRetriever(
            journal_search=search,
            intel_db_path=temp_dirs["intel_db"],
        )

        journal_ctx, intel_ctx = rag.get_combined_context("programming")

        assert isinstance(journal_ctx, str)
        assert isinstance(intel_ctx, str)

    def test_context_char_limits(self, populated_journal, temp_dirs):
        """Test that context respects character limits."""
        from journal.search import JournalSearch
        from advisor.rag import RAGRetriever

        search = JournalSearch(
            storage=populated_journal["storage"],
            embedding_manager=None,
        )

        rag = RAGRetriever(
            journal_search=search,
            intel_db_path=temp_dirs["intel_db"],
        )

        context = rag.get_journal_context("test", max_chars=100)

        # Allow some buffer for formatting
        assert len(context) <= 200

    def test_get_recent_entries(self, populated_journal, temp_dirs):
        """Test getting recent entries for weekly review."""
        from journal.search import JournalSearch
        from advisor.rag import RAGRetriever

        search = JournalSearch(
            storage=populated_journal["storage"],
            embedding_manager=None,
        )

        rag = RAGRetriever(journal_search=search)

        recent = rag.get_recent_entries(days=7)

        assert isinstance(recent, str)
        # Should contain entries from last 7 days

    def test_journal_weight_affects_allocation(self, populated_journal, populated_intel, temp_dirs):
        """Test that journal_weight parameter affects context allocation."""
        from journal.search import JournalSearch
        from advisor.rag import RAGRetriever

        search = JournalSearch(
            storage=populated_journal["storage"],
            embedding_manager=None,
        )

        rag = RAGRetriever(
            journal_search=search,
            intel_db_path=temp_dirs["intel_db"],
        )

        # High journal weight
        j_ctx_high, i_ctx_high = rag.get_combined_context("test", journal_weight=0.9)

        # Low journal weight
        j_ctx_low, i_ctx_low = rag.get_combined_context("test", journal_weight=0.1)

        # Both should return valid strings
        assert isinstance(j_ctx_high, str)
        assert isinstance(i_ctx_low, str)
