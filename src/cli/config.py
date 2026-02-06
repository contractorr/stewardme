"""Configuration loading and management."""

import os
import structlog
from pathlib import Path
from typing import Optional, Union

import yaml

from .config_models import CoachConfig, LimitsConfig

logger = structlog.get_logger()


# Default values for tunable parameters (backwards compat)
DEFAULTS = LimitsConfig().model_dump()

# Default config dict (backwards compat)
DEFAULT_CONFIG = CoachConfig().to_dict()


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
    """Load configuration from file or defaults.

    Returns dict for backwards compatibility. Use load_config_model() for typed access.
    """
    model = load_config_model(config_path)
    return model.to_dict()


def load_config_model(config_path: Optional[Path] = None) -> CoachConfig:
    """Load configuration as Pydantic model with validation."""
    base_config = {}

    path = config_path or find_config()
    if path and path.exists():
        try:
            with open(path) as f:
                base_config = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in config file: {e}")

    try:
        return CoachConfig.from_dict(base_config)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Config validation failed: {e}")


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
    from cli.logging_config import setup_logging as _setup
    log_config = config.get("logging", {})
    level = log_config.get("level", "INFO")
    json_mode = log_config.get("json_mode", False)
    _setup(json_mode=json_mode, level=level)
