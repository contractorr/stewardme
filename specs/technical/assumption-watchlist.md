# Tracked Topics and Assumptions

**Status:** Updated for the simplified product model

## Overview

Tracked topics and assumption data remain advanced configuration inputs that feed Radar and recommendation ranking.

## Key Modules

- `src/web/routes/intel.py`
- `src/web/routes/suggestions.py`
- `web/src/app/(dashboard)/settings/page.tsx`

Note (2026-07): the standalone `/api/assumptions` CRUD route module
(`src/web/routes/assumptions.py`) was removed — no frontend ever called it.
Assumptions are still extracted from journal entries at save time
(`advisor/assumptions.py` + per-user `AssumptionStore`) and surface through
suggestion payloads and return briefings; management UX, if built, should
come back through those surfaces rather than a bare CRUD API.

## Interfaces

- `GET/POST/PATCH/DELETE /api/intel/watchlist`
- suggestion payloads that reference watchlist evidence
- Settings anchors such as `/settings#watchlist`

## Simplified Product Notes

- The user-facing placement is Settings, not a dedicated watchlist workspace.
- Radar consumes tracked-topic context to explain why a signal matters.
