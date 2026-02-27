"""Tests for RAGRetriever memory integration."""

from unittest.mock import MagicMock

import pytest

from memory.models import FactCategory, FactSource, StewardFact
from memory.store import FactStore


@pytest.fixture
def store(tmp_path):
    db = tmp_path / "test.db"
    return FactStore(db, chroma_dir=None)


@pytest.fixture
def rag_with_memory(store):
    from advisor.rag import RAGRetriever

    journal_search = MagicMock()
    journal_search.storage = MagicMock()
    return RAGRetriever(
        journal_search=journal_search,
        fact_store=store,
        memory_config={"max_context_facts": 25, "high_confidence_threshold": 0.9},
    )


@pytest.fixture
def rag_without_memory():
    from advisor.rag import RAGRetriever

    journal_search = MagicMock()
    journal_search.storage = MagicMock()
    return RAGRetriever(journal_search=journal_search)


def _fact(store, id, text, category=FactCategory.PREFERENCE, confidence=0.85):
    f = StewardFact(
        id=id,
        text=text,
        category=category,
        source_type=FactSource.JOURNAL,
        source_id="e1",
        confidence=confidence,
    )
    store.add(f)
    return f


class TestMemoryContext:
    def test_memory_block_included(self, rag_with_memory, store):
        _fact(store, "f1", "User prefers Python", FactCategory.PREFERENCE, confidence=0.95)
        _fact(store, "f2", "User knows SQL", FactCategory.SKILL, confidence=0.95)

        ctx = rag_with_memory.get_memory_context("Python")
        assert "<user_memory>" in ctx
        assert "User prefers Python" in ctx
        assert "User knows SQL" in ctx

    def test_high_confidence_always_included(self, rag_with_memory, store):
        _fact(store, "f1", "Core identity fact", FactCategory.CONTEXT, confidence=0.95)
        _fact(store, "f2", "Low confidence fact", FactCategory.CONTEXT, confidence=0.6)

        ctx = rag_with_memory.get_memory_context("unrelated query")
        assert "Core identity fact" in ctx

    def test_max_context_facts_respected(self, store):
        from advisor.rag import RAGRetriever

        journal_search = MagicMock()
        journal_search.storage = MagicMock()
        rag = RAGRetriever(
            journal_search=journal_search,
            fact_store=store,
            memory_config={"max_context_facts": 3, "high_confidence_threshold": 0.9},
        )

        for i in range(10):
            _fact(store, f"f{i}", f"Fact number {i}", confidence=0.8)

        ctx = rag.get_memory_context("test")
        # Count "- " lines (facts)
        fact_lines = [l for l in ctx.split("\n") if l.startswith("- ")]
        assert len(fact_lines) <= 3

    def test_disabled_memory_returns_empty(self, rag_without_memory):
        ctx = rag_without_memory.get_memory_context("test")
        assert ctx == ""

    def test_empty_store_returns_empty(self, rag_with_memory):
        ctx = rag_with_memory.get_memory_context("test")
        assert ctx == ""

    def test_grouped_by_category(self, rag_with_memory, store):
        _fact(store, "f1", "User prefers Python", FactCategory.PREFERENCE, confidence=0.95)
        _fact(store, "f2", "Currently job searching", FactCategory.CONTEXT, confidence=0.95)
        _fact(store, "f3", "User knows Rust", FactCategory.SKILL, confidence=0.95)

        ctx = rag_with_memory.get_memory_context("career")
        assert "## Preferences" in ctx
        assert "## Current Context" in ctx
        assert "## Skills" in ctx
