"""Dependency injection for FastAPI routes.

Split into sub-modules for maintainability:
- deps_base: shared config/paths infrastructure
- deps_storage: per-user and shared store factories
- deps_credentials: LLM credential resolution and API key management
- deps_features: feature toggles and settings masks

This file re-exports everything for backwards compatibility.
"""

# --- Base infrastructure ---
from web.deps_base import get_coach_paths, get_config, get_secret_key  # noqa: F401

# --- Credential resolution ---
from web.deps_credentials import (  # noqa: F401
    SECRET_KEY_FIELDS,
    SHARED_LLM_MODEL,
    SUPPORTED_LLM_PROVIDERS,
    enforce_onboarding_shared_key_usage_limit,
    enforce_shared_key_usage_limit,
    get_api_key_for_provider,
    get_api_key_for_user,
    get_api_key_with_source,
    get_council_members_for_user,
    get_custom_providers_for_user,
    get_decrypted_secrets,
    get_decrypted_secrets_for_user,
    get_personal_llm_keys_for_user,
    llm_secret_key,
    require_personal_research_key,
    resolve_llm_credentials_for_user,
)

# --- Feature flags & settings ---
from web.deps_features import (  # noqa: F401
    get_settings_mask,
    get_settings_mask_for_user,
    resolve_feature_toggle,
)

# --- Storage factories ---
from web.deps_storage import (  # noqa: F401
    get_assumption_store,
    get_company_movement_store,
    get_dossier_escalation_store,
    get_follow_up_store,
    get_github_repo_store,
    get_hiring_baseline_tracker,
    get_hiring_signal_store,
    get_insight_store,
    get_intel_search,
    get_intel_storage,
    get_library_index,
    get_memory_store,
    get_mind_map_store,
    get_outcome_store,
    get_profile_embedding_manager,
    get_profile_path,
    get_profile_storage,
    get_receipt_store,
    get_recommendation_storage,
    get_regulatory_alert_store,
    get_thread_inbox_service,
    get_thread_inbox_state_store,
    get_thread_store,
    get_user_intel_storage,
    get_user_paths,
    get_watchlist_store,
    safe_user_id,
)
