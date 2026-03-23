"""Storage factory functions — per-user and shared store construction."""

from pathlib import Path

import structlog

from storage_access import (
    create_follow_up_store,
    create_insight_store,
    create_intel_storage,
    create_memory_store,
    create_mind_map_store,
    create_profile_embedding_manager,
    create_profile_storage,
    create_recommendation_storage,
    create_thread_store,
    create_watchlist_store,
)
from storage_access import (
    get_profile_path as resolve_profile_path,
)
from storage_paths import StoragePaths
from storage_paths import get_user_paths as resolve_user_paths
from storage_paths import safe_user_id as _safe_user_id
from web.deps_base import get_coach_paths, get_config

logger = structlog.get_logger()


def safe_user_id(user_id: str) -> str:
    """Sanitize user_id for use in file paths and collection names."""
    return _safe_user_id(user_id)


def get_user_paths(user_id: str) -> StoragePaths:
    """Per-user data directories under ~/coach/users/{user_id}/."""
    return resolve_user_paths(user_id)


def get_profile_path(user_id: str):
    """Get the canonical profile path for a user."""
    return resolve_profile_path(get_user_paths(user_id))


def get_profile_storage(user_id: str):
    """Construct the per-user profile store."""
    return create_profile_storage(get_user_paths(user_id))


def get_profile_embedding_manager(user_id: str):
    """Construct the embedding manager used for profile indexing."""
    return create_profile_embedding_manager(get_user_paths(user_id))


def get_memory_store(user_id: str):
    """Construct the per-user memory store."""
    return create_memory_store(get_user_paths(user_id))


def get_thread_store(user_id: str):
    """Construct the per-user thread store."""
    return create_thread_store(get_user_paths(user_id))


def get_mind_map_store(user_id: str):
    """Construct the per-user journal mind-map store."""
    return create_mind_map_store(get_user_paths(user_id))


def get_receipt_store(user_id: str):
    """Construct the per-user extraction receipt store."""
    from journal.extraction_receipts import ExtractionReceiptStore

    return ExtractionReceiptStore(get_user_paths(user_id)["receipts_db"])


def get_thread_inbox_state_store(user_id: str):
    """Construct the per-user thread inbox state store."""
    from journal.thread_inbox import ThreadInboxStateStore

    return ThreadInboxStateStore(get_user_paths(user_id)["threads_db"])


def get_thread_inbox_service(user_id: str):
    """Construct the merged recurring-thread inbox service."""
    from journal.storage import JournalStorage
    from journal.thread_inbox import ThreadInboxService

    paths = get_user_paths(user_id)
    return ThreadInboxService(
        create_thread_store(paths),
        get_thread_inbox_state_store(user_id),
        JournalStorage(paths["journal_dir"]),
    )


def get_intel_storage():
    """Construct the shared intel storage."""
    return create_intel_storage(get_coach_paths())


def get_user_intel_storage(user_id: str):
    """Construct user-scoped intel storage (shared items + user's own)."""
    from intelligence.user_intel_view import UserIntelView

    return UserIntelView(get_intel_storage(), user_id)


def get_intel_search(user_id: str | None = None):
    """Construct IntelSearch with optional user-scoping."""
    from intelligence.search import IntelSearch

    storage = get_intel_storage()
    embedding_manager = None
    try:
        from intelligence.embeddings import IntelEmbeddingManager

        paths = get_coach_paths()
        chroma_dir = Path(paths.get("chroma_dir", paths["intel_db"]).parent / "chroma")
        mgr = IntelEmbeddingManager(chroma_dir)
        if mgr.is_available:
            embedding_manager = mgr
    except Exception:
        pass
    return IntelSearch(storage, embedding_manager=embedding_manager, user_id=user_id)


def get_watchlist_store(user_id: str):
    """Construct the per-user watchlist store."""
    return create_watchlist_store(get_user_paths(user_id))


def get_follow_up_store(user_id: str):
    """Construct the per-user follow-up store."""
    return create_follow_up_store(get_user_paths(user_id))


def get_recommendation_storage(user_id: str):
    """Construct the per-user recommendation store."""
    return create_recommendation_storage(get_user_paths(user_id))


def get_dossier_escalation_store(user_id: str):
    """Construct the per-user dossier escalation store."""
    from research.escalation import DossierEscalationStore

    return DossierEscalationStore(get_user_paths(user_id)["escalations_db"])


def get_outcome_store(user_id: str):
    """Construct the per-user harvested outcome store."""
    from advisor.outcomes import HarvestedOutcomeStore

    return HarvestedOutcomeStore(get_user_paths(user_id)["outcomes_db"])


def get_assumption_store(user_id: str):
    """Construct the per-user assumption store."""
    from advisor.assumptions import AssumptionStore

    return AssumptionStore(get_user_paths(user_id)["assumptions_db"])


def get_github_repo_store():
    """Construct the shared GitHub repo monitoring store."""
    from intelligence.github_repo_store import GitHubRepoStore

    return GitHubRepoStore(get_coach_paths()["intel_db"])


def get_company_movement_store():
    """Construct the shared company movement store."""
    from intelligence.company_watch import CompanyMovementStore

    return CompanyMovementStore(get_coach_paths()["intel_db"])


def get_hiring_signal_store():
    """Construct the shared hiring signal store."""
    from intelligence.hiring_signals import HiringSignalStore

    return HiringSignalStore(get_coach_paths()["intel_db"])


def get_hiring_baseline_tracker():
    """Construct the shared hiring baseline tracker."""
    from intelligence.hiring_signals import HiringBaselineTracker

    return HiringBaselineTracker(get_coach_paths()["intel_db"])


def get_regulatory_alert_store():
    """Construct the shared regulatory alert store."""
    from intelligence.regulatory import RegulatoryAlertStore

    return RegulatoryAlertStore(get_coach_paths()["intel_db"])


def get_library_index(user_id: str):
    """Construct the per-user library index with semantic search."""
    from library.embeddings import LibraryEmbeddingManager
    from library.index import LibraryIndex

    paths = get_user_paths(user_id)
    config = get_config()
    config_dict = config.to_dict() if hasattr(config, "to_dict") else None
    embeddings = LibraryEmbeddingManager(paths["chroma_dir"], config=config_dict)
    return LibraryIndex(Path(paths["data_dir"]) / "library", embedding_manager=embeddings)


def get_insight_store():
    """Construct the shared insight store."""
    return create_insight_store(get_coach_paths())
