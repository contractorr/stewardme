# Goal-Intel Matching

**Status:** Implemented

## Overview

Matches scraped intel items to active goals via fused keyword + semantic scoring.

## Key Modules

- `src/intelligence/goal_intel_match.py`

## Classes

- `GoalIntelMatchStore` — SQLite persistence for matches
- `GoalIntelMatcher` — core matching logic
- `GoalIntelLLMEvaluator` — optional LLM re-ranking

## Scoring

Fused score = `0.6 * keyword_score + 0.4 * semantic_score`

**Keyword:** extracts terms from goal title/tags/content → `score_profile_relevance()` against intel items

**Semantic:** queries ChromaDB `IntelEmbeddingManager` for similar embeddings. Falls back to 0 if unavailable.

**Urgency tiers:** high (≥0.15), medium (≥0.08), low (≥0.04)

## LLM Re-ranking

`GoalIntelLLMEvaluator`:
- Processes matches in batches of 20
- Cheap LLM filters false positives
- Preserves pre-LLM matches on failure

## Adaptive Recency

- Lookback = days since last match for each goal, clamped [7, 30]
- Goals with no recent matches get wider search window

## Dedup

- 7-day dedup on (goal_path, url) in `GoalIntelMatchStore`

## Storage

- SQLite table via `GoalIntelMatchStore` using `db.wal_connect`

## Dependencies

- `intelligence.scraper.IntelStorage`
- `intelligence.embeddings.IntelEmbeddingManager` (optional)
- `intelligence.search.score_profile_relevance`
- `llm.factory.create_cheap_provider`
