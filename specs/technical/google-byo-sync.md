---
id: google-byo-sync
status: draft
implements:
  - google-byo-sync
code_paths:
  - src/web/google_sync.py
  - src/web/routes/google.py
  - src/web/brief_models.py
  - src/web/brief_generator.py
  - web/src/app/(dashboard)/brief/page.tsx
  - web/src/types/brief.ts
test_paths:
  - tests/web/test_google_routes.py
  - tests/web/test_brief_routes.py
last_updated: 2026-07-03
---

# Bring-Your-Own-Credential Gmail + Calendar Sync

## Overview

Per-user read credentials (no OAuth, no Google app verification):
- **Calendar** via the user's **secret iCal URL** — fetched with `httpx`
  (SSRF-guarded) and parsed with `icalendar` + `recurring_ical_events`
  (RRULE expansion over the window).
- **Gmail** via the user's **address + app password** — read over IMAP
  (`imaplib.IMAP4_SSL` to `imap.gmail.com`), using Gmail's `X-GM-RAW` search
  extension for the same importance filter as before. Stdlib only.

Both feed the existing two brief sections. Credentials live in the
Fernet-encrypted `user_secrets` store (same as the LLM key).

## Dependencies

**Depends on:** `user_secrets` (`set/get/delete_user_secret` via
`web.user_store`, Fernet key from `web.deps_base.get_secret_key`),
`url_guard` (`ensure_public_url`, `public_url_event_hooks`), `web.auth` JWT,
`web.brief_generator`. New libs: `icalendar`, `recurring-ical-events` (web extra).
**Depended on by:** brief generation, Brief settings UI.

## Components

### Sync client (`src/web/google_sync.py`)

**Status:** Experimental

Secret keys: `calendar_ical_url`, `gmail_address`, `gmail_app_password`.
Helper `_secret(user_id, key)` / `_set/_del` wrap the store with the Fernet key.

- `calendar_connected(user_id) -> bool` — iCal URL secret present.
- `gmail_connected(user_id) -> bool` — both Gmail secrets present.
- `gmail_address(user_id) -> str | None`.
- `verify_calendar(url) -> None` (async) — `ensure_public_url` then fetch with
  `public_url_event_hooks`; parse with `icalendar`; raise `ValueError` on
  unreachable / non-calendar content.
- `verify_gmail(address, app_password) -> None` — IMAP SSL login test; raise
  `ValueError` on auth failure.
- `store_calendar(user_id, url)` / `store_gmail(user_id, address, pw)` /
  `clear_calendar(user_id)` / `clear_gmail(user_id)`.
- `fetch_calendar_events(user_id, days=7) -> list[dict] | None` — `None` when
  not connected/errored; else normalized `{title, start, end, all_day,
  location}` (start/end ISO strings; all-day → date-only start), sorted by
  start, recurrences expanded within [now, now+days].
- `fetch_important_emails(user_id, limit=12) -> list[dict] | None` — `None`
  when not connected/errored; else `{from, subject, date, snippet}` (snippet
  `""` in v1 — headers-only fetch to stay light). Search uses `X-GM-RAW`
  with `is:unread newer_than:7d (is:important OR category:primary)
  -category:promotions -category:social`.

Fetchers never raise into the caller — all IMAP/HTTP/parse errors are caught,
logged, and surfaced as `None` so brief generation degrades gracefully.

### Routes (`src/web/routes/google.py`) — `APIRouter(prefix="/api/google")`

All require auth (`get_current_user`). No OAuth callback.

- `GET /api/google/status` → `{calendar_connected: bool, gmail_connected:
  bool, gmail_address: str | null}`.
- `PUT /api/google/calendar` body `{ical_url}` → `verify_calendar` then store;
  `400` on invalid/unsafe URL. Returns status.
- `DELETE /api/google/calendar` → clears; returns status.
- `PUT /api/google/gmail` body `{address, app_password}` → `verify_gmail` then
  store; `400` on login failure. Returns status.
- `DELETE /api/google/gmail` → clears both secrets; returns status.

### Brief integration

- `BriefConfig` regains `include_calendar: bool = True`,
  `include_email: bool = True` (no-ops until connected).
- `brief_generator._build_calendar_section` (kind `calendar`, title
  "Coming up") and `_build_email_section` (kind `email`, title "Inbox watch")
  are unchanged in structure — they call the same `fetch_calendar_events` /
  `fetch_important_emails` names; `None` → section omitted. LLM planning +
  deterministic fallback identical to the prior implementation.

#### Error Handling

- Save-time verification failures → `400` with a human message; nothing stored.
- Generation-time fetch failures → `None`, section omitted, other sections
  unaffected. Details logged server-side only.

#### Configuration

No server env required (per-user credentials). `FRONTEND_ORIGIN` unchanged.
`GOOGLE_CLIENT_ID/SECRET` remain **only** for NextAuth sign-in and are unused
here.

### Frontend

- `types/brief.ts`: config regains `include_calendar`, `include_email`; new
  `GoogleStatus { calendar_connected; gmail_connected; gmail_address }`.
- Brief settings **Connected accounts**: two forms —
  - Calendar: iCal URL input, Save/Disconnect, "how to get this" hint.
  - Gmail: address + app-password inputs, Save/Disconnect, hint (needs 2FA).
  Each shows connected state; toggles for the two sections appear when the
  matching service is connected. Always visible (no server-config gate).

## Validation Strategy

- `tests/web/test_google_routes.py`: status; calendar PUT happy-path (patched
  fetch/parse) + bad URL (`400`); gmail PUT happy-path (patched IMAP) + bad
  login (`400`); disconnect; auth required.
- `tests/web/test_brief_routes.py`: calendar/email sections appear with patched
  fetchers; omitted when fetchers return `None`.
- High-risk regressions: brief latency (live IMAP/HTTP fetch), SSRF via iCal
  URL, IMAP credential handling.
