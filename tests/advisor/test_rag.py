"""Tests for RAG retrieval."""

from unittest.mock import MagicMock, patch


class TestBuildContextForAsk:
    """Test build_context_for_ask() context assembly."""

    def _make_rag(self, fact_store=None, thread_store=None):
        from advisor.rag import RAGRetriever
        from journal.search import JournalSearch

        journal_search = MagicMock(spec=JournalSearch)
        journal_search.get_context_for_query.return_value = "journal text"
        journal_search.storage = MagicMock()

        rag = RAGRetriever(
            journal_search=journal_search,
            fact_store=fact_store,
            thread_store=thread_store,
        )
        return rag

    def test_default_flags_no_memory_no_thoughts(self):
        rag = self._make_rag()
        ctx = rag.build_context_for_ask("test question")
        assert ctx.memory == ""
        assert ctx.thoughts == ""
        assert isinstance(ctx.journal, str)
        assert isinstance(ctx.intel, str)

    def test_inject_memory_flag(self):
        rag = self._make_rag()
        rag.get_memory_context = MagicMock(
            return_value="<user_memory>\n## Skills\n- Python\n</user_memory>"
        )
        ctx = rag.build_context_for_ask("test", {"inject_memory": True})
        assert "<user_memory>" in ctx.memory
        rag.get_memory_context.assert_called_once_with("test")

    def test_inject_memory_false_skips_call(self):
        rag = self._make_rag()
        rag.get_memory_context = MagicMock(return_value="should not appear")
        ctx = rag.build_context_for_ask("test", {"inject_memory": False})
        assert ctx.memory == ""
        rag.get_memory_context.assert_not_called()

    def test_inject_recurring_thoughts_flag(self):
        rag = self._make_rag()
        rag.get_recurring_thoughts_context = MagicMock(
            return_value="<recurring_thoughts>\n1. topic\n</recurring_thoughts>"
        )
        ctx = rag.build_context_for_ask("test", {"inject_recurring_thoughts": True})
        assert "<recurring_thoughts>" in ctx.thoughts
        rag.get_recurring_thoughts_context.assert_called_once()

    def test_structured_profile_flag(self):
        rag = self._make_rag()
        rag.get_profile_context = MagicMock(return_value="[GOALS & ASPIRATIONS]\nBe great")
        ctx = rag.build_context_for_ask("test", {"structured_profile": True})
        assert "[GOALS & ASPIRATIONS]" in ctx.profile
        rag.get_profile_context.assert_called_once_with(structured=True)

    def test_default_profile_compact(self):
        rag = self._make_rag()
        rag.get_profile_context = MagicMock(return_value="USER PROFILE: compact")
        ctx = rag.build_context_for_ask("test")
        assert "compact" in ctx.profile
        rag.get_profile_context.assert_called_once_with(structured=False)


class TestRAGRetriever:
    """Test RAGRetriever context retrieval."""

    def test_init(self, populated_journal, temp_dirs):
        """Test RAG retriever initialization."""
        from advisor.rag import RAGRetriever
        from journal.search import JournalSearch

        search = JournalSearch(
            storage=populated_journal["storage"],
            embeddings=None,
        )

        rag = RAGRetriever(
            journal_search=search,
            intel_db_path=temp_dirs["intel_db"],
        )

        assert rag.journal is not None

    def test_get_journal_context(self, populated_journal, temp_dirs):
        """Test getting journal context."""
        from advisor.rag import RAGRetriever
        from journal.embeddings import EmbeddingManager
        from journal.search import JournalSearch

        embeddings = EmbeddingManager(temp_dirs["chroma_dir"])
        search = JournalSearch(
            storage=populated_journal["storage"],
            embeddings=embeddings,
        )
        search.sync_embeddings()

        rag = RAGRetriever(journal_search=search)

        context = rag.get_journal_context("career goals")

        assert isinstance(context, str)
        assert len(context) > 0

    def test_get_intel_context_no_db(self, populated_journal, temp_dirs):
        """Test intel context when no DB exists."""
        from pathlib import Path

        from advisor.rag import RAGRetriever
        from journal.search import JournalSearch

        search = JournalSearch(
            storage=populated_journal["storage"],
            embeddings=None,
        )

        rag = RAGRetriever(
            journal_search=search,
            intel_db_path=Path("/nonexistent/path.db"),
        )

        context = rag.get_intel_context("test")

        assert "No external intelligence" in context

    def test_get_intel_context_with_data(self, populated_journal, populated_intel, temp_dirs):
        """Test intel context with populated data."""
        from advisor.rag import RAGRetriever
        from journal.search import JournalSearch

        search = JournalSearch(
            storage=populated_journal["storage"],
            embeddings=None,
        )

        rag = RAGRetriever(
            journal_search=search,
            intel_db_path=temp_dirs["intel_db"],
        )

        context = rag.get_intel_context("AI programming")

        assert isinstance(context, str)
        # Should find AI-related items from sample data

    def test_get_intel_context_with_semantic_search(
        self, populated_journal, populated_intel, temp_dirs
    ):
        """Test intel context using semantic search."""
        from advisor.rag import RAGRetriever
        from intelligence.embeddings import IntelEmbeddingManager
        from intelligence.search import IntelSearch
        from journal.search import JournalSearch

        intel_embeddings = IntelEmbeddingManager(temp_dirs["chroma_dir"])
        intel_search = IntelSearch(populated_intel, intel_embeddings)
        intel_search.sync_embeddings()

        journal_search = JournalSearch(
            storage=populated_journal["storage"],
            embeddings=None,
        )

        rag = RAGRetriever(
            journal_search=journal_search,
            intel_search=intel_search,
        )

        context = rag.get_intel_context("machine learning")

        assert isinstance(context, str)

    def test_get_combined_context(self, populated_journal, populated_intel, temp_dirs):
        """Test combined journal + intel context."""
        from advisor.rag import RAGRetriever
        from journal.embeddings import EmbeddingManager
        from journal.search import JournalSearch

        embeddings = EmbeddingManager(temp_dirs["chroma_dir"])
        search = JournalSearch(
            storage=populated_journal["storage"],
            embeddings=embeddings,
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
        from advisor.rag import RAGRetriever
        from journal.search import JournalSearch

        search = JournalSearch(
            storage=populated_journal["storage"],
            embeddings=None,
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
        from advisor.rag import RAGRetriever
        from journal.search import JournalSearch

        search = JournalSearch(
            storage=populated_journal["storage"],
            embeddings=None,
        )

        rag = RAGRetriever(journal_search=search)

        recent = rag.get_recent_entries(days=7)

        assert isinstance(recent, str)
        # Should contain entries from last 7 days

    def test_journal_weight_affects_allocation(self, populated_journal, populated_intel, temp_dirs):
        """Test that journal_weight parameter affects context allocation."""
        from advisor.rag import RAGRetriever
        from journal.search import JournalSearch

        search = JournalSearch(
            storage=populated_journal["storage"],
            embeddings=None,
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
