"""LLM credential resolution and API key management."""

import os

from fastapi import Depends, HTTPException

from web.auth import get_current_user
from web.deps_base import get_config, get_secret_key
from web.rate_limit import check_shared_key_rate_limit
from web.user_store import get_user_secrets

SUPPORTED_LLM_PROVIDERS = ("claude", "openai", "gemini")
LLM_PROVIDER_ENV_KEYS = {
    "claude": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "gemini": "GOOGLE_API_KEY",
}

SECRET_KEY_FIELDS = [
    "llm_api_key",
    "llm_api_key_claude",
    "llm_api_key_openai",
    "llm_api_key_gemini",
    "tavily_api_key",
    "github_token",
    "github_pat",
    "eventbrite_token",
]

SHARED_LLM_MODEL = "claude-haiku-4-5"


# --- Helpers ---


def get_decrypted_secrets_for_user(user_id: str) -> dict:
    """Load all decrypted secrets for a specific user."""
    return get_user_secrets(user_id, get_secret_key())


def llm_secret_key(provider: str) -> str:
    """Return the per-provider secret key name."""
    return f"llm_api_key_{provider}"


def _normalize_llm_provider(provider: str | None) -> str | None:
    if not provider:
        return None
    provider = provider.lower().strip()
    if provider == "auto":
        return "auto"
    if provider in SUPPORTED_LLM_PROVIDERS:
        return provider
    return None


def _parse_bool_secret(value: str | None, default: bool = True) -> bool:
    if value is None:
        return default
    return str(value).strip().lower() not in {"0", "false", "no", "off"}


def _detect_provider_from_key(api_key: str | None) -> str | None:
    if not api_key:
        return None
    if api_key.startswith("sk-ant-"):
        return "claude"
    if api_key.startswith("sk-"):
        return "openai"
    if api_key.startswith("AIza"):
        return "gemini"
    return None


def _get_personal_llm_keys_from_secrets(secrets: dict[str, str]) -> dict[str, str]:
    keys: dict[str, str] = {}
    for provider in SUPPORTED_LLM_PROVIDERS:
        value = secrets.get(llm_secret_key(provider))
        if value:
            keys[provider] = value

    if keys:
        return keys

    legacy_key = secrets.get("llm_api_key")
    if legacy_key:
        provider = _normalize_llm_provider(secrets.get("llm_provider"))
        if provider in SUPPORTED_LLM_PROVIDERS:
            keys[provider] = legacy_key
        else:
            inferred = _detect_provider_from_key(legacy_key)
            if inferred:
                keys[inferred] = legacy_key
    return keys


def get_personal_llm_keys_for_user(user_id: str) -> dict[str, str]:
    """Return configured personal LLM API keys keyed by provider."""
    return _get_personal_llm_keys_from_secrets(get_decrypted_secrets_for_user(user_id))


def _get_shared_llm_key(provider: str | None = None) -> tuple[str | None, str | None]:
    if provider and provider in LLM_PROVIDER_ENV_KEYS:
        value = os.getenv(LLM_PROVIDER_ENV_KEYS[provider])
        if value:
            return value, provider

    for candidate in SUPPORTED_LLM_PROVIDERS:
        env_var = LLM_PROVIDER_ENV_KEYS[candidate]
        value = os.getenv(env_var)
        if value:
            return value, candidate

    config = get_config()
    if config.llm.api_key:
        configured = _normalize_llm_provider(config.llm.provider) or provider or "claude"
        return config.llm.api_key, configured

    return None, None


def resolve_llm_credentials_for_user(
    user_id: str,
    provider: str | None = None,
) -> tuple[str | None, str | None, str | None]:
    """Resolve (provider, api_key, source) for a user's normal single-provider LLM call."""
    config = get_config()
    secrets = get_decrypted_secrets_for_user(user_id)
    personal_keys = _get_personal_llm_keys_from_secrets(secrets)
    preferred = (
        _normalize_llm_provider(provider)
        or _normalize_llm_provider(secrets.get("llm_provider"))
        or _normalize_llm_provider(config.llm.provider)
    )

    if preferred in SUPPORTED_LLM_PROVIDERS and personal_keys.get(preferred):
        return preferred, personal_keys[preferred], "user"

    if preferred == "auto" or preferred is None:
        for candidate in SUPPORTED_LLM_PROVIDERS:
            if personal_keys.get(candidate):
                return candidate, personal_keys[candidate], "user"

    if preferred in SUPPORTED_LLM_PROVIDERS:
        shared_key, shared_provider = _get_shared_llm_key(preferred)
        if shared_key:
            return shared_provider, shared_key, "shared"

    for candidate in SUPPORTED_LLM_PROVIDERS:
        if personal_keys.get(candidate):
            return candidate, personal_keys[candidate], "user"

    shared_key, shared_provider = _get_shared_llm_key(preferred)
    if shared_key:
        return shared_provider, shared_key, "shared"

    return preferred if preferred in SUPPORTED_LLM_PROVIDERS else None, None, None


def get_custom_providers_for_user(user_id: str) -> list[dict[str, str]]:
    """Return user's custom OpenAI-compatible provider configs."""
    import json

    secrets = get_decrypted_secrets_for_user(user_id)
    raw = secrets.get("llm_custom_providers")
    if not raw:
        return []
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return []


def get_council_members_for_user(user_id: str) -> list[dict[str, str]]:
    """Return configured personal provider credentials eligible for council mode."""
    secrets = get_decrypted_secrets_for_user(user_id)
    enabled = _parse_bool_secret(secrets.get("llm_council_enabled"), default=True)
    if not enabled:
        return []

    members = []
    for provider, api_key in _get_personal_llm_keys_from_secrets(secrets).items():
        if api_key:
            members.append({"provider": provider, "api_key": api_key})

    for custom in get_custom_providers_for_user(user_id):
        members.append(
            {
                "provider": "openai_compatible",
                "api_key": custom["api_key"],
                "model": custom["model"],
                "display_name": custom["display_name"],
                "base_url": custom["base_url"],
            }
        )

    return members


def get_api_key_with_source(user_id: str) -> tuple[str | None, str | None]:
    """Get LLM API key + source. Returns (key, source) where source is "user"|"shared"|None."""
    _provider, api_key, source = resolve_llm_credentials_for_user(user_id)
    return api_key, source


def get_api_key_for_user(user_id: str, provider: str | None = None) -> str | None:
    """Get LLM API key for a user: user secrets first, then env vars, then config."""
    _provider, api_key, _source = resolve_llm_credentials_for_user(user_id, provider=provider)
    return api_key


def enforce_shared_key_usage_limit(user: dict = Depends(get_current_user)) -> None:
    """Apply the shared-key rate limit when a user is on the shared key path."""
    _key, source = get_api_key_with_source(user["id"])
    if source == "shared":
        check_shared_key_rate_limit(user["id"])


def enforce_onboarding_shared_key_usage_limit(user: dict = Depends(get_current_user)) -> None:
    """Apply the onboarding-specific shared-key rate limit when needed."""
    _key, source = get_api_key_with_source(user["id"])
    if source == "shared":
        check_shared_key_rate_limit(user["id"], onboarding=True)


def require_personal_research_key(user: dict = Depends(get_current_user)) -> None:
    """Block deep research for shared-key users where quality is intentionally gated."""
    _key, source = get_api_key_with_source(user["id"])
    if source == "shared":
        raise HTTPException(
            status_code=403,
            detail="Deep research requires your own API key. Add one in Settings to unlock.",
        )


def _hint(value: str | None) -> str | None:
    """Return last 4 chars as hint, or None."""
    if not value or len(value) < 4:
        return None
    return f"...{value[-4:]}"


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
