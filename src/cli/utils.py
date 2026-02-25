"""Shared CLI utilities."""

import sys
from pathlib import Path

import structlog
from rich.console import Console

console = Console()
logger = structlog.get_logger()


def get_components(skip_advisor: bool = False):
    """Initialize all components from config.

    Args:
        skip_advisor: If True, skip advisor init (for commands that don't need LLM)
    """
    from advisor import RAGRetriever
    from advisor.engine import AdvisorEngine, APIKeyMissingError
    from cli.config import get_paths, load_config, load_config_model
    from intelligence.embeddings import IntelEmbeddingManager
    from intelligence.scraper import IntelStorage
    from intelligence.search import IntelSearch
    from journal import EmbeddingManager, JournalSearch, JournalStorage

    config = load_config()
    config_model = load_config_model()

    paths = get_paths(config)

    storage = JournalStorage(paths["journal_dir"])
    intel_storage = IntelStorage(paths["intel_db"])

    try:
        embeddings = EmbeddingManager(paths["chroma_dir"])
        intel_embeddings = IntelEmbeddingManager(paths["chroma_dir"] / "intel")
    except Exception as e:
        err = str(e).lower()
        if "dimension" in err or "mismatch" in err:
            console.print(
                "[red]ChromaDB dimension mismatch — embedding model may have changed.[/]\n"
                "Run [bold]coach db rebuild --collection all[/] to fix."
            )
            sys.exit(1)
        raise

    search = JournalSearch(storage, embeddings)
    intel_search = IntelSearch(intel_storage, intel_embeddings)

    # Pass intel_search to RAG for semantic intel retrieval
    profile_path = get_profile_path(config)
    rag = RAGRetriever(
        search,
        paths["intel_db"],
        intel_search=intel_search,
        max_context_chars=config_model.rag.max_context_chars,
        journal_weight=config_model.rag.journal_weight,
        profile_path=profile_path,
    )

    advisor = None
    if not skip_advisor:
        try:
            llm_cfg = config_model.llm
            advisor = AdvisorEngine(
                rag,
                model=llm_cfg.model,
                provider=llm_cfg.provider,
                api_key=llm_cfg.api_key,
            )
        except APIKeyMissingError as e:
            console.print(f"[red]Config error:[/] {e}")
            sys.exit(1)

    return {
        "config": config,
        "config_model": config_model,
        "paths": paths,
        "storage": storage,
        "embeddings": embeddings,
        "search": search,
        "intel_storage": intel_storage,
        "intel_search": intel_search,
        "rag": rag,
        "advisor": advisor,
    }


def get_rec_db_path(config: dict) -> Path:
    """Get recommendations directory path."""
    intel_db = Path(config["paths"]["intel_db"]).expanduser()
    return intel_db.parent / "recommendations"


def get_profile_storage(config: dict | None = None):
    """Get ProfileStorage instance from config."""
    from profile.storage import ProfileStorage

    if config is None:
        from cli.config import load_config

        config = load_config()
    path = config.get("profile", {}).get("path", "~/coach/profile.yaml")
    return ProfileStorage(path)


def get_profile_path(config: dict) -> str:
    """Get profile YAML path from config."""
    return config.get("profile", {}).get("path", "~/coach/profile.yaml")
