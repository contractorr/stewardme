"""Tests for PredictionRecorder."""

from datetime import datetime
from unittest.mock import MagicMock

from predictions.recorder import CATEGORY_HORIZONS, record_from_recommendation
from predictions.store import PredictionStore


def _make_rec(score=8.0, category="learning", metadata=None):
    rec = MagicMock()
    rec.score = score
    rec.category = category
    rec.title = "Test Rec"
    rec.rationale = "Because reasons " * 20
    rec.id = "rec123"
    rec.metadata = metadata or {}
    return rec


def test_record_from_recommendation(tmp_path):
    store = PredictionStore(tmp_path / "intel.db")
    rec = _make_rec(score=8.0)

    pid = record_from_recommendation(rec, store)
    assert pid is not None

    rows = store.get_all()
    assert len(rows) == 1
    assert rows[0]["recommendation_id"] == "rec123"
    assert rows[0]["category"] == "learning"


def test_skip_low_score(tmp_path):
    store = PredictionStore(tmp_path / "intel.db")
    rec = _make_rec(score=5.0)

    pid = record_from_recommendation(rec, store)
    assert pid is None

    rows = store.get_all()
    assert len(rows) == 0


def test_horizon_per_category(tmp_path):
    store = PredictionStore(tmp_path / "intel.db")

    for cat, days in CATEGORY_HORIZONS.items():
        rec = _make_rec(category=cat)
        record_from_recommendation(rec, store)

    rows = store.get_all(limit=100)
    assert len(rows) == len(CATEGORY_HORIZONS)

    for row in rows:
        expected_days = CATEGORY_HORIZONS[row["category"]]
        created = datetime.fromisoformat(row["created_at"])
        due = datetime.fromisoformat(row["evaluation_due"])
        delta = (due - created).days
        assert abs(delta - expected_days) <= 1


def test_extracts_confidence_from_metadata(tmp_path):
    store = PredictionStore(tmp_path / "intel.db")
    rec = _make_rec(
        metadata={
            "reasoning_trace": {"confidence": 0.9},
            "confidence": "High",
            "intel_trigger": "intel-abc",
        }
    )

    record_from_recommendation(rec, store)
    rows = store.get_all()
    assert rows[0]["confidence"] == 0.9
    assert rows[0]["confidence_bucket"] == "High"
    assert "intel-abc" in rows[0]["source_intel_ids"]
