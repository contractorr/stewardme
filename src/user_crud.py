"""User CRUD, onboarding, and display name management."""

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import structlog

from db import wal_connect
from storage_paths import get_coach_home

logger = structlog.get_logger()


def get_default_db_path() -> Path:
    """Resolve the default users DB path from the current environment."""
    explicit_path = os.environ.get("COACH_USERS_DB_PATH")
    if explicit_path:
        return Path(explicit_path).expanduser()

    coach_home = os.environ.get("COACH_HOME")
    if coach_home:
        return Path(coach_home).expanduser() / "users.db"

    return get_coach_home() / "users.db"


def _get_conn(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or get_default_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = wal_connect(path, row_factory=True)
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db(db_path: Path | None = None) -> None:
    """Create tables if they don't exist."""
    conn = _get_conn(db_path)
    try:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT,
                name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS user_secrets (
                user_id TEXT NOT NULL REFERENCES users(id),
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                PRIMARY KEY (user_id, key)
            );
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                title TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            CREATE INDEX IF NOT EXISTS idx_conv_user ON conversations(user_id, updated_at DESC);
            CREATE TABLE IF NOT EXISTS conversation_messages (
                id TEXT PRIMARY KEY,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('user','assistant')),
                content TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
            );
            CREATE INDEX IF NOT EXISTS idx_msg_conv ON conversation_messages(conversation_id, created_at ASC);
            CREATE TABLE IF NOT EXISTS conversation_message_attachments (
                id TEXT PRIMARY KEY,
                message_id TEXT NOT NULL,
                library_item_id TEXT NOT NULL,
                file_name TEXT,
                mime_type TEXT,
                created_at TIMESTAMP NOT NULL,
                FOREIGN KEY (message_id) REFERENCES conversation_messages(id) ON DELETE CASCADE
            );
            CREATE INDEX IF NOT EXISTS idx_msg_attachment_message ON conversation_message_attachments(message_id);

            CREATE TABLE IF NOT EXISTS onboarding_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL REFERENCES users(id),
                turn_number INTEGER NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('user','assistant')),
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS idx_onboard_user ON onboarding_responses(user_id, created_at);

            CREATE TABLE IF NOT EXISTS engagement_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL REFERENCES users(id),
                event_type TEXT NOT NULL CHECK(event_type IN (
                    'opened','saved','dismissed','acted_on','feedback_useful','feedback_irrelevant'
                )),
                target_type TEXT NOT NULL,
                target_id TEXT NOT NULL,
                metadata_json TEXT DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS idx_engage_user ON engagement_events(user_id, created_at DESC);

            CREATE TABLE IF NOT EXISTS usage_events (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                event      TEXT NOT NULL,
                user_id    TEXT,
                metadata   TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS idx_usage_event ON usage_events(event, created_at DESC);

            CREATE TABLE IF NOT EXISTS user_rss_feeds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL REFERENCES users(id),
                url TEXT NOT NULL,
                name TEXT,
                added_by TEXT NOT NULL DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, url)
            );
            CREATE INDEX IF NOT EXISTS idx_rss_user ON user_rss_feeds(user_id);
        """)
        conn.commit()
        # Migration: add last_login to existing DBs
        try:
            conn.execute("ALTER TABLE users ADD COLUMN last_login TIMESTAMP")
            conn.commit()
        except sqlite3.OperationalError:
            pass  # column already exists
        # Migration: add onboarded flag (default TRUE for existing users)
        try:
            conn.execute("ALTER TABLE users ADD COLUMN onboarded BOOLEAN NOT NULL DEFAULT 1")
            conn.commit()
        except sqlite3.OperationalError:
            pass  # column already exists
    finally:
        conn.close()


def _migrate_secrets(conn: sqlite3.Connection, target_id: str, email: str) -> None:
    """Copy secrets from old user IDs (same email) to the new stable ID."""
    old_users = conn.execute(
        "SELECT id FROM users WHERE email = ? AND id != ?",
        (email, target_id),
    ).fetchall()
    if not old_users:
        return
    migrated = 0
    for (old_id,) in old_users:
        rows = conn.execute(
            "SELECT key, value FROM user_secrets WHERE user_id = ?", (old_id,)
        ).fetchall()
        for key, value in rows:
            exists = conn.execute(
                "SELECT 1 FROM user_secrets WHERE user_id = ? AND key = ?",
                (target_id, key),
            ).fetchone()
            if not exists:
                conn.execute(
                    "INSERT INTO user_secrets (user_id, key, value) VALUES (?, ?, ?)",
                    (target_id, key, value),
                )
                migrated += 1
    if migrated:
        conn.commit()
        logger.info("user_store.secrets_migrated", target=target_id, migrated=migrated)


def get_or_create_user(
    user_id: str,
    email: str | None = None,
    name: str | None = None,
    db_path: Path | None = None,
) -> dict[str, Any]:
    """Upsert user on OAuth login. Returns user dict."""
    conn = _get_conn(db_path)
    try:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if row:
            now = datetime.now(timezone.utc).isoformat()
            conn.execute(
                "UPDATE users SET email = COALESCE(?, email), name = COALESCE(name, ?), last_login = ? WHERE id = ?",
                (email, name, now, user_id),
            )
            conn.commit()
            if email:
                _migrate_secrets(conn, user_id, email)
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            return dict(row)
        else:
            now = datetime.now(timezone.utc).isoformat()
            conn.execute(
                "INSERT INTO users (id, email, name, created_at, last_login, onboarded) VALUES (?, ?, ?, ?, ?, 0)",
                (user_id, email, name, now, now),
            )
            conn.commit()
            if email:
                _migrate_secrets(conn, user_id, email)
            return {
                "id": user_id,
                "email": email,
                "name": name,
                "created_at": now,
                "last_login": now,
            }
    finally:
        conn.close()


def is_onboarded(user_id: str, db_path: Path | None = None) -> bool:
    """Check if user has completed onboarding."""
    conn = _get_conn(db_path)
    try:
        row = conn.execute("SELECT onboarded FROM users WHERE id = ?", (user_id,)).fetchone()
        return bool(row and row["onboarded"])
    finally:
        conn.close()


def mark_onboarded(user_id: str, db_path: Path | None = None) -> None:
    """Mark user as having completed onboarding."""
    conn = _get_conn(db_path)
    try:
        conn.execute("UPDATE users SET onboarded = 1 WHERE id = ?", (user_id,))
        conn.commit()
    finally:
        conn.close()


def update_user_name(user_id: str, name: str, db_path: Path | None = None) -> None:
    """Update the display name for a user."""
    conn = _get_conn(db_path)
    try:
        conn.execute("UPDATE users SET name = ? WHERE id = ?", (name, user_id))
        conn.commit()
    finally:
        conn.close()


def get_user_name(user_id: str, db_path: Path | None = None) -> str | None:
    """Get the display name for a user."""
    conn = _get_conn(db_path)
    try:
        row = conn.execute("SELECT name FROM users WHERE id = ?", (user_id,)).fetchone()
        return row["name"] if row else None
    finally:
        conn.close()


def save_onboarding_turn(
    user_id: str, turn_number: int, role: str, content: str, db_path: Path | None = None
) -> None:
    """Persist a single onboarding conversation turn."""
    conn = _get_conn(db_path)
    try:
        conn.execute(
            "INSERT INTO onboarding_responses (user_id, turn_number, role, content) VALUES (?, ?, ?, ?)",
            (user_id, turn_number, role, content),
        )
        conn.commit()
    finally:
        conn.close()


def get_onboarding_responses(user_id: str, db_path: Path | None = None) -> list[dict]:
    """Get all onboarding responses for a user, ordered by turn."""
    conn = _get_conn(db_path)
    try:
        rows = conn.execute(
            "SELECT turn_number, role, content, created_at FROM onboarding_responses "
            "WHERE user_id = ? ORDER BY turn_number, created_at",
            (user_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def clear_onboarding_responses(user_id: str, db_path: Path | None = None) -> None:
    """Delete all onboarding responses for a user (for re-onboarding)."""
    conn = _get_conn(db_path)
    try:
        conn.execute("DELETE FROM onboarding_responses WHERE user_id = ?", (user_id,))
        conn.commit()
    finally:
        conn.close()


def delete_user(user_id: str, db_path: Path | None = None) -> bool:
    """Delete a user and all associated data. Returns True if user existed."""
    conn = _get_conn(db_path)
    try:
        row = conn.execute("SELECT 1 FROM users WHERE id = ?", (user_id,)).fetchone()
        if not row:
            return False
        conn.execute("DELETE FROM user_secrets WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM onboarding_responses WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM engagement_events WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM usage_events WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM user_rss_feeds WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        logger.info("user_store.user_deleted", user_id=user_id)
        return True
    finally:
        conn.close()
