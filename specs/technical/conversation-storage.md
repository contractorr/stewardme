# Conversation Storage

**Status:** Implemented

## Overview

Per-user chat persistence in SQLite (`users.db`), consumed by the advisor chat UI.

## Key Modules

- `src/web/conversation_store.py`
- `src/web/routes/advisor.py` (consumer)

## Schema

Three tables in `users.db`:

- `conversations` (id TEXT PK, user_id TEXT, title TEXT, created_at, updated_at)
- `conversation_messages` (id TEXT PK, conversation_id TEXT FK CASCADE, role TEXT, content TEXT, created_at)
- `conversation_message_attachments` (id INTEGER PK, message_id TEXT FK CASCADE, library_item_id TEXT, file_name TEXT, mime_type TEXT)

## Interfaces

- `create_conversation(user_id, title?) -> conversation`
- `list_conversations(user_id) -> list`
- `get_conversation(user_id, conv_id) -> conversation + messages`
- `add_message(user_id, conv_id, role, content, attachments?) -> message`
- `delete_message(user_id, conv_id, msg_id)`
- `delete_conversation(user_id, conv_id)`
- `get_messages(user_id, conv_id) -> list`

All functions enforce `user_id` ownership. Attachments loaded via `_load_attachments()` JOIN on message_id.

## Config

No explicit config. Inherits `COACH_HOME` / `COACH_USERS_DB_PATH` env vars. Uses `db.wal_connect` for WAL mode.
