# API Versioning

## Problem
25 route modules at `/api/{name}` with no version prefix. Adding later is a breaking change.

## Desired Behavior
- All API endpoints accessible at `/api/v1/{path}`
- Old `/api/{path}` routes still work for backward compat but signal deprecation
- `/api/health` stays unversioned

## Acceptance Criteria
- `GET /api/v1/health` returns 200
- `GET /api/v1/journal` returns same result as `GET /api/journal`
- Old `/api/journal` returns `Deprecation: true` header
- `/api/health` does NOT get deprecation header
- Frontend updated to use `/api/v1/` prefix everywhere

## Edge Cases
- Nested paths like `/api/v1/advisor/conversations/{id}` must rewrite correctly
- Query parameters preserved through rewrite
