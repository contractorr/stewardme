"""Tests for prediction web API routes."""

from datetime import datetime, timedelta

from predictions.store import Prediction, PredictionStore


def test_list_empty(client, auth_headers, tmp_path):
    res = client.get("/api/predictions", headers=auth_headers)
    assert res.status_code == 200
    assert res.json() == []


def test_list_with_predictions(client, auth_headers, tmp_path):
    # Insert via store using same intel_db path the client fixture uses
    from web.deps import get_user_paths

    paths = get_user_paths("user-123")
    store = PredictionStore(paths["intel_db"])
    store.save(
        Prediction(
            category="learning",
            claim_text="test claim",
            evaluation_due=(datetime.now() + timedelta(days=30)).isoformat(),
        )
    )

    res = client.get("/api/predictions", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["claim_text"] == "test claim"


def test_stats(client, auth_headers, tmp_path):
    res = client.get("/api/predictions/stats", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert "total" in data
    assert "by_outcome" in data


def test_review_due(client, auth_headers, tmp_path):
    from web.deps import get_user_paths

    paths = get_user_paths("user-123")
    store = PredictionStore(paths["intel_db"])
    store.save(
        Prediction(
            category="career",
            claim_text="past due",
            evaluation_due=(datetime.now() - timedelta(days=5)).isoformat(),
        )
    )

    res = client.get("/api/predictions/review", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["claim_text"] == "past due"


def test_record_outcome(client, auth_headers, tmp_path):
    from web.deps import get_user_paths

    paths = get_user_paths("user-123")
    store = PredictionStore(paths["intel_db"])
    pred = Prediction(
        category="learning",
        claim_text="will confirm",
        evaluation_due=(datetime.now() - timedelta(days=1)).isoformat(),
    )
    store.save(pred)

    res = client.post(
        f"/api/predictions/{pred.id}/review",
        json={"outcome": "confirmed", "notes": "yes"},
        headers=auth_headers,
    )
    assert res.status_code == 200
    assert res.json()["ok"] is True

    # Verify persisted
    all_preds = store.get_all()
    assert all_preds[0]["outcome"] == "confirmed"
