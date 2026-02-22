"""Tests for onboarding API routes (start, chat, completion)."""

from unittest.mock import patch

_LLM_PATCH = "web.routes.onboarding._make_llm_caller"
_SAVE_PATCH = "web.routes.onboarding._save_results"


def _fake_caller(response_text):
    """Return a fake LLM caller that always returns the given text."""

    def caller(system, prompt, max_tokens=1500):
        return response_text

    return caller


def test_start_onboarding(client, auth_headers):
    with patch(_LLM_PATCH, return_value=_fake_caller("Welcome! What's your current role?")):
        res = client.post("/api/onboarding/start", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["done"] is False
    assert "Welcome" in data["message"]


def test_chat_without_start_fails(client, auth_headers):
    # Clear any existing session
    from web.routes.onboarding import _sessions

    _sessions.pop("user-123", None)

    res = client.post(
        "/api/onboarding/chat",
        headers=auth_headers,
        json={"message": "Hello"},
    )
    assert res.status_code == 400


def test_chat_continues_conversation(client, auth_headers):
    with patch(_LLM_PATCH, return_value=_fake_caller("What are your skills?")):
        client.post("/api/onboarding/start", headers=auth_headers)

    # Patch the caller inside the session
    from web.routes.onboarding import _sessions

    _sessions["user-123"]["caller"] = _fake_caller("Tell me your goals.")

    res = client.post(
        "/api/onboarding/chat",
        headers=auth_headers,
        json={"message": "I'm a senior engineer"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["done"] is False
    assert "goals" in data["message"].lower()


def test_chat_completes_with_json(client, auth_headers):
    with patch(_LLM_PATCH, return_value=_fake_caller("Starting!")):
        client.post("/api/onboarding/start", headers=auth_headers)

    completion_response = """Great, here's your profile!
```json
{"done": true, "profile": {
  "current_role": "Engineer",
  "career_stage": "senior",
  "skills": [{"name": "Python", "proficiency": 4}],
  "languages_frameworks": ["python"],
  "interests": ["AI"],
  "aspirations": "Lead a team",
  "location": "SF",
  "learning_style": "hands-on",
  "weekly_hours_available": 5
}, "goals": [
  {"title": "Learn Rust", "description": "Systems programming"}
]}
```"""

    from web.routes.onboarding import _sessions

    _sessions["user-123"]["caller"] = _fake_caller(completion_response)

    with patch(_SAVE_PATCH, return_value=1) as mock_save:
        res = client.post(
            "/api/onboarding/chat",
            headers=auth_headers,
            json={"message": "That's everything"},
        )
    assert res.status_code == 200
    data = res.json()
    assert data["done"] is True
    assert data["goals_created"] == 1
    mock_save.assert_called_once()
