# Advisor Package

Conversational advising, recommendations, goals, briefing flows, and orchestration logic live here.

## Related Specs

- `specs/functional/ask-advice.md`
- `specs/functional/recommendations.md`
- `specs/functional/goal-tracking.md`
- `specs/functional/since-you-were-away-why-now.md`
- `specs/technical/advisor.md`
- `specs/technical/action-plans.md`
- `specs/technical/suggestions-engine.md`
- `specs/technical/llm-council.md`

## Entry Points

- `engine.py`: primary ask/reply orchestration and result packaging
- `agentic.py`: tool-enabled advisor loop
- `context_assembler.py`, `rag.py`, `retrievers/`: journal, intel, memory, and profile retrieval
- `recommendations.py`, `recommendation_storage.py`, `scoring.py`: recommendation generation, persistence, and feedback-aware ranking
- `goals.py`, `projects.py`, `nudges.py`, `outcomes.py`: goal and execution support flows
- `daily_brief.py`, `action_brief.py`, `return_brief.py`, `why_now.py`, `greeting.py`: briefing and "what changed" surfaces
- `council.py`, `tools.py`, `trace.py`, `trace_store.py`: council execution, tool wiring, and request tracing

## Working Rules

- Surface layers should call into advisor services and engines rather than duplicating decision logic.
- Behavior changes usually require matching updates in specs, route payloads, and frontend consumers.
- New context sources or tool calls should degrade cleanly when user data, credentials, or providers are unavailable.

## Validation

- `just test-advisor`
- `uv run pytest tests/advisor/ -q`
- `uv run pytest tests/web/test_advisor_routes.py tests/web/test_recommendations_routes.py tests/web/test_suggestions_routes.py tests/web/test_goals_routes.py tests/web/test_briefing_routes.py tests/web/test_greeting_routes.py tests/web/test_trace_routes.py -q`
