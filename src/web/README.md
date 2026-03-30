# Web Backend Package

FastAPI app assembly, request models, route modules, and web persistence adapters live here.

## Related Specs

- `specs/technical/web.md`
- `specs/technical/api-versioning.md`
- `specs/technical/user-data-storage.md`

## Entry Points

- `app.py`: application factory, middleware, and route registration
- `models.py`: shared request and response schemas exported to the frontend
- `routes/`: API surfaces grouped by workspace and capability
- `deps.py`, `deps_base.py`, `deps_credentials.py`, `deps_features.py`, `deps_storage.py`: dependency wiring and user-scoped access
- `auth.py`, `crypto.py`, `rate_limit.py`: auth, encryption, and request guards
- `conversation_store.py`, `user_store.py`, `notification_store.py`: web-facing persistence helpers
- `services/journal_entries.py`: web-specific journal formatting helpers

## Working Rules

- Contract changes should regenerate `web/openapi.json` and `web/src/types/api.generated.ts`.
- Route modules should stay thin and delegate behavior to domain packages or shared services.
- Hotspots in `routes/curriculum.py` and `models.py` should only grow through helper extraction or split modules.

## Validation

- `just test-web`
- `just contracts-check`
- `uv run pytest tests/web/ -q`
