"""Tests for JournalRetriever."""

from unittest.mock import MagicMock

from advisor.retrievers.journal import JournalRetriever


class TestJournalRetriever:
    def _make(self, cache=None):
        js = MagicMock()
        js.get_context_for_query.return_value = "journal text"
        js.storage.list_entries.return_value = []
        return JournalRetriever(js, cache=cache)

    def test_search_property(self):
        js = MagicMock()
        jr = JournalRetriever(js)
        assert jr.search is js

    def test_get_journal_context_no_cache(self):
        jr = self._make()
        result = jr.get_journal_context("q")
        assert result == "journal text"
        jr.search.get_context_for_query.assert_called_once()

    def test_get_journal_context_cache_hit(self):
        cache = MagicMock()
        cache.make_key.return_value = "k"
        cache.get.return_value = "cached"
        jr = self._make(cache=cache)
        assert jr.get_journal_context("q") == "cached"
        jr.search.get_context_for_query.assert_not_called()

    def test_get_journal_context_cache_miss(self):
        cache = MagicMock()
        cache.make_key.return_value = "k"
        cache.get.return_value = None
        jr = self._make(cache=cache)
        result = jr.get_journal_context("q")
        assert result == "journal text"
        cache.set.assert_called_once_with("k", "journal text")

    def test_get_recent_entries_empty(self):
        jr = self._make()
        result = jr.get_recent_entries()
        assert "No journal entries" in result

    def test_get_research_context_no_entries(self):
        jr = self._make()
        assert jr.get_research_context("q") == ""

    def test_get_research_context_fallback(self):
        js = MagicMock()
        entry = {"title": "Report", "path": "/tmp/r.md", "type": "research"}
        js.storage.list_entries.return_value = [entry]
        post = MagicMock()
        post.content = "body"
        js.storage.read.return_value = post
        del js.semantic_search
        jr = JournalRetriever(js)
        result = jr.get_research_context("q")
        assert "Report" in result
