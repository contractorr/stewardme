"""Shared fixtures for MCP tests."""

import pytest

from coach_mcp.bootstrap import _components_var


@pytest.fixture(autouse=True)
def reset_bootstrap():
    """Reset the bootstrap ContextVar between tests."""
    token = _components_var.set(None)
    yield
    _components_var.reset(token)
