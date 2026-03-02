# Goal Tracking

**Status:** Approved
**Author:** —
**Date:** 2026-03-02

## Problem

Users set career and learning goals but lack a structured way to track progress, break them into milestones, and get accountability. Goals mentioned in journal entries aren't actionable without explicit tracking.

## Users

Users who set explicit goals during onboarding or manually. Most useful for mid-to-senior professionals with deliberate growth plans.

## Desired Behavior

### Creating goals

1. User creates a goal with a title and optional description
2. System stores as a markdown file with YAML frontmatter in journal directory
3. Goal gets a status (`active` by default) and 0% progress

### Milestones

1. User adds milestones to a goal (sub-tasks with titles)
2. User marks milestones complete as they progress
3. Completing milestones updates the goal's progress percentage

### Check-ins

1. User records a check-in on a goal with a text note
2. Check-in is timestamped and appended to the goal's history
3. System tracks check-in frequency for staleness detection

### Goal status

- `active` — in progress
- `completed` — all milestones done or manually marked complete
- `paused` — temporarily deprioritized
- `abandoned` — explicitly dropped

### Goal analysis

1. Advisor can analyze progress on a specific goal or all goals
2. Analysis considers: milestone completion %, time since last check-in, journal entries mentioning the goal, relevant intel
3. Stale goals (no check-in for extended period) are flagged

### Goal-intel matching

1. System matches incoming intel items against active goals
2. Matched items surface in heartbeat notifications
3. Up to 8 active goals are summarized in the agentic advisor's system prompt

## Acceptance Criteria

- [ ] User can create, update, and delete goals
- [ ] Goals support milestones with completion tracking
- [ ] Check-ins are timestamped and persisted
- [ ] Progress percentage reflects milestone completion
- [ ] Advisor can analyze goal progress with journal + intel context
- [ ] Stale goals are flagged (no recent check-in)
- [ ] Active goals are injected into agentic advisor context
- [ ] Available via CLI, web, and MCP

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| Goal with no milestones | Progress is 0% until manually updated or milestones added |
| All milestones completed | Goal progress is 100%; status remains `active` until user marks complete |
| No active goals | Goal analysis returns empty; agentic prompt has no goals section |
| Goal file corrupted | Silently skipped in listings; error on direct access |
| 8+ active goals | Only first 8 shown in advisor context |

## Out of Scope

- Goal templates or pre-built goal libraries
- Deadline tracking or calendar integration
- Goal sharing or accountability partners
- Automatic goal completion (always user-initiated)
