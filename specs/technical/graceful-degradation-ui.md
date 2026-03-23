# Graceful Degradation UI — Technical Spec

## Backend

### `src/degradation_collector.py` (new)
- `ContextVar`-based request-scoped list
- `init_collector()`, `record_degradation(component, message)`, `get_degradations()`, `clear_collector()`

### `src/graceful.py` hook
- `_log_and_count()` additionally calls `record_degradation()`
- Metric name → user-friendly message mapping

### FastAPI middleware (`src/web/app.py`)
- Init collector before request, clear after

### Response enrichment
- Advisor, briefing, greeting routes include `degradations` in response
- Advisor streaming emits degradation SSE events

## Frontend
### `DegradationBanner.tsx`
- Amber banner, renders when `degradations.length > 0`
- Added to `EmbeddedAdvisor.tsx` and advisor page

## ContextVar note
- Uses `contextvars.copy_context().run()` for 3.11 compat with `asyncio.to_thread()`
