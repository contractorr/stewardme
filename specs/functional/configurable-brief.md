---
id: configurable-brief
status: implemented
owner: product
last_updated: 2026-07-02
technical_specs:
  - specs/technical/configurable-brief.md
---

# Configurable Brief

## Problem

Users want one place that catches them up: what changed in their tracked
sources, what their journal is telling them, and a few standing extras they
personally care about. The existing return brief is a stateless snapshot —
it cannot be revisited, configured, or marked as handled, and its content
does not accumulate across a multi-day absence.

## Users

All web app users. Most valuable to users who check in irregularly and want
the gap covered when they return.

## Desired Behavior

1. The app maintains a per-user **brief**: a generated digest covering the
   window since the previous brief (so content accumulates across absences —
   a 5-day gap yields a brief covering all 5 days).
2. A brief contains, per the user's configuration:
   - **What changed** — a summary of new intel/signal items from the user's
     sources since the last brief, with links to the underlying items.
   - **From your journal** — feedback, insights, and helpful suggestions
     grounded in the journal entries written in the window (plus active
     insights such as recurring blockers and emerging topics).
   - **Custom standing sections** — user-authored instructions the brief
     always honors, e.g. "always include a well-researched summary of an
     esoteric but important topic I might find interesting". Sections marked
     as researched use live web search before synthesis; the brief avoids
     repeating topics covered in recent briefs.
3. The latest unread brief is surfaced on Home as a card; a dedicated
   **Brief** page shows the full brief, past briefs, and configuration.
4. The user can **mark a brief as read** and **dismiss** it. Dismissed briefs
   leave Home immediately but remain in history, visibly labeled.
5. Configuration lets the user toggle the built-in sections, add/remove/edit
   custom standing sections, and set how often a new brief may be generated
   (minimum interval). The user can also trigger "Generate now".
6. A new brief is generated on demand: when the user visits and the latest
   brief is older than the configured interval, the app generates the next
   one covering everything since the previous brief.

## Acceptance Criteria

- [ ] Given new intel items exist since the last brief, the next brief's
      "What changed" section summarizes them and links to sources.
- [ ] Given journal entries were written in the window, the brief contains a
      journal section with observations and suggestions grounded in them.
- [ ] Given a custom section instruction exists, every generated brief
      includes a section produced from that instruction; researched sections
      cite web sources.
- [ ] Given the user was away 5 days, the next brief's window spans the full
      gap (period start = previous brief's period end).
- [ ] Marking read updates status and keeps the brief in history; dismissing
      removes it from Home but keeps it in history as "dismissed".
- [ ] Past briefs are listable, newest first, and openable in full.
- [ ] Config changes (toggles, custom sections, interval) persist per user
      and apply to the next generation.
- [ ] Generating again before the minimum interval returns the existing
      brief instead of creating a duplicate (unless forced from the Brief
      page).
- [ ] With no LLM available, generation degrades to item lists without
      crashing; with no new content, the brief says so plainly.

## Edge Cases

| Scenario | Expected Behavior |
| --- | --- |
| First ever brief (no history) | Window defaults to the last 3 days |
| No new intel and no journal entries in window | Brief is still generated with a quiet "nothing new" note per empty section |
| Web search unavailable for a researched custom section | Section falls back to LLM-only synthesis and says it was not web-researched |
| Very long absence (months) | Window is capped (14 days of intel) so the brief stays readable; the cap is stated in the brief |
| LLM call fails mid-generation | Affected section falls back to a raw item list; other sections unaffected |
| Custom section instructions are empty | Section is skipped, not sent to the LLM |

## Out of Scope

- Email/push delivery of briefs (surface is in-app only).
- Scheduled/cron generation while the user is away (generation is on-visit;
  the accumulation window makes the result equivalent).
- Replacing the existing return brief or greeting (they remain; see
  `specs/functional/since-you-were-away-why-now.md`). Follow-up work may
  consolidate them once this feature settles.
- Per-item read state inside a brief (state is per-brief).

## Validation Notes

- Smallest meaningful validation slice: route tests for generate/list/read/
  dismiss/config with patched LLM + intel fixtures; frontend build.
- Contract impact: new `/api/brief*` endpoints and frontend `types/brief.ts`.
- Follow-up spec work: consolidation with return brief; notification-on-new-
  brief integration.
