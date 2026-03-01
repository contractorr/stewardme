"""Tests for batch-aware velocity scoring."""

from datetime import datetime, timedelta

from intelligence.trending_radar import _velocity_score


class TestBatchSpreading:
    def test_batch_scraped_items_diluted(self):
        """Items all scraped within 30min window get spread, not inflated."""
        now = datetime.now()
        # 10 items all scraped within 5 minutes — classic batch
        items = [{"scraped_at": (now - timedelta(minutes=m)).isoformat()} for m in range(10)]
        score = _velocity_score(items, now, total_days=7, hot_hours=24)
        # Batch items spread over 7d → most fall outside hot window → low velocity
        assert score < 2.0
        assert score >= 0

    def test_published_dates_passthrough(self):
        """Items with real published dates are used as-is, no spreading."""
        now = datetime.now()
        items = [
            {
                "scraped_at": (now - timedelta(minutes=1)).isoformat(),
                "published": (now - timedelta(hours=h)).isoformat(),
            }
            for h in range(1, 8)
        ]
        score = _velocity_score(items, now, total_days=7, hot_hours=24)
        # Published dates are spread across hours, so velocity is meaningful
        assert score > 0

    def test_mixed_published_and_scraped(self):
        """Mix of published-date and scraped-only items."""
        now = datetime.now()
        # 3 with published dates (spread over days)
        pub_items = [
            {
                "scraped_at": (now - timedelta(minutes=2)).isoformat(),
                "published": (now - timedelta(days=d)).isoformat(),
            }
            for d in range(3)
        ]
        # 3 scraped-only in a batch
        batch_items = [{"scraped_at": (now - timedelta(minutes=m)).isoformat()} for m in range(3)]
        score = _velocity_score(pub_items + batch_items, now, total_days=7, hot_hours=24)
        assert 0 <= score <= 5.0

    def test_non_batch_scraped_items_normal(self):
        """Scraped items spread over hours are not treated as batch."""
        now = datetime.now()
        items = [{"scraped_at": (now - timedelta(hours=h)).isoformat()} for h in range(1, 20)]
        score = _velocity_score(items, now, total_days=7, hot_hours=24)
        assert score > 1.0  # accelerating

    def test_empty_items(self):
        now = datetime.now()
        score = _velocity_score([], now, total_days=7, hot_hours=24)
        assert score == 1.0

    def test_cap_at_five(self):
        now = datetime.now()
        # Many items with published dates all in recent window
        items = [
            {
                "scraped_at": (now - timedelta(minutes=1)).isoformat(),
                "published": (now - timedelta(hours=h * 0.1)).isoformat(),
            }
            for h in range(100)
        ]
        score = _velocity_score(items, now, total_days=7, hot_hours=24)
        assert score <= 5.0
