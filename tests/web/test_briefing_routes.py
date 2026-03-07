"""Tests for briefing API routes."""

from types import SimpleNamespace
from unittest.mock import patch


def test_briefing_includes_daily_brief_and_feedback_count(client, auth_headers):
    data = {
        "recommendations": [
            {
                "id": "rec-1",
                "category": "projects",
                "title": "Ship MVP",
                "description": "Scope tightly",
                "score": 9.1,
                "status": "suggested",
                "reasoning_trace": None,
                "critic": None,
            }
        ],
        "stale_goals": [{"path": "goal-1.md", "title": "Learn Rust", "status": "active", "days_since_check": 12}],
        "all_goals": [{"path": "goal-1.md", "title": "Learn Rust", "status": "active", "days_since_check": 12}],
        "goal_intel_matches": [
            {
                "id": 1,
                "goal_path": "goal-1.md",
                "goal_title": "Learn Rust",
                "url": "https://example.com/rust",
                "title": "Rust update",
                "summary": "New release",
                "score": 0.8,
                "urgency": "medium",
                "match_reasons": ["matches goal"],
                "created_at": "2026-03-07T00:00:00",
                "llm_evaluated": False,
            }
        ],
    }
    brief = SimpleNamespace(
        items=[
            SimpleNamespace(
                kind="stale_goal",
                title="Check in on Learn Rust",
                description="Goal has gone quiet",
                time_minutes=15,
                action="Open goal",
                priority=9,
            )
        ],
        budget_minutes=60,
        used_minutes=15,
        generated_at="2026-03-07T08:00:00",
    )

    with patch("web.routes.briefing.assemble_briefing_data", return_value=data), patch(
        "web.routes.briefing.get_feedback_count", return_value=4
    ), patch("advisor.daily_brief.DailyBriefBuilder.build", return_value=brief):
        response = client.get("/api/briefing?max_recommendations=5", headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert body["has_data"] is True
    assert body["adaptation_count"] == 4
    assert body["recommendations"][0]["title"] == "Ship MVP"
    assert body["daily_brief"]["budget_minutes"] == 60
    assert body["daily_brief"]["items"][0]["title"] == "Check in on Learn Rust"
    assert body["goal_intel_matches"][0]["goal_title"] == "Learn Rust"


def test_briefing_gracefully_skips_daily_brief_failures(client, auth_headers):
    data = {
        "recommendations": [],
        "stale_goals": [],
        "all_goals": [],
        "goal_intel_matches": [],
    }

    with patch("web.routes.briefing.assemble_briefing_data", return_value=data), patch(
        "web.routes.briefing.get_feedback_count", side_effect=RuntimeError("feedback down")
    ), patch("advisor.daily_brief.DailyBriefBuilder.build", side_effect=RuntimeError("brief failed")):
        response = client.get("/api/briefing", headers=auth_headers)

    assert response.status_code == 200
    assert response.json() == {
        "recommendations": [],
        "stale_goals": [],
        "goals": [],
        "has_data": False,
        "adaptation_count": 0,
        "daily_brief": None,
        "goal_intel_matches": [],
    }
