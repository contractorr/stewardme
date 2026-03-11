# Conversation Storage

**Status:** Implemented
**Author:** —
**Date:** 2026-03-11

## Problem

Users interact with the advisor through multi-turn chat. Without persistence, conversations are lost on page reload or session end, preventing users from continuing a line of inquiry or reviewing past advice.

## Users

All web app users who interact with the advisor chat.

## Desired Behavior

1. Each user can have multiple named conversations persisted across sessions.
2. Conversations store messages (role, content, timestamps) with full ordering.
3. Messages can reference library items as attachments (e.g., uploaded PDFs discussed in chat).
4. Users can list, open, rename, and delete conversations.
5. Deleting a conversation cascades to all its messages and attachment links.
6. Conversation ownership is enforced — users can only access their own conversations.

## Acceptance Criteria

- [ ] Conversations persist across page reloads and sessions.
- [ ] Messages maintain correct ordering within a conversation.
- [ ] Attachment links connect messages to library items without duplicating file data.
- [ ] Deletion cascades to messages and attachment links.
- [ ] User isolation enforced on all read/write/delete operations.

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| User deletes a library item linked as attachment | Attachment link becomes orphaned; conversation still loads |
| Concurrent message writes to same conversation | SQLite WAL mode handles; messages ordered by created_at |
| User has no conversations | Empty list returned; no error |

## Out of Scope

- Conversation sharing between users
- Conversation export
- Real-time sync across devices
