# Services Package

Cross-surface service helpers shared by web, CLI, and MCP layers live here.

## Entry Points

- `advice.py`: shared advisor request lifecycle helpers
- `daily_brief.py`, `recommendation_actions.py`, `projects.py`, `profile.py`: surface-neutral orchestration helpers
- `tool_registry.py`: shared tool registration and execution
- `ranking.py`, `reranker.py`, `temporal.py`: ranking and recency helpers
- `entity_bridge.py`, `tokens.py`, `redact.py`: shared support utilities

## Working Rules

- Service helpers should stay surface-neutral and avoid importing route-specific or CLI-specific presentation concerns.
- Shared DTO serialization belongs here when multiple delivery surfaces need the same shape.
- Tool-registry changes must stay aligned with both advisor tool use and MCP registration.

## Validation

- `uv run pytest tests/services/ tests/coach_mcp/test_registry.py -q`
