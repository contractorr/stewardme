# Curriculum User-Authored Guides

**Status:** Implemented  
**Author:** Codex  
**Date:** 2026-03-29

## Overview

Learn now supports user-authored guides as a first-class curriculum layer. Built-in guides remain
repository-backed and immutable. User-generated guides and guide extensions are written into a
per-user curriculum root, scanned into the same per-user curriculum database, and surfaced through
the existing Learn flows.

The key architectural decision is unchanged from the draft: `Extend guide` creates a separate
linked supplemental guide instead of mutating the source guide in place. That keeps built-in guides
immutable, avoids mixed-origin chapter sets, and fits the current scanner/store model cleanly.

## Implemented Architecture

### Storage Layout

**Files:** `src/storage_paths.py`, `src/curriculum/user_content.py`

- Added per-user active and archive roots under the existing user data directory:
  - `curriculum/`
  - `curriculum-archive/`
- User-authored guides are stored as scanner-compatible directories:
  - `<curriculum>/<guide_id>/guide.yaml`
  - `<curriculum>/<guide_id>/<nn>-<chapter>.mdx`
- `guide.yaml` stores guide-level metadata that the scanner now reads:
  - `title`
  - `origin`
  - `kind`
  - `owner_user_id`
  - `base_guide_id`
  - `category`
  - `difficulty`
  - generation context such as `topic_prompt`, `depth`, `audience`, `time_budget`, `created_at`
- Archive is implemented by moving the guide directory from the active per-user curriculum root to
  the archive root. Archived guides are therefore outside all scanned content roots.

### Scanner and Models

**Files:** `src/curriculum/models.py`, `src/curriculum/scanner.py`,
`src/web/routes/curriculum.py`

- Added guide metadata enums:
  - `GuideOrigin`: `builtin | user`
  - `GuideKind`: `core | standalone | extension`
  - `GuideDepth`: `survey | practitioner | deep_dive`
- Added request models:
  - `GuideGenerationRequest`
  - `GuideExtensionRequest`
- `_content_dirs(user_id)` now includes:
  - repository curriculum root
  - configured extra content dirs
  - per-user curriculum root
- `CurriculumScanner` now reads optional `guide.yaml` metadata and applies it to scanned guides.
- Built-in guides continue to scan correctly when `guide.yaml` is absent.
- User-authored extensions remain separate guide rows and are linked by `base_guide_id`.

### Generation Service

**File:** `src/curriculum/guide_generator.py`

- Added `GuideGenerationService` to handle:
  - standalone guide generation from topic
  - linked extension generation from an existing guide
- Generation flow:
  1. use the authenticated user's resolved LLM credentials
  2. ask the model for a JSON guide plan
  3. generate chapter MDX files with frontmatter
  4. write into a temporary guide directory
  5. validate each chapter with `load_curriculum_document()`
  6. atomically rename the temp directory into the user's curriculum root
- Created guides are not auto-enrolled.
- Extensions do not modify the source guide's files.

### Store Schema and Query Model

**File:** `src/curriculum/store.py`

- Schema version bumped from `4` to `5`.
- Added guide columns:
  - `origin TEXT NOT NULL DEFAULT 'builtin'`
  - `kind TEXT NOT NULL DEFAULT 'core'`
  - `owner_user_id TEXT NOT NULL DEFAULT ''`
  - `base_guide_id TEXT`
  - `archived_at TEXT`
  - `archive_path TEXT NOT NULL DEFAULT ''`
- Archive state is stored directly on the `guides` table.
- There is no separate archival metadata table in the implemented version.
- Added store helpers:
  - `list_archived_guides()`
  - `archive_guide()`
  - `restore_guide()`
  - `is_guide_archived()`
  - `list_linked_extensions()`
- Active guide queries now exclude archived guides by default.
- Review, progress, and stats queries were updated to ignore archived guides unless explicitly
  requested.
- Built-in-only surfaces remain intentionally restricted to built-in content:
  - `list_tracks()`
  - `get_tree_data()`
  - `get_ready_guides()`

### API Surface

**File:** `src/web/routes/curriculum.py`

Implemented backend routes:

- `GET /api/curriculum/guides`
- `GET /api/curriculum/guides/archived`
- `GET /api/curriculum/guides/{guide_id}`
- `POST /api/curriculum/guides/generate`
- `POST /api/curriculum/guides/{guide_id}/extend`
- `DELETE /api/curriculum/guides/{guide_id}`
- `POST /api/curriculum/guides/{guide_id}/restore`

Key behavior:

- guide generation requires LLM credentials and returns `424` if unavailable
- generation and extension both sync the catalog before returning the created guide
- deletion is archive-only for user-authored guides
- restore moves the guide directory back to the active curriculum root and preserves prior learning
  state
- all guide detail payloads now include:
  - `origin`
  - `kind`
  - `owner_user_id`
  - `base_guide_id`
  - `archived_at`
  - `archive_path`
  - `linked_extensions`

Route-layer content resolution changes:

- chapter content loading is now user-aware through `_load_chapter_document(..., user_id=...)`
- catalog initialization and sync now use user-aware scanners

### Frontend

**Files:** `web/src/types/curriculum.ts`, `web/src/components/curriculum/GuideCard.tsx`,
`web/src/app/(dashboard)/learn/page.tsx`,
`web/src/app/(dashboard)/learn/[guideId]/page.tsx`

Implemented UI behavior:

- `/learn` now has a dedicated `Your Guides` section separate from the built-in library
- active and archived user-authored guides are shown in separate tabs
- `Create guide` dialog captures:
  - `topic`
  - `depth`
  - `audience`
  - `time_budget`
  - optional `instruction`
- guide cards show a `Your guide` badge for user-authored guides
- guide detail now shows:
  - built-in vs user-authored badge
  - extension badge for linked supplemental guides
  - `Extend guide` action for both built-in and user-authored guides
  - `Delete guide` action only for user-authored guides
  - linked extensions section when extensions exist
- archived guides can be restored from the Learn landing page

### Configuration

**File:** `src/cli/config_models.py`

Added curriculum config:

- `user_guide_default_chapters = 4`
- `user_guide_max_chapters = 6`
- `user_guide_max_topic_length = 240`
- `user_guide_generation_timeout_seconds = 120`

Validation now enforces sensible chapter-count bounds.

## Data and Ownership Rules

- Built-in guides always have `origin='builtin'` and remain immutable.
- User-generated guides always have `origin='user'`.
- Linked extensions are represented as user-authored guides with:
  - `kind='extension'`
  - `base_guide_id=<source guide id>`
- Archive is only valid for `origin='user'`.
- Progress state is preserved across archive and restore because the progress tables are unchanged
  and only active-query filtering changes.

## Request and Response Shapes

### Create Guide

Request:

```json
{
  "topic": "AI product strategy",
  "depth": "practitioner",
  "audience": "Product manager moving into AI",
  "time_budget": "3 hours per week",
  "instruction": "Optional free-form guidance"
}
```

Response:

- Returns the full decorated guide payload from `GET /guides/{guide_id}`

### Extend Guide

Request:

```json
{
  "prompt": "Add material on regulated launches and model risk decisions",
  "depth": "deep_dive",
  "audience": "Technical product lead",
  "time_budget": "2 focused sessions",
  "instruction": "Optional free-form guidance"
}
```

Response:

- Returns the full decorated extension guide payload

### Archive / Restore

Responses:

```json
{ "archived": true, "guide_id": "..." }
```

```json
{ "restored": true, "guide_id": "..." }
```

## Error Handling

- `400`
  - invalid request fields
  - topic too long
- `403`
  - built-in guide mutation attempt
- `404`
  - missing guide or missing archived content directory
- `409`
  - archive/restore attempted in the wrong state
  - target active or archive path already exists
- `424`
  - no available LLM credentials for generation
- `500`
  - generation failure after rollback
  - guide missing after sync when it should have been created

## Test Coverage

**File:** `tests/web/test_curriculum_routes.py`

Added route coverage for:

- generating a separate user-owned guide
- extending an existing guide into a linked extension
- archiving and restoring a user guide while preserving progress
- rejecting archive attempts for built-in guides

## Known Limitations

- Guide generation is synchronous in the request path.
- The built-in program graph and tree intentionally exclude user-authored guides in this version.
- Archived guides are restored from the Learn landing page, not from guide detail pages.
- There is no manual chapter editing flow yet; authoring is generation-based only.
