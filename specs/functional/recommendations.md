# Recommendations

**Status:** Approved
**Author:** —
**Date:** 2026-03-02

## Problem

Users want actionable, personalized recommendations (articles to read, skills to learn, projects to try) based on their profile, goals, and current intel — not generic lists.

## Users

Users with a completed profile and some journal history. Recommendations improve as more data accumulates.

## Desired Behavior

### Generation

1. System periodically generates recommendations by analyzing user profile, journal patterns, goals, and recent intel
2. Each recommendation is scored on four weighted dimensions: relevance (30%), urgency (25%), feasibility (25%), impact (20%)
3. Recommendations below a minimum score threshold (default 6.0) are filtered out
4. At most 3 recommendations per category are kept to avoid overload
5. Recommendations are deduplicated against recent ones (similarity threshold over a 30-day window)

### Viewing

1. User lists current recommendations
2. Each recommendation shows: title, category, score, rationale, and suggested action
3. Recommendations are sorted by score descending

### Feedback

1. User can rate a recommendation (useful / not useful / already knew)
2. Rating feeds back into the scoring system as a rating boost for future relevance tuning
3. User can dismiss a recommendation to remove it from active list

### Delivery

1. Recommendations are saved as markdown files in `~/coach/recommendations/`
2. On the configured schedule (default: weekly, Sunday 8am), new recommendations are generated and stored
3. Available for retrieval via CLI, web, and MCP

## Acceptance Criteria

- [ ] Recommendations are personalized based on profile and journal content
- [ ] Scoring weights sum to 1.0; recommendations below threshold are excluded
- [ ] Max 3 per category prevents recommendation fatigue
- [ ] Dedup prevents the same recommendation from recurring within 30 days
- [ ] User can rate recommendations and ratings affect future scoring
- [ ] Recommendations are viewable via CLI, web, and MCP
- [ ] Scheduled generation runs without manual intervention

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| No profile, no journal | Cannot generate meaningful recommendations; return empty or generic fallback |
| All recommendations below threshold | Return empty list, not low-quality recs |
| User rates everything as "not useful" | Rating boost adjusts; future recs shift focus |
| No intel items available | Recommendations based on profile + journal only |
| Duplicate recommendation within 30 days | Filtered by similarity dedup |

## Out of Scope

- External content fetching (recommendations link out but don't fetch full articles)
- Recommendation categories management (categories are derived, not user-defined)
- Email or push delivery of recommendations
