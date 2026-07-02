---
id: google-brief-sync
status: implemented
implements:
  - google-brief-sync
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
last_updated: 2026-07-02
---

# Google Sync for the Brief

## Overview

Backend-managed Google OAuth (authorization-code + refresh token) with
read-only Gmail/Calendar REST access, feeding two new brief sections.
No Google SDK dependency — plain `httpx` against the REST endpoints.

## Dependencies

**Depends on:** `user_secrets` (Fernet-encrypted per-user secrets, via
`web.user_store` re-exports), `web.auth` JWT secret (state signing),
`web.brief_generator`, env `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`
(same OAuth client as NextAuth sign-in) + `GOOGLE_REDIRECT_URI`.
**Depended on by:** brief generation, Brief settings UI.

## Components

### GoogleSync client (`src/web/google_sync.py`)

**Status:** Experimental

- `is_configured() -> bool` — both env vars set.
- `build_auth_url(state) -> str` — consent URL with scopes
  `gmail.readonly calendar.readonly`, `access_type=offline`,
  `prompt=consent`.
- `exchange_code(code) -> dict` — POST `oauth2.googleapis.com/token`;
  returns token payload (must contain `refresh_token`).
- `_access_token(user_id) -> str | None` — refresh-token grant using the
  stored secret; returns None when not connected or refresh fails
  (revoked → deletes the stored secrets).
- `fetch_profile_email(access_token) -> str | None` — Gmail
  `users/me/profile`.
- `fetch_calendar_events(user_id, days=7) -> list[dict] | None` — primary
  calendar, `singleEvents=true&orderBy=startTime`, window now → now+days.
  Normalized: `{title, start, end, all_day, location}`. `None` = not
  connected/error; `[]` = connected but empty.
- `fetch_important_emails(user_id, limit=12) -> list[dict] | None` — Gmail
  query `is:unread newer_than:7d (is:important OR category:primary)
  -category:promotions -category:social`, then per-message metadata
  (`From`, `Subject`, `Date`) + snippet. Normalized:
  `{from, subject, date, snippet}`.
- State token: JWS (`jose`) `{sub, purpose:"google_oauth", return_to,
  exp: +10min}` signed with `NEXTAUTH_SECRET`. `return_to` is one of the
  whitelisted keys in `RETURN_PATHS` (`brief` -> `/brief`, `onboarding` ->
  `/onboarding`); unknown values fall back to `/brief`.
- Secrets: `google_refresh_token`, `google_account_email`.

### Routes (`src/web/routes/google.py`) — `APIRouter(prefix="/api/google")`

- `GET /api/google/status` → `{available, connected, email}` (auth required).
- `GET /api/google/auth-url?return_to=brief|onboarding` → `{url}`; 503 when
  not `is_configured()`. `return_to` (default `brief`) is embedded in the
  signed state.
- `GET /api/google/callback?code&state` — **unauthenticated** (browser
  redirect); validates the signed `state`, exchanges the code, stores
  secrets, then 302 → `FRONTEND_ORIGIN + <return path>` with
  `?google=connected` (`?google=error` on failure — never 500s to the
  browser). The return path comes from the state's whitelisted `return_to`.
- `POST /api/google/disconnect` → deletes both secrets, `{ok: true}`.

### Brief integration

- `BriefConfig` gains `include_calendar: bool = True`,
  `include_email: bool = True` (no-ops until connected).
- `brief_generator._build_calendar_section` (kind `calendar`, title
  "Coming up"): events fetched via `fetch_calendar_events`; `None` → section
  omitted. LLM plans **Today** (time-ordered, prep pointers) and **This
  week** (outlook); fallback = grouped bullet list. `items` carries the
  normalized events (capped).
- `brief_generator._build_email_section` (kind `email`, title
  "Inbox watch"): same pattern; LLM prioritizes what needs attention with
  sender/subject and a suggested action; fallback = `From — Subject` list.
- Section failures/errors are contained per section, as with existing kinds.

#### Error Handling

- Refresh-token 400/401 (`invalid_grant`) → secrets deleted, functions
  return `None`, sections omitted.
- Callback errors redirect with `?google=error`; details logged server-side
  only.

#### Configuration

`GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` (shared with NextAuth),
`GOOGLE_REDIRECT_URI` (e.g. `https://api.example.com/api/v1/google/callback`
— must be registered in the Google console), `FRONTEND_ORIGIN` (existing).

### Frontend

- `types/brief.ts`: config gains `include_calendar`, `include_email`;
  new `GoogleStatus` type.
- Brief settings adds **Connected accounts**: status chip (address when
  connected), Connect (`window.location.href = auth-url`), Disconnect;
  toggles for the two sections. Hidden entirely when `available` is false.
- `/brief?google=connected|error` shows a toast once and cleans the query.
- Onboarding (`web/src/app/(dashboard)/onboarding/page.tsx`): new `google`
  phase after feeds are saved, shown only when `/api/google/status` reports
  `available && !connected`; Connect uses `auth-url?return_to=onboarding`,
  Skip completes onboarding. On return, `/onboarding?google=connected|error`
  toasts and redirects to Home (profile + feeds were already persisted
  before the redirect, so no onboarding state is lost).

## Validation Strategy

- `tests/web/test_google_routes.py`: status unavailable/available/connected,
  auth-url 503 + URL shape, callback happy-path (patched exchange) + bad
  state + missing refresh token, disconnect, auth required.
- `tests/web/test_brief_routes.py` additions: calendar/email sections appear
  with patched fetchers; omitted when fetchers return `None`.
- High-risk regressions: brief generation latency (two extra HTTP calls),
  redirect URI mismatches in deployment.
