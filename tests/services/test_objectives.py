"""Tests for the objectives gate-pulse loader and renderer."""

from datetime import date

import pytest
from pydantic import ValidationError

from services.objectives import Gate, Objectives, load_objectives, render_gate_pulse

VALID_YAML = """\
last_reviewed: 2026-07-02
gates:
  - name: LP discovery conversations
    target: 15
    current: 4
  - name: Paid concierge pilots
    target: 3
    current: 1
clock:
  runway_ends: 2028-06
  go_no_go: 2026-11-01
"""


class TestLoader:
    def test_loads_valid_file(self, tmp_path):
        path = tmp_path / "objectives.yaml"
        path.write_text(VALID_YAML)

        obj = load_objectives(path)

        assert obj is not None
        assert obj.last_reviewed == date(2026, 7, 2)
        assert [g.name for g in obj.gates] == [
            "LP discovery conversations",
            "Paid concierge pilots",
        ]
        assert obj.gates[0].target == 15
        assert obj.clock.go_no_go == date(2026, 11, 1)
        assert obj.clock.runway_ends == "2028-06"

    def test_absent_file_returns_none(self, tmp_path):
        assert load_objectives(tmp_path / "objectives.yaml") is None

    def test_empty_file_returns_none(self, tmp_path):
        path = tmp_path / "objectives.yaml"
        path.write_text("")
        assert load_objectives(path) is None

    def test_invalid_schema_returns_none_without_raising(self, tmp_path):
        path = tmp_path / "objectives.yaml"
        path.write_text("gates:\n  - name: X\n    target: not-a-number\n")
        assert load_objectives(path) is None

    def test_invalid_yaml_returns_none(self, tmp_path):
        path = tmp_path / "objectives.yaml"
        path.write_text("gates: [unclosed")
        assert load_objectives(path) is None

    def test_default_path_under_coach_home(self, tmp_path, monkeypatch):
        monkeypatch.setenv("COACH_HOME", str(tmp_path))
        (tmp_path / "objectives.yaml").write_text(VALID_YAML)
        assert load_objectives() is not None

    def test_model_validates_gate_target(self):
        with pytest.raises(ValidationError):
            Gate.model_validate({"name": "X", "target": "not-a-number"})


class TestRenderGatePulse:
    def _objectives(self, **overrides):
        data = {
            "last_reviewed": date(2026, 7, 2),
            "gates": [
                {"name": "LP discovery conversations", "target": 15, "current": 4},
                {"name": "Paid concierge pilots", "target": 3, "current": 1},
            ],
            "clock": {"runway_ends": "2028-06", "go_no_go": date(2026, 11, 1)},
        }
        data.update(overrides)
        return Objectives.model_validate(data)

    def test_renders_numbers_only(self):
        pulse = render_gate_pulse(self._objectives(), today=date(2026, 7, 2))

        lines = pulse.splitlines()
        assert lines[0] == "GATE PULSE"
        assert "- LP discovery conversations: 4 / 15" in lines
        assert "- Paid concierge pilots: 1 / 3" in lines
        assert "- go/no-go: 2026-11-01 (122 days)" in lines
        assert "- runway ends: 2028-06" in lines

    def test_none_renders_empty(self):
        assert render_gate_pulse(None) == ""

    def test_fresh_last_reviewed_has_no_staleness_line(self):
        pulse = render_gate_pulse(self._objectives(), today=date(2026, 8, 12))
        assert "stale measuring stick" not in pulse

    def test_stale_last_reviewed_prepends_one_line(self):
        pulse = render_gate_pulse(self._objectives(), today=date(2026, 8, 14))
        first = pulse.splitlines()[0]
        assert first == "objectives.yaml last reviewed 2026-07-02 — stale measuring stick."
        assert pulse.count("stale measuring stick") == 1

    def test_missing_clock_renders_gates_only(self):
        pulse = render_gate_pulse(self._objectives(clock={}), today=date(2026, 7, 2))
        assert "go/no-go" not in pulse
        assert "runway" not in pulse
        assert "- LP discovery conversations: 4 / 15" in pulse

    def test_past_go_no_go_shows_negative_days(self):
        pulse = render_gate_pulse(self._objectives(), today=date(2026, 11, 11))
        assert "(-10 days)" in pulse


class TestWeeklyReviewIntegration:
    def test_weekly_review_leads_with_pulse(self, tmp_path, monkeypatch):
        from unittest.mock import MagicMock, patch

        monkeypatch.setenv("COACH_HOME", str(tmp_path))
        (tmp_path / "objectives.yaml").write_text(VALID_YAML)

        from advisor.engine import AdvisorEngine

        engine = AdvisorEngine.__new__(AdvisorEngine)
        engine.rag = MagicMock()
        engine.rag.get_recent_entries.return_value = "entries"
        engine.rag.get_intel_context.return_value = "intel"
        engine.rag.get_recurring_thoughts_context.return_value = ""
        engine.rag.get_profile_context.return_value = ""
        with patch.object(AdvisorEngine, "_call_llm", return_value="LLM review body"):
            review = engine.weekly_review()

        assert review.startswith("GATE PULSE")
        assert "- LP discovery conversations: 4 / 15" in review
        assert review.rstrip().endswith("LLM review body")

    def test_weekly_review_unchanged_without_file(self, tmp_path, monkeypatch):
        from unittest.mock import MagicMock, patch

        monkeypatch.setenv("COACH_HOME", str(tmp_path))

        from advisor.engine import AdvisorEngine

        engine = AdvisorEngine.__new__(AdvisorEngine)
        engine.rag = MagicMock()
        engine.rag.get_recent_entries.return_value = "entries"
        engine.rag.get_intel_context.return_value = "intel"
        engine.rag.get_recurring_thoughts_context.return_value = ""
        engine.rag.get_profile_context.return_value = ""
        with patch.object(AdvisorEngine, "_call_llm", return_value="LLM review body"):
            review = engine.weekly_review()

        assert review == "LLM review body"
