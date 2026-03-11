# Engagement Scoring

**Status:** Implemented

## Overview

Event-based engagement tracking feeding dynamic recommendation weighting.

## Key Modules

- `src/web/routes/engagement.py`
- `src/web/user_store.py` — `log_engagement()`, `get_engagement_stats()`, `get_feedback_count()`

## Interfaces

- `POST /api/engagement` — record event (body: `EngagementEvent`)
- `GET /api/engagement/stats?days=30` — grouped counts (response: `EngagementStats`)

## Event Types

`opened`, `saved`, `dismissed`, `acted_on`, `feedback_useful`, `feedback_irrelevant`

## Storage

- `engagement_events` table in users.db: user_id, target_type, target_id, event_type, created_at
- Feedback events also write to `usage_events` as `recommendation_feedback` for admin analytics

## Models

- `EngagementEvent` (Pydantic): target_type, target_id, event_type
- `EngagementStats` (Pydantic): grouped counts by target_type × event_type

## Dynamic Weighting

`get_feedback_count(user_id)` aggregates across both tables. Feeds `compute_dynamic_weight()` in `advisor.rag` to adjust journal:intel ratio (default 70:30).

## Dependencies

- `web.user_store`
- `web.models`
- Consumed by: `advisor.rag.compute_dynamic_weight()`
