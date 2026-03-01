"""Tests for onboarding API routes (start, chat, completion, feed selection)."""

from unittest.mock import patch

from web.user_store import get_user_rss_feeds

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


# --- Feed category / selection tests ---


def test_get_feed_categories(client, auth_headers):
    """Returns all categories, general_tech always preselected."""
    res = client.get("/api/onboarding/feed-categories", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 10
    ids = {c["id"] for c in data}
    assert "general_tech" in ids
    assert "ai_ml" in ids
    # general_tech should be preselected even without a profile
    gt = next(c for c in data if c["id"] == "general_tech")
    assert gt["preselected"] is True
    # All items have expected fields
    for c in data:
        assert "id" in c
        assert "label" in c
        assert "icon" in c
        assert "feed_count" in c
        assert c["feed_count"] > 0


def test_get_feed_categories_with_profile(client, auth_headers, tmp_path):
    """Profile interests drive preselections."""
    # Create a profile with AI interests
    from profile.storage import ProfileStorage, UserProfile

    # Find the profile path from mock_user_paths
    base = tmp_path / "users" / "user-123"
    base.mkdir(parents=True, exist_ok=True)
    profile_path = base / "profile.yaml"

    profile = UserProfile(
        interests=["machine learning", "AI"], technologies_watching=["kubernetes"]
    )
    storage = ProfileStorage(profile_path)
    storage.save(profile)

    with patch("web.routes.onboarding.get_user_paths") as mock_paths:
        mock_paths.return_value = {
            "journal_dir": base / "journal",
            "chroma_dir": base / "chroma",
            "recommendations_dir": base / "recommendations",
            "learning_paths_dir": base / "learning_paths",
            "profile": profile_path,
            "intel_db": tmp_path / "intel.db",
        }
        res = client.get("/api/onboarding/feed-categories", headers=auth_headers)

    assert res.status_code == 200
    data = res.json()
    ai = next(c for c in data if c["id"] == "ai_ml")
    assert ai["preselected"] is True
    devops = next(c for c in data if c["id"] == "devops_cloud")
    assert devops["preselected"] is True


def test_set_feeds_saves_to_db(client, auth_headers):
    """Selected categories result in feeds in user_rss_feeds."""
    res = client.post(
        "/api/onboarding/feeds",
        headers=auth_headers,
        json={"selected_category_ids": ["ai_ml", "security"]},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["feeds_added"] >= 5  # ai_ml(4) + security(3) = 7
    assert "ai_ml" in data["categories"]
    assert "security" in data["categories"]

    # Verify feeds are in DB
    feeds = get_user_rss_feeds("user-123")
    assert len(feeds) >= 5
    urls = {f["url"] for f in feeds}
    assert "https://rss.arxiv.org/rss/cs.AI" in urls


def test_set_feeds_empty_selection_fallback(client, auth_headers):
    """Empty selection gets general_tech feeds via padding."""
    res = client.post(
        "/api/onboarding/feeds",
        headers=auth_headers,
        json={"selected_category_ids": []},
    )
    assert res.status_code == 200
    data = res.json()
    # Empty selection → feeds_for_categories returns [] then pads with general_tech
    assert data["feeds_added"] >= 4  # general_tech has 4 feeds


def test_set_feeds_idempotent(client, auth_headers):
    """Calling twice doesn't error or duplicate feeds."""
    payload = {"selected_category_ids": ["web_dev"]}
    res1 = client.post("/api/onboarding/feeds", headers=auth_headers, json=payload)
    assert res1.status_code == 200
    count1 = res1.json()["feeds_added"]

    res2 = client.post("/api/onboarding/feeds", headers=auth_headers, json=payload)
    assert res2.status_code == 200
    count2 = res2.json()["feeds_added"]

    # Both succeed with same count (UPSERT semantics)
    assert count1 == count2

    # No duplicates in DB
    feeds = get_user_rss_feeds("user-123")
    urls = [f["url"] for f in feeds]
    assert len(urls) == len(set(urls))
