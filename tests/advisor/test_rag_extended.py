"""Extended tests for RAG retriever — covers profile, filtered intel, research,
AI capabilities, full context, dynamic weight, and caching paths."""

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_journal_search():
    """Minimal mock JournalSearch."""
    js = MagicMock()
    js.get_context_for_query.return_value = "journal context"
    js.storage.list_entries.return_value = []
    return js


@pytest.fixture
def rag(mock_journal_search):
    from advisor.rag import RAGRetriever

    return RAGRetriever(journal_search=mock_journal_search)


# ── get_profile_context ──────────────────────────────────────────────


class TestGetProfileContext:
    def test_structured_output(self, rag):
        profile = MagicMock()
        profile.structured_summary.return_value = "STRUCTURED"
        ps_instance = MagicMock()
        ps_instance.load.return_value = profile

        with patch("profile.storage.ProfileStorage", return_value=ps_instance):
            result = rag.get_profile_context(structured=True)

        assert "STRUCTURED" in result

    def test_compact_output(self, rag):
        profile = MagicMock()
        profile.summary.return_value = "compact summary"
        ps_instance = MagicMock()
        ps_instance.load.return_value = profile

        with patch("profile.storage.ProfileStorage", return_value=ps_instance):
            result = rag.get_profile_context(structured=False)

        assert "USER PROFILE" in result
        assert "compact summary" in result

    def test_no_profile_returns_empty(self, rag):
        ps_instance = MagicMock()
        ps_instance.load.return_value = None

        with patch("profile.storage.ProfileStorage", return_value=ps_instance):
            assert rag.get_profile_context() == ""

    def test_exception_returns_empty(self, rag):
        with patch("profile.storage.ProfileStorage", side_effect=ImportError("no module")):
            assert rag.get_profile_context() == ""


# ── get_profile_keywords ─────────────────────────────────────────────


class TestGetProfileKeywords:
    def _make_skill(self, name):
        s = MagicMock()
        s.name = name
        return s

    def test_populated_profile(self, rag):
        profile = MagicMock()
        profile.skills = [self._make_skill("Python"), self._make_skill("Rust")]
        profile.languages_frameworks = ["FastAPI"]
        profile.technologies_watching = ["WebGPU"]
        profile.industries_watching = ["fintech"]
        profile.interests = ["compilers"]
        profile.active_projects = ["AI Coach"]
        ps_instance = MagicMock()
        ps_instance.load.return_value = profile

        with patch("profile.storage.ProfileStorage", return_value=ps_instance):
            kw = rag.get_profile_keywords()

        assert "python" in kw
        assert "fastapi" in kw

    def test_empty_profile_returns_empty(self, rag):
        ps_instance = MagicMock()
        ps_instance.load.return_value = None

        with patch("profile.storage.ProfileStorage", return_value=ps_instance):
            assert rag.get_profile_keywords() == []

    def test_exception_returns_empty(self, rag):
        with patch("profile.storage.ProfileStorage", side_effect=Exception("boom")):
            assert rag.get_profile_keywords() == []


# ── _load_profile_terms ──────────────────────────────────────────────


class TestLoadProfileTerms:
    def test_builds_profile_terms(self, rag):
        profile = MagicMock()
        skill = MagicMock()
        skill.name = "Python"
        profile.skills = [skill]
        profile.languages_frameworks = ["FastAPI"]
        profile.technologies_watching = ["WASM"]
        profile.interests = ["compilers"]
        profile.industries_watching = ["fintech"]
        profile.active_projects = ["AI Coach"]
        profile.goals_short_term = "learn distributed systems"
        profile.goals_long_term = "become staff engineer"
        profile.aspirations = "open source maintainer"
        ps_instance = MagicMock()
        ps_instance.load.return_value = profile

        with patch("profile.storage.ProfileStorage", return_value=ps_instance):
            terms = rag._load_profile_terms()

        assert "python" in {s.lower() for s in terms.skills} if isinstance(terms.skills, list) else "python" in terms.skills
        assert any("fastapi" in t.lower() for t in terms.tech)

    def test_no_profile_returns_empty_terms(self, rag):
        ps_instance = MagicMock()
        ps_instance.load.return_value = None

        with patch("profile.storage.ProfileStorage", return_value=ps_instance):
            terms = rag._load_profile_terms()

        assert terms.is_empty

    def test_exception_returns_empty_terms(self, rag):
        with patch("profile.storage.ProfileStorage", side_effect=Exception("x")):
            terms = rag._load_profile_terms()
        assert terms.is_empty


# ── get_filtered_intel_context ────────────────────────────────────────


class TestGetFilteredIntelContext:
    def test_with_intel_search(self, mock_journal_search):
        from advisor.rag import RAGRetriever

        intel_search = MagicMock()
        intel_search.get_filtered_context_for_query.return_value = "filtered"

        rag = RAGRetriever(journal_search=mock_journal_search, intel_search=intel_search)

        with patch.object(rag, "_load_profile_terms") as lpt:
            lpt.return_value = MagicMock()
            result = rag.get_filtered_intel_context("AI")

        assert result == "filtered"
        intel_search.get_filtered_context_for_query.assert_called_once()

    def test_falls_back_without_intel_search(self, mock_journal_search):
        from advisor.rag import RAGRetriever

        rag = RAGRetriever(journal_search=mock_journal_search)

        with patch.object(rag, "get_intel_context", return_value="fallback") as gic:
            result = rag.get_filtered_intel_context("query")

        assert result == "fallback"
        gic.assert_called_once()


# ── get_research_context ──────────────────────────────────────────────


class TestGetResearchContext:
    def test_no_entries_returns_empty(self, mock_journal_search):
        from advisor.rag import RAGRetriever

        mock_journal_search.storage.list_entries.return_value = []
        rag = RAGRetriever(journal_search=mock_journal_search)

        assert rag.get_research_context("q") == ""

    def test_with_entries_via_fallback(self, mock_journal_search):
        from advisor.rag import RAGRetriever

        entry = {"title": "Report", "path": "/tmp/r.md", "type": "research"}
        mock_journal_search.storage.list_entries.return_value = [entry]
        post = MagicMock()
        post.content = "Research body text"
        mock_journal_search.storage.read.return_value = post
        # No semantic_search attr → fallback path
        del mock_journal_search.semantic_search

        rag = RAGRetriever(journal_search=mock_journal_search)
        result = rag.get_research_context("q")

        assert "Report" in result
        assert "Research body text" in result

    def test_char_limit_respected(self, mock_journal_search):
        from advisor.rag import RAGRetriever

        entries = [
            {"title": f"Report {i}", "path": f"/tmp/r{i}.md", "type": "research"}
            for i in range(5)
        ]
        mock_journal_search.storage.list_entries.return_value = entries
        post = MagicMock()
        post.content = "x" * 2000
        mock_journal_search.storage.read.return_value = post
        del mock_journal_search.semantic_search

        rag = RAGRetriever(journal_search=mock_journal_search)
        result = rag.get_research_context("q", max_chars=500)

        assert len(result) <= 2000  # each entry capped at 1500 content + header

    def test_semantic_search_path(self, mock_journal_search):
        from advisor.rag import RAGRetriever

        entry = {"title": "Report", "path": "/tmp/r.md", "type": "research"}
        mock_journal_search.storage.list_entries.return_value = [entry]
        mock_journal_search.semantic_search.return_value = [
            {"title": "Semantic Hit", "content": "matched body"}
        ]

        rag = RAGRetriever(journal_search=mock_journal_search)
        result = rag.get_research_context("q")

        assert "Semantic Hit" in result


# ── get_ai_capabilities_context ───────────────────────────────────────


class TestGetAICapabilitiesContext:
    def test_combines_kb_and_intel(self, mock_journal_search):
        from advisor.rag import RAGRetriever

        rag = RAGRetriever(journal_search=mock_journal_search)

        with patch("advisor.ai_capabilities_kb.render_summary", return_value="KB SUMMARY"):
            with patch.object(rag, "get_intel_context", return_value="recent intel"):
                result = rag.get_ai_capabilities_context("AI models")

        assert "KB SUMMARY" in result
        assert "recent intel" in result

    def test_no_intel_when_remaining_small(self, mock_journal_search):
        from advisor.rag import RAGRetriever

        rag = RAGRetriever(journal_search=mock_journal_search)

        # KB summary eats almost all budget
        with patch("advisor.ai_capabilities_kb.render_summary", return_value="x" * 1500):
            with patch.object(rag, "get_intel_context") as gic:
                rag.get_ai_capabilities_context("q", max_chars=1500)

        # remaining < 100 → intel not fetched
        gic.assert_not_called()


# ── get_full_context ──────────────────────────────────────────────────


class TestGetFullContext:
    def test_returns_three_tuple(self, rag):
        with patch.object(rag, "get_combined_context", return_value=("j", "i")):
            with patch.object(rag, "get_research_context", return_value="r"):
                j, i, r = rag.get_full_context("q")

        assert (j, i, r) == ("j", "i", "r")

    def test_include_research_false_skips(self, rag):
        with patch.object(rag, "get_combined_context", return_value=("j", "i")):
            with patch.object(rag, "get_research_context") as grc:
                j, i, r = rag.get_full_context("q", include_research=False)

        assert r == ""
        grc.assert_not_called()


# ── compute_dynamic_weight ────────────────────────────────────────────


class TestComputeDynamicWeight:
    def test_no_user_id_returns_default(self, mock_journal_search):
        from advisor.rag import RAGRetriever

        rag = RAGRetriever(journal_search=mock_journal_search)
        assert rag.compute_dynamic_weight() == 0.7

    def test_fewer_than_10_events_returns_default(self, mock_journal_search, tmp_path):
        from advisor.rag import RAGRetriever

        db_path = tmp_path / "users.db"
        import sqlite3

        conn = sqlite3.connect(db_path)
        conn.execute(
            """CREATE TABLE engagement_events (
                user_id TEXT, target_type TEXT, event_type TEXT,
                created_at TEXT DEFAULT (datetime('now')))"""
        )
        # Insert only 5 rows — below threshold
        for _ in range(5):
            conn.execute(
                "INSERT INTO engagement_events (user_id, target_type, event_type) VALUES (?,?,?)",
                ("u1", "journal", "opened"),
            )
        conn.commit()
        conn.close()

        rag = RAGRetriever(
            journal_search=mock_journal_search,
            users_db_path=db_path,
            user_id="u1",
        )
        assert rag.compute_dynamic_weight() == 0.7

    def test_with_engagement_data(self, mock_journal_search, tmp_path):
        from advisor.rag import RAGRetriever

        db_path = tmp_path / "users.db"
        import sqlite3

        conn = sqlite3.connect(db_path)
        conn.execute(
            """CREATE TABLE engagement_events (
                user_id TEXT, target_type TEXT, event_type TEXT,
                created_at TEXT DEFAULT (datetime('now')))"""
        )
        # 8 journal positive + 2 intel positive = 10 total, ratio=0.8
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

        rag = RAGRetriever(
            journal_search=mock_journal_search,
            users_db_path=db_path,
            user_id="u1",
        )
        weight = rag.compute_dynamic_weight()
        # ratio=0.8 → 0.7 + 0.15*(0.8-0.5) = 0.745
        assert 0.5 <= weight <= 0.85
        assert abs(weight - 0.745) < 0.01

    def test_db_error_returns_default(self, mock_journal_search, tmp_path):
        from advisor.rag import RAGRetriever

        rag = RAGRetriever(
            journal_search=mock_journal_search,
            users_db_path=tmp_path / "nonexistent.db",
            user_id="u1",
        )
        assert rag.compute_dynamic_weight() == 0.7


# ── cache hit/miss ────────────────────────────────────────────────────


class TestCaching:
    def test_journal_cache_hit(self, mock_journal_search):
        from advisor.rag import RAGRetriever

        cache = MagicMock()
        cache.make_key.return_value = "k"
        cache.get.return_value = "cached journal"

        rag = RAGRetriever(journal_search=mock_journal_search, cache=cache)
        result = rag.get_journal_context("q")

        assert result == "cached journal"
        mock_journal_search.get_context_for_query.assert_not_called()

    def test_journal_cache_miss(self, mock_journal_search):
        from advisor.rag import RAGRetriever

        cache = MagicMock()
        cache.make_key.return_value = "k"
        cache.get.return_value = None

        rag = RAGRetriever(journal_search=mock_journal_search, cache=cache)
        result = rag.get_journal_context("q")

        assert result == "journal context"
        cache.set.assert_called_once_with("k", "journal context")

    def test_intel_cache_hit(self, mock_journal_search):
        from advisor.rag import RAGRetriever

        cache = MagicMock()
        cache.make_key.return_value = "k"
        cache.get.return_value = "cached intel"

        rag = RAGRetriever(journal_search=mock_journal_search, cache=cache)
        result = rag.get_intel_context("q")

        assert result == "cached intel"

    def test_intel_cache_miss(self, mock_journal_search):
        from advisor.rag import RAGRetriever

        cache = MagicMock()
        cache.make_key.return_value = "k"
        cache.get.return_value = None

        intel_search = MagicMock()
        intel_search.get_context_for_query.return_value = "intel result"

        rag = RAGRetriever(
            journal_search=mock_journal_search, intel_search=intel_search, cache=cache
        )
        result = rag.get_intel_context("q")

        assert result == "intel result"
        cache.set.assert_called_once_with("k", "intel result")
