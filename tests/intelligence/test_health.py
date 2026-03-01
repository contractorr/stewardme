"""Tests for ScraperHealthTracker."""

from datetime import datetime, timedelta
from unittest.mock import patch

from intelligence.health import _MAX_BACKOFF_SECONDS, ScraperHealthTracker
from intelligence.scraper import IntelStorage


class TestScraperHealthTracker:
    """Test scraper health tracking and backoff."""

    def _make_tracker(self, temp_dirs):
        # IntelStorage._init_db creates the scraper_health table
        IntelStorage(temp_dirs["intel_db"])
        return ScraperHealthTracker(temp_dirs["intel_db"])

    def test_record_success_resets_errors(self, temp_dirs):
        tracker = self._make_tracker(temp_dirs)

        # Fail twice then succeed
        tracker.record_failure("hn", "timeout")
        tracker.record_failure("hn", "timeout")
        tracker.record_success("hn")

        health = tracker.get_source_health("hn")
        assert health["consecutive_errors"] == 0
        assert health["last_error"] is None
        assert health["backoff_until"] is None
        assert health["total_runs"] == 3
        assert health["total_errors"] == 2

    def test_backoff_increases_exponentially(self, temp_dirs):
        tracker = self._make_tracker(temp_dirs)

        tracker.record_failure("rss", "500 error")
        h1 = tracker.get_source_health("rss")

        tracker.record_failure("rss", "500 error")
        h2 = tracker.get_source_health("rss")

        tracker.record_failure("rss", "500 error")
        h3 = tracker.get_source_health("rss")

        # backoff_until should increase: 2^1*60=120s, 2^2*60=240s, 2^3*60=480s
        _b1 = datetime.fromisoformat(h1["backoff_until"])
        b2 = datetime.fromisoformat(h2["backoff_until"])
        b3 = datetime.fromisoformat(h3["backoff_until"])
        r2 = datetime.fromisoformat(h2["last_run_at"])
        r3 = datetime.fromisoformat(h3["last_run_at"])

        # Each backoff window should be longer than the previous
        delta2 = (b2 - r2).total_seconds()
        delta3 = (b3 - r3).total_seconds()
        assert delta2 > 120  # 2^2 * 60 = 240
        assert delta3 > delta2

    def test_should_skip_during_backoff(self, temp_dirs):
        tracker = self._make_tracker(temp_dirs)

        tracker.record_failure("gh", "rate limited")

        assert tracker.should_skip("gh") is True

    def test_should_not_skip_after_backoff_expires(self, temp_dirs):
        tracker = self._make_tracker(temp_dirs)

        tracker.record_failure("gh", "rate limited")

        # Mock utcnow to be past backoff
        future = datetime.utcnow() + timedelta(hours=2)
        with patch("intelligence.health.datetime") as mock_dt:
            mock_dt.utcnow.return_value = future
            # isoformat needed for comparison in should_skip
            assert tracker.should_skip("gh") is False

    def test_get_all_health_multiple_sources(self, temp_dirs):
        tracker = self._make_tracker(temp_dirs)

        tracker.record_success("hn")
        tracker.record_success("rss")
        tracker.record_failure("arxiv", "timeout")

        all_health = tracker.get_all_health()
        sources = {h["source"] for h in all_health}
        assert sources == {"hn", "rss", "arxiv"}

    def test_backoff_capped_at_3600s(self, temp_dirs):
        tracker = self._make_tracker(temp_dirs)

        # Fail many times to exceed cap
        for _ in range(20):
            tracker.record_failure("broken", "always fails")

        health = tracker.get_source_health("broken")
        backoff_until = datetime.fromisoformat(health["backoff_until"])
        last_run = datetime.fromisoformat(health["last_run_at"])
        delta = (backoff_until - last_run).total_seconds()

        assert delta <= _MAX_BACKOFF_SECONDS + 1  # +1 for timing tolerance

    def test_get_source_health_unknown(self, temp_dirs):
        tracker = self._make_tracker(temp_dirs)
        assert tracker.get_source_health("nonexistent") is None

    def test_error_truncated_to_500_chars(self, temp_dirs):
        tracker = self._make_tracker(temp_dirs)

        long_error = "x" * 1000
        tracker.record_failure("hn", long_error)

        health = tracker.get_source_health("hn")
        assert len(health["last_error"]) == 500

    def test_record_success_with_metrics(self, temp_dirs):
        tracker = self._make_tracker(temp_dirs)

        tracker.record_success("hn", items_scraped=25, items_new=10, duration_s=3.14)

        health = tracker.get_source_health("hn")
        assert health["last_items_scraped"] == 25
        assert health["last_items_new"] == 10
        assert abs(health["last_duration_seconds"] - 3.14) < 0.01

    def test_record_success_without_metrics(self, temp_dirs):
        """Backward compat: new cols default to 0/None when not passed."""
        tracker = self._make_tracker(temp_dirs)

        tracker.record_success("hn")

        health = tracker.get_source_health("hn")
        assert health["last_items_scraped"] == 0
        assert health["last_items_new"] == 0
        assert health["last_duration_seconds"] is None

    def test_get_health_summary_statuses(self, temp_dirs):
        tracker = self._make_tracker(temp_dirs)

        # healthy: 0 consecutive errors
        tracker.record_success("hn")
        # 1 error with active backoff → backoff takes priority
        tracker.record_failure("rss", "err")
        # degraded: 2 errors, but backoff expired
        tracker.record_failure("degraded_src", "err")
        tracker.record_failure("degraded_src", "err")
        # failing: 3+ consecutive errors
        for _ in range(3):
            tracker.record_failure("arxiv", "err")

        summary = {r["source"]: r for r in tracker.get_health_summary()}
        assert summary["hn"]["status"] == "healthy"
        assert summary["rss"]["status"] == "backoff"  # active backoff
        assert summary["arxiv"]["status"] in ("failing", "backoff")

    def test_get_health_summary_error_rate(self, temp_dirs):
        tracker = self._make_tracker(temp_dirs)

        tracker.record_success("hn")
        tracker.record_failure("hn", "err")
        # 2 runs, 1 error → 50%
        summary = {r["source"]: r for r in tracker.get_health_summary()}
        assert summary["hn"]["error_rate"] == 50.0

    def test_consecutive_failure_warning(self, temp_dirs, capsys):
        tracker = self._make_tracker(temp_dirs)

        tracker.record_failure("hn", "err")
        tracker.record_failure("hn", "err")
        # 3rd should trigger warning
        tracker.record_failure("hn", "err")

        captured = capsys.readouterr().out
        assert "scraper_consecutive_failures" in captured
