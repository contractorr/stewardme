"""Tests for API versioning middleware."""


def test_v1_health(client):
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}
    assert "Deprecation" not in res.headers


def test_old_health_no_deprecation(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert "Deprecation" not in res.headers


def test_old_path_deprecation_header(client, auth_headers):
    res = client.get("/api/settings", headers=auth_headers)
    assert res.status_code == 200
    assert res.headers.get("Deprecation") == "true"


def test_v1_path_no_deprecation(client, auth_headers):
    res = client.get("/api/v1/settings", headers=auth_headers)
    assert res.status_code == 200
    assert "Deprecation" not in res.headers


def test_v1_nested_path(client, auth_headers):
    """Nested v1 paths rewrite correctly."""
    res = client.get("/api/v1/journal", headers=auth_headers)
    assert res.status_code == 200
