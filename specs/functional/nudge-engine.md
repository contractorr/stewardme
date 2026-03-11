# Nudge Engine

**Status:** Implemented
**Author:** —
**Date:** 2026-03-11

## Problem

CLI users benefit from lightweight behavioral reminders about profile freshness, stale goals, and journaling streaks. These nudges encourage consistent engagement without requiring the user to check each subsystem.

## Users

CLI users (not exposed via web).

## Desired Behavior

1. During CLI interactions, the system checks three conditions:
   - **Profile staleness:** profile not updated in `interview_refresh_days` (default 90 days)
   - **Stale goals:** goals with no check-in for 14+ days
   - **Journal streak:** 0 entries in last 7 days (warning) or 5+ entries (celebration)
2. Relevant nudges displayed as short messages in CLI output.
3. Nudges are non-blocking — they don't interrupt the primary CLI workflow.

## Acceptance Criteria

- [ ] Profile staleness nudge triggers after configured interval.
- [ ] Stale goal nudge lists goal titles that need attention.
- [ ] Journal gap nudge triggers at 0 entries in 7 days.
- [ ] Journal streak celebration triggers at 5+ entries in 7 days.
- [ ] Nudges are concise single-line messages.

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| User has no profile | Profile staleness nudge always fires |
| User has no goals | Stale goal check skipped |
| Journal storage unavailable | Journal nudge skipped; no error |

## Out of Scope

- Web UI nudges (web uses suggestions engine instead)
- Nudge dismissal or snooze
