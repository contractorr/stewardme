"""Tests for MCP server init and tool listing."""

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, PropertyMock, patch

import pytest

from coach_mcp.bootstrap import reset_components, set_components
from coach_mcp.tools import build_tool_registry


@pytest.fixture
def mock_components():
    """Set bootstrap components directly to avoid real config/DB init."""
    components = {
        "config": {"paths": {"intel_db": "/tmp/test_intel.db"}},
        "config_model": MagicMock(),
        "paths": {
            "journal_dir": "/tmp/test_journal",
            "chroma_dir": "/tmp/test_chroma",
            "intel_db": Path("/tmp/test_intel.db"),
        },
        "storage": MagicMock(),
        "embeddings": MagicMock(),
        "search": MagicMock(),
        "intel_storage": MagicMock(),
        "intel_search": MagicMock(),
        "rag": MagicMock(),
        "advisor": None,
    }
    token = set_components(components)
    yield components
    reset_components(token)


def _build_registry(components):
    return build_tool_registry(components)


def test_load_tools_returns_20(mock_components):
    """Server should register exactly 47 tools."""
    registry = _build_registry(mock_components)
    tools = registry.get_mcp_definitions()
    assert len(tools) == 53
    assert len(registry.get_definitions()) == 53


def test_load_tools_names(mock_components):
    """All expected tool names should be present."""
    tools = _build_registry(mock_components).get_mcp_definitions()
    names = {t.name for t in tools}

    expected = {
        "journal_get_context",
        "journal_create",
        "journal_list",
        "journal_read",
        "journal_search",
        "journal_delete",
        "goals_list",
        "goals_add",
        "goals_check_in",
        "goals_update_status",
        "goals_add_milestone",
        "goals_complete_milestone",
        "intel_search",
        "intel_get_recent",
        "intel_scrape_now",
        "events_upcoming",
        "intel_trending_radar",
        "watchlist_list",
        "watchlist_upsert",
        "watchlist_delete",
        "recommendations_list",
        "recommendations_update_status",
        "recommendations_action_create",
        "recommendations_action_update",
        "recommendations_action_list",
        "recommendations_action_weekly_plan",
        "recommendations_rate",
        "research_topics",
        "research_run",
        "research_dossiers_list",
        "research_dossier_create",
        "get_reflection_prompts",
        "profile_get",
        "profile_update_field",
        "projects_discover",
        "projects_ideas",
        "projects_list",
        "get_insights",
        "get_daily_brief",
        "memory_list_facts",
        "memory_search_facts",
        "memory_delete_fact",
        "memory_get_stats",
        "memory_list_observations",
        "threads_list",
        "threads_get_entries",
        "threads_reindex",
        "curriculum_list_guides",
        "curriculum_get_chapter",
        "curriculum_progress",
        "curriculum_due_reviews",
        "curriculum_recommend_next",
        "curriculum_skill_tree",
    }
    assert names == expected


def test_tools_have_descriptions(mock_components):
    """Every tool must have a non-empty description."""
    tools = _build_registry(mock_components).get_mcp_definitions()
    for tool in tools:
        assert tool.description, f"Tool {tool.name} missing description"


def test_tools_have_input_schemas(mock_components):
    """Every tool must have an inputSchema with type=object."""
    tools = _build_registry(mock_components).get_mcp_definitions()
    for tool in tools:
        assert tool.inputSchema["type"] == "object", f"Tool {tool.name} bad schema type"


def test_recommendation_tools_publish_string_rec_ids(mock_components):
    """Recommendation MCP schemas should consistently expose string recommendation IDs."""
    tools = {tool.name: tool for tool in _build_registry(mock_components).get_mcp_definitions()}

    assert (
        tools["recommendations_action_create"].inputSchema["properties"]["rec_id"]["type"]
        == "string"
    )
    assert (
        tools["recommendations_action_update"].inputSchema["properties"]["rec_id"]["type"]
        == "string"
    )
    assert (
        tools["recommendations_update_status"].inputSchema["properties"]["rec_id"]["type"]
        == "string"
    )
    assert tools["recommendations_rate"].inputSchema["properties"]["rec_id"]["type"] == "string"


def _mock_request_context(registry):
    """Return a context manager that patches app.request_context for direct handler calls."""
    from coach_mcp.server import app

    ctx = SimpleNamespace(lifespan_context={"registry": registry})
    return patch.object(type(app), "request_context", new_callable=PropertyMock, return_value=ctx)


@pytest.mark.asyncio
async def test_call_unknown_tool(mock_components):
    """Calling unknown tool should return error JSON."""
    from coach_mcp.server import call_tool

    registry = _build_registry(mock_components)
    with _mock_request_context(registry):
        result = await call_tool("nonexistent_tool", {})
    assert len(result) == 1
    data = json.loads(result[0].text)
    assert "error" in data
    assert "Unknown tool" in data["error"]


@pytest.mark.asyncio
async def test_call_tool_omits_traceback(mock_components):
    """Tool failures should not leak tracebacks back to MCP clients."""
    from coach_mcp.server import call_tool
    from services.tool_registry import ToolRegistry

    registry = ToolRegistry()
    registry.register(
        name="broken_tool",
        toolset="test",
        description="broken",
        schema={"type": "object", "properties": {}, "required": []},
        handler=lambda _args: (_ for _ in ()).throw(ValueError("boom")),
    )

    with _mock_request_context(registry):
        result = await call_tool("broken_tool", {})
    data = json.loads(result[0].text)
    assert data == {"error": "broken_tool: boom"}


@pytest.mark.asyncio
async def test_list_tools_async(mock_components):
    """list_tools should return Tool objects."""
    from coach_mcp.server import list_tools

    registry = _build_registry(mock_components)
    with _mock_request_context(registry):
        tools = await list_tools()
    assert len(tools) == 53
