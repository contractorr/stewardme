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
