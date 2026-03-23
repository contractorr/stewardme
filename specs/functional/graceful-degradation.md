# Graceful Degradation

## Problem

~30 `except Exception: pass` blocks silently swallow errors across advisor/, journal/, services/, intelligence/, and coach_mcp/. When these features degrade, there is zero logging or metrics — diagnostic blindness in production.

## Desired Behavior

When a non-critical subsystem fails (cache init, goal loading, profile lookup, etc.), the system should:

1. **Continue operating** with the same fallback values as today (empty string, None, etc.)
2. **Log** the failure via structlog at an appropriate level (warning for unexpected, debug for expected)
3. **Increment** an observability counter so failures are visible in metrics summaries

## Acceptance Criteria

- [ ] Two reusable primitives: `@graceful` decorator and `graceful_context` context manager
- [x] All 9 Phase 1 sites replaced (engine.py, advice.py, scheduler.py)
- [ ] All 20 Phase 2 sites replaced (tools, nudges, recs, threads, trends, MCP)
- [ ] Each site produces a structlog warning (or debug) with `exc_info=True` on failure
- [ ] Each site increments a named `metrics.counter()` on failure
- [ ] Zero behavioral change: all fallback values remain identical to current code
- [ ] `exc_types` parameter allows narrowing which exceptions are caught
- [ ] `log_level` parameter allows debug-level logging for expected failures (e.g., missing web module in CLI mode)
- [ ] The primitives themselves never raise — last-resort catch writes to stderr

## Edge Cases

- If structlog or metrics themselves fail, the primitives must not propagate the error
- `exc_types` narrowing: uncaught exception types must propagate normally
- Context manager: variables assigned inside the block retain their pre-block default when an exception fires before assignment
- Decorator with `fallback=None`: must return None (not raise) on exception
