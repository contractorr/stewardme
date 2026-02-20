"""Multi-user isolation tests: two users can't see each other's data."""


def test_journal_isolation(client, auth_headers, auth_headers_b):
    """User A's journal entries invisible to User B."""
    # User A creates entry
    res = client.post(
        "/api/journal",
        headers=auth_headers,
        json={"content": "User A private", "entry_type": "daily", "title": "A's entry"},
    )
    assert res.status_code == 201

    # User A sees it
    res = client.get("/api/journal", headers=auth_headers)
    assert len(res.json()) == 1
    assert res.json()[0]["title"] == "A's entry"

    # User B sees nothing
    res = client.get("/api/journal", headers=auth_headers_b)
    assert len(res.json()) == 0


def test_goals_isolation(client, auth_headers, auth_headers_b):
    """User A's goals invisible to User B."""
    client.post(
        "/api/goals",
        headers=auth_headers,
        json={"title": "A's goal"},
    )

    res_a = client.get("/api/goals", headers=auth_headers)
    assert len(res_a.json()) == 1

    res_b = client.get("/api/goals", headers=auth_headers_b)
    assert len(res_b.json()) == 0


def test_settings_isolation(client, auth_headers, auth_headers_b, secret_key):
    """User A's API key not visible to User B."""
    res_a = client.get("/api/settings", headers=auth_headers)
    assert res_a.status_code == 200
    assert res_a.json()["llm_api_key_set"] is False

    res_b = client.get("/api/settings", headers=auth_headers_b)
    assert res_b.status_code == 200
    assert res_b.json()["llm_api_key_set"] is False


def test_both_users_can_create_entries(client, auth_headers, auth_headers_b):
    """Both users can independently create and list entries."""
    client.post(
        "/api/journal",
        headers=auth_headers,
        json={"content": "A entry 1", "entry_type": "daily"},
    )
    client.post(
        "/api/journal",
        headers=auth_headers,
        json={"content": "A entry 2", "entry_type": "daily"},
    )
    client.post(
        "/api/journal",
        headers=auth_headers_b,
        json={"content": "B entry 1", "entry_type": "daily"},
    )

    res_a = client.get("/api/journal", headers=auth_headers)
    assert len(res_a.json()) == 2

    res_b = client.get("/api/journal", headers=auth_headers_b)
    assert len(res_b.json()) == 1
