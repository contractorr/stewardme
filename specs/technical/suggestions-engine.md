# Suggestions Engine

**Status:** Implemented

## Overview

Unified suggestion endpoint merging items from all active subsystems with `why_now` annotations.

## Key Modules

- `src/web/routes/suggestions.py`
- `src/web/briefing_data.py` — `assemble_briefing_data()`
- `src/advisor/why_now.py` — `WhyNowReasoner`

## Interfaces

- `GET /api/suggestions?limit=10` → `list[SuggestionItem]`

## Data Assembly

`assemble_briefing_data()` collects from:
1. Daily brief items
2. Remaining recommendations
3. Company movement alerts
4. Hiring signal alerts
5. Regulatory change alerts
6. Assumption watchlist alerts
7. Dossier escalation candidates

Each source returns typed items. `WhyNowReasoner` annotates each with timing context via cheap LLM.

## Response Model

`SuggestionItem` (Pydantic): source_type, title, summary, why_now, metadata dict, created_at.

## Dependencies

- `advisor.why_now.WhyNowReasoner`
- `research.escalation.DossierEscalationEngine`
- `services.daily_brief`
- `web.briefing_data.assemble_briefing_data`
- `web.deps` (thread inbox, watchlist, profile)
