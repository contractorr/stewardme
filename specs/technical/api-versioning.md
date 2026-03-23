# API Versioning — Technical Spec

## Approach
Middleware rewrite in `src/web/app.py`. Zero router file changes.

## Middleware
- Rewrites `/api/v1/{path}` → `/api/{path}` internally before routing
- Adds `Deprecation: true` response header on non-v1 `/api/*` paths (excluding `/api/health`)

## Frontend
- All API calls in `web/src/` updated from `/api/` to `/api/v1/` prefix
- Applies to `apiFetch`, `apiFetchSSE`, and raw `fetch` calls

## Files Modified
- `src/web/app.py` — middleware added in `create_app()`
- `web/src/lib/api.ts` — path prefix update
- ~30 frontend files — `/api/` → `/api/v1/` string literal updates
