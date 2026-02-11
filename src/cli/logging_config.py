"""Structured logging configuration using structlog."""

import logging
import re
import sys

import structlog

# Patterns to redact from log output
_REDACT_PATTERNS = [
    # API keys: sk-ant-..., sk-..., Bearer tokens
    (re.compile(r"(sk-ant-[a-zA-Z0-9_-]{10})[a-zA-Z0-9_-]*"), r"\1...REDACTED"),
    (re.compile(r"(sk-[a-zA-Z0-9_-]{6})[a-zA-Z0-9_-]{20,}"), r"\1...REDACTED"),
    (re.compile(r"(Bearer\s+)[a-zA-Z0-9_.-]{20,}"), r"\1REDACTED"),
    # Generic API key patterns in key=value
    (re.compile(r"(api[_-]?key['\"]?\s*[:=]\s*['\"]?)[a-zA-Z0-9_-]{10,}"), r"\1REDACTED"),
    # Email addresses
    (re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"), "REDACTED@email"),
]


def _redact_sensitive(_, __, event_dict: dict) -> dict:
    """Structlog processor to redact API keys/tokens from log output."""
    for key, value in event_dict.items():
        if isinstance(value, str):
            for pattern, replacement in _REDACT_PATTERNS:
                value = pattern.sub(replacement, value)
            event_dict[key] = value
    return event_dict


def setup_logging(json_mode: bool = False, level: str = "INFO") -> None:
    """Configure structlog with appropriate renderer.

    Args:
        json_mode: Use JSON renderer (for daemon/machine consumption).
                   False = console renderer (Rich-compatible, for CLI).
        level: Log level string (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """
    log_level = getattr(logging, level.upper(), logging.INFO)

    # Shared processors
    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.CallsiteParameterAdder(
            [
                structlog.processors.CallsiteParameter.MODULE,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
            ]
        ),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
        _redact_sensitive,
    ]

    if json_mode:
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer()

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Configure stdlib logging to use structlog formatter
    formatter = structlog.stdlib.ProcessorFormatter(
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
    )

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(log_level)
