"""Extended tests for RecommendationScorer — engagement_boost, adjust_score, caching."""

import sqlite3

import pytest


@pytest.fixture
def scorer():
    from advisor.scoring import RecommendationScorer

    return RecommendationScorer()


@pytest.fixture
def users_db(tmp_path):
    """Create a users DB with engagement_events table."""
    db_path = tmp_path / "users.db"
    conn = sqlite3.connect(db_path)
    conn.execute(
        """CREATE TABLE engagement_events (
            user_id TEXT,
            target_type TEXT,
            event_type TEXT,
            metadata_json TEXT DEFAULT '{}',
            created_at TEXT DEFAULT (datetime('now'))
        )"""
    )
    conn.commit()
    conn.close()
    return db_path


# ── engagement_boost ──────────────────────────────────────────────────


class TestEngagementBoost:
    def test_no_db_returns_zero(self, scorer):
        assert scorer.engagement_boost("career") == 0.0

    def test_no_user_id_returns_zero(self, users_db):
        from advisor.scoring import RecommendationScorer

        s = RecommendationScorer(users_db_path=users_db)
        assert s.engagement_boost("career") == 0.0

    def test_with_feedback_rows(self, users_db):
        from advisor.scoring import RecommendationScorer

        conn = sqlite3.connect(users_db)
        # 12 useful + 0 irrelevant for "career" → ratio=1.0 → boost=+MAX_BOOST
        for _ in range(12):
            conn.execute(
                "INSERT INTO engagement_events (user_id, target_type, event_type, metadata_json) "
                "VALUES (?,?,?,?)",
                ("u1", "recommendation", "feedback_useful", '{"category":"career"}'),
            )
        conn.commit()
        conn.close()

        s = RecommendationScorer(users_db_path=users_db, user_id="u1")
        boost = s.engagement_boost("career")
        assert boost == pytest.approx(1.5, abs=0.01)

    def test_negative_boost(self, users_db):
        from advisor.scoring import RecommendationScorer

        conn = sqlite3.connect(users_db)
        # 0 useful + 15 irrelevant → ratio=0.0 → boost=-MAX_BOOST
        for _ in range(15):
            conn.execute(
                "INSERT INTO engagement_events (user_id, target_type, event_type, metadata_json) "
                "VALUES (?,?,?,?)",
                ("u1", "recommendation", "feedback_irrelevant", '{"category":"health"}'),
            )
        conn.commit()
        conn.close()

        s = RecommendationScorer(users_db_path=users_db, user_id="u1")
        boost = s.engagement_boost("health")
        assert boost == pytest.approx(-1.5, abs=0.01)

    def test_below_min_events_skipped(self, users_db):
        from advisor.scoring import RecommendationScorer

        conn = sqlite3.connect(users_db)
        # Only 5 events — below MIN_EVENTS_FOR_BOOST (10)
        for _ in range(5):
            conn.execute(
                "INSERT INTO engagement_events (user_id, target_type, event_type, metadata_json) "
                "VALUES (?,?,?,?)",
                ("u1", "recommendation", "feedback_useful", '{"category":"tech"}'),
            )
        conn.commit()
        conn.close()

        s = RecommendationScorer(users_db_path=users_db, user_id="u1")
        assert s.engagement_boost("tech") == 0.0

    def test_caching(self, users_db):
        from advisor.scoring import RecommendationScorer

        conn = sqlite3.connect(users_db)
        for _ in range(12):
            conn.execute(
                "INSERT INTO engagement_events (user_id, target_type, event_type, metadata_json) "
                "VALUES (?,?,?,?)",
                ("u1", "recommendation", "feedback_useful", '{"category":"career"}'),
            )
        conn.commit()
        conn.close()

        s = RecommendationScorer(users_db_path=users_db, user_id="u1")
        # First call populates cache
        _b1 = s.engagement_boost("career")
        # Mutate internal cache to verify second call uses it
        s._category_boosts["career"] = 99.0
        b2 = s.engagement_boost("career")
        assert b2 == 99.0  # proves cache was used, not re-queried

    def test_unknown_category_returns_zero(self, users_db):
        from advisor.scoring import RecommendationScorer

        conn = sqlite3.connect(users_db)
        for _ in range(12):
            conn.execute(
                "INSERT INTO engagement_events (user_id, target_type, event_type, metadata_json) "
                "VALUES (?,?,?,?)",
                ("u1", "recommendation", "feedback_useful", '{"category":"career"}'),
            )
        conn.commit()
        conn.close()

        s = RecommendationScorer(users_db_path=users_db, user_id="u1")
        assert s.engagement_boost("nonexistent") == 0.0


# ── adjust_score ──────────────────────────────────────────────────────


class TestAdjustScore:
    def test_positive_boost(self, users_db):
        from advisor.scoring import RecommendationScorer

        s = RecommendationScorer(users_db_path=users_db, user_id="u1")
        s._category_boosts = {"career": 1.0}
        assert s.adjust_score(7.0, "career") == 8.0

    def test_negative_boost(self, users_db):
        from advisor.scoring import RecommendationScorer

        s = RecommendationScorer(users_db_path=users_db, user_id="u1")
        s._category_boosts = {"health": -1.0}
        assert s.adjust_score(5.0, "health") == 4.0

    def test_clamps_at_10(self):
        from advisor.scoring import RecommendationScorer

        s = RecommendationScorer()
        s._category_boosts = {"x": 1.5}
        assert s.adjust_score(9.5, "x") == 10.0

    def test_clamps_at_0(self):
        from advisor.scoring import RecommendationScorer

        s = RecommendationScorer()
        s._category_boosts = {"x": -1.5}
        assert s.adjust_score(1.0, "x") == 0.0

    def test_no_boost_category(self):
        from advisor.scoring import RecommendationScorer

        s = RecommendationScorer()
        s._category_boosts = {}
        assert s.adjust_score(6.0, "unknown") == 6.0
