# Projects & Opportunities

**Status:** Implemented
**Author:** -
**Date:** 2026-03-07

## Problem

Users want help turning their profile and current market signals into concrete project opportunities, especially open-source issues to contribute to and project ideas they could pursue next.

## Users

Users who want practical opportunities derived from their skills, interests, and current intelligence.

## Desired Behavior

### Matching issues

1. User can request GitHub issues that match their profile.
2. System uses profile context plus recent intelligence to rank issue opportunities.
3. Each result includes title, URL, summary, tags, source, and a match score.

### Project ideas

1. User can request generated project ideas.
2. System uses profile, journal, and broader retrieval context to produce idea suggestions.
3. Generated ideas are returned as a lightweight list rather than a full project-management board.

Current interface scope:
- This capability is currently exposed through web API routes.
- There is not yet a dedicated dashboard page for project opportunities.

## Acceptance Criteria

- [ ] User can fetch matching issues from the product API.
- [ ] User can generate project ideas from the product API.
- [ ] Matching uses available profile context when present.
- [ ] Missing profile data degrades gracefully rather than crashing the feature.

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| No profile exists | Return weaker but still valid matches or ideas |
| No LLM key exists for idea generation | Product returns a clear configuration error |
| Matching pipeline fails | Feature returns an empty or error state without breaking the rest of the app |

## Out of Scope

- Full project planning boards
- Automatic issue application or PR submission
- Persistent project-idea storage and editing UI
