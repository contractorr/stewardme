"""Tests for goals API routes."""


def test_list_empty(client, auth_headers):
    res = client.get("/api/goals", headers=auth_headers)
    assert res.status_code == 200
    assert res.json() == []


def test_create_goal(client, auth_headers):
    res = client.post(
        "/api/goals",
        headers=auth_headers,
        json={"title": "Learn Rust", "content": "Systems programming goal"},
    )
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "Learn Rust"
    assert "path" in data


def test_create_and_list(client, auth_headers):
    client.post(
        "/api/goals",
        headers=auth_headers,
        json={"title": "Goal 1"},
    )
    res = client.get("/api/goals", headers=auth_headers)
    assert res.status_code == 200
    goals = res.json()
    assert len(goals) == 1
    assert goals[0]["title"] == "Goal 1"
