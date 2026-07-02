"""Tests for the configurable brief routes and store."""

from unittest.mock import patch


class FakeLLM:
    """Deterministic LLM stub for generator tests."""

    def __init__(self, text="Generated section body."):
        self.text = text
        self.calls = []

    def generate(self, messages, system=None, max_tokens=2000, use_thinking=False):
        self.calls.append({"messages": messages, "system": system})
        return self.text


def test_brief_config_roundtrip(client, auth_headers):
    resp = client.get("/api/v1/brief/config", headers=auth_headers)
    assert resp.status_code == 200
    default = resp.json()
    assert default["enabled"] is True
    assert default["custom_sections"] == []

    payload = {
        "enabled": True,
        "min_interval_hours": 24,
        "include_signals": True,
        "include_journal": False,
        "max_items_per_section": 5,
        "custom_sections": [
            {
                "title": "Esoteric topic",
                "instructions": "Always include a well researched summary of an esoteric but important topic.",
                "use_research": True,
            }
        ],
    }
    resp = client.put("/api/v1/brief/config", json=payload, headers=auth_headers)
    assert resp.status_code == 200
    saved = resp.json()
    assert saved["min_interval_hours"] == 24
    assert saved["include_journal"] is False
    assert len(saved["custom_sections"]) == 1
    assert saved["custom_sections"][0]["id"]  # server-assigned

    resp = client.get("/api/v1/brief/config", headers=auth_headers)
    assert resp.json() == saved


def test_brief_config_validation(client, auth_headers):
    resp = client.put(
        "/api/v1/brief/config",
        json={"min_interval_hours": 0},
        headers=auth_headers,
    )
    assert resp.status_code == 422


def test_latest_empty_state(client, auth_headers):
    resp = client.get("/api/v1/brief/latest", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["brief"] is None
    assert data["should_generate"] is True


def test_generate_without_llm_degrades(client, auth_headers):
    with patch("web.brief_generator._resolve_llm", return_value=(None, None, None)):
        resp = client.post("/api/v1/brief/generate", headers=auth_headers)
    assert resp.status_code == 200
    brief = resp.json()
    assert brief["status"] == "unread"
    kinds = [s["kind"] for s in brief["sections"]]
    assert "signals" in kinds
    assert "journal" in kinds
    assert brief["summary"]


def test_generate_respects_interval_and_force(client, auth_headers):
    with patch("web.brief_generator._resolve_llm", return_value=(None, None, None)):
        first = client.post("/api/v1/brief/generate", headers=auth_headers).json()
        again = client.post("/api/v1/brief/generate", headers=auth_headers).json()
        forced = client.post("/api/v1/brief/generate?force=true", headers=auth_headers).json()

    assert again["id"] == first["id"]  # inside min interval -> existing brief
    assert forced["id"] != first["id"]
    # Accumulation: next window starts where the previous one ended.
    assert forced["period_start"] == first["period_end"]


def test_generate_with_llm_and_custom_section(client, auth_headers):
    config = {
        "custom_sections": [
            {"title": "Deep cut", "instructions": "Cover an esoteric topic.", "use_research": False}
        ]
    }
    client.put("/api/v1/brief/config", json=config, headers=auth_headers)

    fake = FakeLLM("Interesting body text.")
    with patch("web.brief_generator._resolve_llm", return_value=(fake, "claude", "key")):
        resp = client.post("/api/v1/brief/generate?force=true", headers=auth_headers)

    assert resp.status_code == 200
    brief = resp.json()
    custom = [s for s in brief["sections"] if s["kind"] == "custom"]
    assert len(custom) == 1
    assert custom[0]["title"] == "Deep cut"
    assert custom[0]["body"]
    assert custom[0]["researched"] is False
    # Reset config for other tests
    client.put("/api/v1/brief/config", json={}, headers=auth_headers)


def test_read_and_dismiss_lifecycle(client, auth_headers):
    with patch("web.brief_generator._resolve_llm", return_value=(None, None, None)):
        brief = client.post("/api/v1/brief/generate?force=true", headers=auth_headers).json()

    resp = client.post(f"/api/v1/brief/{brief['id']}/read", headers=auth_headers)
    assert resp.status_code == 200
    listed = client.get("/api/v1/brief", headers=auth_headers).json()
    target = next(b for b in listed if b["id"] == brief["id"])
    assert target["status"] == "read"

    resp = client.post(f"/api/v1/brief/{brief['id']}/dismiss", headers=auth_headers)
    assert resp.status_code == 200
    listed = client.get("/api/v1/brief", headers=auth_headers).json()
    target = next(b for b in listed if b["id"] == brief["id"])
    assert target["status"] == "dismissed"

    # Dismissed briefs stay in history but can be filtered out.
    filtered = client.get("/api/v1/brief?include_dismissed=false", headers=auth_headers).json()
    assert all(b["id"] != brief["id"] for b in filtered)


def test_read_unknown_brief_404(client, auth_headers):
    resp = client.post("/api/v1/brief/nope/read", headers=auth_headers)
    assert resp.status_code == 404
    resp = client.post("/api/v1/brief/nope/dismiss", headers=auth_headers)
    assert resp.status_code == 404


def test_brief_isolation_between_users(client, auth_headers, auth_headers_b):
    with patch("web.brief_generator._resolve_llm", return_value=(None, None, None)):
        client.post("/api/v1/brief/generate?force=true", headers=auth_headers)

    resp = client.get("/api/v1/brief", headers=auth_headers_b)
    assert resp.status_code == 200
    assert resp.json() == []

    resp = client.get("/api/v1/brief/latest", headers=auth_headers_b)
    assert resp.json()["brief"] is None


def test_brief_requires_auth(client):
    resp = client.get("/api/v1/brief/latest")
    assert resp.status_code in (401, 403)
