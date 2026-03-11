# Signals

**Status:** Implemented
**Author:** —
**Date:** 2026-03-11

## Problem

Users need proactive alerts when important patterns emerge across their data — stale goals, topic surges, journal gaps, upcoming deadlines, recurring blockers. Without automated detection, users must manually monitor each area.

## Users

All users. Signals feed into suggestions, insights, and advisor context.

## Desired Behavior

1. The system runs 7 detectors across all data sources:
   - **Goal staleness:** goals with no check-in beyond threshold
   - **Goal completion candidate:** goals meeting completion criteria
   - **Journal gap:** no journal entries in recent window
   - **Topic emergence:** new topics appearing with high frequency
   - **Deadline urgency:** upcoming CFP/event deadlines within warning window
   - **Research trigger:** topic mentioned 3+ times in 7 days
   - **Recurring blocker:** negative keyword clusters in journal entries
2. Each signal has a severity (1–10), type, title, detail, and source reference.
3. Signals are hash-deduplicated to avoid re-surfacing acknowledged issues.
4. Signals dual-persist to both `SignalStore` (SQLite) and `InsightStore`.

## Acceptance Criteria

- [ ] All 7 detectors produce correctly typed signals.
- [ ] Severity scores are in 1–10 range.
- [ ] Hash dedup prevents duplicate signals for the same underlying event.
- [ ] Signals persist to SQLite via `SignalStore`.
- [ ] Signals also write to `InsightStore` for unified consumption.

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| No goals exist | Goal-related detectors return empty |
| No journal entries | Journal gap detector fires; topic/blocker detectors return empty |
| Detector throws exception | Other detectors still run; error logged |
| Same signal detected on consecutive runs | Hash dedup prevents duplicate |

## Out of Scope

- Signal dismissal UI (handled via insights/engagement)
- Custom detector configuration per user
