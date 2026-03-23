# Graceful Degradation — Technical Spec

## Module: `src/graceful.py`

### Exports

```python
@graceful(metric: str, *, fallback=None, log_level: str = "warning", exc_types: tuple = (Exception,))
```

Decorator. On exception matching `exc_types`: log, count, return `fallback`.

```python
graceful_context(metric: str, *, log_level: str = "warning", exc_types: tuple = (Exception,))
```

Context manager. On exception matching `exc_types`: log, count, suppress.

### Shared helper

```python
_log_and_count(metric: str, log_level: str, qualname: str | None = None) -> None
```

- `structlog.get_logger().log(level, "graceful.caught", metric=metric, qualname=qualname, exc_info=True)`
- `metrics.counter(metric)`
- Wrapped in bare `try/except` → `sys.stderr.write()` as last resort

### Invariants

- `_log_and_count` never raises
- Decorator preserves `__name__` and `__doc__` via `functools.wraps`
- Context manager uses `contextlib.contextmanager` or `__enter__`/`__exit__`
- Exceptions not in `exc_types` propagate unchanged

### Metric naming convention

`graceful.<module>.<operation>` — e.g. `graceful.advisor.cache_init`

### Dependencies

- `structlog` (already in deps)
- `observability.metrics` singleton (already exists)
- `sys` (stdlib)
- `functools` (stdlib)

## Sites

| File | Lines | Metric | fallback | log_level | exc_types |
|------|-------|--------|----------|-----------|-----------|
| advisor/engine.py | 99-105 | graceful.advisor.cache_init | N/A (ctx mgr) | warning | (Exception,) |
| advisor/engine.py | 127-144 | graceful.advisor.goal_init | N/A (ctx mgr) | warning | (Exception,) |
| advisor/engine.py | 151-161 | graceful.advisor.journal_fallback | N/A (ctx mgr) | warning | (Exception,) |
| services/advice.py | 109-122 | graceful.advice.collect_usage | None | warning | (Exception,) |
| services/advice.py | 125-133 | graceful.advice.get_model | None | warning | (Exception,) |
| intelligence/scheduler.py | 276-299 | graceful.scheduler.rss_merge | N/A (ctx mgr) | debug | (Exception,) |
| intelligence/scheduler.py | 351-362 | graceful.scheduler.event_location | N/A (ctx mgr) | warning | (Exception,) |
| intelligence/scheduler.py | 419-430 | graceful.scheduler.gh_issues_langs | N/A (ctx mgr) | warning | (Exception,) |
| intelligence/scheduler.py | 544-551 | graceful.scheduler.log_event | N/A (ctx mgr) | debug | (ImportError,) |

## Phase 2 Sites

| File | Metric | fallback | log_level | exc_types |
|------|--------|----------|-----------|-----------|
| advisor/tools.py | graceful.tools.embed_journal | N/A (ctx mgr) | warning | (Exception,) |
| advisor/tools.py | graceful.tools.embed_goal | N/A (ctx mgr) | warning | (Exception,) |
| advisor/tools.py | graceful.tools.goal_intel_match | N/A (ctx mgr) | warning | (Exception,) |
| advisor/tools.py | graceful.tools.goal_search | N/A (ctx mgr) | warning | (Exception,) |
| advisor/nudges.py | graceful.nudges.profile_stale | N/A (ctx mgr) | warning | (Exception,) |
| advisor/nudges.py | graceful.nudges.stale_goals | N/A (ctx mgr) | warning | (Exception,) |
| advisor/nudges.py | graceful.nudges.journal_streak | N/A (ctx mgr) | warning | (Exception,) |
| advisor/nudges.py | graceful.nudges.profile_init | N/A (ctx mgr) | warning | (Exception,) |
| advisor/recommendations.py | graceful.recs.journal_check | N/A (ctx mgr) | warning | (Exception,) |
| advisor/recommendations.py | graceful.recs.profile_hours | N/A (ctx mgr) | warning | (Exception,) |
| advisor/action_brief.py | graceful.action_brief.profile_load | N/A (ctx mgr) | warning | (Exception,) |
| advisor/entity_retriever.py | graceful.entity_retriever.bridge_init | N/A (ctx mgr) | warning | (Exception,) |
| advisor/retrievers/memory.py | graceful.retriever.observations | N/A (ctx mgr) | warning | (Exception,) |
| journal/threads.py | graceful.threads.label_extract | N/A (ctx mgr) | warning | (Exception,) |
| journal/threads.py | graceful.threads.entry_date | N/A (ctx mgr) | warning | (Exception,) |
| journal/trends.py | graceful.trends.llm_analysis | N/A (ctx mgr) | warning | (Exception,) |
| journal/trends.py | graceful.trends.embedding_lookup | N/A (ctx mgr) | warning | (Exception,) |
| coach_mcp/tools/journal.py | graceful.mcp.journal.goals_summary | N/A (ctx mgr) | debug | (Exception,) |
| coach_mcp/tools/journal.py | graceful.mcp.journal.health | N/A (ctx mgr) | debug | (Exception,) |
| coach_mcp/tools/journal.py | graceful.mcp.journal.title_gen | N/A (ctx mgr) | debug | (Exception,) |
| coach_mcp/tools/journal.py | graceful.mcp.journal.date_parse | N/A (ctx mgr) | debug | (Exception,) |
| coach_mcp/tools/intelligence.py | graceful.mcp.intel.profile_load | N/A (ctx mgr) | debug | (Exception,) |
| coach_mcp/tools/projects.py | graceful.mcp.projects.profile_load | N/A (ctx mgr) | debug | (Exception,) |
