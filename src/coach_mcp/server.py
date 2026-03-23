"""MCP server entry point — stdio transport, tool routing by prefix."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import structlog
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from coach_mcp.bootstrap import get_components
from coach_mcp.tools import build_tool_registry

logger = structlog.get_logger()


@asynccontextmanager
async def _lifespan(server: Server) -> AsyncIterator[dict]:
    components = get_components()
    registry = build_tool_registry(components)
    yield {"registry": registry}


app = Server("stewardme", lifespan=_lifespan)


@app.list_tools()
async def list_tools() -> list[Tool]:
    registry = app.request_context.lifespan_context["registry"]
    return registry.get_mcp_definitions()


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    registry = app.request_context.lifespan_context["registry"]
    text = registry.execute(name, arguments)
    return [TextContent(type="text", text=text)]


async def run():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


def main():
    import asyncio

    asyncio.run(run())


if __name__ == "__main__":
    main()
