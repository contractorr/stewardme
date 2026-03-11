# Signals

**Status:** Implemented

## Overview

Signal detection engine scanning data sources to produce prioritized actionable signals.

## Key Modules

- `src/advisor/signals.py`

## Classes

- `SignalType` (enum): TOPIC_EMERGENCE, GOAL_STALE, GOAL_COMPLETE_CANDIDATE, DEADLINE_URGENT, JOURNAL_GAP, LEARNING_STALLED, RESEARCH_TRIGGER, RECURRING_BLOCKER
- `Signal` (dataclass): type, title, detail, severity (1–10), source_ref, created_at
- `SignalStore`: SQLite persistence with hash-based dedup
- `SignalDetector`: runs 7 detection methods, collects results

## Storage

- SQLite table via `SignalStore` using `db.wal_connect`
- Hash dedup: SHA256 of (type + title + source_ref) prevents re-insertion
- Dual-write: each signal also persisted to `InsightStore` via `advisor.insights`

## Detectors

1. `_detect_stale_goals()` — `GoalTracker.get_stale_goals()`
2. `_detect_goal_completion()` — completion candidate heuristic
3. `_detect_journal_gap()` — no entries in recent window
4. `_detect_topic_emergence()` — `TrendDetector` from journal trends
5. `_detect_deadline_urgency()` — upcoming events within `deadline_warning_days`
6. `_detect_research_triggers()` — topic mentioned 3+ times in 7d in intel
7. `_detect_recurring_blockers()` — negative keyword clustering in journal

## Config

- `config.agent.signals.deadline_warning_days` (default 14)
- `config.agent.signals.topic_mention_threshold` (default 3)

## Dependencies

- `advisor.goals.GoalTracker`
- `advisor.insights.InsightStore`
- `advisor.events.get_upcoming_events`
- `journal.trends.TrendDetector`
- `intelligence.scraper.IntelStorage`
