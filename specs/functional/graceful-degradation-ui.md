# Graceful Degradation UI

## Problem
Backend handles failures via `@graceful()` but frontend shows nothing. User doesn't know advice is based on partial data.

## Desired Behavior
- When backend components fail gracefully, collect degradation info per request
- Include `degradations` array in advisor/briefing/greeting JSON responses
- Frontend shows subtle amber banner: "Partial data — {messages}"
- Advisor streaming emits `{"type": "degradation", ...}` SSE events

## Acceptance Criteria
- `degradations` field present in responses when components failed
- Empty array when everything succeeded
- Banner visible when degradations exist, hidden otherwise
- No impact on request latency or error behavior
