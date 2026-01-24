"""Configuration loading and management."""

import os
from pathlib import Path
from typing import Optional

import yaml


DEFAULT_CONFIG = {
    "llm": {
        "provider": "claude",
        "model": "claude-sonnet-4-20250514",
    },
    "paths": {
        "journal_dir": "~/coach/journal",
        "chroma_dir": "~/coach/chroma",
        "intel_db": "~/coach/intel.db",
    },
    "sources": {
        "custom_blogs": [],
        "rss_feeds": [
            "https://news.ycombinator.com/rss",
        ],
        "enabled": ["hn_top", "rss_feeds"],
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
    }
