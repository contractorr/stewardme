# Nudge Engine

**Status:** Implemented

## Overview

CLI-only behavioral nudges for profile freshness, goal staleness, and journal streaks.

## Key Modules

- `src/advisor/nudges.py`

## Interfaces

- `NudgeEngine(profile_storage, goal_tracker, journal_storage)` — constructor
- `get_nudges_for_cli(config) -> list[str]` — convenience function

## Checks

1. **Profile staleness:** compares `profile.last_updated` against `config.profile.interview_refresh_days` (default 90)
2. **Stale goals:** calls `GoalTracker.get_stale_goals(threshold_days=14)`
3. **Journal streak:** queries `JournalStorage` for entries in last 7 days; flags 0 (gap) or celebrates 5+ (streak)

## Dependencies

- `profile.storage.ProfileStorage`
- `advisor.goals.GoalTracker`
- `journal.storage.JournalStorage`

## Config

- `config.profile.interview_refresh_days` (default 90)
