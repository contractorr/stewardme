# Goal-Intel Matching

**Status:** Implemented
**Author:** —
**Date:** 2026-03-11

## Problem

Intel items may be directly relevant to a user's active goals but won't surface unless the user searches manually. Automated matching connects scraped intelligence to goals, surfacing opportunities and threats in context.

## Users

Users with active goals and intelligence scraping enabled.

## Desired Behavior

1. The system matches scraped intel items against active goals using fused keyword + semantic scoring (60% keyword, 40% semantic).
2. Keyword matching extracts terms from goal title, tags, and content, then uses profile relevance scoring.
3. Semantic matching queries ChromaDB embeddings when available.
4. Results categorized into three urgency tiers: high (≥0.15), medium (≥0.08), low (≥0.04).
5. Optional LLM re-ranking (`GoalIntelLLMEvaluator`) filters false positives in batches of 20.
6. Adaptive recency window: days since last match, clamped [7, 30].
7. 7-day dedup on (goal_path, url) prevents repeat matches.

## Acceptance Criteria

- [ ] Keyword and semantic scores fused at configured weight.
- [ ] Three urgency tiers correctly assigned by score threshold.
- [ ] LLM evaluator filters false positives when enabled.
- [ ] Adaptive window expands lookback when no recent matches exist.
- [ ] Dedup prevents same item matching same goal within 7 days.
- [ ] Works without ChromaDB (keyword-only fallback).

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| Goal has no tags or content | Keyword matching uses title only |
| ChromaDB unavailable | Semantic weight drops to 0; keyword-only scoring |
| LLM evaluator call fails | Pre-LLM matches returned as-is |
| All matches below low threshold | Empty result |
| Goal archived after match generated | Match still persisted; UI filters by active goals |

## Out of Scope

- Bi-directional matching (intel suggesting new goals)
- User-tunable match thresholds
