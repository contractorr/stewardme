"""Tests for data export endpoint."""


def test_export_returns_json(client, auth_headers):
    res = client.get("/api/v1/export", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert "exported_at" in data
    assert "journal" in data
    assert "memory" in data
    assert "goals" in data
    assert "curriculum" in data
    assert "profile" in data
    assert res.headers.get("content-disposition") == "attachment; filename=coach_export.json"


def test_export_has_journal_entries(client, auth_headers):
    """Seed a journal entry, verify it appears in export."""
    client.post(
        "/api/v1/journal",
        headers=auth_headers,
        json={"content": "Export test entry", "entry_type": "daily", "title": "ExportTest"},
    )
    res = client.get("/api/v1/export", headers=auth_headers)
    data = res.json()
    assert len(data["journal"]) >= 1
    titles = [e.get("metadata", {}).get("title") for e in data["journal"]]
    assert "ExportTest" in titles


def test_export_multi_user_isolation(client, auth_headers, auth_headers_b):
    """User B cannot see user A's data."""
    client.post(
        "/api/v1/journal",
        headers=auth_headers,
        json={"content": "Private entry", "entry_type": "daily", "title": "Private"},
    )
    res = client.get("/api/v1/export", headers=auth_headers_b)
    data = res.json()
    titles = [e.get("metadata", {}).get("title") for e in data["journal"]]
    assert "Private" not in titles


def test_export_requires_auth(client):
    res = client.get("/api/v1/export")
    assert res.status_code in (401, 403)
