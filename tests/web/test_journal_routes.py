"""Tests for journal API routes."""


def test_list_empty(client, auth_headers):
    res = client.get("/api/journal", headers=auth_headers)
    assert res.status_code == 200
    assert res.json() == []


def test_create_entry(client, auth_headers):
    res = client.post(
        "/api/journal",
        headers=auth_headers,
        json={"content": "Test journal entry", "entry_type": "daily", "title": "Test"},
    )
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "Test"
    assert data["type"] == "daily"
    assert data["content"] == "Test journal entry"


def test_create_and_list(client, auth_headers):
    client.post(
        "/api/journal",
        headers=auth_headers,
        json={"content": "Entry one", "entry_type": "daily"},
    )
    client.post(
        "/api/journal",
        headers=auth_headers,
        json={"content": "Entry two", "entry_type": "reflection"},
    )
    res = client.get("/api/journal", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_create_invalid_type(client, auth_headers):
    res = client.post(
        "/api/journal",
        headers=auth_headers,
        json={"content": "Bad", "entry_type": "invalid"},
    )
    assert res.status_code == 400


def test_delete_entry(client, auth_headers):
    create_res = client.post(
        "/api/journal",
        headers=auth_headers,
        json={"content": "To delete", "entry_type": "daily", "title": "Delete Me"},
    )
    path = create_res.json()["path"]
    del_res = client.delete(f"/api/journal/{path}", headers=auth_headers)
    assert del_res.status_code == 204
