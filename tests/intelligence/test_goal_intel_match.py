"""Tests for GoalIntelMatcher, GoalIntelMatchStore, and GoalIntelLLMEvaluator."""

import sqlite3
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from intelligence.goal_intel_match import (
    GoalIntelLLMEvaluator,
    GoalIntelMatcher,
    GoalIntelMatchStore,
    _URGENCY_HIGH,
    _URGENCY_LOW,
    _URGENCY_MEDIUM,
)


# --- Fixtures ---


@pytest.fixture
def tmp_db(tmp_path):
    return tmp_path / "test_intel.db"


@pytest.fixture
def store(tmp_db):
    return GoalIntelMatchStore(tmp_db)


@pytest.fixture
def mock_intel_storage():
    storage = MagicMock()
    storage.db_path = Path("/tmp/fake.db")
    return storage


@pytest.fixture
def matcher(mock_intel_storage):
    return GoalIntelMatcher(mock_intel_storage)


def _intel_item(title="Some Python Framework Released", url="https://example.com/1", summary="A new python web framework", tags=None):
    return {
        "title": title,
        "url": url,
        "summary": summary,
        "content": "",
        "tags": tags or [],
    }


def _goal(title="Learn Python web development", path="goals/python-web.md", tags=None):
    return {
        "title": title,
        "path": path,
        "status": "active",
        "tags": tags or ["python", "web"],
    }


def _match(goal_path="goals/g1.md", goal_title="Goal 1", url="https://ex.com/1", title="Item 1", score=0.2, urgency="high"):
    return {
        "goal_path": goal_path,
        "goal_title": goal_title,
        "url": url,
        "title": title,
        "summary": "summary",
        "score": score,
        "urgency": urgency,
        "match_reasons": ["skill:python"],
    }


# --- GoalIntelMatcher tests ---


class TestExtractGoalKeywords:
    def test_title_and_tags_extracted(self, matcher):
        goal = _goal(title="Learn Rust systems programming", tags=["rust", "systems"])
        keywords = matcher._extract_goal_keywords(goal)
        assert any("rust" in k for k in keywords)
        assert any("systems" in k for k in keywords)

    def test_stopwords_filtered(self, matcher):
        goal = _goal(title="Learn about the basics of programming", tags=[])
        keywords = matcher._extract_goal_keywords(goal)
        assert "the" not in keywords
        assert "about" not in keywords
        assert "basics" in keywords or "programming" in keywords

    @patch("intelligence.goal_intel_match.frontmatter")
    def test_content_from_file_included(self, mock_fm, matcher):
        mock_post = MagicMock()
        mock_post.content = "kubernetes docker containers orchestration"
        mock_post.metadata = {"tags": ["devops"]}
        mock_fm.load.return_value = mock_post

        goal = _goal(title="Deploy services", path="goals/deploy.md", tags=[])
        keywords = matcher._extract_goal_keywords(goal)
        assert "kubernetes" in keywords
        assert "docker" in keywords

    def test_capped_at_30(self, matcher):
        long_title = " ".join(f"term{i}" for i in range(50))
        goal = _goal(title=long_title, tags=[])
        keywords = matcher._extract_goal_keywords(goal)
        assert len(keywords) <= 30


class TestScoreToUrgency:
    def test_high(self):
        assert GoalIntelMatcher._score_to_urgency(_URGENCY_HIGH) == "high"
        assert GoalIntelMatcher._score_to_urgency(0.3) == "high"

    def test_medium(self):
        assert GoalIntelMatcher._score_to_urgency(_URGENCY_MEDIUM) == "medium"
        assert GoalIntelMatcher._score_to_urgency(0.12) == "medium"

    def test_low(self):
        assert GoalIntelMatcher._score_to_urgency(_URGENCY_LOW) == "low"
        assert GoalIntelMatcher._score_to_urgency(0.05) == "low"

    def test_below_threshold_returns_none(self):
        assert GoalIntelMatcher._score_to_urgency(0.01) is None
        assert GoalIntelMatcher._score_to_urgency(0.0) is None


class TestMatchGoal:
    def test_filters_below_threshold(self, matcher):
        """Items that score below low threshold are excluded."""
        # Item with no keyword overlap should be filtered
        goal = _goal(title="Quantum computing research", tags=["quantum"])
        item = _intel_item(title="Latest sports results", summary="Football scores")
        matches = matcher.match_goal(goal, [item])
        assert len(matches) == 0

    def test_matching_item_included(self, matcher):
        goal = _goal(title="Python web framework", tags=["python", "web"])
        item = _intel_item(title="New Python Web Framework", summary="python web development")
        matches = matcher.match_goal(goal, [item])
        assert len(matches) > 0
        assert matches[0]["urgency"] in ("high", "medium", "low")

    def test_sorted_by_score(self, matcher):
        goal = _goal(title="Python machine learning", tags=["python", "ml"])
        items = [
            _intel_item(title="Generic news", url="https://ex.com/1", summary="unrelated content"),
            _intel_item(title="Python ML Framework", url="https://ex.com/2", summary="python machine learning library"),
        ]
        matches = matcher.match_goal(goal, items)
        if len(matches) > 1:
            assert matches[0]["score"] >= matches[1]["score"]


class TestMatchAllGoals:
    def test_calls_get_recent_once(self, matcher, mock_intel_storage):
        """Verify single DB call for intel regardless of goal count."""
        mock_intel_storage.get_recent.return_value = [
            _intel_item(url="https://ex.com/1"),
            _intel_item(url="https://ex.com/2"),
        ]
        goals = [_goal(path="g/1.md"), _goal(path="g/2.md"), _goal(path="g/3.md")]
        matcher.match_all_goals(goals, days=7)
        mock_intel_storage.get_recent.assert_called_once_with(days=7, limit=500)

    def test_empty_intel_returns_empty(self, matcher, mock_intel_storage):
        mock_intel_storage.get_recent.return_value = []
        result = matcher.match_all_goals([_goal()])
        assert result == []

    def test_respects_limit(self, matcher, mock_intel_storage):
        mock_intel_storage.get_recent.return_value = [
            _intel_item(title=f"Python item {i}", url=f"https://ex.com/{i}", summary="python web")
            for i in range(20)
        ]
        goals = [_goal()]
        result = matcher.match_all_goals(goals, limit=5)
        assert len(result) <= 5


# --- GoalIntelMatchStore tests ---


class TestStoreSaveAndRetrieve:
    def test_roundtrip(self, store):
        matches = [_match()]
        inserted = store.save_matches(matches)
        assert inserted == 1

        results = store.get_matches()
        assert len(results) == 1
        assert results[0]["goal_title"] == "Goal 1"
        assert results[0]["match_reasons"] == ["skill:python"]
        assert results[0]["score"] == 0.2

    def test_empty_list(self, store):
        assert store.save_matches([]) == 0


class TestStoreDedup:
    def test_dedup_within_7_days(self, store):
        m = _match()
        store.save_matches([m])
        inserted = store.save_matches([m])  # same goal_path + url
        assert inserted == 0

        results = store.get_matches()
        assert len(results) == 1

    def test_dedup_allows_after_7_days(self, store, tmp_db):
        m = _match()
        store.save_matches([m])

        # Backdate the existing row to 8 days ago
        with sqlite3.connect(str(tmp_db)) as conn:
            conn.execute(
                "UPDATE goal_intel_matches SET created_at = datetime('now', '-8 days')"
            )

        inserted = store.save_matches([m])
        assert inserted == 1

        results = store.get_matches()
        assert len(results) == 2

    def test_different_url_not_deduped(self, store):
        m1 = _match(url="https://ex.com/1")
        m2 = _match(url="https://ex.com/2")
        store.save_matches([m1])
        inserted = store.save_matches([m2])
        assert inserted == 1


class TestStoreGetMatchesFilters:
    def test_filters_by_goal_paths(self, store):
        store.save_matches([
            _match(goal_path="g/a.md", url="https://ex.com/1"),
            _match(goal_path="g/b.md", url="https://ex.com/2"),
            _match(goal_path="g/c.md", url="https://ex.com/3"),
        ])
        results = store.get_matches(goal_paths=["g/a.md", "g/c.md"])
        paths = {r["goal_path"] for r in results}
        assert paths == {"g/a.md", "g/c.md"}

    def test_orders_by_urgency_then_score(self, store):
        store.save_matches([
            _match(url="https://ex.com/1", urgency="low", score=0.9),
            _match(url="https://ex.com/2", urgency="high", score=0.2),
            _match(url="https://ex.com/3", urgency="medium", score=0.5),
        ])
        results = store.get_matches()
        urgencies = [r["urgency"] for r in results]
        assert urgencies == ["high", "medium", "low"]

    def test_min_urgency_filter(self, store):
        store.save_matches([
            _match(url="https://ex.com/1", urgency="low", score=0.05),
            _match(url="https://ex.com/2", urgency="high", score=0.2),
        ])
        results = store.get_matches(min_urgency="medium")
        assert all(r["urgency"] in ("high", "medium") for r in results)


class TestStoreCleanupOld:
    def test_deletes_old_rows(self, store, tmp_db):
        store.save_matches([_match()])

        # Backdate to 31 days ago
        with sqlite3.connect(str(tmp_db)) as conn:
            conn.execute(
                "UPDATE goal_intel_matches SET created_at = datetime('now', '-31 days')"
            )

        deleted = store.cleanup_old(days=30)
        assert deleted == 1
        assert store.get_matches() == []

    def test_keeps_recent_rows(self, store):
        store.save_matches([_match()])
        deleted = store.cleanup_old(days=30)
        assert deleted == 0
        assert len(store.get_matches()) == 1


class TestInactiveGoalsSkipped:
    def test_completed_goals_not_matched(self, matcher, mock_intel_storage):
        """GoalTracker.get_goals(include_inactive=False) already filters completed goals.
        This test verifies the matcher works correctly with the pre-filtered list."""
        mock_intel_storage.get_recent.return_value = [
            _intel_item(title="Python news", summary="python update")
        ]
        # Only active goals should be passed to match_all_goals
        active_goals = [_goal(title="Active goal", path="g/active.md")]
        # Completed goal not in list (filtered by GoalTracker)
        result = matcher.match_all_goals(active_goals)
        # All matches should be for active goal only
        for m in result:
            assert m["goal_path"] == "g/active.md"


# --- GoalIntelLLMEvaluator tests ---


class TestGoalIntelLLMEvaluator:
    @patch.dict("os.environ", {}, clear=True)
    def test_is_available_false_no_keys(self):
        assert GoalIntelLLMEvaluator.is_available() is False

    @patch.dict("os.environ", {"ANTHROPIC_API_KEY": "sk-ant-test"})
    def test_is_available_true_with_key(self):
        assert GoalIntelLLMEvaluator.is_available() is True

    def test_evaluate_drops_false_positive(self):
        provider = MagicMock()
        provider.generate.return_value = (
            "ITEM_1_RELEVANT: no\n"
            "ITEM_1_URGENCY: drop\n"
            "ITEM_2_RELEVANT: yes\n"
            "ITEM_2_URGENCY: high\n"
        )
        evaluator = GoalIntelLLMEvaluator(provider=provider)
        matches = [
            _match(url="https://ex.com/1", title="False positive"),
            _match(url="https://ex.com/2", title="Real match"),
        ]
        result = evaluator.evaluate(matches)
        assert len(result) == 1
        assert result[0]["title"] == "Real match"

    def test_evaluate_overrides_urgency(self):
        provider = MagicMock()
        provider.generate.return_value = (
            "ITEM_1_RELEVANT: yes\n"
            "ITEM_1_URGENCY: high\n"
        )
        evaluator = GoalIntelLLMEvaluator(provider=provider)
        matches = [_match(urgency="medium")]
        result = evaluator.evaluate(matches)
        assert len(result) == 1
        assert result[0]["urgency"] == "high"

    def test_evaluate_fallback_on_failure(self):
        provider = MagicMock()
        provider.generate.side_effect = Exception("API error")
        evaluator = GoalIntelLLMEvaluator(provider=provider)
        matches = [_match(), _match(url="https://ex.com/2")]
        result = evaluator.evaluate(matches)
        # All original matches returned unchanged
        assert len(result) == 2

    def test_batch_size_respected(self):
        provider = MagicMock()
        provider.generate.return_value = "\n".join(
            f"ITEM_{i+1}_RELEVANT: yes\nITEM_{i+1}_URGENCY: medium"
            for i in range(20)
        )
        evaluator = GoalIntelLLMEvaluator(provider=provider)
        matches = [_match(url=f"https://ex.com/{i}") for i in range(45)]
        evaluator.evaluate(matches)
        assert provider.generate.call_count == 3  # 20 + 20 + 5

    def test_llm_evaluated_flag_set(self):
        provider = MagicMock()
        provider.generate.return_value = (
            "ITEM_1_RELEVANT: yes\n"
            "ITEM_1_URGENCY: medium\n"
        )
        evaluator = GoalIntelLLMEvaluator(provider=provider)
        matches = [_match()]
        result = evaluator.evaluate(matches)
        assert len(result) == 1
        assert result[0]["llm_evaluated"] == 1

    def test_llm_evaluated_flag_absent_on_fallback(self):
        provider = MagicMock()
        provider.generate.side_effect = Exception("fail")
        evaluator = GoalIntelLLMEvaluator(provider=provider)
        matches = [_match()]
        result = evaluator.evaluate(matches)
        assert result[0].get("llm_evaluated", 0) == 0

    def test_store_llm_evaluated_roundtrip(self, store):
        m = _match()
        m["llm_evaluated"] = 1
        store.save_matches([m])
        results = store.get_matches()
        assert results[0]["llm_evaluated"] == 1

    def test_schema_migration_idempotent(self, tmp_db):
        """Double-init should not crash."""
        s1 = GoalIntelMatchStore(tmp_db)
        s2 = GoalIntelMatchStore(tmp_db)
        # Both should work fine
        s2.save_matches([_match()])
        assert len(s2.get_matches()) == 1
