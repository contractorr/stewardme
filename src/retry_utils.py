"""Retry utilities with exponential backoff.

Single implementation with named presets. ``http_retry`` and ``llm_retry``
are thin wrappers around ``with_retry`` kept for backwards compatibility.
"""

import logging

import structlog
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = structlog.stdlib.get_logger(__name__)

# Named presets: (max_attempts, min_wait, max_wait)
_PRESETS: dict[str, tuple[int, float, float]] = {
    "http": (3, 2.0, 10.0),
    "llm": (3, 2.0, 30.0),
}


def with_retry(
    max_attempts: int = 3,
    min_wait: float = 2.0,
    max_wait: float = 10.0,
    exceptions: tuple = (Exception,),
    preset: str | None = None,
):
    """Retry decorator with exponential backoff.

    Use ``preset`` for common defaults ("http", "llm") or pass explicit
    parameters for full control.
    """
    if preset and preset in _PRESETS:
        max_attempts, min_wait, max_wait = _PRESETS[preset]

    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=min_wait, max=max_wait),
        retry=retry_if_exception_type(exceptions),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )


# Convenience aliases (backwards-compatible)
def http_retry(
    max_attempts: int = 3,
    min_wait: float = 2.0,
    max_wait: float = 10.0,
    exceptions: tuple = (Exception,),
):
    """Retry preset for HTTP/scraper operations."""
    return with_retry(
        max_attempts=max_attempts, min_wait=min_wait, max_wait=max_wait, exceptions=exceptions
    )


def llm_retry(
    max_attempts: int = 3,
    min_wait: float = 2.0,
    max_wait: float = 30.0,
    exceptions: tuple = (Exception,),
):
    """Retry preset for LLM API calls (longer max_wait for rate limits)."""
    return with_retry(
        max_attempts=max_attempts, min_wait=min_wait, max_wait=max_wait, exceptions=exceptions
    )


def retry_from_config(config: dict, retry_type: str = "http"):
    """Create retry decorator from config dict."""
    retry_config = config.get("retry", {})

    max_attempts = retry_config.get("max_attempts", 3)
    min_wait = retry_config.get("min_wait", 2.0)

    if retry_type == "llm":
        max_wait = retry_config.get("llm_max_wait", 30.0)
    else:
        max_wait = retry_config.get("max_wait", 10.0)

    return with_retry(max_attempts=max_attempts, min_wait=min_wait, max_wait=max_wait)
