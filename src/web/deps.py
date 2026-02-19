"""Dependency injection for FastAPI routes."""

import os
from functools import lru_cache

import structlog

from cli.config import get_paths, load_config_model
from web.crypto import load_secrets

logger = structlog.get_logger()

SECRET_KEY_FIELDS = [
    "llm_api_key",
    "tavily_api_key",
    "github_token",
    "eventbrite_token",
    "smtp_pass",
]


@lru_cache
def get_config():
    """Load shared config from ~/coach/config.yaml."""
    return load_config_model()


def get_coach_paths() -> dict:
    """Get expanded paths dict."""
    config = get_config()
    return get_paths(config.to_dict())


def get_secret_key() -> str:
    """Get Fernet secret key from env."""
    key = os.getenv("SECRET_KEY")
    if not key:
        raise RuntimeError("SECRET_KEY env var required for API key encryption")
    return key


def get_decrypted_secrets() -> dict:
    """Load all decrypted secrets."""
    return load_secrets(get_secret_key())


def get_api_key_for_provider(provider: str | None = None) -> str | None:
    """Get LLM API key: secrets.enc first, then env vars, then config."""
    secrets = get_decrypted_secrets()

    # 1. Check encrypted secrets store
    if secrets.get("llm_api_key"):
        return secrets["llm_api_key"]

    # 2. Check env vars (same logic as llm/factory.py)
    for env_var in ["ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY"]:
        val = os.getenv(env_var)
        if val:
            return val

    # 3. Check config
    config = get_config()
    if config.llm.api_key:
        return config.llm.api_key

    return None


def _hint(value: str | None) -> str | None:
    """Return last 4 chars as hint, or None."""
    if not value or len(value) < 4:
        return None
    return f"...{value[-4:]}"


def get_settings_mask() -> dict:
    """Return settings with bool mask for secrets."""
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
        "smtp_host": secrets.get("smtp_host"),
        "smtp_port": secrets.get("smtp_port"),
        "smtp_user": secrets.get("smtp_user"),
        "smtp_pass_set": bool(secrets.get("smtp_pass")),
        "smtp_to": secrets.get("smtp_to"),
    }
