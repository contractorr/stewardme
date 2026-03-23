"""Tests for ContextAssembler."""

from unittest.mock import MagicMock

from advisor.context_assembler import AskContext, ContextAssembler
from advisor.retrievers.intel import IntelRetriever
from advisor.retrievers.journal import JournalRetriever
from advisor.retrievers.memory import MemoryRetriever
from advisor.retrievers.profile import ProfileRetriever


def _make_assembler(**kw):
    js = MagicMock()
    js.get_context_for_query.return_value = "journal text"
    js.storage = MagicMock()
    journal = JournalRetriever(js)
    intel = IntelRetriever()
    profile = ProfileRetriever("/nonexistent")
    return ContextAssembler(journal=journal, intel=intel, profile=profile, **kw)


class TestGetCombinedContext:
    def test_returns_tuple(self):
        asm = _make_assembler()
        j, i = asm.get_combined_context("test")
        assert isinstance(j, str)
        assert isinstance(i, str)

    def test_cache_hit(self):
        cache = MagicMock()
        cache.make_key.return_value = "k"
        import json

        cache.get.return_value = json.dumps({"journal": "j", "intel": "i"})
        asm = _make_assembler(cache=cache)
        j, i = asm.get_combined_context("test")
        assert j == "j"
        assert i == "i"

    def test_cache_miss(self):
        cache = MagicMock()
        cache.make_key.return_value = "k"
        cache.get.return_value = None
        asm = _make_assembler(cache=cache)
        j, i = asm.get_combined_context("test")
        assert isinstance(j, str)
        cache.set.assert_called_once()


class TestGetEnhancedContext:
    def test_no_analyzer_falls_back(self):
        asm = _make_assembler()
        ctx = asm.get_enhanced_context("test")
        assert isinstance(ctx, AskContext)
        assert isinstance(ctx.journal, str)

    def test_with_analyzer(self):
        from advisor.query_analyzer import QueryAnalyzer

        asm = _make_assembler(query_analyzer=QueryAnalyzer())
        ctx = asm.get_enhanced_context("compare AI models")
        assert isinstance(ctx, AskContext)


class TestGetFullContext:
    def test_returns_three_tuple(self):
        asm = _make_assembler()
        j, i, r = asm.get_full_context("q")
        assert isinstance(j, str)
        assert isinstance(i, str)
        assert isinstance(r, str)


class TestBuildContextForAsk:
    def test_default_flags(self):
        asm = _make_assembler()
        ctx = asm.build_context_for_ask("test")
        assert isinstance(ctx, AskContext)
        assert ctx.memory == ""
        assert ctx.thoughts == ""

    def test_with_memory(self):
        mem = MagicMock(spec=MemoryRetriever)
        mem.get_memory_context.return_value = "<user_memory>facts</user_memory>"
        asm = _make_assembler(memory=mem)
        ctx = asm.build_context_for_ask("test", {"inject_memory": True})
        assert "<user_memory>" in ctx.memory


class TestComputeDynamicWeight:
    def test_no_user_returns_default(self):
        asm = _make_assembler()
        assert asm.compute_dynamic_weight() == 0.7

    def test_with_engagement_data(self, tmp_path):
        import sqlite3

        db = tmp_path / "users.db"
        conn = sqlite3.connect(db)
        conn.execute(
            """CREATE TABLE engagement_events (
                user_id TEXT, target_type TEXT, event_type TEXT,
                created_at TEXT DEFAULT (datetime('now')))"""
        )
        for _ in range(8):
            conn.execute(
                "INSERT INTO engagement_events (user_id, target_type, event_type) VALUES (?,?,?)",
                ("u1", "journal", "opened"),
            )
        for _ in range(2):
            conn.execute(
                "INSERT INTO engagement_events (user_id, target_type, event_type) VALUES (?,?,?)",
                ("u1", "intel", "opened"),
            )
        conn.commit()
        conn.close()

        asm = _make_assembler(users_db_path=db, user_id="u1")
        weight = asm.compute_dynamic_weight()
        assert 0.5 <= weight <= 0.85
