# Data Export — Technical Spec

## Web API

### `GET /api/export`
Returns full user data as JSON with `Content-Disposition: attachment`.

Sections:
- `journal` — via `JournalStorage` markdown files parsed with frontmatter
- `intel` — recent intel items from user-scoped DB
- `memory` — `FactStore.get_all_active()` serialized
- `goals` — `GoalTracker.get_goals(include_inactive=True)`
- `curriculum` — `CurriculumStore.get_stats()` + enrollments
- `profile` — `ProfileStorage.load()` dict

Auth: requires JWT (per-user isolation).

## CLI Extensions

### `coach export memory`
Dumps all active facts as JSON via `FactStore.get_all_active()`.

### `coach export curriculum`
Exports enrollment + progress + review stats.

### `coach export goals`
Exports all goals (active + inactive) with milestones.

## Files
- New: `src/web/routes/export.py`, `tests/web/test_export.py`
- Modify: `src/web/routes/__init__.py`, `src/cli/commands/export.py`
