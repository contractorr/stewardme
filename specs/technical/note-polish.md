---
id: note-polish
category: tracked_module
status: experimental
implements:
- note-polish
code_paths:
- src/notes
- src/web/routes/notes.py
- web/src/app/(dashboard)/notes
- tests/notes
- tests/web/test_notes_routes.py
last_reviewed: '2026-07-02'
---

# Note Polish — Technical Spec

## Overview

LLM pipeline that turns messy markdown/plain text into sanitized HTML through an explicit
review gate: polish → diff + itemized corrections → user accepts (store HTML, drop original)
or discards (delete everything). New `src/notes/` package with a per-user SQLite store, a
polisher that wraps the standard `LLMProvider`, a markdown→HTML renderer, and an allowlist
HTML sanitizer built on BeautifulSoup (already a core dependency — no new deps).

## Dependencies

**Depends on:** `llm` (provider factory), `db.wal_connect`, `beautifulsoup4`, stdlib `difflib`.
**Depended on by:** `web.routes.notes`.

## Data Model (`notes.db` in the user's data dir)

```sql
CREATE TABLE notes (
    id TEXT PRIMARY KEY,                 -- uuid4 hex
    user_id TEXT NOT NULL,
    title TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'pending',   -- 'pending' | 'accepted'
    original_text TEXT,                  -- NULLed on accept (never stored after acceptance)
    polished_markdown TEXT NOT NULL DEFAULT '',
    polished_html TEXT NOT NULL DEFAULT '',
    diff TEXT NOT NULL DEFAULT '',       -- unified diff original → polished
    corrections TEXT NOT NULL DEFAULT '[]',   -- JSON list of correction objects
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accepted_at TIMESTAMP
);
CREATE INDEX idx_notes_user ON notes(user_id, status, created_at);
```

Correction object: `{"type": "spelling|grammar|factual|rewording|removal",
"original": str, "corrected": str, "reason": str}` (unknown types coerced to `rewording`).

## Components

### `notes/polisher.py`

```python
MAX_NOTE_CHARS = 40_000

@dataclass
class PolishResult:
    polished_markdown: str
    corrections: list[dict]
    diff: str            # difflib.unified_diff(original, polished, lineterm="")

class NotePolisher:
    def __init__(self, llm_provider: LLMProvider): ...
    def polish(self, text: str) -> PolishResult   # raises NotePolishError
```

Single LLM call (`provider.generate`, `max_tokens=8000`). System prompt instructs: fix
spelling/grammar, correct clear factual errors, reword awkward sections, remove repetitive or
duplicative content, preserve meaning/structure/voice, keep code blocks verbatim, never add
new claims; respond with JSON `{"polished_markdown": ..., "corrections": [...]}`. Parsing:
strip code fences, `json.loads`; on failure fall back to treating the entire response as
polished markdown with `corrections=[]`; if the response is empty raise `NotePolishError`
(retryable — nothing persisted). Correction types are normalized against the allowed set.
The diff is computed locally with `difflib` (never trusted from the LLM).

### `notes/rendering.py`

```python
def markdown_to_html(md: str) -> str    # minimal CommonMark-ish renderer, stdlib only
def sanitize_html(html: str) -> str     # BeautifulSoup allowlist filter
```

`markdown_to_html` covers the constructs the polisher is prompted to emit: ATX headings,
paragraphs, `**bold**`/`*italic*`/`` `code` ``, fenced code blocks (escaped verbatim),
ordered/unordered lists, blockquotes, links, tables (GitHub pipe style), and horizontal
rules. Everything is HTML-escaped first; markup is generated, never passed through.
`sanitize_html` is defense-in-depth over the final document: allowed tags
`h1-h6 p br hr strong em code pre ul ol li blockquote a table thead tbody tr th td`;
allowed attrs `a[href]` only with `http/https` schemes; all other tags unwrapped, comments,
`script`/`style` contents dropped, event-handler attributes removed.

### `notes/store.py` — `NotesStore`

```python
class NotesStore:
    def __init__(self, db_path: str | Path): ...
    def create_pending(self, user_id, title, original_text, result: PolishResult, html: str) -> Note
    def list_notes(self, user_id, status=None, limit=100) -> list[Note]   # list view omits bodies
    def get_note(self, user_id, note_id) -> Note | None
    def accept(self, user_id, note_id) -> Note | None    # status→accepted, original_text→NULL
    def delete(self, user_id, note_id) -> bool
```

`accept` is idempotent; accepting an already-accepted note returns it unchanged. `Note` is a
Pydantic model (`src/notes/models.py`); `original_text` is excluded from all API responses of
accepted notes because the column is NULL.

### `web/routes/notes.py`

`router = APIRouter(prefix="/api/notes", tags=["notes"])`; all endpoints
`Depends(get_current_user)`; polish endpoint additionally
`dependencies=[Depends(enforce_shared_key_usage_limit)]`. LLM resolved with
`resolve_llm_credentials_for_user` (400 when no key); provider built via
`create_llm_provider`, model `SHARED_LLM_MODEL` for shared-source keys. The sync
`polish()` call is wrapped in `asyncio.to_thread`.

| Endpoint | Behavior |
| --- | --- |
| `POST /polish` | body `NotePolishRequest` (`text` 1..40k after strip, optional `title` ≤ 200) → 201 pending note with diff + corrections |
| `GET /` | list notes (`status` filter), newest first |
| `GET /{note_id}` | full note; pending includes original + diff; accepted includes HTML only |
| `POST /{note_id}/accept` | store decision: status→accepted, original discarded → 200 |
| `POST /{note_id}/discard` | delete pending note → 204 (also allowed on accepted = delete) |

Registered in `web/routes/__init__.py` `ROUTERS`. Request/response models are defined
route-locally in `src/web/routes/notes.py` (`NotePolishRequest`, `NoteResponse`,
`NoteSummaryResponse`) because `src/web/models.py` is a line-budget-guarded hotspot.

## Error Paths

- No LLM key → 400 `"No LLM API key configured"` (library convention).
- Text over `MAX_NOTE_CHARS` or empty after strip → 422 (Pydantic validation).
- `NotePolishError` / `LLMError` → 502 with retry guidance; nothing persisted.
- Cross-user note id → 404.
- Accept/discard on missing note → 404.

## Frontend

`web/src/app/(dashboard)/notes/page.tsx` — three states: compose (textarea + Polish button),
review (corrections grouped by type, unified diff rendered with add/remove line colors,
Accept / Discard), and library (accepted notes list + HTML viewer rendering the sanitized
`polished_html` via `dangerouslySetInnerHTML` — safe because sanitization happens server-side
before storage). Types in `web/src/types/notes.ts`.

## Validation

```
uv run pytest tests/notes tests/web/test_notes_routes.py -q
```
