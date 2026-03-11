"""Tests for web app startup helpers."""

from unittest.mock import patch

import pytest
from cryptography.fernet import Fernet
from fastapi.middleware.cors import CORSMiddleware

from web import app as web_app
from web.conversation_store import add_message, create_conversation, get_conversation
from web.user_store import get_or_create_user


def test_start_intel_scheduler_can_be_disabled(monkeypatch):
    monkeypatch.setenv("DISABLE_INTEL_SCHEDULER", "true")

    with patch("intelligence.scheduler.IntelScheduler") as scheduler_cls:
        result = web_app._start_intel_scheduler()

    assert result is None
    scheduler_cls.assert_not_called()


def test_start_intel_scheduler_returns_none_on_failure(monkeypatch):
    monkeypatch.delenv("DISABLE_INTEL_SCHEDULER", raising=False)

    with patch("intelligence.scheduler.IntelScheduler", side_effect=RuntimeError("boom")):
        result = web_app._start_intel_scheduler()

    assert result is None


def test_verify_secret_key_requires_env(monkeypatch):
    monkeypatch.delenv("SECRET_KEY", raising=False)

    with pytest.raises(RuntimeError, match="SECRET_KEY required"):
        web_app._verify_secret_key()


def test_create_app_mounts_projects_route():
    app = web_app.create_app()

    paths = {route.path for route in app.routes}
    assert "/api/projects/issues" in paths
    assert "/api/health" in paths


def test_create_app_uses_frontend_origin_from_env(monkeypatch):
    monkeypatch.setenv("FRONTEND_ORIGIN", "https://frontend.example.com")

    app = web_app.create_app()

    cors = next(m for m in app.user_middleware if m.cls is CORSMiddleware)
    assert cors.kwargs["allow_origins"] == ["https://frontend.example.com"]


def test_startup_services_initialize_attachment_schema(monkeypatch, tmp_path):
    db_path = tmp_path / "users.db"
    monkeypatch.setenv("COACH_USERS_DB_PATH", str(db_path))
    monkeypatch.setenv("SECRET_KEY", Fernet.generate_key().decode())
    monkeypatch.setenv("DISABLE_INTEL_SCHEDULER", "1")

    state = web_app._startup_services()
    try:
        get_or_create_user("u1", db_path=db_path)
        conv_id = create_conversation("u1", "Attachment test", db_path=db_path)
        add_message(
            conv_id,
            "user",
            "See attached",
            attachments=[
                {
                    "library_item_id": "item-1",
                    "file_name": "brief.md",
                    "mime_type": "text/markdown",
                }
            ],
            db_path=db_path,
        )

        conversation = get_conversation(conv_id, "u1", db_path=db_path)

        assert conversation is not None
        assert conversation["messages"][0]["attachments"][0]["library_item_id"] == "item-1"
    finally:
        web_app._shutdown_services(state)
