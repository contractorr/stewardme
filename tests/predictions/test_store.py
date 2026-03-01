"""Tests for PredictionStore."""

from datetime import datetime, timedelta

from predictions.store import Prediction, PredictionStore


def test_save_and_retrieve(tmp_path):
    db = tmp_path / "intel.db"
    store = PredictionStore(db)

    pred = Prediction(
        recommendation_id="rec1",
        category="learning",
        claim_text="Learn Rust: systems programming skill",
        confidence=0.8,
        confidence_bucket="High",
        evaluation_due=(datetime.now() + timedelta(days=90)).isoformat(),
    )
    pid = store.save(pred)
    assert pid == pred.id

    rows = store.get_all()
    assert len(rows) == 1
    assert rows[0]["claim_text"] == "Learn Rust: systems programming skill"
    assert rows[0]["confidence"] == 0.8


def test_get_review_due(tmp_path):
    db = tmp_path / "intel.db"
    store = PredictionStore(db)

    # Past due
    past = Prediction(
        category="career",
        claim_text="past due prediction",
        evaluation_due=(datetime.now() - timedelta(days=1)).isoformat(),
    )
    store.save(past)

    # Future
    future = Prediction(
        category="career",
        claim_text="future prediction",
        evaluation_due=(datetime.now() + timedelta(days=30)).isoformat(),
    )
    store.save(future)

    due = store.get_review_due()
    assert len(due) == 1
    assert due[0]["claim_text"] == "past due prediction"


def test_record_outcome(tmp_path):
    db = tmp_path / "intel.db"
    store = PredictionStore(db)

    pred = Prediction(
        category="learning",
        claim_text="test claim",
        evaluation_due=(datetime.now() - timedelta(days=1)).isoformat(),
    )
    pid = store.save(pred)

    ok = store.record_outcome(pid, "confirmed", notes="it happened")
    assert ok

    rows = store.get_all()
    assert rows[0]["outcome"] == "confirmed"
    assert rows[0]["outcome_notes"] == "it happened"
    assert rows[0]["outcome_source"] == "manual_review"


def test_get_pending_filters_by_category(tmp_path):
    db = tmp_path / "intel.db"
    store = PredictionStore(db)

    for cat in ("learning", "career", "learning"):
        store.save(
            Prediction(
                category=cat,
                claim_text=f"{cat} prediction",
                evaluation_due=(datetime.now() + timedelta(days=30)).isoformat(),
            )
        )

    all_pending = store.get_pending()
    assert len(all_pending) == 3

    learning = store.get_pending(category="learning")
    assert len(learning) == 2


def test_get_stats(tmp_path):
    db = tmp_path / "intel.db"
    store = PredictionStore(db)

    # Create mix of predictions
    p1 = Prediction(
        category="learning",
        claim_text="claim1",
        confidence_bucket="High",
        evaluation_due=(datetime.now() - timedelta(days=1)).isoformat(),
    )
    p2 = Prediction(
        category="learning",
        claim_text="claim2",
        confidence_bucket="High",
        evaluation_due=(datetime.now() - timedelta(days=1)).isoformat(),
    )
    p3 = Prediction(
        category="career",
        claim_text="claim3",
        confidence_bucket="Low",
        evaluation_due=(datetime.now() + timedelta(days=30)).isoformat(),
    )
    store.save(p1)
    store.save(p2)
    store.save(p3)

    store.record_outcome(p1.id, "confirmed")
    store.record_outcome(p2.id, "rejected")

    stats = store.get_stats()
    assert stats["total"] == 3
    assert stats["by_outcome"]["confirmed"] == 1
    assert stats["by_outcome"]["rejected"] == 1
    assert stats["by_outcome"]["pending"] == 1
    assert stats["by_category"]["learning"]["accuracy"] == 0.5
    assert stats["by_category"]["career"]["accuracy"] is None
    assert stats["by_confidence_bucket"]["High"]["accuracy"] == 0.5
