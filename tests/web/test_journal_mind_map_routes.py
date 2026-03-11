def test_generate_and_fetch_journal_mind_map(client, auth_headers):
    from web.conversation_store import add_message, create_conversation

    create_res = client.post(
        "/api/journal",
        headers=auth_headers,
        json={
            "content": (
                "I need to focus on finishing my PM portfolio and I am blocked by weak case studies. "
                "I am working on career direction and want a clearer weekly plan."
            ),
            "entry_type": "reflection",
            "title": "Career review",
            "tags": ["career", "portfolio"],
        },
    )
    path = create_res.json()["path"]

    client.post(
        "/api/journal",
        headers=auth_headers,
        json={
            "content": "Research notes on PM portfolio hiring trends and stronger case studies.",
            "entry_type": "research",
            "title": "Research: PM portfolio hiring trends",
            "tags": ["research", "career", "portfolio"],
        },
    )

    conv_id = create_conversation("user-123", "Portfolio chat")
    add_message(
        conv_id,
        "user",
        "I need help improving PM portfolio case studies before the next interview loop.",
    )

    generate_res = client.post(f"/api/journal/{path}/mind-map", headers=auth_headers)
    assert generate_res.status_code == 200
    generated = generate_res.json()
    assert generated["status"] == "ready"
    assert generated["mind_map"]["entry_title"] == "Career review"
    assert len(generated["mind_map"]["nodes"]) >= 3
    kinds = {node["kind"] for node in generated["mind_map"]["nodes"]}
    assert "research" in kinds or "conversation" in kinds

    fetch_res = client.get(f"/api/journal/{path}/mind-map", headers=auth_headers)
    assert fetch_res.status_code == 200
    fetched = fetch_res.json()
    assert fetched["status"] == "ready"
    assert fetched["mind_map"]["entry_path"] == path


def test_update_entry_invalidates_cached_journal_mind_map(client, auth_headers):
    create_res = client.post(
        "/api/journal",
        headers=auth_headers,
        json={
            "content": (
                "I need to focus on interview preparation and I am working on product strategy."
            ),
            "entry_type": "reflection",
            "title": "Interview prep",
        },
    )
    path = create_res.json()["path"]

    client.post(f"/api/journal/{path}/mind-map", headers=auth_headers)

    update_res = client.put(
        f"/api/journal/{path}",
        headers=auth_headers,
        json={"content": "Short update.", "metadata": {"title": "Interview prep updated"}},
    )
    assert update_res.status_code == 200

    fetch_res = client.get(f"/api/journal/{path}/mind-map", headers=auth_headers)
    assert fetch_res.status_code == 200
    assert fetch_res.json() == {"status": "not_available", "mind_map": None}


def test_generate_journal_mind_map_reports_insufficient_signal(client, auth_headers):
    create_res = client.post(
        "/api/journal",
        headers=auth_headers,
        json={
            "content": "Tired today.",
            "entry_type": "reflection",
            "title": "Quick note",
        },
    )
    path = create_res.json()["path"]

    generate_res = client.post(f"/api/journal/{path}/mind-map", headers=auth_headers)
    assert generate_res.status_code == 200
    assert generate_res.json() == {"status": "insufficient_signal", "mind_map": None}

    fetch_res = client.get(f"/api/journal/{path}/mind-map", headers=auth_headers)
    assert fetch_res.status_code == 200
    assert fetch_res.json() == {"status": "not_available", "mind_map": None}
