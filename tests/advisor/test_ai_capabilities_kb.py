"""Tests for AI capabilities knowledge base."""

from datetime import datetime, timedelta
from unittest.mock import patch

from advisor.ai_capabilities_kb import (
    AI_CAPABILITY_DOMAINS,
    LAST_UPDATED,
    STALENESS_DAYS,
    render_context,
    render_summary,
)


class TestAICapabilitiesKB:
    """Test static KB rendering and staleness."""

    def test_render_summary_returns_string(self):
        summary = render_summary()
        assert isinstance(summary, str)
        assert len(summary) > 100

    def test_render_summary_contains_key_data(self):
        summary = render_summary()
        assert "SWE-bench" in summary
        assert "autonomy" in summary.lower() or "autonomous" in summary.lower()
        assert "tool use" in summary.lower() or "function calling" in summary.lower()

    def test_render_summary_reasonable_length(self):
        summary = render_summary()
        assert len(summary) < 600

    def test_render_context_all_domains(self):
        ctx = render_context()
        assert "Coding" in ctx
        assert "Research" in ctx
        assert "Reasoning" in ctx
        assert "Autonomy" in ctx
        assert "Creative" in ctx
        assert "Tool Use" in ctx

    def test_render_context_specific_domains(self):
        ctx = render_context(domains=["coding", "autonomy"])
        assert "Coding" in ctx
        assert "Autonomy" in ctx
        assert "Creative" not in ctx

    def test_render_context_contains_benchmarks(self):
        ctx = render_context(domains=["coding"])
        assert "SWE-bench" in ctx or "HumanEval" in ctx

    def test_render_context_unknown_domain_ignored(self):
        ctx = render_context(domains=["coding", "nonexistent"])
        assert "Coding" in ctx
        # Should not crash on unknown domain

    def test_render_context_includes_date(self):
        ctx = render_context()
        assert LAST_UPDATED.strftime("%Y-%m") in ctx

    def test_all_domains_have_required_keys(self):
        required = {"what_works", "limitations", "key_benchmarks", "trajectory"}
        for domain, data in AI_CAPABILITY_DOMAINS.items():
            assert required.issubset(data.keys()), f"{domain} missing keys"

    def test_staleness_warning_when_old(self):
        """KB logs warning when data is stale."""
        old_date = datetime.now() - timedelta(days=STALENESS_DAYS + 10)
        with patch("advisor.ai_capabilities_kb.LAST_UPDATED", old_date):
            with patch("advisor.ai_capabilities_kb.logger") as mock_logger:
                render_summary()
                mock_logger.warning.assert_called_once()
                assert "stale" in mock_logger.warning.call_args[0][0]

    def test_no_staleness_warning_when_fresh(self):
        """KB does not warn when data is fresh."""
        with patch("advisor.ai_capabilities_kb.LAST_UPDATED", datetime.now()):
            with patch("advisor.ai_capabilities_kb.logger") as mock_logger:
                render_summary()
                mock_logger.warning.assert_not_called()
