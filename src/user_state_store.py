"""Multi-user SQLite store — re-export hub.

Split into sub-modules for maintainability:
- user_crud: DB init, connection, user CRUD, onboarding, display name
- user_secrets: encrypted per-user secret storage
- user_analytics: engagement events, usage analytics, RSS feeds, feedback
"""

# --- User CRUD ---
# --- Analytics & engagement ---
from user_analytics import (  # noqa: F401
    add_user_rss_feed,
    get_all_user_rss_feeds,
    get_engagement_stats,
    get_feedback_count,
    get_usage_stats,
    get_user_rss_feeds,
    get_user_usage_stats,
    log_engagement,
    log_event,
    remove_user_rss_feed,
)
from user_crud import (  # noqa: F401
    _get_conn,
    _migrate_secrets,
    clear_onboarding_responses,
    delete_user,
    get_default_db_path,
    get_onboarding_responses,
    get_or_create_user,
    get_user_name,
    init_db,
    is_onboarded,
    mark_onboarded,
    save_onboarding_turn,
    update_user_name,
)

# --- Secrets ---
from user_secrets import (  # noqa: F401
    delete_user_secret,
    get_user_secret,
    get_user_secrets,
    set_user_secret,
)
