"""Tests for MemoryRetriever."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from advisor.retrievers.memory import MemoryRetriever
from memory.models import FactCategory, StewardFact


def _make_fact(id, text, category, confidence=0.8):
    return StewardFact(
        id=id,
        text=text,
        category=category,
        source_type="journal",
        source_id="j1",
        confidence=confidence,
    )


class TestGetMemoryContext:
    def test_no_fact_store(self):
        mr = MemoryRetriever()
        assert mr.get_memory_context("q") == ""

    def test_with_facts(self):
        fs = MagicMock()
        fact = _make_fact("f1", "Likes Python", FactCategory.PREFERENCE, 0.95)
        fs.search.return_value = [fact]
        fs.get_all_active.return_value = [fact]
        mr = MemoryRetriever(fact_store=fs, memory_config={"high_confidence_threshold": 0.9})
        result = mr.get_memory_context("coding")
        assert "<user_memory>" in result
        assert "Likes Python" in result

    def test_no_facts_returns_empty(self):
        fs = MagicMock()
        fs.search.return_value = []
        fs.get_all_active.return_value = []
        mr = MemoryRetriever(fact_store=fs)
        assert mr.get_memory_context("q") == ""

    def test_exception_returns_empty(self):
        fs = MagicMock()
        fs.search.side_effect = RuntimeError("boom")
        fs.get_all_active.side_effect = RuntimeError("boom")
        mr = MemoryRetriever(fact_store=fs)
        assert mr.get_memory_context("q") == ""


class TestFormatMemoryBlock:
    def test_grouped_by_category(self):
        mr = MemoryRetriever()
        facts = [
            _make_fact("f1", "TDD", FactCategory.PREFERENCE, 0.9),
            _make_fact("f2", "Python", FactCategory.SKILL, 0.8),
        ]
        result = mr._format_memory_block(facts)
        assert "## Preferences" in result
        assert "## Skills" in result

    def test_display_order(self):
        mr = MemoryRetriever()
        facts = [
            _make_fact("f1", "Working on X", FactCategory.CONTEXT, 0.9),
            _make_fact("f2", "Constrained", FactCategory.CONSTRAINT, 0.8),
            _make_fact("f3", "vim", FactCategory.PREFERENCE, 0.9),
        ]
        result = mr._format_memory_block(facts)
        assert result.index("Current Context") < result.index("Preferences")
        assert result.index("Preferences") < result.index("Constraints")


class TestGetRecurringThoughtsContext:
    def test_no_thread_store(self):
        mr = MemoryRetriever()
        assert mr.get_recurring_thoughts_context() == ""

    def test_exception_returns_empty(self):
        ts = MagicMock()
        ts.get_active_threads.side_effect = RuntimeError("boom")
        mr = MemoryRetriever(thread_store=ts)
        assert mr.get_recurring_thoughts_context() == ""

    def test_with_active_threads(self):
        now = datetime.now()

        @dataclass
        class FakeThread:
            id: str = "t1"
            label: str = "career switch"
            entry_count: int = 5
            created_at: datetime = now - timedelta(days=30)
            updated_at: datetime = now
            strength: float = 0.8

        @dataclass
        class FakeEntry:
            entry_date: datetime = now - timedelta(days=1)
            entry_id: str = "e1"

        ts = MagicMock()
        mr = MemoryRetriever(thread_store=ts)
        mr._run_async = MagicMock(side_effect=[[FakeThread()], [FakeEntry(), FakeEntry()]])
        result = mr.get_recurring_thoughts_context()
        assert "<recurring_thoughts>" in result
        assert "career switch" in result


class TestEffectiveFactConfidence:
    def test_no_boost(self):
        fact = _make_fact("f1", "x", FactCategory.SKILL, 0.8)
        assert MemoryRetriever._effective_fact_confidence(fact, {}) == 0.8

    def test_with_boost(self):
        fact = _make_fact("f1", "x", FactCategory.SKILL, 0.8)
        boosts = {"j1": 0.1}
        assert MemoryRetriever._effective_fact_confidence(fact, boosts) == 0.9

    def test_capped_at_1(self):
        fact = _make_fact("f1", "x", FactCategory.SKILL, 0.95)
        boosts = {"j1": 0.1}
        assert MemoryRetriever._effective_fact_confidence(fact, boosts) == 1.0
