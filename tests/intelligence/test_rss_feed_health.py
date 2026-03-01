"""Tests for RSSFeedHealthTracker."""

from intelligence.health import RSSFeedHealthTracker
from intelligence.scraper import IntelStorage


class TestRSSFeedHealthTracker:
    def _make_tracker(self, temp_dirs):
        IntelStorage(temp_dirs["intel_db"])
        return RSSFeedHealthTracker(temp_dirs["intel_db"])

    def test_record_success(self, temp_dirs):
        tracker = self._make_tracker(temp_dirs)
        tracker.record_success("https://example.com/rss")

        h = tracker.get_feed_health("https://example.com/rss")
        assert h is not None
        assert h["consecutive_errors"] == 0
        assert h["total_attempts"] == 1
        assert h["last_success_at"] is not None
        assert h["last_error"] is None

    def test_record_failure(self, temp_dirs):
        tracker = self._make_tracker(temp_dirs)
        tracker.record_failure("https://example.com/rss", "timeout")

        h = tracker.get_feed_health("https://example.com/rss")
        assert h["consecutive_errors"] == 1
        assert h["total_errors"] == 1
        assert h["last_error"] == "timeout"

    def test_success_resets_errors(self, temp_dirs):
        tracker = self._make_tracker(temp_dirs)
        tracker.record_failure("https://a.com/rss", "err1")
        tracker.record_failure("https://a.com/rss", "err2")
        tracker.record_success("https://a.com/rss")

        h = tracker.get_feed_health("https://a.com/rss")
        assert h["consecutive_errors"] == 0
        assert h["total_attempts"] == 3
        assert h["total_errors"] == 2
        assert h["last_error"] is None

    def test_get_all_health(self, temp_dirs):
        tracker = self._make_tracker(temp_dirs)
        tracker.record_success("https://a.com/rss")
        tracker.record_failure("https://b.com/rss", "500")

        all_h = tracker.get_all_health()
        urls = {h["feed_url"] for h in all_h}
        assert urls == {"https://a.com/rss", "https://b.com/rss"}

    def test_get_feed_health_unknown(self, temp_dirs):
        tracker = self._make_tracker(temp_dirs)
        assert tracker.get_feed_health("https://nonexistent.com/rss") is None

    def test_error_truncated(self, temp_dirs):
        tracker = self._make_tracker(temp_dirs)
        tracker.record_failure("https://a.com/rss", "x" * 1000)
        h = tracker.get_feed_health("https://a.com/rss")
        assert len(h["last_error"]) == 500
