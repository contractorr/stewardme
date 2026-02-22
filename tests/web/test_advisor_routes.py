"""Tests for advisor API routes (ask, streaming, conversations)."""

from unittest.mock import MagicMock, patch


def _mock_get_engine(user_id, use_tools=False):
    """Return a mock AdvisorEngine that returns canned answers."""
    engine = MagicMock()

    def _ask(question, advice_type="general", conversation_history=None, event_callback=None):
        # Fire fake tool events if callback provided
        if event_callback:
            event_callback({"type": "tool_start", "tool": "journal_search"})
            event_callback({"type": "tool_done", "tool": "journal_search", "is_error": False})
        return f"Mock advice for: {question}"

    engine.ask.side_effect = _ask
    return engine


_ENGINE_PATCH = "web.routes.advisor._get_engine"


def test_ask_returns_answer(client, auth_headers):
    with patch(_ENGINE_PATCH, side_effect=_mock_get_engine):
        res = client.post(
            "/api/advisor/ask",
            headers=auth_headers,
            json={"question": "What should I do?"},
        )
    assert res.status_code == 200
    data = res.json()
    assert "Mock advice" in data["answer"]
    assert data["advice_type"] == "general"
    assert "conversation_id" in data


def test_ask_creates_conversation(client, auth_headers):
    with patch(_ENGINE_PATCH, side_effect=_mock_get_engine):
        res = client.post(
            "/api/advisor/ask",
            headers=auth_headers,
            json={"question": "Test question"},
        )
    conv_id = res.json()["conversation_id"]
    assert conv_id

    # Verify conversation is persisted
    res2 = client.get(f"/api/advisor/conversations/{conv_id}", headers=auth_headers)
    assert res2.status_code == 200
    assert len(res2.json()["messages"]) == 2  # user + assistant


def test_ask_with_existing_conversation(client, auth_headers):
    with patch(_ENGINE_PATCH, side_effect=_mock_get_engine):
        # First message creates conversation
        res1 = client.post(
            "/api/advisor/ask",
            headers=auth_headers,
            json={"question": "First"},
        )
        conv_id = res1.json()["conversation_id"]

        # Second message uses same conversation
        res2 = client.post(
            "/api/advisor/ask",
            headers=auth_headers,
            json={"question": "Second", "conversation_id": conv_id},
        )
    assert res2.json()["conversation_id"] == conv_id

    # Should have 4 messages total (2 user + 2 assistant)
    detail = client.get(f"/api/advisor/conversations/{conv_id}", headers=auth_headers)
    assert len(detail.json()["messages"]) == 4


def test_ask_stream_sse_events(client, auth_headers):
    with patch(_ENGINE_PATCH, side_effect=_mock_get_engine):
        res = client.post(
            "/api/advisor/ask/stream",
            headers=auth_headers,
            json={"question": "Stream me"},
        )
    assert res.status_code == 200
    assert "text/event-stream" in res.headers.get("content-type", "")

    # Parse SSE events
    events = []
    for line in res.text.strip().split("\n"):
        line = line.strip()
        if line.startswith("data: "):
            import json

            events.append(json.loads(line[6:]))

    types = [e["type"] for e in events]
    assert "tool_start" in types
    assert "tool_done" in types
    assert "answer" in types

    answer_event = next(e for e in events if e["type"] == "answer")
    assert "conversation_id" in answer_event
    assert "Mock advice" in answer_event["content"]


def test_conversations_crud(client, auth_headers):
    # List empty
    res = client.get("/api/advisor/conversations", headers=auth_headers)
    assert res.status_code == 200
    assert res.json() == []

    # Create via ask
    with patch(_ENGINE_PATCH, side_effect=_mock_get_engine):
        ask_res = client.post(
            "/api/advisor/ask",
            headers=auth_headers,
            json={"question": "Hello"},
        )
    conv_id = ask_res.json()["conversation_id"]

    # List should have 1
    res = client.get("/api/advisor/conversations", headers=auth_headers)
    assert len(res.json()) == 1

    # Get specific
    res = client.get(f"/api/advisor/conversations/{conv_id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["id"] == conv_id

    # Delete
    res = client.delete(f"/api/advisor/conversations/{conv_id}", headers=auth_headers)
    assert res.status_code == 200

    # List empty again
    res = client.get("/api/advisor/conversations", headers=auth_headers)
    assert res.json() == []


def test_conversation_isolation(client, auth_headers, auth_headers_b):
    """User A can't access User B's conversations."""
    with patch(_ENGINE_PATCH, side_effect=_mock_get_engine):
        res = client.post(
            "/api/advisor/ask",
            headers=auth_headers,
            json={"question": "Private question"},
        )
    conv_id = res.json()["conversation_id"]

    # User B can't get it
    res = client.get(f"/api/advisor/conversations/{conv_id}", headers=auth_headers_b)
    assert res.status_code == 404

    # User B can't delete it
    res = client.delete(f"/api/advisor/conversations/{conv_id}", headers=auth_headers_b)
    assert res.status_code == 404

    # User B can't send messages to it
    with patch(_ENGINE_PATCH, side_effect=_mock_get_engine):
        res = client.post(
            "/api/advisor/ask",
            headers=auth_headers_b,
            json={"question": "Hijack", "conversation_id": conv_id},
        )
    assert res.status_code == 404
