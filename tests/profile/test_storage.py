"""Tests for profile storage — UserProfile model + ProfileStorage CRUD."""

from datetime import datetime, timedelta
from profile.storage import ProfileStorage, Skill, UserProfile

import pytest

from shared_types import CareerStage

# ── UserProfile.is_stale ──


class TestIsStale:
    def test_no_updated_at_is_stale(self):
        p = UserProfile()
        assert p.is_stale()

    def test_recent_date_not_stale(self):
        p = UserProfile(updated_at=datetime.now().isoformat())
        assert not p.is_stale()

    def test_91_days_ago_is_stale(self):
        old = (datetime.now() - timedelta(days=91)).isoformat()
        p = UserProfile(updated_at=old)
        assert p.is_stale()

    def test_89_days_ago_not_stale(self):
        recent = (datetime.now() - timedelta(days=89)).isoformat()
        p = UserProfile(updated_at=recent)
        assert not p.is_stale()

    def test_custom_days_param(self):
        old = (datetime.now() - timedelta(days=31)).isoformat()
        p = UserProfile(updated_at=old)
        assert p.is_stale(days=30)
        assert not p.is_stale(days=60)


# ── UserProfile.summary ──


class TestSummary:
    def test_empty_profile_minimal(self):
        p = UserProfile()
        s = p.summary()
        assert "Learning style: mixed" in s

    def test_full_profile_all_sections(self):
        p = UserProfile(
            current_role="Staff Eng",
            career_stage=CareerStage.SENIOR,
            skills=[
                Skill(name="Python", proficiency=5),
                Skill(name="Go", proficiency=3),
                Skill(name="Rust", proficiency=4),
            ],
            languages_frameworks=["FastAPI", "React"],
            interests=["distributed systems", "ML"],
            aspirations="CTO at a startup",
            goals_short_term="Ship v2",
            goals_long_term="Start a company",
            industries_watching=["fintech"],
            technologies_watching=["WebAssembly"],
            active_projects=["ai-coach"],
            fears_risks=["burnout"],
            location="SF",
            constraints={"time_per_week": 10, "geography": "US West", "budget_sensitivity": "low"},
            learning_style="hands-on",
        )
        s = p.summary()
        assert "Staff Eng" in s
        assert "Python(5)" in s  # sorted by proficiency desc
        assert "FastAPI" in s
        assert "distributed systems" in s
        assert "CTO" in s
        assert "Ship v2" in s
        assert "Start a company" in s
        assert "fintech" in s
        assert "WebAssembly" in s
        assert "ai-coach" in s
        assert "burnout" in s
        assert "SF" in s
        assert "10h/week" in s
        assert "US West" in s
        assert "budget: low" in s

    def test_constraints_dict_suppresses_weekly_hours_fallback(self):
        p = UserProfile(
            constraints={"time_per_week": 15},
            weekly_hours_available=5,
        )
        s = p.summary()
        assert "15h/week" in s
        assert "Available: 5h/week" not in s

    def test_no_constraints_uses_weekly_hours(self):
        p = UserProfile(weekly_hours_available=8)
        s = p.summary()
        assert "Available: 8h/week" in s


# ── UserProfile.structured_summary ──


class TestStructuredSummary:
    def test_empty_profile_identity_and_constraints_only(self):
        p = UserProfile()
        ss = p.structured_summary()
        assert "[IDENTITY]" in ss
        assert "[CONSTRAINTS]" in ss
        assert "[GOALS & ASPIRATIONS]" not in ss

    def test_full_profile_all_8_sections(self):
        p = UserProfile(
            current_role="Lead",
            career_stage=CareerStage.LEAD,
            location="NYC",
            goals_short_term="Scale team",
            goals_long_term="VP Eng",
            aspirations="Impact",
            skills=[
                Skill(name="Python", proficiency=5),
                Skill(name="TypeScript", proficiency=4),
                Skill(name="SQL", proficiency=3),
            ],
            languages_frameworks=["Django"],
            interests=["platform eng"],
            industries_watching=["healthtech"],
            technologies_watching=["LLMs"],
            active_projects=["infra-rewrite"],
            constraints={
                "time_per_week": 6,
                "geography": "East Coast",
                "budget_sensitivity": "medium",
            },
            fears_risks=["market downturn"],
            learning_style="reading",
        )
        ss = p.structured_summary()
        for section in [
            "[IDENTITY]",
            "[GOALS & ASPIRATIONS]",
            "[SKILLS]",
            "[TECH STACK]",
            "[INTERESTS & WATCHING]",
            "[ACTIVE PROJECTS]",
            "[CONSTRAINTS]",
            "[CONCERNS & RISKS]",
        ]:
            assert section in ss

    def test_skills_grouped_by_proficiency(self):
        p = UserProfile(
            skills=[
                Skill(name="Python", proficiency=5),
                Skill(name="Rust", proficiency=5),
                Skill(name="Go", proficiency=3),
            ]
        )
        ss = p.structured_summary()
        assert "Expert (5/5): Python, Rust" in ss
        assert "Intermediate (3/5): Go" in ss


# ── ProfileStorage CRUD ──


class TestProfileStorage:
    def test_save_load_round_trip(self, tmp_path):
        path = tmp_path / "profile.yaml"
        ps = ProfileStorage(path)
        orig = UserProfile(
            current_role="Dev",
            skills=[Skill(name="Go", proficiency=4)],
            interests=["infra"],
        )
        ps.save(orig)
        loaded = ps.load()
        assert loaded is not None
        assert loaded.current_role == "Dev"
        assert loaded.skills[0].name == "Go"
        assert loaded.updated_at is not None

    def test_load_returns_none_when_no_file(self, tmp_path):
        ps = ProfileStorage(tmp_path / "nope.yaml")
        assert ps.load() is None

    def test_update_field_modifies_and_persists(self, tmp_path):
        path = tmp_path / "profile.yaml"
        ps = ProfileStorage(path)
        ps.save(UserProfile(current_role="Dev"))
        updated = ps.update_field("current_role", "Staff")
        assert updated.current_role == "Staff"
        reloaded = ps.load()
        assert reloaded.current_role == "Staff"

    def test_update_field_raises_for_unknown(self, tmp_path):
        path = tmp_path / "profile.yaml"
        ps = ProfileStorage(path)
        ps.save(UserProfile())
        with pytest.raises(ValueError, match="Unknown profile field"):
            ps.update_field("nonexistent_field", "val")

    def test_get_or_empty_returns_empty_when_no_file(self, tmp_path):
        ps = ProfileStorage(tmp_path / "nope.yaml")
        p = ps.get_or_empty()
        assert isinstance(p, UserProfile)
        assert p.current_role == ""

    def test_exists_true_false(self, tmp_path):
        path = tmp_path / "profile.yaml"
        ps = ProfileStorage(path)
        assert not ps.exists()
        ps.save(UserProfile())
        assert ps.exists()
