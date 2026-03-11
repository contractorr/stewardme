# Trending Radar

**Status:** Implemented
**Author:** —
**Date:** 2026-03-11

## Problem

Users want to see what topics are trending across their intelligence sources without manually scanning each feed. Cross-source trend detection surfaces emerging themes that no single source would reveal.

## Users

All users with active intelligence scraping. Trends surface in Radar and advisor context.

## Desired Behavior

1. The system aggregates intel items from the recent window (default 7 days) and identifies trending topics.
2. Two detection modes:
   - **NLP pipeline:** RAKE-style phrase extraction + Dunning log-likelihood bigram collocation, scored by frequency (0.35), source diversity (0.35), and velocity (0.3). Requires min 2 source families and min 4 items per topic.
   - **LLM mode:** sends 500 recent articles to cheap LLM for structured topic extraction.
3. Results capped at max 15 topics per snapshot.
4. Snapshots persisted to SQLite, pruned to last 20 rows.

## Acceptance Criteria

- [ ] NLP mode produces topic list without LLM dependency.
- [ ] LLM mode produces structured topics when enabled.
- [ ] Source diversity requirement prevents single-source topic dominance.
- [ ] Minimum item threshold filters out noise.
- [ ] Snapshots persisted and retrievable.
- [ ] Old snapshots pruned beyond 20 rows.

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| Fewer than 4 items in window | No topics produced |
| All items from single source | Topics filtered out (diversity < 2) |
| LLM call fails | Falls back to NLP-only results |
| No intel items at all | Empty result; no error |

## Out of Scope

- User-curated topic lists (handled by watchlists)
- Real-time streaming trend detection
