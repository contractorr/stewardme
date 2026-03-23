"""Shared infrastructure used by deps sub-modules."""

import os
from functools import lru_cache
from pathlib import Path

from coach_config import LegacyPaths, get_paths, load_config_model


@lru_cache
def get_config():
    """Load shared config from ~/coach/config.yaml."""
    return load_config_model()


def get_coach_paths() -> LegacyPaths:
    """Get expanded paths dict (CLI / legacy single-user)."""
    coach_home = os.getenv("COACH_HOME")
    if coach_home:
        base = Path(coach_home).expanduser()
        return LegacyPaths(
            journal_dir=base / "journal",
            chroma_dir=base / "chroma",
            intel_db=base / "intel.db",
            log_file=base / "coach.log",
        )

    config = get_config()
    return get_paths(config.to_dict())


def get_secret_key() -> str:
    """Get Fernet secret key from env."""
    key = os.getenv("SECRET_KEY")
    if not key:
        raise RuntimeError("SECRET_KEY env var required for API key encryption")
    return key
