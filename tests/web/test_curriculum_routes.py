"""Tests for curriculum tree endpoint."""


def test_tree_endpoint(client, auth_headers):
    """GET /api/curriculum/tree returns tracks, nodes, edges."""
    # Sync catalog first
    client.post("/api/curriculum/sync", headers=auth_headers)

    resp = client.get("/api/curriculum/tree", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "tracks" in data
    assert "nodes" in data
    assert "edges" in data
    assert isinstance(data["nodes"], list)
    assert isinstance(data["edges"], list)

    # If nodes exist, check structure
    if data["nodes"]:
        node = data["nodes"][0]
        assert "id" in node
        assert "position" in node
        assert "status" in node
        assert "is_entry_point" in node
