# Per-User LLM Cost Estimation

**Status:** Implemented
**Date:** 2026-03-10

## Problem

Users have no visibility into how much their advisor queries cost. Token counts and pricing are available from providers but never surfaced.

## Users

All web app users who ask advisor questions.

## Desired Behavior

1. After each advisor chat query, token usage and estimated cost are recorded alongside existing latency metadata.
2. User opens Settings and sees a Usage card showing total queries, estimated cost, and per-model breakdown for the last 30 days.
3. If no queries have been made, the card shows "No usage data yet."

## Acceptance Criteria

- [x] Claude, OpenAI, and Gemini providers all record token usage after each call
- [x] Agentic orchestrator accumulates tokens across all iterations (not just last)
- [x] `GET /api/settings/usage?days=N` returns per-user aggregated stats
- [x] Usage data is isolated per user
- [x] Settings page shows Usage card with total queries, estimated cost, and per-model breakdown
- [x] Empty state handled gracefully

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| No queries yet | "No usage data yet" message |
| Pre-existing events without token metadata | Still count as queries; tokens/cost show as 0 |
| Gemini (free tier) | Cost shows as $0.00 |

## Out of Scope

- Tracking non-advisor LLM calls (memory extraction, entity extraction, recommendations)
- Council member costs (only lead provider tracked)
- Budget alerts or spending limits
- Real-time streaming cost display
