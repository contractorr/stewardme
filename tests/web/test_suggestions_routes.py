"""Tests for suggestions API routes."""

from types import SimpleNamespace
from unittest.mock import patch


def test_suggestions_merge_brief_and_recommendations(client, auth_headers):
    briefing_data = {
        "stale_goals": [],
        "all_goals": [],
        "goal_intel_matches": [],
        "recommendations": [
            {"title": "Ship weekly review", "description": "Do the review", "score": 8.5},
            {"title": "Explore Rust tooling", "description": "Evaluate cargo tools", "score": 7.0},
        ],
    }
    brief = SimpleNamespace(
        items=[
            SimpleNamespace(
                kind="nudge",
                title="Ship weekly review",
                description="Prompted from brief",
                action="Open weekly review",
                priority=10,
            ),
            SimpleNamespace(
                kind="intel_match",
                title="Read AI infra update",
                description="New infra release",
                action="Open source item",
                priority=8,
            ),
        ]
    )

    with patch("web.routes.suggestions.assemble_briefing_data", return_value=briefing_data), patch(
        "advisor.daily_brief.DailyBriefBuilder.build", return_value=brief
    ):
        response = client.get("/api/suggestions?limit=10", headers=auth_headers)

    assert response.status_code == 200
    assert response.json() == [
        {
            "source": "brief",
            "kind": "nudge",
            "title": "Ship weekly review",
            "description": "Prompted from brief",
            "action": "Open weekly review",
            "priority": 10,
            "score": 0.0,
        },
        {
            "source": "brief",
            "kind": "intel_match",
            "title": "Read AI infra update",
            "description": "New infra release",
            "action": "Open source item",
            "priority": 8,
            "score": 0.0,
        },
        {
            "source": "recommendation",
            "kind": "recommendation",
            "title": "Explore Rust tooling",
            "description": "Evaluate cargo tools",
            "action": "Tell me more about: Explore Rust tooling",
            "priority": 0,
            "score": 7.0,
        },
    ]


def test_suggestions_falls_back_to_recommendations_when_brief_fails(client, auth_headers):
    briefing_data = {
        "stale_goals": [],
        "all_goals": [],
        "goal_intel_matches": [],
        "recommendations": [
            {"title": "Review roadmap", "description": "Tighten scope", "score": 6.5}
        ],
    }

    with patch("web.routes.suggestions.assemble_briefing_data", return_value=briefing_data), patch(
        "advisor.daily_brief.DailyBriefBuilder.build", side_effect=RuntimeError("brief failed")
    ):
        response = client.get("/api/suggestions", headers=auth_headers)

    assert response.status_code == 200
    assert response.json() == [
        {
            "source": "recommendation",
            "kind": "recommendation",
            "title": "Review roadmap",
            "description": "Tighten scope",
            "action": "Tell me more about: Review roadmap",
            "priority": 0,
            "score": 6.5,
        }
    ]
