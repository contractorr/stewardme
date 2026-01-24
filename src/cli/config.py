"""Configuration loading and management."""

import logging
import os
from pathlib import Path
from typing import Optional

import yaml


# Default values for tunable parameters (previously magic numbers)
DEFAULTS = {
    # Scraping limits
    "hn_max_stories": 30,
    "rss_max_entries": 20,
    "github_max_repos": 25,

    # Context limits for RAG
    "journal_max_entries": 5,
    "journal_max_chars": 6000,
    "intel_max_items": 5,
    "intel_max_chars": 3000,
    "total_context_chars": 8000,

    # Summary truncation lengths
    "summary_truncate": 500,
    "preview_truncate": 200,

    # LLM settings
    "llm_max_tokens": 2000,
}


DEFAULT_CONFIG = {
    "llm": {
        "provider": "claude",
        "model": "claude-sonnet-4-20250514",
    },
    "paths": {
        "journal_dir": "~/coach/journal",
        "chroma_dir": "~/coach/chroma",
        "intel_db": "~/coach/intel.db",
        "log_file": "~/coach/coach.log",
    },
    "sources": {
        "custom_blogs": [],
        "rss_feeds": [
            "https://news.ycombinator.com/rss",
        ],
        "enabled": ["hn_top", "rss_feeds"],
    },
    "limits": DEFAULTS,
    "logging": {
        "level": "INFO",
        "file_level": "DEBUG",
    },
}


def find_config() -> Optional[Path]:
    """Find config file in standard locations."""
    locations = [
        Path.cwd() / "config.yaml",
        Path.home() / ".coach" / "config.yaml",
        Path.home() / "coach" / "config.yaml",
    ]
    for loc in locations:
        if loc.exists():
            return loc
    return None


def load_config(config_path: Optional[Path] = None) -> dict:
    """Load configuration from file or defaults."""
    config = DEFAULT_CONFIG.copy()

    path = config_path or find_config()
    if path and path.exists():
        with open(path) as f:
            user_config = yaml.safe_load(f) or {}
            config = _deep_merge(config, user_config)

    # Expand environment variables in API keys
    if "llm" in config and "api_key" in config["llm"]:
        api_key = config["llm"]["api_key"]
        if api_key.startswith("${") and api_key.endswith("}"):
            env_var = api_key[2:-1]
            config["llm"]["api_key"] = os.getenv(env_var, "")

    return config


def _deep_merge(base: dict, override: dict) -> dict:
    """Deep merge two dictionaries."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def get_paths(config: dict) -> dict:
    """Get expanded paths from config."""
    paths = config.get("paths", DEFAULT_CONFIG["paths"])
    return {
        "journal_dir": Path(paths["journal_dir"]).expanduser(),
        "chroma_dir": Path(paths["chroma_dir"]).expanduser(),
        "intel_db": Path(paths["intel_db"]).expanduser(),
        "log_file": Path(paths.get("log_file", "~/coach/coach.log")).expanduser(),
    }


def get_limits(config: dict) -> dict:
    """Get limit values, merging user config with defaults."""
    return {**DEFAULTS, **config.get("limits", {})}


def setup_logging(config: dict) -> None:
    """Configure logging based on config."""
    log_config = config.get("logging", {})
    console_level = getattr(logging, log_config.get("level", "INFO").upper(), logging.INFO)
    file_level = getattr(logging, log_config.get("file_level", "DEBUG").upper(), logging.DEBUG)

    # Root logger
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    # Console handler
    console = logging.StreamHandler()
    console.setLevel(console_level)
    console.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    root.addHandler(console)

    # File handler (optional)
    paths = get_paths(config)
    log_file = paths.get("log_file")
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(file_level)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
        )
        root.addHandler(file_handler)
