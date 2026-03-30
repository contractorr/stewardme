"""Tests for suggestions API routes."""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch


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

    with (
        patch("web.routes.suggestions.assemble_briefing_data", return_value=briefing_data),
        patch("advisor.daily_brief.DailyBriefBuilder.build", return_value=brief),
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

    with (
        patch("web.routes.suggestions.assemble_briefing_data", return_value=briefing_data),
        patch(
            "advisor.daily_brief.DailyBriefBuilder.build", side_effect=RuntimeError("brief failed")
        ),
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


def test_suggestions_include_pipeline_intel_items(client, auth_headers):
    briefing_data = {
        "stale_goals": [],
        "all_goals": [],
        "goal_intel_matches": [],
        "recommendations": [],
        "company_movements": [
            {
                "title": "OpenAI pricing update",
                "summary": "Enterprise plan changed",
                "significance": 0.82,
            }
        ],
        "hiring_signals": [
            {"title": "Hiring signal at OpenAI", "summary": "Open roles expanded", "strength": 0.7}
        ],
        "regulatory_alerts": [
            {
                "title": "EU AI Act finalized",
                "summary": "New guidance landed",
                "urgency": "high",
                "relevance": 0.88,
            }
        ],
    }

    with (
        patch("web.routes.suggestions.assemble_briefing_data", return_value=briefing_data),
        patch(
            "advisor.daily_brief.DailyBriefBuilder.build", return_value=SimpleNamespace(items=[])
        ),
    ):
        response = client.get("/api/suggestions?limit=10", headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert body[0]["source"] == "company_movement"
    assert body[1]["source"] == "hiring_signal"
    assert body[2]["source"] == "regulatory_alert"
    assert body[2]["priority"] == 2


def test_suggestions_include_assumption_alert_items(client, auth_headers):
    briefing_data = {
        "stale_goals": [],
        "all_goals": [],
        "goal_intel_matches": [],
        "recommendations": [],
        "assumptions": [
            {
                "id": "asm-1",
                "title": "Hiring stays strong for Acme",
                "detail": "Recent layoffs undermine this assumption.",
                "status": "invalidated",
                "updated_at": "2026-03-07T00:00:00",
            }
        ],
    }

    with (
        patch("web.routes.suggestions.assemble_briefing_data", return_value=briefing_data),
        patch(
            "advisor.daily_brief.DailyBriefBuilder.build", return_value=SimpleNamespace(items=[])
        ),
    ):
        response = client.get("/api/suggestions?limit=10", headers=auth_headers)

    assert response.status_code == 200
    assert response.json() == [
        {
            "source": "assumption_alert",
            "kind": "assumption_alert",
            "title": "Hiring stays strong for Acme",
            "description": "Recent layoffs undermine this assumption.",
            "action": "Review assumption",
            "priority": 3,
            "score": 0.95,
            "payload": {
                "id": "asm-1",
                "title": "Hiring stays strong for Acme",
                "detail": "Recent layoffs undermine this assumption.",
                "status": "invalidated",
                "updated_at": "2026-03-07T00:00:00",
            },
            "why_now": [
                {
                    "code": "assumption_invalidated",
                    "label": "Assumption may be invalid",
                    "severity": "warning",
                    "detail": {
                        "status": "invalidated",
                        "evidence_summary": "Recent layoffs undermine this assumption.",
                    },
                }
            ],
        }
    ]


def test_suggestions_suppress_dossier_escalation_when_active_dossier_exists(client, auth_headers):
    briefing_data = {
        "stale_goals": [],
        "all_goals": [],
        "goal_intel_matches": [],
        "recommendations": [],
        "company_movements": [],
        "hiring_signals": [],
        "regulatory_alerts": [],
    }

    with (
        patch("web.routes.suggestions.assemble_briefing_data", return_value=briefing_data),
        patch("web.routes.suggestions.build_daily_brief_payload", return_value={"items": []}),
        patch(
            "web.routes.suggestions.load_dossier_escalation_context",
            return_value={
                "threads": [{"label": "Acme hiring", "entry_count": 6, "id": "thread-1"}],
                "recent_intel": [{"title": "Acme hiring expands", "summary": "More roles added"}],
                "watchlist": [],
                "goals": [],
                "dossiers": [{"topic": "Acme hiring", "title": "Acme hiring"}],
            },
        ),
    ):
        response = client.get("/api/suggestions?limit=10", headers=auth_headers)

    assert response.status_code == 200
    assert all(item["kind"] != "dossier_escalation" for item in response.json())


def test_suggestions_include_learning_guide_candidates(client, auth_headers):
    briefing_data = {
        "stale_goals": [],
        "all_goals": [],
        "goal_intel_matches": [],
        "recommendations": [
            {
                "id": "rec-guide-1",
                "category": "learning",
                "title": "AI Pricing Strategy",
                "description": "You keep returning to pricing questions that the current catalog does not cover.",
                "score": 8.9,
                "recommendation_kind": "learning_guide_candidate",
                "guide_candidate": {
                    "topic": "AI Pricing Strategy",
                    "depth": "practitioner",
                    "audience": "Product or strategy operators",
                    "time_budget": "3 focused sessions",
                    "instruction": "Focus on SaaS and usage-based pricing trade-offs.",
                    "confidence": 0.91,
                    "rationale": "The user keeps returning to pricing questions.",
                    "approval_required": True,
                },
            }
        ],
    }

    thread_service = MagicMock()
    thread_service.list_inbox = AsyncMock(return_value=[])
    watchlist_store = MagicMock()
    watchlist_store.list_items.return_value = []

    with (
        patch("web.routes.suggestions.assemble_briefing_data", return_value=briefing_data),
        patch("web.routes.suggestions.build_daily_brief_payload", return_value={"items": []}),
        patch("web.routes.suggestions.get_thread_inbox_service", return_value=thread_service),
        patch("web.routes.suggestions.get_watchlist_store", return_value=watchlist_store),
        patch("curriculum.assistant_actions.find_matching_guides", return_value=[]),
    ):
        response = client.get("/api/suggestions?limit=10", headers=auth_headers)

    assert response.status_code == 200
    assert response.json() == [
        {
            "source": "learning_guide_candidate",
            "kind": "learning_guide_candidate",
            "title": "AI Pricing Strategy",
            "description": "You keep returning to pricing questions that the current catalog does not cover.",
            "action": "Ask the assistant to create this guide",
            "priority": 1,
            "score": 8.9,
            "why_now": [
                {
                    "code": "missing_learning_topic",
                    "label": "Missing topic worth studying",
                    "severity": "info",
                    "detail": {
                        "topic": "AI Pricing Strategy",
                        "rationale": "You keep returning to pricing questions that the current catalog does not cover.",
                    },
                },
                {
                    "code": "high_confidence_candidate",
                    "label": "High-confidence proposal",
                    "severity": "info",
                    "detail": {"confidence": 0.91},
                },
            ],
            "payload": {
                "recommendation_id": "rec-guide-1",
                "topic": "AI Pricing Strategy",
                "depth": "practitioner",
                "audience": "Product or strategy operators",
                "time_budget": "3 focused sessions",
                "instruction": "Focus on SaaS and usage-based pricing trade-offs.",
                "confidence": 0.91,
                "approval_required": True,
            },
        }
    ]


def test_suggestions_suppress_learning_guide_candidate_when_guide_exists(client, auth_headers):
    briefing_data = {
        "stale_goals": [],
        "all_goals": [],
        "goal_intel_matches": [],
        "recommendations": [
            {
                "id": "rec-guide-1",
                "category": "learning",
                "title": "AI Pricing Strategy",
                "description": "Missing topic suggestion.",
                "score": 8.9,
                "recommendation_kind": "learning_guide_candidate",
                "guide_candidate": {
                    "topic": "AI Pricing Strategy",
                    "depth": "practitioner",
                    "audience": "Operators",
                    "time_budget": "3 focused sessions",
                    "confidence": 0.91,
                    "approval_required": True,
                },
            }
        ],
    }

    thread_service = MagicMock()
    thread_service.list_inbox = AsyncMock(return_value=[])
    watchlist_store = MagicMock()
    watchlist_store.list_items.return_value = []

    with (
        patch("web.routes.suggestions.assemble_briefing_data", return_value=briefing_data),
        patch("web.routes.suggestions.build_daily_brief_payload", return_value={"items": []}),
        patch("web.routes.suggestions.get_thread_inbox_service", return_value=thread_service),
        patch("web.routes.suggestions.get_watchlist_store", return_value=watchlist_store),
        patch(
            "curriculum.assistant_actions.find_matching_guides",
            return_value=[{"id": "existing-guide", "title": "AI Pricing Strategy", "score": 0.94}],
        ),
    ):
        response = client.get("/api/suggestions?limit=10", headers=auth_headers)

    assert response.status_code == 200
    assert response.json() == []
