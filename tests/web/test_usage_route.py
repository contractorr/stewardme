"""Tests for GET /api/settings/usage endpoint."""

from web.user_store import log_event


def test_usage_empty(client, auth_headers):
    """No events → empty response."""
    resp = client.get("/api/settings/usage", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_queries"] == 0
    assert data["total_estimated_cost_usd"] == 0.0
    assert data["by_model"] == []
    assert data["days"] == 30


def test_usage_with_events(client, auth_headers):
    """Events with token metadata show up aggregated by model."""
    # Seed two events for user-123
    log_event(
        "chat_query",
        "user-123",
        {
            "latency_ms": 500,
            "model": "claude-sonnet-4-6",
            "input_tokens": 1000,
            "output_tokens": 200,
            "billed_input_tokens": 1000.0,
            "estimated_cost_usd": 0.006,
        },
    )
    log_event(
        "chat_query",
        "user-123",
        {
            "latency_ms": 300,
            "model": "claude-sonnet-4-6",
            "input_tokens": 800,
            "output_tokens": 150,
            "billed_input_tokens": 800.0,
            "estimated_cost_usd": 0.00465,
        },
    )

    resp = client.get("/api/settings/usage", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_queries"] == 2
    assert data["total_estimated_cost_usd"] > 0
    assert len(data["by_model"]) == 1
    model = data["by_model"][0]
    assert model["model"] == "claude-sonnet-4-6"
    assert model["query_count"] == 2
    assert model["input_tokens"] == 1800
    assert model["output_tokens"] == 350


def test_usage_user_isolation(client, auth_headers, auth_headers_b):
    """Events from user B don't appear in user A's stats."""
    log_event(
        "chat_query",
        "user-456",
        {
            "latency_ms": 100,
            "model": "gpt-4o",
            "input_tokens": 500,
            "output_tokens": 100,
            "billed_input_tokens": 500.0,
            "estimated_cost_usd": 0.002,
        },
    )
    resp = client.get("/api/settings/usage", headers=auth_headers)
    data = resp.json()
    # user-123 should have no gpt-4o events
    gpt_models = [m for m in data["by_model"] if m["model"] == "gpt-4o"]
    assert gpt_models == []


def test_usage_custom_days(client, auth_headers):
    """Custom days param is accepted."""
    resp = client.get("/api/settings/usage?days=7", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["days"] == 7


def test_usage_no_token_metadata(client, auth_headers):
    """Events without token metadata still count as queries."""
    log_event("chat_query", "user-123", {"latency_ms": 200})
    resp = client.get("/api/settings/usage", headers=auth_headers)
    assert resp.status_code == 200
    # Should have at least one query (from this or prior tests in the session)
    assert resp.json()["total_queries"] >= 1
