"""Tests for settings routes."""

import os
from unittest.mock import patch


def test_health(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_get_settings_unauthed(client):
    res = client.get("/api/settings")
    # HTTPBearer returns 403 when no Authorization header
    assert res.status_code in (401, 403)


def test_get_settings(client, auth_headers, secret_key):
    with patch.dict(os.environ, {"SECRET_KEY": secret_key}):
        res = client.get("/api/settings", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert "llm_api_key_set" in data
        assert data["llm_api_key_set"] is False


def test_put_settings(client, auth_headers, secret_key, tmp_path):
    secrets_path = tmp_path / "secrets.enc"
    with patch.dict(os.environ, {"SECRET_KEY": secret_key}):
        with patch("web.crypto._secrets_path", return_value=secrets_path):
            # Save a key
            res = client.put(
                "/api/settings",
                headers=auth_headers,
                json={"llm_api_key": "sk-test1234", "llm_provider": "claude"},
            )
            assert res.status_code == 200
            data = res.json()
            assert data["llm_api_key_set"] is True
            assert data["llm_api_key_hint"] == "...1234"
            assert data["llm_provider"] == "claude"
