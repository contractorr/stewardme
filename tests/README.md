# Test Layout

Tests mirror the package roots and delivery surfaces they protect.

## Fast Navigation

- `tests/advisor/`: advisor, goals, briefings, and recommendation behavior
- `tests/cli/`: CLI registration and command behavior
- `tests/coach_mcp/`: MCP server and tool registration
- `tests/curriculum/`: guide storage, scanning, and review flows
- `tests/embeddings/`: shared embedding-provider helpers
- `tests/eval/`: evaluation and quality guardrails
- `tests/integration/`: broader end-to-end slices
- `tests/intelligence/`: scrapers, radar, watchlists, and ranking
- `tests/journal/`: journal storage, search, threads, exports, and mind maps
- `tests/library/`: library storage, indexing, and embeddings
- `tests/llm/`: provider compatibility shims
- `tests/memory/`: memory persistence and consolidation
- `tests/profile/`: profile storage and interview flows
- `tests/research/`: topic selection, search, synthesis, dossiers, and escalation
- `tests/services/`: shared service helpers
- `tests/web/`: FastAPI routes, app startup, and API contracts

## Working Rules

- Prefer the smallest slice that covers the files you changed.
- Route changes should usually add or update a matching `tests/web/` case.
- Structural repo metadata changes should keep guardrail tests green.
- The default fast CI slice is `uv run pytest -m "not slow and not web and not integration" --durations=20`.
