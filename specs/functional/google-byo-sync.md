---
id: google-byo-sync
status: draft
owner: product
last_updated: 2026-07-03
technical_specs:
  - specs/technical/google-byo-sync.md
  - specs/technical/configurable-brief.md
---

# Bring-Your-Own-Credential Gmail + Calendar Sync

## Problem

Users want their brief to plan the day (calendar) and keep an eye on important
email (inbox), but the OAuth path to Gmail/Calendar requires Google's
restricted-scope verification and an annual third-party security assessment
(CASA) — too costly for this product. Users already supply their own LLM API
key to power their agent, so they can supply their own read credentials for
Gmail and Calendar the same way, with no app-level Google verification.

## Users

Web app users who want calendar/inbox context in their brief and are willing to
provide per-account read credentials (stored encrypted, same as their LLM key).

## Desired Behavior

1. In Brief settings a **Connected accounts** block offers two independent
   connections, each with a short "how to get this" hint:
   - **Google Calendar** — the user pastes their calendar's **secret iCal
     URL** (Calendar settings → "Secret address in iCal format").
   - **Gmail** — the user enters their Gmail **address** and a Google
     **app password** (16 characters; requires 2-Step Verification).
2. On save, the server **verifies** the credential before storing it (fetch +
   parse the iCal feed; IMAP login test). Invalid credentials are rejected with
   a clear message and nothing is stored.
3. Once connected, the matching brief section activates (each toggleable):
   - **Coming up** — today's schedule in order plus a short week outlook,
     from the calendar feed.
   - **Inbox watch** — unread important/primary email from the last few days,
     prioritized with sender, subject, and likely next action.
4. Access is read-only. Credentials are stored Fernet-encrypted per user
   (same store as the LLM key). Disconnect deletes them.
5. If a service is not connected, its section is simply omitted; the settings
   block explains what connecting adds.
6. A broken/expired credential never breaks brief generation — the affected
   section is skipped and other sections still render; status reflects the
   failure on the next check.

## Acceptance Criteria

- [ ] Saving a valid iCal URL stores it (encrypted) and status shows calendar
      connected; Disconnect removes it.
- [ ] Saving a valid Gmail address + app password stores them (encrypted),
      status shows the address; Disconnect removes both.
- [ ] Invalid credentials (unreachable//non-iCal URL, failed IMAP login) are
      rejected on save with a clear error and nothing is persisted.
- [ ] A user-supplied iCal URL is SSRF-guarded (public hosts only, redirects
      re-validated) before any fetch.
- [ ] With events in the next 7 days, "Coming up" lists today's events
      (time-ordered) and a week outlook; recurring events are expanded.
- [ ] With unread important emails, "Inbox watch" surfaces them prioritized
      with sender and subject.
- [ ] Both sections degrade to plain lists when no LLM is available, and to a
      quiet note when the calendar/inbox is empty.
- [ ] A revoked/expired credential never 500s brief generation — the section
      is skipped and others still render.

## Edge Cases

| Scenario | Expected Behavior |
| --- | --- |
| iCal URL points at a private/internal host | Rejected by SSRF guard on save; never fetched |
| App passwords disabled (Workspace admin / no 2FA) | IMAP login fails; save rejected with guidance; Calendar still available independently |
| Credential valid at save, later revoked | Section skipped at generation; status shows disconnected on next check; no crash |
| No events this week / inbox at zero | Section says so in one quiet line |
| All-day events | Listed without a time, before timed events for that day |
| Recurring events (weekly standup, etc.) | Expanded into concrete instances within the 7-day window |

## Out of Scope

- Sending email or creating/editing events (read-only by design).
- OAuth "Connect with Google" flow (removed; this replaces it).
- Full mailbox/calendar mirroring — data is fetched live at brief-generation
  time; only the generated brief text is persisted.
- Non-Google providers (Outlook, etc.), and connecting during onboarding
  (Brief settings only for now).

## Validation Notes

- Smallest meaningful slice: route tests for connect/status/disconnect with
  mocked IMAP + mocked iCal fetch; generator tests with mocked fetchers;
  frontend build.
- Contract impact: `/api/google/*` connect/status/disconnect endpoints;
  `BriefConfig` gains `include_calendar` and `include_email`.
