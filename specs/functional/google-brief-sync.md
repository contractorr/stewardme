---
id: google-brief-sync
status: implemented
owner: product
last_updated: 2026-07-02
technical_specs:
  - specs/technical/google-brief-sync.md
  - specs/technical/configurable-brief.md
---

# Google Sync for the Brief (Gmail + Calendar)

## Problem

The brief covers sources and the journal, but not the user's actual day. Users
want the brief to plan ahead — what's on the calendar today and this week —
and to keep an eye on important email so nothing urgent slips while they're
heads-down.

## Users

Web app users who sign in with (or separately connect) a Google account.

## Desired Behavior

1. In Brief settings the user sees a **Connected accounts** block with a
   "Connect Google" button. Clicking it runs a Google consent flow requesting
   read-only Gmail and Calendar access; on return the block shows the
   connected address and a Disconnect button.
2. Once connected, two new built-in brief sections activate (individually
   toggleable):
   - **Coming up** — plans ahead from the calendar: today's schedule in
     order with anything that needs preparation, then a short outlook for
     the rest of the week (busy days, deadlines, gaps).
   - **Inbox watch** — the important-looking unread emails from the last
     few days (primary/important, promotions and social excluded),
     prioritized, with who it's from, what it's about, and what likely
     needs a reply.
3. Access is read-only; the app never sends mail or edits events. Tokens are
   stored encrypted per user, and Disconnect deletes them.
4. If Google is not connected, the calendar/email sections are simply
   omitted; the settings block explains what connecting adds.
5. New users are offered the connection during **onboarding**, as an
   optional step after picking feed topics: it explains what connecting
   adds, offers "Connect Google" and "Skip for now", and only appears when
   the server integration is configured and the account is not already
   connected. Completing the consent flow (or skipping) lands on Home with
   a confirmation; connecting later from Brief settings stays available.

## Acceptance Criteria

- [ ] Connect flow stores a refresh token (encrypted) and status shows the
      Google address; Disconnect removes stored tokens and status reflects it.
- [ ] With events in the next 7 days, the brief's "Coming up" section lists
      today's events (time-ordered) and a week outlook.
- [ ] With unread primary/important emails, "Inbox watch" surfaces them
      prioritized with sender and subject.
- [ ] Both sections degrade to plain lists when no LLM is available, and to
      a quiet note when the calendar/inbox is empty.
- [ ] A revoked/expired Google token never breaks brief generation — the
      affected section is skipped and other sections still render.
- [ ] All Google API access is read-only scoped (gmail.readonly,
      calendar.readonly).
- [ ] Onboarding shows the connect step only when the integration is
      available and not yet connected; both Connect and Skip complete
      onboarding, and the OAuth return lands the user on Home with a
      confirmation toast.

## Edge Cases

| Scenario | Expected Behavior |
| --- | --- |
| Token revoked at Google's end | Section skipped; status shows disconnected on next check; no crash |
| No events this week / inbox at zero | Section says so in one quiet line |
| All-day events | Listed without a time, before timed events for that day |
| OAuth env vars not configured on the server | Connect button hidden; status endpoint says the integration is unavailable |
| User connects a different Google account than their sign-in account | Allowed — the connected address is displayed so it's visible |

## Out of Scope

- Sending email, creating/editing events (read-only by design).
- Full mailbox/calendar mirroring into local storage — data is fetched live
  at brief-generation time and only the generated brief text is persisted.
- Non-Google providers (Outlook etc.).
- Push notifications for new important email between briefs.

## Validation Notes

- Smallest meaningful validation slice: route tests for connect/status/
  disconnect with mocked token exchange; generator tests with mocked
  calendar/email fetchers; frontend build.
- Contract impact: new `/api/google/*` endpoints; `BriefConfig` gains
  `include_calendar` and `include_email`.
- Follow-up spec work: scheduled generation + notification when an
  important email arrives.
