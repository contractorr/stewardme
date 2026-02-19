"""Fernet encryption for API keys. Stores encrypted JSON at ~/coach/secrets.enc."""

import json
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet, InvalidToken


def _get_fernet(secret_key: str) -> Fernet:
    """Create Fernet instance from SECRET_KEY (must be 32-byte url-safe base64)."""
    return Fernet(secret_key.encode() if isinstance(secret_key, str) else secret_key)


def _secrets_path() -> Path:
    return Path.home() / "coach" / "secrets.enc"


def load_secrets(secret_key: str) -> dict[str, Any]:
    """Load and decrypt secrets file. Returns empty dict if missing/invalid."""
    path = _secrets_path()
    if not path.exists():
        return {}
    try:
        f = _get_fernet(secret_key)
        decrypted = f.decrypt(path.read_bytes())
        return json.loads(decrypted)
    except (InvalidToken, json.JSONDecodeError, Exception):
        return {}


def save_secrets(secret_key: str, data: dict[str, Any]) -> None:
    """Encrypt and save secrets dict."""
    path = _secrets_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    f = _get_fernet(secret_key)
    encrypted = f.encrypt(json.dumps(data).encode())
    path.write_bytes(encrypted)


def get_secret(secret_key: str, key: str) -> str | None:
    """Get a single secret by key."""
    return load_secrets(secret_key).get(key)


def set_secret(secret_key: str, key: str, value: str) -> None:
    """Set a single secret."""
    data = load_secrets(secret_key)
    data[key] = value
    save_secrets(secret_key, data)


def delete_secret(secret_key: str, key: str) -> None:
    """Delete a single secret."""
    data = load_secrets(secret_key)
    data.pop(key, None)
    save_secrets(secret_key, data)
