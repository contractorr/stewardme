# Trending Radar

**Status:** Implemented

## Overview

Cross-source topic trend detection from intelligence items, surfaced in Radar.

## Key Modules

- `src/intelligence/trending_radar.py`

## Classes

- `TrendingRadar(db_path, days=7, min_source_families=2, min_items=4, max_topics=15, weights=None)`
- Methods: `compute()` (NLP), `compute_llm(llm)` (LLM), `refresh()`, `load()`

## NLP Pipeline

1. `_extract_title_terms()` — RAKE-style phrase extraction from item titles
2. `_detect_collocations()` — Dunning log-likelihood bigram collocation detection
3. Scoring: `0.35 * sublinear_freq + 0.35 * source_family_diversity + 0.3 * velocity_score`
4. Gated by `min_source_families` and `min_items`
5. `_velocity_score()` — measures acceleration (recent items vs older items within window)

## LLM Mode

- Sends up to 500 recent article titles/summaries to cheap LLM
- Prompt requests structured JSON topic extraction
- Validates output; falls back to NLP results on failure

## Storage

- SQLite table `trending_radar` in intel.db
- Schema: snapshot_date, topics_json, mode (nlp/llm), created_at
- Pruned to 20 most recent rows on each write

## Config

Constructor params (no config.yaml keys currently):
- `days` (default 7)
- `min_source_families` (default 2)
- `min_items` (default 4)
- `max_topics` (default 15)
- `weights` dict (default: freq=0.35, diversity=0.35, velocity=0.3)

## Dependencies

- `db.wal_connect`
- `intel_items` table in intel.db
- `llm.factory.create_cheap_provider` (optional, for LLM mode)
