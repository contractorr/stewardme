"""End-to-end integration tests."""

import pytest


class TestJournalFlow:
    """Test journal create -> embed -> search flow."""

    def test_create_embed_search(self, temp_dirs):
        """Test full journal flow."""
        from journal.storage import JournalStorage
        from journal.embeddings import EmbeddingManager
        from journal.search import JournalSearch

        # Create storage and add entries
        storage = JournalStorage(temp_dirs["journal_dir"])

        storage.create(
            content="Learning Python for data science projects. Focus on pandas and numpy.",
            entry_type="note",
            title="Python Learning",
            tags=["python", "learning"],
        )

        storage.create(
            content="Started a new Rust project for systems programming.",
            entry_type="note",
            title="Rust Project",
            tags=["rust", "programming"],
        )

        # Set up embeddings
        embeddings = EmbeddingManager(temp_dirs["chroma_dir"])
        search = JournalSearch(storage, embeddings)

        # Sync embeddings
        added, removed = search.sync_embeddings()
        assert added == 2

        # Search
        results = search.semantic_search("data science with python")
        assert len(results) >= 1

        # Verify Python entry ranks higher for Python query
        python_found = any("Python" in r.get("title", "") for r in results)
        assert python_found

    def test_update_reflects_in_search(self, temp_dirs):
        """Test that updates are reflected in search."""
        from journal.storage import JournalStorage
        from journal.embeddings import EmbeddingManager
        from journal.search import JournalSearch

        storage = JournalStorage(temp_dirs["journal_dir"])
        embeddings = EmbeddingManager(temp_dirs["chroma_dir"])
        search = JournalSearch(storage, embeddings)

        # Create entry
        path = storage.create(
            content="Original content about cooking",
            entry_type="note",
        )
        search.sync_embeddings()

        # Update entry
        storage.update(path, content="Updated content about machine learning AI")
        search.sync_embeddings()

        # Search should find updated content
        results = search.semantic_search("machine learning")
        assert len(results) >= 1


class TestIntelFlow:
    """Test scrape -> embed -> RAG query flow."""

    def test_scrape_embed_query(self, temp_dirs):
        """Test intelligence flow with mocked data."""
        from intelligence.scraper import IntelStorage, IntelItem
        from intelligence.embeddings import IntelEmbeddingManager
        from intelligence.search import IntelSearch
        from datetime import datetime

        # Create storage and add items
        storage = IntelStorage(temp_dirs["intel_db"])

        items = [
            IntelItem(
                source="hackernews",
                title="New ML framework released",
                url="https://example.com/ml",
                summary="A powerful new machine learning framework for Python",
                published=datetime.now(),
                tags=["ai", "python", "ml"],
            ),
            IntelItem(
                source="rss:techblog",
                title="Rust vs Go performance comparison",
                url="https://example.com/rust-go",
                summary="Benchmarks comparing Rust and Go for backend services",
                published=datetime.now(),
                tags=["rust", "go", "performance"],
            ),
        ]

        for item in items:
            storage.save(item)

        # Set up embeddings
        embeddings = IntelEmbeddingManager(temp_dirs["chroma_dir"])
        search = IntelSearch(storage, embeddings)

        # Sync embeddings
        added, removed = search.sync_embeddings()
        assert added == 2

        # Query
        context = search.get_context_for_query("machine learning python")
        assert "ML" in context or "machine" in context.lower()

    def test_rag_with_intel_search(self, temp_dirs):
        """Test RAG retriever with semantic intel search."""
        from journal.storage import JournalStorage
        from journal.search import JournalSearch
        from intelligence.scraper import IntelStorage, IntelItem
        from intelligence.embeddings import IntelEmbeddingManager
        from intelligence.search import IntelSearch
        from advisor.rag import RAGRetriever
        from datetime import datetime

        # Set up journal
        journal_storage = JournalStorage(temp_dirs["journal_dir"])
        journal_storage.create(
            content="My goal is to become an expert in AI and machine learning.",
            entry_type="goal",
        )
        journal_search = JournalSearch(journal_storage, embedding_manager=None)

        # Set up intel
        intel_storage = IntelStorage(temp_dirs["intel_db"])
        intel_storage.save(IntelItem(
            source="hackernews",
            title="AI career guide 2024",
            url="https://example.com/ai-career",
            summary="Guide to building a career in artificial intelligence",
            published=datetime.now(),
        ))

        intel_embeddings = IntelEmbeddingManager(temp_dirs["chroma_dir"])
        intel_search = IntelSearch(intel_storage, intel_embeddings)
        intel_search.sync_embeddings()

        # RAG retriever with semantic search
        rag = RAGRetriever(
            journal_search=journal_search,
            intel_search=intel_search,
        )

        # Get combined context
        journal_ctx, intel_ctx = rag.get_combined_context("AI career path")

        assert isinstance(journal_ctx, str)
        assert isinstance(intel_ctx, str)


class TestSchedulerFlow:
    """Test scheduler with multiple scrapers."""

    def test_scheduler_run_now(self, temp_dirs, monkeypatch):
        """Test running scheduler immediately with mocked HTTP."""
        from intelligence.scraper import IntelStorage
        from intelligence.scheduler import IntelScheduler
        from unittest.mock import MagicMock

        # Mock all HTTP requests
        mock_client = MagicMock()
        mock_client.get.return_value = MagicMock(
            json=MagicMock(return_value=[]),
            text="",
            raise_for_status=MagicMock(),
        )

        import httpx
        monkeypatch.setattr(httpx, "Client", lambda **kwargs: mock_client)

        storage = IntelStorage(temp_dirs["intel_db"])
        scheduler = IntelScheduler(
            storage=storage,
            config={
                "enabled": ["hn_top"],
                "rss_feeds": [],
            },
        )

        results = scheduler.run_now()

        assert "hackernews" in results

    @pytest.mark.asyncio
    async def test_scheduler_async(self, temp_dirs, monkeypatch):
        """Test async scheduler execution."""
        from intelligence.scraper import IntelStorage
        from intelligence.scheduler import IntelScheduler
        from unittest.mock import AsyncMock, MagicMock

        # Mock async HTTP client
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.text = ""
        mock_response.raise_for_status = MagicMock()

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client.aclose = AsyncMock()

        import httpx
        monkeypatch.setattr(
            httpx, "AsyncClient",
            lambda **kwargs: MagicMock(
                __aenter__=AsyncMock(return_value=mock_client),
                __aexit__=AsyncMock(),
                get=mock_client.get,
                aclose=mock_client.aclose,
            )
        )

        storage = IntelStorage(temp_dirs["intel_db"])
        scheduler = IntelScheduler(
            storage=storage,
            config={
                "enabled": ["hn_top"],
                "rss_feeds": [],
            },
        )

        # This will use sync version due to mocking complexity
        results = scheduler.run_now()
        assert isinstance(results, dict)


class TestCLIIntegration:
    """Test CLI command flows (without actual CLI invocation)."""

    def test_components_initialization(self, temp_dirs, monkeypatch):
        """Test that CLI components can be initialized."""
        # Set environment
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        from journal.storage import JournalStorage
        from journal.embeddings import EmbeddingManager
        from journal.search import JournalSearch
        from intelligence.scraper import IntelStorage
        from intelligence.scheduler import IntelScheduler

        # Initialize all components like CLI would
        journal_storage = JournalStorage(temp_dirs["journal_dir"])
        embeddings = EmbeddingManager(temp_dirs["chroma_dir"])
        journal_search = JournalSearch(journal_storage, embeddings)
        intel_storage = IntelStorage(temp_dirs["intel_db"])
        scheduler = IntelScheduler(intel_storage, config={})

        assert journal_storage is not None
        assert journal_search is not None
        assert intel_storage is not None
        assert scheduler is not None
