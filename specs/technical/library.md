# Library

**Status:** Updated for the simplified product model

## Overview

Library is the durable reference workspace for uploaded documents, generated reports, and archived dossier outputs.

## Key Modules

- `src/web/routes/library.py`
- `src/web/routes/research.py`
- `web/src/app/(dashboard)/library/page.tsx`

## Interfaces

- `GET /api/library/reports` and related detail/update endpoints
- `GET /api/research/dossiers?include_archived=true&limit=50`
- report refresh, archive, and file download flows

## Library Package (`src/library/`)

### `reports.py` — `ReportStore`
- Markdown files with YAML frontmatter in `~/coach/users/{id}/library/`
- Lifecycle states: `ready`, `archived`, `restored`
- `_generate_report_content()` uses LLM with user profile + active goals as context
- PDF binary storage in `attachments/{report_id}.pdf`, extracted text in `extracted/`

### `index.py` — `LibraryIndex`
- SQLite FTS5 index with Porter stemmer
- Columns: title, body, extracted_text, collection, filename
- Supports search across all library item types (reports + uploads)

### `pdf_text.py`
- `extract_text_from_pdf_bytes()` — uses `pypdf` (optional)
- Falls back gracefully if pypdf unavailable
- Extracted text feeds FTS5 index + optional memory pipeline

### Routes
- `POST /api/library/reports/upload` — PDF upload with text extraction
- `GET /api/library/reports/{id}/file` — FileResponse download, path traversal protected
- `GET /api/library/reports` — list with FTS search support
- Report CRUD: create, update, archive, restore, delete

## Simplified Product Notes

- Active dossiers stay in Radar until archived.
- Library should feel like a reference surface, not an active monitoring console.
