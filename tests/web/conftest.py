"""Shared fixtures for web API tests."""

import os
from unittest.mock import patch

import pytest
from cryptography.fernet import Fernet
from fastapi.testclient import TestClient
from jose import jwt


@pytest.fixture
def secret_key():
    return Fernet.generate_key().decode()


@pytest.fixture
def jwt_secret():
    return "test-nextauth-secret"


@pytest.fixture
def auth_token(jwt_secret):
    return jwt.encode(
        {"sub": "user-123", "email": "test@example.com", "name": "Test"},
        jwt_secret,
        algorithm="HS256",
    )


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def mock_paths(tmp_path):
    """Each test gets a fresh temp directory."""
    journal_dir = tmp_path / "journal"
    journal_dir.mkdir()
    return {
        "journal_dir": journal_dir,
        "chroma_dir": tmp_path / "chroma",
        "intel_db": tmp_path / "intel.db",
        "log_file": tmp_path / "coach.log",
    }


@pytest.fixture
def client(jwt_secret, secret_key, mock_paths):
    """Test client with isolated tmp dirs per test."""
    env = {
        "NEXTAUTH_SECRET": jwt_secret,
        "SECRET_KEY": secret_key,
        "ANTHROPIC_API_KEY": "test-key",
    }

    # Patch at every import site so the already-imported references are replaced
    patches = [
        patch.dict(os.environ, env),
        patch("web.deps.get_coach_paths", return_value=mock_paths),
        patch("web.routes.journal.get_coach_paths", return_value=mock_paths),
        patch("web.routes.goals.get_coach_paths", return_value=mock_paths),
        patch("web.routes.intel.get_coach_paths", return_value=mock_paths),
    ]

    for p in patches:
        p.start()

    from web.app import app

    yield TestClient(app)

    for p in reversed(patches):
        p.stop()
