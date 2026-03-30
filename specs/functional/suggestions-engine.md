# Suggestions Engine

**Status:** Implemented
**Date:** 2026-03-30

## Problem

Users need a single prioritized feed of actionable next steps drawn from multiple subsystems
(briefing, recommendations, company movements, hiring signals, regulatory alerts, assumptions,
dossier escalations, and assistant-proposed learning guide candidates). Without unification, the
user must check each subsystem separately.

## Users

All web app users. Suggestions surface in Home and Goals.

## Product Placement

- Workspace: `Home` (top next steps), `Goals` (suggested next actions)
- Each suggestion carries a `why_now` annotation explaining its timeliness

## Desired Behavior

1. `GET /api/suggestions` returns a merged, prioritized list from all active subsystems.
2. Each item includes source type, title, summary, and `why_now` reasoning.
3. Items are sorted by source priority: daily brief first, then recommendations and learning guide
   candidates, then company movements, hiring, regulatory, assumptions, escalations.
4. Default limit is 10 items; max 30.
5. `WhyNowReasoner` annotates each item with timing context.
6. The feed may include `learning_guide_candidate` suggestions representing assistant-proposed new
   guides that still require approval before generation.

## Learning Guide Candidates

The suggestions engine can surface a proposed learning guide when the assistant has high confidence
that a missing topic would be useful to the user.

Behavior:

- a learning guide candidate is suggestion-first, not silently generated content
- it should include why the topic is useful now plus the generation payload needed to create it
- it should not appear if an overlapping active guide already exists
- it should not duplicate an already-active candidate for the same topic
- accepting the idea should lead to guide generation through the assistant flow

Payload expectations:

- topic
- desired depth
- intended audience
- time budget
- confidence
- rationale for why the guide is being proposed now

## Acceptance Criteria

- [ ] Endpoint merges items from all active subsystems into one list.
- [ ] Each item has a `why_now` annotation.
- [ ] Source priority ordering is consistent.
- [ ] Limit parameter respected (1-30).
- [ ] Missing or empty subsystems don't cause errors.
- [ ] Learning guide candidates can appear as suggestion items with approval-first semantics.
- [ ] Learning guide candidates are deduplicated against existing guides and recent candidates.

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| No active subsystems have items | Empty list returned |
| A subsystem throws an error during assembly | Other subsystems still contribute; error logged |
| User has no profile yet | Suggestions still work from non-profile-dependent sources |
| A guide candidate overlaps with an existing guide | The candidate is suppressed |
| A guide candidate remains after the guide was later created | The candidate stops surfacing as active guidance |

## Out of Scope

- Per-item dismiss/save (handled by engagement endpoints)
- Suggestion generation logic for each subsystem (owned by the source subsystem)
- Silent autonomous guide creation without approval
