"""Dependency injection for FastAPI routes."""

import os
from functools import lru_cache
from pathlib import Path

import structlog

from cli.config import get_paths, load_config_model
from web.user_store import get_user_secrets

logger = structlog.get_logger()

SECRET_KEY_FIELDS = [
    "llm_api_key",
    "tavily_api_key",
    "github_token",
    "eventbrite_token",
]


@lru_cache
def get_config():
    """Load shared config from ~/coach/config.yaml."""
    return load_config_model()


def get_coach_paths() -> dict:
    """Get expanded paths dict (CLI / legacy single-user)."""
    config = get_config()
    return get_paths(config.to_dict())


def get_secret_key() -> str:
    """Get Fernet secret key from env."""
    key = os.getenv("SECRET_KEY")
    if not key:
        raise RuntimeError("SECRET_KEY env var required for API key encryption")
    return key


# --- Per-user paths ---


def get_user_paths(user_id: str) -> dict:
    """Per-user data directories under ~/coach/users/{user_id}/."""
    base = Path.home() / "coach" / "users" / user_id
    base.mkdir(parents=True, exist_ok=True)
    journal_dir = base / "journal"
    journal_dir.mkdir(exist_ok=True)
    return {
        "journal_dir": journal_dir,
        "chroma_dir": base / "chroma",
        "recommendations_dir": base / "recommendations",
        "learning_paths_dir": base / "learning_paths",
        "profile": base / "profile.yaml",
        # Intel stays global
        "intel_db": Path.home() / "coach" / "intel.db",
    }


# --- Per-user secrets ---


def get_decrypted_secrets_for_user(user_id: str) -> dict:
    """Load all decrypted secrets for a specific user."""
    return get_user_secrets(user_id, get_secret_key())


def get_api_key_for_user(user_id: str, provider: str | None = None) -> str | None:
    """Get LLM API key for a user: user secrets first, then env vars, then config."""
    secrets = get_decrypted_secrets_for_user(user_id)

    # 1. User's encrypted secrets
    if secrets.get("llm_api_key"):
        return secrets["llm_api_key"]

    # 2. Env vars (shared fallback)
    for env_var in ["ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY"]:
        val = os.getenv(env_var)
        if val:
            return val

    # 3. Config file
    config = get_config()
    if config.llm.api_key:
        return config.llm.api_key

    return None


def _hint(value: str | None) -> str | None:
    """Return last 4 chars as hint, or None."""
    if not value or len(value) < 4:
        return None
    return f"...{value[-4:]}"


def get_settings_mask_for_user(user_id: str) -> dict:
    """Return settings with bool mask for secrets, per-user."""
    secrets = get_decrypted_secrets_for_user(user_id)
    config = get_config()

    return {
        "llm_provider": secrets.get("llm_provider") or config.llm.provider,
        "llm_model": secrets.get("llm_model") or config.llm.model,
        "llm_api_key_set": bool(secrets.get("llm_api_key")),
        "llm_api_key_hint": _hint(secrets.get("llm_api_key")),
        "tavily_api_key_set": bool(secrets.get("tavily_api_key")),
        "tavily_api_key_hint": _hint(secrets.get("tavily_api_key")),
        "github_token_set": bool(secrets.get("github_token")),
        "github_token_hint": _hint(secrets.get("github_token")),
        "eventbrite_token_set": bool(secrets.get("eventbrite_token")),
    }


# --- Legacy single-user compat (used by old tests / CLI) ---


def get_decrypted_secrets() -> dict:
    """Load all decrypted secrets from legacy file."""
    from web.crypto import load_secrets
    return load_secrets(get_secret_key())


def get_api_key_for_provider(provider: str | None = None) -> str | None:
    """Legacy: get API key from file-based secrets."""
    secrets = get_decrypted_secrets()
    if secrets.get("llm_api_key"):
        return secrets["llm_api_key"]
    for env_var in ["ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY"]:
        val = os.getenv(env_var)
        if val:
            return val
    config = get_config()
    if config.llm.api_key:
        return config.llm.api_key
    return None


def get_settings_mask() -> dict:
    """Legacy single-user settings mask."""
    secrets = get_decrypted_secrets()
    config = get_config()
    return {
        "llm_provider": secrets.get("llm_provider") or config.llm.provider,
        "llm_model": secrets.get("llm_model") or config.llm.model,
        "llm_api_key_set": bool(secrets.get("llm_api_key")),
        "llm_api_key_hint": _hint(secrets.get("llm_api_key")),
        "tavily_api_key_set": bool(secrets.get("tavily_api_key")),
        "tavily_api_key_hint": _hint(secrets.get("tavily_api_key")),
        "github_token_set": bool(secrets.get("github_token")),
        "github_token_hint": _hint(secrets.get("github_token")),
        "eventbrite_token_set": bool(secrets.get("eventbrite_token")),
    }
