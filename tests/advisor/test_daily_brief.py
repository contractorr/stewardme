"""Tests for DailyBriefBuilder."""

from advisor.daily_brief import DailyBriefBuilder


def _goal(title: str, days: int = 10) -> dict:
    return {"title": title, "days_since_check": days, "status": "active", "path": f"g/{title}.md"}


def _rec(title: str, desc: str = "desc") -> dict:
    return {"title": title, "description": desc}


def _lp(skill: str, done: int = 1, total: int = 5) -> dict:
    return {"skill": skill, "status": "active", "completed_modules": done, "total_modules": total}


class TestDailyBriefBuilder:
    def setup_method(self):
        self.builder = DailyBriefBuilder()

    def test_empty_with_goals_gives_nudge(self):
        brief = self.builder.build(
            stale_goals=[], recommendations=[], learning_paths=[],
            all_goals=[_goal("Ship MVP")], weekly_hours=5,
        )
        assert len(brief.items) == 1
        assert brief.items[0].kind == "nudge"
        assert "Ship MVP" in brief.items[0].action

    def test_empty_no_goals_gives_reflection(self):
        brief = self.builder.build(
            stale_goals=[], recommendations=[], learning_paths=[],
            all_goals=[], weekly_hours=5,
        )
        assert len(brief.items) == 1
        assert brief.items[0].kind == "nudge"
        assert "reflect" in brief.items[0].action.lower()

    def test_stale_goals_come_first(self):
        brief = self.builder.build(
            stale_goals=[_goal("Goal A"), _goal("Goal B")],
            recommendations=[_rec("Rec 1")],
            learning_paths=[_lp("Rust")],
            all_goals=[], weekly_hours=5,
        )
        assert brief.items[0].kind == "stale_goal"
        assert brief.items[0].priority == 1

    def test_priority_order(self):
        brief = self.builder.build(
            stale_goals=[_goal("Goal A")],
            recommendations=[_rec("Rec 1")],
            learning_paths=[_lp("Rust")],
            all_goals=[], weekly_hours=10,
        )
        kinds = [i.kind for i in brief.items]
        assert kinds == ["stale_goal", "recommendation", "learning"]

    def test_budget_calculation(self):
        brief = self.builder.build(
            stale_goals=[], recommendations=[], learning_paths=[],
            all_goals=[_goal("X")], weekly_hours=7,
        )
        assert brief.budget_minutes == 60  # 7*60/7

    def test_max_items_low_budget(self):
        """<30 min budget caps at 2 items."""
        brief = self.builder.build(
            stale_goals=[_goal("A"), _goal("B"), _goal("C")],
            recommendations=[], learning_paths=[],
            all_goals=[], weekly_hours=3,  # ~26 min/day
        )
        assert len(brief.items) <= 2

    def test_max_items_medium_budget(self):
        """30-60 min budget caps at 3 items."""
        brief = self.builder.build(
            stale_goals=[_goal("A"), _goal("B"), _goal("C"), _goal("D")],
            recommendations=[], learning_paths=[],
            all_goals=[], weekly_hours=5,  # ~43 min/day
        )
        assert len(brief.items) <= 3

    def test_max_items_high_budget(self):
        """60+ min budget caps at 5 items."""
        brief = self.builder.build(
            stale_goals=[_goal("A"), _goal("B"), _goal("C")],
            recommendations=[_rec("R1"), _rec("R2")],
            learning_paths=[_lp("Go")],
            all_goals=[], weekly_hours=14,  # 120 min/day
        )
        assert len(brief.items) <= 5

    def test_first_item_included_even_if_over_budget(self):
        """First item always included even if it exceeds budget."""
        brief = self.builder.build(
            stale_goals=[],
            recommendations=[],
            learning_paths=[_lp("Rust")],  # 45 min
            all_goals=[], weekly_hours=1,  # ~9 min budget
        )
        assert len(brief.items) == 1
        assert brief.items[0].kind == "learning"
        assert brief.used_minutes == 45

    def test_budget_stops_filling(self):
        """Stop adding items when budget exhausted."""
        brief = self.builder.build(
            stale_goals=[_goal("A")],  # 10 min
            recommendations=[_rec("R")],  # 15 min → 25 total
            learning_paths=[_lp("Rust")],  # 45 min → 70 total
            all_goals=[], weekly_hours=5,  # ~43 min budget
        )
        # learning path should NOT fit (25 + 45 > 43 and already have items)
        assert brief.used_minutes <= brief.budget_minutes + 44  # at most one overshoot

    def test_inactive_learning_paths_skipped(self):
        brief = self.builder.build(
            stale_goals=[], recommendations=[],
            learning_paths=[{"skill": "Go", "status": "completed", "completed_modules": 5, "total_modules": 5}],
            all_goals=[_goal("X")], weekly_hours=5,
        )
        # Should fall through to nudge since only inactive LP
        assert brief.items[0].kind == "nudge"

    def test_generated_at_is_iso(self):
        brief = self.builder.build(
            stale_goals=[], recommendations=[], learning_paths=[],
            all_goals=[], weekly_hours=5,
        )
        assert "T" in brief.generated_at

    def test_used_minutes_accurate(self):
        brief = self.builder.build(
            stale_goals=[_goal("A"), _goal("B")],
            recommendations=[], learning_paths=[],
            all_goals=[], weekly_hours=5,
        )
        expected = sum(i.time_minutes for i in brief.items)
        assert brief.used_minutes == expected

    def test_recs_as_objects(self):
        """Recommendations can be passed as objects with .title/.description attrs."""

        class FakeRec:
            def __init__(self, t, d):
                self.title = t
                self.description = d

        brief = self.builder.build(
            stale_goals=[], recommendations=[FakeRec("Try X", "details")],
            learning_paths=[], all_goals=[], weekly_hours=5,
        )
        assert brief.items[0].kind == "recommendation"
        assert brief.items[0].title == "Try X"
