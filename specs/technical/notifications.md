# Notifications — Technical Spec

## Architecture
Hybrid on-demand model: compute candidates from existing data sources, persist only read state.

## Backend

### `src/web/notification_store.py`
- SQLite `read_state(notification_id, read_at)` table per user
- Path: `~/coach/users/{user_id}/notifications.db`
- Methods: `is_read()`, `mark_read()`, `mark_all_read()`, `cleanup_old(days=30)`

### `src/web/notification_sources.py`
- `compute_notifications(user_id, store)` — returns list of notification dicts
- Sources: `_due_review_notification()`, `_stale_goal_notifications()`
- Dedup by composite ID `{type}:{source_id}`

### `src/web/routes/notifications.py`
- `GET /api/notifications` — list with limit + unread_only
- `GET /api/notifications/count` — `{"unread": N}`
- `POST /api/notifications/{id}/read`
- `POST /api/notifications/read-all`

## Frontend

### `NotificationBell.tsx` — Bell icon + red badge, polls /count every 60s
### `NotificationPanel.tsx` — shadcn Popover, fetches list on open
### `useNotifications.ts` — polling hook, count state, mark-read
### Integration: `<NotificationBell />` added to `AppHeader.tsx`

## Files
- New: notification_store.py, notification_sources.py, routes/notifications.py, frontend components, tests
- Modify: routes/__init__.py, AppHeader.tsx
