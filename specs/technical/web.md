---
id: web
category: tracked_module
status: updated
implements:
- analytics-admin
- anki-decks
- ask-advice
- curriculum
- deep-research
- goal-tracking
- intelligence-feed
- journaling
- landing-page
- library-reports
- memory-threads
- note-polish
- profile-onboarding
- settings-account
code_paths:
- src/web
- web/src
- tests/web
last_reviewed: '2026-03-30'
---

# Web

**Status:** Updated for the simplified product model

## Overview

The web app presents four primary product surfaces: `Home`, `Radar`, `Learn`, and `Journal`. `Goals` and `Research` remain available as contextual secondary workspaces that users reach from those primary surfaces instead of from the main navigation. Today those map to `/home`, `/radar`, `/learn`, `/journal`, `/goals` (with `/focus` alias), `/research` (with `/library` alias), and `/settings`.

The FastAPI surface now boots a single canonical user-state schema from `src/user_state_store.py`. `src/web/user_store.py` is a compatibility wrapper only, so fresh startup must initialize conversation, attachment, onboarding, usage, and user-secret tables through the shared store module.

## Key Modules

- `src/web/app.py`
- `src/user_state_store.py`
- `src/web/user_store.py`
- `src/web/routes/onboarding.py`
- `src/web/routes/recommendations.py`
- `src/web/services/journal_entries.py`
- `web/src/components/Sidebar.tsx`
- `web/src/app/page.tsx`
- `web/src/app/(dashboard)/home/page.tsx`
- `web/src/app/(dashboard)/focus/page.tsx`
- `web/src/app/(dashboard)/goals/page.tsx`
- `web/src/app/(dashboard)/radar/page.tsx`
- `web/src/app/(dashboard)/library/page.tsx`
- `web/src/app/(dashboard)/research/page.tsx`
- `web/src/components/research/ResearchWorkspace.tsx`
- `web/src/app/(dashboard)/learn/page.tsx`
- `web/src/app/(dashboard)/settings/page.tsx`

## Interfaces

- Public root route: `/`
- Primary app routes: `/home`, `/radar`, `/learn`, `/journal`, `/settings`
- Secondary workspace routes: `/goals`, `/research`
- Legacy alias routes: `/focus`, `/library`
- Secondary deep-link routes: `/advisor`, `/intel`, `/projects`
- Page-view tracking includes the simplified paths
- Startup must initialize the canonical user-state DB before any chat or onboarding traffic
- Conversation persistence includes attachment rows in `conversation_message_attachments`
- Shared journal-entry validation for goal-linked flows lives in `src/web/services/journal_entries.py`

## Rate Limiting

`src/web/rate_limit.py` holds two layers of in-memory sliding-window limits
(process-local, reset on deploy):

1. **Shared-key ("lite mode") limits** — unchanged: 30/day + 10s burst for
   users on the shared key, separate onboarding budget.
2. **Per-user route limits** (all users): `check_route_rate_limit(user_id,
   bucket)` with buckets `"llm"` and `"general"`. Configured via
   `web.rate_limit` in `config.yaml` (`enabled`, `llm_per_minute` default 20,
   `general_per_minute` default 120 — see `config.example.yaml`); settings
   are cached after first read and cleared by `reset_rate_limits()`.
   Exceeding a limit raises HTTP 429 with a `Retry-After` header.

Wiring:
- `enforce_llm_rate_limit` dependency on advisor `/ask` + `/ask/stream`,
  research `/run` + `POST /dossiers`, onboarding `/start` + `/chat`.
- Curriculum applies the LLM bucket inside `_build_question_generator` (only
  when credentials resolve) and `_build_guide_generation_service`, covering
  every quiz/teachback/assessment/placement/guide endpoint at one chokepoint.
- The general bucket runs as an app middleware on `/api/*` (except
  `/api/health`), keyed on a hash of the Authorization header, falling back
  to client IP.

## Outbound URL Guard (SSRF)

**File:** `src/url_guard.py`

- `validate_public_url(url)` — raises `UnsafeURLError` unless the URL is
  `http(s)` with a hostname whose EVERY resolved address is publicly
  routable (`ipaddress.is_global`, plus explicit loopback/private/
  link-local/reserved refusals). Literal IPs are checked without DNS.
  Blocking (does `socket.getaddrinfo`) — call from async code via
  `await ensure_public_url(url)`.
- `public_url_event_hooks()` — httpx event hooks that re-validate every
  request in a redirect chain; pass to `httpx.AsyncClient(event_hooks=...)`
  wherever `follow_redirects=True` fetches user-supplied URLs.
- `COACH_ALLOW_PRIVATE_URLS=1` disables all checks (single-user/local
  deployments with localhost LLM endpoints).
- Enforced at: `intel.py:add_rss_feed` (URL + redirect hops),
  `settings.py` custom-provider add/update/test (`base_url`), and
  `BaseScraper.fetch_html`. Research needs no guard: `web_search.py` only
  calls fixed search endpoints (Tavily/DuckDuckGo), never result URLs.
- DNS-rebinding TOCTOU between validation and fetch is accepted residual
  risk; internal schemes (`research://`, `localdrop://`) never hit the
  network and are exempt upstream.

## Async Handler Conventions

The backend is a single-process asyncio server: any synchronous LLM,
embedding, or bulk-file call executed directly inside an `async def` route
(or an `asyncio.create_task` coroutine) stalls EVERY user until it returns.

Rules:

- Sync LLM provider calls (`LLMProvider.generate`), embedding calls, and
  embedding-manager construction (which parses the whole vector store JSON)
  must run via `asyncio.to_thread` when invoked from async request paths.
  Reference patterns: `advisor.py` `_run_in_thread`, `greeting.py`,
  `notes.py:polish_note`, `settings.py:test-llm`.
- Background coroutines scheduled with `asyncio.create_task` share the
  request event loop — the same rule applies inside them (journal
  post-create hooks). Task handles must be kept (module-level set) so
  in-flight work isn't garbage-collected.
- `GuideGenerationService._generate_text` and `QuestionGenerator._call_llm`
  wrap their sync providers in `asyncio.to_thread` internally, so curriculum
  routes may await them directly.

## Simplified Product Notes

- Home is the default landing page after onboarding.
- The sidebar should teach the product through the four primary surfaces plus `Settings`, not through internal subsystem names.
- Goals and Research should stay accessible through contextual links from Home, Radar, Journal, onboarding, and guided flows rather than as first-class sidebar destinations.
- Onboarding, help, and page-view tracking should mirror the same information architecture.
- Research and Settings should prefer progressive disclosure over always-open advanced forms and control panels.
- Onboarding sessions are still process-local in-memory state, but same-user requests are serialized with per-user async locks and forced finalization always clears the session.
