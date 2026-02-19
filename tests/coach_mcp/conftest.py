"""Shared fixtures for MCP tests."""

import pytest

import coach_mcp.bootstrap


@pytest.fixture(autouse=True)
def reset_bootstrap():
    """Reset the bootstrap singleton between tests."""
    coach_mcp.bootstrap._components = None
    yield
    coach_mcp.bootstrap._components = None
