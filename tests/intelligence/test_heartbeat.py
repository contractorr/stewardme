"""Tests for heartbeat pipeline: filter, evaluator, store, pipeline."""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from intelligence.heartbeat import (
    ActionBrief,
    ActionBriefStore,
    HeartbeatEvaluator,
    HeartbeatFilter,
    HeartbeatPipeline,
    ScoredItem,
)


# --- Fixtures ---


@pytest.fixture
def tmp_db(tmp_path):
    return tmp_path / "test_intel.db"


@pytest.fixture
def store(tmp_db):
    return ActionBriefStore(tmp_db)


def _goal(title="Learn Python web development", path="goals/python-web.md", tags=None):
    return {
        "title": title,
        "path": path,
        "status": "active",
        "tags": tags or ["python", "web"],
    }


def _item(
    title="New Python Framework Released",
    url="https://example.com/1",
    summary="A new python web framework for building APIs",
    source="hn",
    scraped_at=None,
    item_id=1,
):
    return {
        "id": item_id,
        "title": title,
        "url": url,
        "summary": summary,
        "source": source,
        "scraped_at": (scraped_at or datetime.now()).isoformat(),
        "tags": [],
    }


def _brief(
    url="https://example.com/1",
    title="Item 1",
    goal_id="goals/g1.md",
    urgency="medium",
    relevance=0.5,
):
    b = ActionBrief(
        intel_item_id=1,
        intel_url=url,
        intel_title=title,
        intel_summary="summary",
        relevance=relevance,
        urgency=urgency,
        suggested_action="Review",
        reasoning="Matched goal",
        related_goal_id=goal_id,
    )
    b.notification_hash = b.compute_hash()
    return b


def _scored(item=None, goal=None, composite=0.5):
    item = item or _item()
    goal = goal or _goal()
    return ScoredItem(
        intel_item=item,
        keyword_score=0.5,
        recency_score=0.5,
        source_affinity_score=0.5,
        composite_score=composite,
        matched_goal_path=str(goal.get("path", "")),
        matched_goal_title=goal.get("title", ""),
    )


# --- TestHeartbeatFilter ---


class TestHeartbeatFilter:
    def test_above_threshold_passes(self):
        goals = [_goal(title="Python web framework", tags=["python", "web"])]
        items = [_item(title="Python Web Framework Release", summary="python web development")]
        f = HeartbeatFilter(goals, threshold=0.1)
        result = f.filter(items)
        assert len(result) >= 1

    def test_below_threshold_filtered(self):
        goals = [_goal(title="Quantum computing", tags=["quantum"])]
        items = [_item(title="Sports results", summary="football scores")]
        f = HeartbeatFilter(goals, threshold=0.5)
        result = f.filter(items)
        assert len(result) == 0

    def test_empty_goals_returns_empty(self):
        f = HeartbeatFilter([], threshold=0.1)
        result = f.filter([_item()])
        assert result == []

    def test_empty_items_returns_empty(self):
        f = HeartbeatFilter([_goal()], threshold=0.1)
        result = f.filter([])
        assert result == []

    def test_dedup_per_url_keeps_best_goal(self):
        goals = [
            _goal(title="Python development", path="g/python.md", tags=["python"]),
            _goal(title="Rust systems", path="g/rust.md", tags=["rust"]),
        ]
        items = [_item(title="Python update", summary="python tools")]
        f = HeartbeatFilter(goals, threshold=0.0)
        result = f.filter(items)
        # Only one result per URL
        urls = [s.intel_item["url"] for s in result]
        assert len(urls) == len(set(urls))

    def test_recency_score_decays(self):
        goal = _goal(title="Python web", tags=["python"])
        recent = _item(
            title="Python framework",
            url="https://ex.com/1",
            summary="python",
            scraped_at=datetime.now(),
        )
        old = _item(
            title="Python framework old",
            url="https://ex.com/2",
            summary="python",
            scraped_at=datetime.now() - timedelta(hours=40),
        )
        f = HeartbeatFilter([goal], threshold=0.0)
        s_recent = f.score_item_against_goal(recent, goal)
        s_old = f.score_item_against_goal(old, goal)
        assert s_recent.recency_score > s_old.recency_score

    def test_source_affinity_preferred(self):
        goal = _goal()
        item_preferred = _item(source="hn")
        item_other = _item(source="reddit", url="https://ex.com/2")
        f = HeartbeatFilter([goal], threshold=0.0, preferred_sources=["hn"])
        s1 = f.score_item_against_goal(item_preferred, goal)
        s2 = f.score_item_against_goal(item_other, goal)
        assert s1.source_affinity_score > s2.source_affinity_score

    def test_sorted_by_composite_desc(self):
        goals = [_goal(title="Python web", tags=["python", "web"])]
        items = [
            _item(title="Python web framework", url="https://ex.com/1", summary="python web"),
            _item(title="Sports news", url="https://ex.com/2", summary="football"),
        ]
        f = HeartbeatFilter(goals, threshold=0.0)
        result = f.filter(items)
        if len(result) > 1:
            assert result[0].composite_score >= result[1].composite_score


# --- TestActionBriefStore ---


class TestActionBriefStore:
    def test_roundtrip(self, store):
        b = _brief()
        saved = store.save_briefs([b])
        assert saved == 1
        active = store.get_active()
        assert len(active) == 1
        assert active[0]["intel_url"] == b.intel_url

    def test_cooldown_dedup(self, store):
        b = _brief()
        store.save_briefs([b], cooldown_hours=4)
        saved = store.save_briefs([b], cooldown_hours=4)
        assert saved == 0

    def test_cooldown_allows_after_expiry(self, store, tmp_db):
        b = _brief()
        store.save_briefs([b], cooldown_hours=4)
        # Backdate
        with sqlite3.connect(str(tmp_db)) as conn:
            conn.execute(
                "UPDATE heartbeat_notifications SET created_at = datetime('now', '-5 hours')"
            )
        saved = store.save_briefs([b], cooldown_hours=4)
        assert saved == 1

    def test_dismiss(self, store):
        b = _brief()
        store.save_briefs([b])
        active = store.get_active()
        assert len(active) == 1
        ok = store.dismiss(active[0]["id"])
        assert ok is True
        assert store.get_active() == []

    def test_dismiss_nonexistent(self, store):
        ok = store.dismiss(999)
        assert ok is False

    def test_log_run_and_get_last_run_at(self, store):
        assert store.get_last_run_at() is None
        store.log_run({
            "started_at": datetime.now().isoformat(),
            "finished_at": datetime.now().isoformat(),
            "items_checked": 10,
            "items_passed": 3,
            "briefs_saved": 2,
            "llm_used": 1,
        })
        last = store.get_last_run_at()
        assert last is not None

    def test_cleanup_old(self, store, tmp_db):
        b = _brief()
        store.save_briefs([b])
        with sqlite3.connect(str(tmp_db)) as conn:
            conn.execute(
                "UPDATE heartbeat_notifications SET created_at = datetime('now', '-31 days')"
            )
        deleted = store.cleanup_old(days=30)
        assert deleted == 1
        assert store.get_active() == []


# --- TestHeartbeatEvaluator ---


class TestHeartbeatEvaluator:
    def test_evaluate_with_llm(self):
        provider = MagicMock()
        provider.generate.return_value = (
            "ITEM_1_RELEVANT: yes\n"
            "ITEM_1_URGENCY: high\n"
            "ITEM_1_ACTION: Read the article\n"
            "ITEM_1_REASON: Directly relevant to goal\n"
        )
        evaluator = HeartbeatEvaluator(provider=provider, budget=5)
        scored = [_scored(composite=0.6)]
        result = evaluator.evaluate(scored)
        assert len(result) == 1
        assert result[0].urgency == "high"

    def test_evaluate_drops_irrelevant(self):
        provider = MagicMock()
        provider.generate.return_value = (
            "ITEM_1_RELEVANT: no\n"
            "ITEM_1_URGENCY: drop\n"
            "ITEM_1_ACTION: none\n"
            "ITEM_1_REASON: not relevant\n"
        )
        evaluator = HeartbeatEvaluator(provider=provider, budget=5)
        scored = [_scored(composite=0.6)]
        result = evaluator.evaluate(scored)
        assert len(result) == 0

    def test_fallback_on_llm_error(self):
        provider = MagicMock()
        provider.generate.side_effect = Exception("API error")
        evaluator = HeartbeatEvaluator(provider=provider, budget=5)
        scored = [_scored(composite=0.6)]
        result = evaluator.evaluate(scored)
        # Should fall back to heuristic
        assert len(result) == 1
        assert result[0].urgency in ("high", "medium", "low")

    def test_budget_zero_uses_heuristic_only(self):
        evaluator = HeartbeatEvaluator(budget=0)
        scored = [_scored(composite=0.8)]
        result = evaluator.evaluate(scored)
        assert len(result) == 1
        assert result[0].urgency == "high"

    def test_notification_hash_set(self):
        evaluator = HeartbeatEvaluator(budget=0)
        scored = [_scored(composite=0.6)]
        result = evaluator.evaluate(scored)
        assert result[0].notification_hash != ""


# --- TestHeartbeatPipeline ---


class TestHeartbeatPipeline:
    def test_run_no_items(self, tmp_db):
        intel = MagicMock()
        intel.get_items_since.return_value = []
        pipeline = HeartbeatPipeline(
            intel_storage=intel,
            goals=[_goal()],
            db_path=tmp_db,
            config={"llm_budget_per_cycle": 0},
        )
        result = pipeline.run()
        assert result["items_checked"] == 0
        assert result["briefs_saved"] == 0

    def test_run_no_goals(self, tmp_db):
        intel = MagicMock()
        intel.get_items_since.return_value = [_item()]
        pipeline = HeartbeatPipeline(
            intel_storage=intel,
            goals=[],
            db_path=tmp_db,
            config={"llm_budget_per_cycle": 0},
        )
        result = pipeline.run()
        assert result["items_passed"] == 0

    def test_run_saves_briefs(self, tmp_db):
        intel = MagicMock()
        intel.get_items_since.return_value = [
            _item(title="Python web framework", summary="python web development"),
        ]
        pipeline = HeartbeatPipeline(
            intel_storage=intel,
            goals=[_goal(title="Python web development", tags=["python", "web"])],
            db_path=tmp_db,
            config={"heuristic_threshold": 0.0, "llm_budget_per_cycle": 0},
        )
        result = pipeline.run()
        assert result["items_checked"] == 1
        assert result["briefs_saved"] >= 1

    def test_run_logs_to_db(self, tmp_db):
        intel = MagicMock()
        intel.get_items_since.return_value = []
        pipeline = HeartbeatPipeline(
            intel_storage=intel,
            goals=[_goal()],
            db_path=tmp_db,
            config={"llm_budget_per_cycle": 0},
        )
        pipeline.run()
        store = ActionBriefStore(tmp_db)
        assert store.get_last_run_at() is not None
        runs = store.get_runs()
        assert len(runs) == 1
