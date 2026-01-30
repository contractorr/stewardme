"""Shared CLI utilities."""

import logging
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console

console = Console()
logger = logging.getLogger(__name__)


def get_components(skip_advisor: bool = False):
    """Initialize all components from config.

    Args:
        skip_advisor: If True, skip advisor init (for commands that don't need LLM)
    """
    from cli.config import load_config, get_paths
    from journal import JournalStorage, EmbeddingManager, JournalSearch
    from advisor import RAGRetriever
    from advisor.engine import APIKeyMissingError, AdvisorEngine
    from intelligence.scraper import IntelStorage
    from intelligence.search import IntelSearch
    from intelligence.embeddings import IntelEmbeddingManager

    config = load_config()
    paths = get_paths(config)

    storage = JournalStorage(paths["journal_dir"])
    embeddings = EmbeddingManager(paths["chroma_dir"])
    search = JournalSearch(storage, embeddings)
    intel_storage = IntelStorage(paths["intel_db"])

    # Initialize intel semantic search
    intel_embeddings = IntelEmbeddingManager(paths["chroma_dir"] / "intel")
    intel_search = IntelSearch(intel_storage, intel_embeddings)

    # Pass intel_search to RAG for semantic intel retrieval
    rag = RAGRetriever(search, paths["intel_db"], intel_search=intel_search)

    advisor = None
    if not skip_advisor:
        try:
            advisor = AdvisorEngine(rag, model=config["llm"].get("model", "claude-sonnet-4-20250514"))
        except APIKeyMissingError as e:
            console.print(f"[red]Config error:[/] {e}")
            sys.exit(1)

    return {
        "config": config,
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
    """Get recommendations DB path (same as intel.db directory)."""
    intel_db = Path(config["paths"]["intel_db"]).expanduser()
    return intel_db.parent / "recommendations.db"
