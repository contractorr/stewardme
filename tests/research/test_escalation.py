"""Tests for dossier escalation persistence rules."""

from datetime import datetime, timedelta

from research.escalation import DossierEscalationEngine, DossierEscalationStore


def _context(label: str = "Acme hiring") -> dict:
    return {
        "threads": [{"id": "thread-1", "label": label, "entry_count": 6}],
        "recent_intel": [{"title": f"{label} expands", "summary": "More roles added"}],
        "watchlist": [],
        "goals": [],
        "dossiers": [],
    }


def test_dismissed_escalation_stays_suppressed(tmp_path):
    store = DossierEscalationStore(tmp_path / "escalations.db")
    engine = DossierEscalationEngine(store, min_escalation_score=0.1)

    first = engine.refresh(_context())
    assert len(first) == 1

    escalation_id = first[0]["escalation_id"]
    assert store.dismiss(escalation_id) is True

    second = engine.refresh(_context())

    assert second == []
    assert store.get(escalation_id)["state"] == "dismissed"


def test_snoozed_escalation_hidden_until_expiry(tmp_path):
    store = DossierEscalationStore(tmp_path / "escalations.db")
    engine = DossierEscalationEngine(store, min_escalation_score=0.1)

    first = engine.refresh(_context())
    escalation_id = first[0]["escalation_id"]
    snoozed_until = (datetime.now() + timedelta(days=1)).isoformat()

    assert store.snooze(escalation_id, snoozed_until) is True

    second = engine.refresh(_context())

    assert second == []
    assert store.list_active() == []
    saved = store.get(escalation_id)
    assert saved["state"] == "snoozed"
    assert saved["snoozed_until"] == snoozed_until


def test_expired_snoozed_escalation_reactivates(tmp_path):
    store = DossierEscalationStore(tmp_path / "escalations.db")
    engine = DossierEscalationEngine(store, min_escalation_score=0.1)

    first = engine.refresh(_context())
    escalation_id = first[0]["escalation_id"]
    expired = (datetime.now() - timedelta(minutes=5)).isoformat()

    assert store.snooze(escalation_id, expired) is True

    reactivated = engine.refresh(_context())

    assert len(reactivated) == 1
    saved = store.get(escalation_id)
    assert saved["state"] == "active"
    assert saved["snoozed_until"] is None


def test_accepted_escalation_is_not_reopened(tmp_path):
    store = DossierEscalationStore(tmp_path / "escalations.db")
    engine = DossierEscalationEngine(store, min_escalation_score=0.1)

    first = engine.refresh(_context())
    escalation_id = first[0]["escalation_id"]
    assert store.accept(escalation_id, "dos-123") is True

    second = engine.refresh(_context())

    assert second == []
    saved = store.get(escalation_id)
    assert saved["state"] == "accepted"
    assert saved["accepted_dossier_id"] == "dos-123"
