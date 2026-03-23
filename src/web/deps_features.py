"""Feature toggles and user settings mask."""

from web.deps_base import get_config
from web.deps_credentials import (
    _get_personal_llm_keys_from_secrets,
    _hint,
    _normalize_llm_provider,
    _parse_bool_secret,
    get_custom_providers_for_user,
    get_decrypted_secrets_for_user,
    resolve_llm_credentials_for_user,
)
from web.user_store import is_onboarded


def resolve_feature_toggle(
    secrets: dict[str, str],
    feature_key: str,
    config_default: bool,
) -> bool:
    """User secret takes precedence; falls back to global config value."""
    raw = secrets.get(feature_key)
    if raw is None:
        return config_default
    return _parse_bool_secret(raw, default=config_default)


def get_settings_mask_for_user(user_id: str) -> dict:
    """Return settings with bool mask for secrets, per-user."""
    secrets = get_decrypted_secrets_for_user(user_id)
    config = get_config()
    personal_keys = _get_personal_llm_keys_from_secrets(secrets)
    provider_statuses = [
        {
            "provider": provider,
            "configured": bool(personal_keys.get(provider)),
            "hint": _hint(personal_keys.get(provider)),
            "council_eligible": bool(personal_keys.get(provider)),
        }
        for provider in ("claude", "openai", "gemini")
    ]

    selected_provider, _key, source = resolve_llm_credentials_for_user(user_id)
    has_own_key = bool(personal_keys)
    preferred_provider = _normalize_llm_provider(secrets.get("llm_provider")) or config.llm.provider
    display_provider = preferred_provider if preferred_provider != "auto" else selected_provider
    key_hint = None
    if display_provider in personal_keys:
        key_hint = _hint(personal_keys.get(display_provider))
    elif personal_keys:
        key_hint = _hint(next(iter(personal_keys.values())))
    council_enabled = _parse_bool_secret(secrets.get("llm_council_enabled"), default=True)
    has_profile = is_onboarded(user_id)
    custom_providers = get_custom_providers_for_user(user_id)
    custom_provider_infos = [
        {
            "id": cp["id"],
            "display_name": cp["display_name"],
            "base_url": cp["base_url"],
            "model": cp["model"],
        }
        for cp in custom_providers
    ]
    total_providers = len(personal_keys) + len(custom_providers)

    return {
        "has_profile": has_profile,
        "llm_provider": display_provider,
        "llm_model": secrets.get("llm_model") or config.llm.model,
        "llm_council_enabled": council_enabled,
        "llm_council_ready": council_enabled and total_providers >= 2,
        "llm_provider_keys": provider_statuses,
        "llm_custom_providers": custom_provider_infos,
        "llm_api_key_set": has_own_key,
        "llm_api_key_hint": key_hint,
        "using_shared_key": source == "shared",
        "has_own_key": has_own_key,
        "tavily_api_key_set": bool(secrets.get("tavily_api_key")),
        "tavily_api_key_hint": _hint(secrets.get("tavily_api_key")),
        "github_token_set": bool(secrets.get("github_token")),
        "github_token_hint": _hint(secrets.get("github_token")),
        "github_pat_set": bool(secrets.get("github_pat")),
        "github_pat_hint": _hint(secrets.get("github_pat")),
        "eventbrite_token_set": bool(secrets.get("eventbrite_token")),
        # Feature toggles
        "feature_extended_thinking": resolve_feature_toggle(
            secrets, "feature_extended_thinking", config.llm.extended_thinking
        ),
        "feature_memory_enabled": resolve_feature_toggle(
            secrets, "feature_memory_enabled", config.memory.enabled
        ),
        "feature_threads_enabled": resolve_feature_toggle(
            secrets, "feature_threads_enabled", config.threads.enabled
        ),
        "feature_recommendations_enabled": resolve_feature_toggle(
            secrets, "feature_recommendations_enabled", config.recommendations.enabled
        ),
        "feature_research_enabled": resolve_feature_toggle(
            secrets, "feature_research_enabled", config.research.enabled
        ),
        "feature_entity_extraction_enabled": resolve_feature_toggle(
            secrets, "feature_entity_extraction_enabled", True
        ),
        "feature_trending_radar_enabled": resolve_feature_toggle(
            secrets, "feature_trending_radar_enabled", config.trending_radar.enabled
        ),
        "feature_heartbeat_enabled": resolve_feature_toggle(
            secrets, "feature_heartbeat_enabled", config.heartbeat.enabled
        ),
        "feature_company_movement_enabled": resolve_feature_toggle(
            secrets, "feature_company_movement_enabled", config.company_movement.enabled
        ),
        "feature_hiring_signals_enabled": resolve_feature_toggle(
            secrets, "feature_hiring_signals_enabled", config.hiring.enabled
        ),
        "feature_regulatory_signals_enabled": resolve_feature_toggle(
            secrets, "feature_regulatory_signals_enabled", config.regulatory.enabled
        ),
        "feature_github_monitoring": resolve_feature_toggle(
            secrets, "feature_github_monitoring", config.github_monitoring.enabled
        ),
    }


def get_settings_mask() -> dict:
    """Legacy single-user settings mask."""
    from web.deps_credentials import get_decrypted_secrets

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
