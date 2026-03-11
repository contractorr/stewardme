# Engagement Scoring

**Status:** Implemented
**Author:** —
**Date:** 2026-03-11

## Problem

The system needs feedback on which suggestions and recommendations are useful to improve future prioritization. Without engagement data, the recommendation engine cannot learn from user behavior.

## Users

All web app users. Engagement data feeds into dynamic recommendation weighting.

## Desired Behavior

1. Users can record engagement events against any target: opened, saved, dismissed, acted_on, feedback_useful, feedback_irrelevant.
2. Feedback events (useful/irrelevant) also trigger secondary `recommendation_feedback` usage events for admin analytics.
3. Stats endpoint returns counts grouped by target_type × event_type for last N days plus totals.
4. Engagement data feeds `compute_dynamic_weight()` in advisor RAG to adjust journal:intel weighting.
5. Per-user feedback count available for rate-limiting or profile enrichment.

## Acceptance Criteria

- [ ] All 6 event types recorded correctly.
- [ ] Feedback events dual-write to engagement_events and usage_events.
- [ ] Stats grouped by target_type × event_type.
- [ ] Stats filterable by day range (default 30).
- [ ] Engagement data influences dynamic recommendation weighting.

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| Same event recorded twice for same target | Both recorded (no dedup — events are append-only) |
| Unknown event type submitted | Validation error returned |
| No engagement data yet | Stats return empty groupings; dynamic weight uses defaults |

## Out of Scope

- Engagement-based A/B testing
- Cross-user engagement aggregation
