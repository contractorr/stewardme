# MCP Package

The stdio MCP server and tool registration layer live here.

## Related Specs

- `specs/technical/mcp.md`
- `specs/technical/unified-tool-registry.md`

## Entry Points

- `server.py`: MCP server lifecycle, tool listing, and tool execution
- `bootstrap.py`: shared component initialization for tool handlers
- `tools/`: tool modules grouped by workspace
- `async_utils.py`: async bridging helpers for tool execution

## Working Rules

- Tool modules should register metadata and delegate real work to domain packages or shared services.
- Keep MCP schemas and shared registry behavior aligned with `src/services/tool_registry.py`.
- Metadata-only startup fallback should remain lightweight and safe when full bootstrap is unavailable.

## Validation

- `uv run pytest tests/coach_mcp/ -q`
