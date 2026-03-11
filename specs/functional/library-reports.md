# Library

**Status:** Updated for the simplified product model

## Purpose

Library is the durable reference workspace for uploaded documents, generated reports, and archived dossier outputs. It should feel like a calm reference surface rather than an active monitoring console.

## Product Placement

- Workspace: `Library`
- Primary job: find, reuse, and manage durable reference material
- Journal handoff: the user can jump from Library into the deeper Journal workspace when they need source notes instead of durable artifacts

## Current Behavior

- Library supports type filtering across documents, reports, and dossiers.
- Active dossiers stay in Radar until they are archived.
- Archived dossiers become read-only reference material in Library.
- Report-like items can still be refreshed or edited from the Library workspace.

## User Flows

- Filter the library by content type.
- Open a report or archived dossier for later reference.
- Jump from Library to Journal when the user wants source captures rather than durable outputs.

## Library Index and Search

- `LibraryIndex` provides FTS5 full-text search (Porter stemmer) across title, body, extracted text, collection, and filename.
- Search covers both LLM-generated reports and uploaded PDFs.
- Results ranked by FTS5 relevance score.

## PDF Upload and Extraction

- Users upload PDFs via `POST /api/library/reports/upload`.
- Binary stored in `library/attachments/{report_id}.pdf`; extracted text saved in `library/extracted/`.
- Text extraction uses `pypdf` (optional dependency). Falls back to empty text if unavailable.
- Extracted text feeds into the FTS5 index and optionally into the memory pipeline (`config.memory.enabled`).
- Download via `GET /api/library/reports/{id}/file` as `FileResponse` with path traversal protection.

## Report Storage

- `ReportStore` persists LLM-generated reports as markdown files with YAML frontmatter in `~/coach/users/{id}/library/`.
- Report lifecycle: `ready` → `archived` → `restored`.
- Reports generated using user profile + active goals as context.

## Key System Components

- `web/src/app/(dashboard)/library/page.tsx`
- `src/web/routes/library.py`
- `src/web/routes/research.py`
- `src/library/reports.py` — `ReportStore`
- `src/library/index.py` — `LibraryIndex` (FTS5)
- `src/library/pdf_text.py` — PDF extraction
