# Recurring Threads

**Status:** Updated for the simplified product model

## Overview

Recurring threads are now surfaced through Radar's `Threads` tab instead of a standalone workspace.

## Key Modules

- `src/web/routes/threads.py`
- thread extraction/grouping services
- `web/src/app/(dashboard)/radar/page.tsx`

## Interfaces

- `GET /api/threads/inbox?limit=...`
- thread action endpoints for goal, research, dossier, and dismiss flows
- thread state updates under `/api/threads/{id}/state`

## Thread Model

- `journal_threads` includes an internal `strength REAL NOT NULL DEFAULT 0.0` column.
- `Thread.strength` is derived from:
  - entry count / recurrence
  - average entry similarity inside the thread
  - inactivity since the last matching entry
  - divergence penalty for low-similarity clusters
- Strength is recomputed after entry joins and refreshed on thread reads so stale threads weaken over time.

## Ranking Behavior

- Radar thread APIs can still sort or group for UI workflows, but advisor recurring-thought injection now ranks threads by `strength` first.
- Recent entry count remains a secondary signal for display and tie-breaking, not the primary recurrence score.

## Simplified Product Notes

- This keeps active monitoring work together in Radar.
- Receipt and Journal follow-ups should deep-link to Radar, not to a separate thread workspace concept.

## Thread Inbox State Machine

### Module

`src/journal/thread_inbox.py`

### Constants

```python
VALID_INBOX_STATES = {
    "active", "dismissed", "goal_created",
    "research_started", "dossier_started", "dormant"
}
```

### SQLite Table: `thread_inbox_state`

| Column | Type | Notes |
|---|---|---|
| `thread_id` | TEXT PK | FK → `journal_threads.id` |
| `state` | TEXT | one of `VALID_INBOX_STATES` |
| `linked_goal_path` | TEXT | nullable; set when state = `goal_created` |
| `linked_dossier_id` | TEXT | nullable; set when state = `dossier_started` |
| `updated_at` | TEXT | ISO-8601 timestamp |

### `ThreadInboxStateStore`

- `upsert_state(thread_id, state, linked_goal_path=None, linked_dossier_id=None)` — SQLite `INSERT OR REPLACE`; linked fields are only overwritten if explicitly provided (not None).
- `get_state(thread_id)` → row or None.
- `list_states(state_filter=None)` → list of rows, optionally filtered by state value.

### `ThreadInboxService`

- `list_inbox(limit, state_filter, query)` — JOINs `journal_threads` with `thread_inbox_state` overlay (LEFT JOIN so threads without a state row default to `active`), attaches `snippets` (last 3 matching entries, truncated to 160 chars), resolves `available_actions` from current state, and applies optional state/query filters before returning.
- State → `available_actions` mapping is a module-level dict; `active` returns the full action set, terminal states return view/deep-link actions only, `dormant` returns `["reactivate"]`.

### Invariants

- A thread without a state row behaves as `active` (default).
- `dismissed` → `active` resurface is triggered by the thread-detection pipeline when a new entry joins the thread, not by the state store directly.
- `dormant` transition is applied by a background sweep comparing `journal_threads.last_seen` against a configurable inactivity window.
