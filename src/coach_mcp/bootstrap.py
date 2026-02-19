"""Lazy component initialization for MCP server."""

import structlog

logger = structlog.get_logger()

_components = None


def get_components() -> dict:
    """Lazy singleton wrapping cli.utils.get_components(skip_advisor=True).

    Returns the same dict as cli/utils.py but skips LLM/advisor init.
    """
    global _components
    if _components is None:
        logger.info("mcp_bootstrap_init")
        from cli.utils import get_components as _get

        _components = _get(skip_advisor=True)
    return _components
