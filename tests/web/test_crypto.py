"""Tests for Fernet encryption."""

from unittest.mock import patch

from cryptography.fernet import Fernet

from web.crypto import delete_secret, get_secret, load_secrets, save_secrets, set_secret


def test_roundtrip(tmp_path):
    key = Fernet.generate_key().decode()
    path = tmp_path / "secrets.enc"
    with patch("web.crypto._secrets_path", return_value=path):
        save_secrets(key, {"api_key": "sk-abc123", "provider": "claude"})
        data = load_secrets(key)
        assert data["api_key"] == "sk-abc123"
        assert data["provider"] == "claude"


def test_load_missing(tmp_path):
    key = Fernet.generate_key().decode()
    path = tmp_path / "nonexistent.enc"
    with patch("web.crypto._secrets_path", return_value=path):
        assert load_secrets(key) == {}


def test_load_wrong_key(tmp_path):
    key1 = Fernet.generate_key().decode()
    key2 = Fernet.generate_key().decode()
    path = tmp_path / "secrets.enc"
    with patch("web.crypto._secrets_path", return_value=path):
        save_secrets(key1, {"secret": "value"})
        assert load_secrets(key2) == {}


def test_set_get_delete(tmp_path):
    key = Fernet.generate_key().decode()
    path = tmp_path / "secrets.enc"
    with patch("web.crypto._secrets_path", return_value=path):
        set_secret(key, "token", "abc123")
        assert get_secret(key, "token") == "abc123"

        delete_secret(key, "token")
        assert get_secret(key, "token") is None
