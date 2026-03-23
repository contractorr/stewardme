# Notifications

## Problem
Due reviews, stale goals, intel alerts have no push mechanism. Web app has no notification infra.

## Desired Behavior
- Bell icon in header shows unread count badge
- Clicking bell opens notification dropdown
- Notifications computed on-demand: due reviews, stale goals
- Read state persisted per-user in SQLite
- Polling every 60s for count

## Acceptance Criteria
- Bell visible in AppHeader with unread badge
- Notification panel lists items with title, body, action URL
- Mark-read and mark-all-read work
- Multi-user isolation (user B cannot see user A's notifications)
- Stale goals produce notifications
- Due curriculum reviews produce notifications
