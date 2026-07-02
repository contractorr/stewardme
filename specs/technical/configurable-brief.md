---
id: configurable-brief
status: implemented
implements:
  - configurable-brief
code_paths:
  - src/web/brief_store.py
  - src/web/brief_generator.py
  - src/web/routes/brief.py
  - src/web/brief_models.py
  - src/storage_paths.py
  - web/src/types/brief.ts
  - web/src/app/(dashboard)/brief/page.tsx
  - web/src/components/home/BriefCard.tsx
test_paths:
  - tests/web/test_brief_routes.py
last_updated: 2026-07-02
---

# Configurable Brief

## Overview

Per-user persisted digest with history, read/dismiss state, an accumulation
window (each brief covers since the previous brief), and user-configured
sections including researched custom sections. Reuses `IntelStorage`
(`get_items_since`), journal storage/insights, and the research module's
`WebSearchClient` + `ResearchSynthesizer` for custom sections.

## Dependencies

**Depends on:** `storage_paths.get_user_paths`, `intelligence.scraper.IntelStorage`,
`journal.storage.JournalStorage`, `advisor.insights.InsightStore`,
`research.WebSearchClient` / `ResearchSynthesizer`, `llm.create_cheap_provider`,
`web.deps_credentials.resolve_llm_credentials_for_user`, `web.auth.get_current_user`.
**Depended on by:** Home page (`BriefCard`), `/brief` page.

## Components

### BriefStore

**File:** `src/web/brief_store.py`
**Status:** Stable

#### Behavior

SQLite store at `get_user_paths(user_id)["briefs_db"]` (`briefs.db`, new
`StoragePaths` key). Tables:

- `briefs(id TEXT PK, period_start TEXT, period_end TEXT, status TEXT
  CHECK(status IN ('unread','read','dismissed')), summary TEXT,
  sections TEXT /*JSON list*/, created_at TEXT)`
- `config(key TEXT PK, value TEXT)` — single row `key='config'`, JSON value.

#### Inputs / Outputs

- `save_brief(summary, sections, period_start, period_end) -> dict` — id is
  `uuid4().hex[:12]`, status `unread`.
- `list_briefs(limit=20, include_dismissed=True) -> list[dict]` newest first.
- `get_brief(brief_id) -> dict | None`, `get_latest() -> dict | None`
  (any status; latest by `created_at`).
- `mark_read(brief_id) -> bool`, `dismiss(brief_id) -> bool` (False if id
  unknown). `read` → `dismissed` allowed; `dismissed` is terminal.
- `get_config() -> dict` (empty dict when unset), `save_config(dict)`.
- `recent_custom_topics(limit=10) -> list[str]` — titles of custom-kind
  sections across recent briefs, used to avoid topic repeats.

Sections JSON element shape:
`{kind, title, body, items?: list[dict], sources?: list[{title,url}], researched?: bool}`.
Kinds: `signals`, `journal`, `custom`.

#### Invariants

- Briefs are immutable after save except `status`.
- All timestamps ISO-8601 UTC.

### BriefConfig (Pydantic)

**File:** `src/web/brief_models.py`

```python
class BriefCustomSection(BaseModel):
    id: str = ""            # assigned server-side if empty
    title: str = ""         # display title; derived from instructions if empty
    instructions: str       # standing instruction text
    use_research: bool = False

class BriefConfig(BaseModel):
    enabled: bool = True
    min_interval_hours: int = 12      # 1..168
    include_signals: bool = True
    include_journal: bool = True
    max_items_per_section: int = 8    # 3..20
    custom_sections: list[BriefCustomSection] = []

class BriefResponse(BaseModel):
    id: str; status: str; summary: str
    period_start: str; period_end: str; created_at: str
    sections: list[dict]

class BriefLatestResponse(BaseModel):
    brief: BriefResponse | None = None
    should_generate: bool = False
```

### BriefGenerator

**File:** `src/web/brief_generator.py`
**Status:** Experimental

#### Behavior

`generate_brief(user_id, config: BriefConfig, store: BriefStore) -> dict`:

1. **Window:** `period_start` = previous brief's `period_end`, else
   `now - 72h`. Intel lookback capped at `BRIEF_MAX_WINDOW_DAYS = 14`
   (cap noted in the summary when applied). `period_end = now`.
2. **Signals section** (`include_signals`): `IntelStorage.get_items_since`
   over the (capped) window, truncated to `max_items_per_section * 3` for
   the LLM, `items` payload truncated to `max_items_per_section`. Cheap LLM
   summarizes into short markdown grouped by theme; on LLM failure `body`
   falls back to a plain bullet list of titles.
3. **Journal section** (`include_journal`): entries in window via
   `JournalStorage` (content clipped ~500 chars each, max 15) plus
   `InsightStore.get_active(limit=10)`. Cheap LLM produces observations,
   feedback, and 2-3 concrete suggestions grounded in the entries. Fallback:
   insight titles as bullets.
4. **Custom sections:** for each configured section with non-empty
   instructions: cheap LLM derives a concrete topic from the instructions
   (given `recent_custom_topics()` to avoid repeats); if `use_research` and
   a search provider works, `WebSearchClient.search(topic)` →
   `ResearchSynthesizer.synthesize(topic, results)` and `sources` are
   attached with `researched: true`; otherwise LLM-only synthesis with
   `researched: false`.
5. **Summary:** one-line LLM digest of section headlines (fallback:
   deterministic count sentence).
6. Persists via `store.save_brief` and returns the stored dict.

LLM/search failures are caught per section — a failed section degrades, the
brief still saves. Empty windows produce a "Nothing new" body per section.

#### Configuration

- LLM: `resolve_llm_credentials_for_user` → `create_cheap_provider`; if no
  key resolves, all LLM steps use fallbacks.
- Search: Tavily key via user secret `tavily_api_key`, else DuckDuckGo
  fallback inside `WebSearchClient`.

### Routes

**File:** `src/web/routes/brief.py` — `APIRouter(prefix="/api/brief")`,
registered in `routes/__init__.ROUTERS`. All endpoints depend on
`get_current_user`. Public paths get `/api/v1` via the rewrite middleware.

- `GET /api/brief/latest -> BriefLatestResponse` — latest brief plus
  `should_generate` (config enabled AND (no brief OR latest older than
  `min_interval_hours`)).
- `POST /api/brief/generate?force=false -> BriefResponse` — 200 with the
  existing latest when inside the interval and not forced; otherwise
  generates synchronously.
- `GET /api/brief -> list[BriefResponse]` — history (`limit` 1..50,
  `include_dismissed`).
- `POST /api/brief/{id}/read`, `POST /api/brief/{id}/dismiss` — 404 on
  unknown id, else `{ok: true}`.
- `GET /api/brief/config -> BriefConfig`, `PUT /api/brief/config` —
  validated by Pydantic; custom sections get server-assigned ids.

#### Error Handling

Generation never 500s for missing LLM/search — degradation is in-band.
Unknown brief ids → 404. Config validation errors → 422 (FastAPI default).

### Frontend

- `web/src/types/brief.ts` — `Brief`, `BriefSection`, `BriefConfig`,
  `BriefCustomSection`, `BriefLatestResponse` mirroring the models.
- `web/src/components/home/BriefCard.tsx` — shown on Home when the latest
  brief is `unread`: date-range header, section list, mark-read + dismiss
  actions, link to `/brief`. Triggers `POST /generate` in the background
  when `should_generate` and renders a skeleton meanwhile.
- `web/src/app/(dashboard)/brief/page.tsx` — full latest brief (markdown
  bodies via existing renderer), history list with status badges, config
  editor (toggles, interval, custom sections CRUD), "Generate now" (force).

## Cross-Cutting Concerns

Per-user isolation via `get_user_paths`; no shared state beyond the shared
intel DB reads. Generation is synchronous in-request (seconds); the Home
card fires it as a background fetch so page load never blocks on it.

## Validation Strategy

- Smallest meaningful test slice: `tests/web/test_brief_routes.py` — store
  CRUD + status transitions, config round-trip, generate with patched
  generator internals (no real LLM/search), interval gating, accumulation
  (second brief's `period_start` == first brief's `period_end`), multi-user
  isolation.
- Required mocks: patch `brief_generator._call_llm` / search client; reuse
  `tests/web/conftest.py` fixtures.
- High-risk regressions to watch: `StoragePaths` key addition (TypedDict
  consumers), route registration order, home page load path.
