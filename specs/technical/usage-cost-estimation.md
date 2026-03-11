# Per-User LLM Cost Estimation - Technical Spec

**Status:** Implemented
**Date:** 2026-03-10

## Overview

Track token usage across all three LLM providers, accumulate through agentic iterations, persist as metadata in `usage_events`, and expose via a per-user API endpoint plus settings UI card.

## Components Modified

### Provider layer (`src/llm/providers/`)

All three providers gain `_last_usage: dict | None` instance property, set after every `generate()` and `generate_with_tools()` call.

- **Claude**: already had `_record_usage()`; now sets `self._last_usage` from its return value
- **OpenAI**: new `_extract_and_record_usage()` reads `response.usage.prompt_tokens` and `completion_tokens`, calls `metrics.token_usage()`, returns dict with `input_tokens`, `output_tokens`, `billed_input_tokens`
- **Gemini**: same pattern, reads `response.usage_metadata.prompt_token_count` and `candidates_token_count`

### Agentic orchestrator (`src/advisor/agentic.py`)

- `_total_usage: dict` - zeroed at start of `run()`, accumulated from each `generate_with_tools()` response
- Bug fix: `_total_input_tokens = input_tokens` became `_total_input_tokens += input_tokens`

### Cost computation (`src/observability.py`)

- `compute_cost(model, billed_input, output_tokens) -> float` - reuses `Metrics._get_pricing()` lookup

### Service layer (`src/services/advice.py`)

- `_collect_usage_from_engine(engine)` - reads `_orchestrator._total_usage` (agentic) or `llm._last_usage` (classic)
- `_get_model_name(engine)` - reads `llm.model_name` or `llm.model`
- `run_advice()` - adds `usage` and `model` keys to return payload
- `finish_conversation_turn()` - optional `usage` and `model` params; enriches `log_event()` metadata with `input_tokens`, `output_tokens`, `billed_input_tokens`, `estimated_cost_usd`, and `model`

### Web routes (`src/web/routes/advisor.py`)

Both `ask_advisor()` and `ask_advisor_stream()` pass `usage` and `model` to `finish_conversation_turn()`.

### User state store (`src/user_state_store.py`)

`get_user_usage_stats(user_id, days=30)` queries `usage_events` with `json_extract` on metadata fields and groups by model.

`src/web/user_store.py` re-exports this function as a compatibility wrapper for existing web imports.

### API (`src/web/routes/settings.py`)

`GET /api/settings/usage?days=30` returns `UsageStatsResponse`.

### Models (`src/web/models.py`)

- `UsageModelStats`
- `UsageStatsResponse`

### Frontend (`web/src/app/(dashboard)/settings/page.tsx`)

The usage card sits between AI and Keys sections. It fetches `/api/settings/usage` on mount and shows total queries, estimated cost, and per-model breakdown with token counts.

## Data flow

```text
LLM response -> provider._last_usage -> orchestrator._total_usage (if agentic)
    -> _collect_usage_from_engine() -> run_advice() return
    -> finish_conversation_turn() -> log_event("chat_query", metadata={...tokens, cost, model})
    -> get_user_usage_stats() in user_state_store -> json_extract aggregation
    -> GET /api/settings/usage
```

## No new tables

All data is stored as JSON in the existing `usage_events.metadata` column.
