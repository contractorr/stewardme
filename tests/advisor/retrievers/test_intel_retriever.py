"""Tests for IntelRetriever."""

from unittest.mock import MagicMock, patch

from advisor.retrievers.intel import IntelRetriever


class TestIntelRetriever:
    def test_get_intel_context_no_db(self):
        ir = IntelRetriever()
        result = ir.get_intel_context("test")
        assert "No external intelligence" in result

    def test_get_intel_context_with_semantic_search(self):
        isearch = MagicMock()
        isearch.get_context_for_query.return_value = "semantic result"
        ir = IntelRetriever(intel_search=isearch)
        assert ir.get_intel_context("q") == "semantic result"

    def test_get_intel_context_cache_hit(self):
        cache = MagicMock()
        cache.make_key.return_value = "k"
        cache.get.return_value = "cached intel"
        ir = IntelRetriever(cache=cache)
        assert ir.get_intel_context("q") == "cached intel"

    def test_get_intel_context_cache_miss(self):
        cache = MagicMock()
        cache.make_key.return_value = "k"
        cache.get.return_value = None
        isearch = MagicMock()
        isearch.get_context_for_query.return_value = "fresh"
        ir = IntelRetriever(intel_search=isearch, cache=cache)
        result = ir.get_intel_context("q")
        assert result == "fresh"
        cache.set.assert_called_once_with("k", "fresh")

    def test_get_filtered_intel_context_with_search(self):
        isearch = MagicMock()
        isearch.get_filtered_context_for_query.return_value = "filtered"
        loader = MagicMock(return_value=None)
        ir = IntelRetriever(intel_search=isearch, profile_loader=loader)
        result = ir.get_filtered_intel_context("q")
        assert result == "filtered"

    def test_get_filtered_intel_context_fallback(self):
        ir = IntelRetriever()
        result = ir.get_filtered_intel_context("q")
        assert "No external intelligence" in result

    def test_get_ai_capabilities_context(self):
        isearch = MagicMock()
        isearch.get_context_for_query.return_value = "ai intel"
        ir = IntelRetriever(intel_search=isearch)
        with patch("advisor.ai_capabilities_kb.render_summary", return_value="KB"):
            result = ir.get_ai_capabilities_context("q")
        assert "KB" in result

    def test_get_capability_context_no_db(self):
        ir = IntelRetriever()
        assert ir.get_capability_context() == ""
