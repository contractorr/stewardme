"""Tests for outcome_boost integration in RecommendationScorer."""

from datetime import datetime, timedelta

from advisor.scoring import (
    MAX_OUTCOME_BOOST,
    MIN_OUTCOMES_FOR_BOOST,
    RecommendationScorer,
)
from predictions.store import Prediction, PredictionStore


def test_outcome_boost_no_data(tmp_path):
    """No intel_db_path → returns 0.0."""
    scorer = RecommendationScorer()
    assert scorer.outcome_boost("learning") == 0.0


def test_outcome_boost_below_threshold(tmp_path):
    db = tmp_path / "intel.db"
    store = PredictionStore(db)

    # Insert fewer than MIN_OUTCOMES_FOR_BOOST resolved predictions
    for i in range(MIN_OUTCOMES_FOR_BOOST - 1):
        p = Prediction(
            category="learning",
            claim_text=f"claim-{i}",
            evaluation_due=(datetime.now() - timedelta(days=1)).isoformat(),
        )
        store.save(p)
        store.record_outcome(p.id, "confirmed")

    scorer = RecommendationScorer(intel_db_path=db)
    assert scorer.outcome_boost("learning") == 0.0


def test_outcome_boost_high_accuracy(tmp_path):
    db = tmp_path / "intel.db"
    store = PredictionStore(db)

    # All confirmed → accuracy = 1.0 → boost = MAX_OUTCOME_BOOST
    for i in range(MIN_OUTCOMES_FOR_BOOST):
        p = Prediction(
            category="career",
            claim_text=f"claim-{i}",
            evaluation_due=(datetime.now() - timedelta(days=1)).isoformat(),
        )
        store.save(p)
        store.record_outcome(p.id, "confirmed")

    scorer = RecommendationScorer(intel_db_path=db)
    boost = scorer.outcome_boost("career")
    assert abs(boost - MAX_OUTCOME_BOOST) < 0.01


def test_outcome_boost_low_accuracy(tmp_path):
    db = tmp_path / "intel.db"
    store = PredictionStore(db)

    # All rejected → accuracy = 0.0 → boost = -MAX_OUTCOME_BOOST
    for i in range(MIN_OUTCOMES_FOR_BOOST):
        p = Prediction(
            category="investment",
            claim_text=f"claim-{i}",
            evaluation_due=(datetime.now() - timedelta(days=1)).isoformat(),
        )
        store.save(p)
        store.record_outcome(p.id, "rejected")

    scorer = RecommendationScorer(intel_db_path=db)
    boost = scorer.outcome_boost("investment")
    assert abs(boost - (-MAX_OUTCOME_BOOST)) < 0.01


def test_adjust_score_combines_boosts(tmp_path):
    """adjust_score applies both engagement + outcome boosts."""
    db = tmp_path / "intel.db"
    store = PredictionStore(db)

    for i in range(MIN_OUTCOMES_FOR_BOOST):
        p = Prediction(
            category="learning",
            claim_text=f"claim-{i}",
            evaluation_due=(datetime.now() - timedelta(days=1)).isoformat(),
        )
        store.save(p)
        store.record_outcome(p.id, "confirmed")

    scorer = RecommendationScorer(intel_db_path=db)
    raw = 7.0
    adjusted = scorer.adjust_score(raw, "learning")
    # engagement_boost = 0.0 (no users_db), outcome_boost = +MAX_OUTCOME_BOOST
    assert adjusted == raw + MAX_OUTCOME_BOOST
