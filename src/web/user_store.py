"""Multi-user SQLite store: users table + per-user encrypted secrets."""

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import structlog

from web.crypto import decrypt_value, encrypt_value

logger = structlog.get_logger()

_DEFAULT_DB_PATH = Path(os.environ.get("COACH_HOME", Path.home() / "coach")) / "users.db"


def _get_conn(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or _DEFAULT_DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
        """)
        conn.commit()
    finally:
        conn.close()


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
            # Update email/name if changed
            if email or name:
                conn.execute(
                    "UPDATE users SET email = COALESCE(?, email), name = COALESCE(?, name) WHERE id = ?",
                    (email, name, user_id),
                )
                conn.commit()
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            return dict(row)
        else:
            now = datetime.now(timezone.utc).isoformat()
            conn.execute(
                "INSERT INTO users (id, email, name, created_at) VALUES (?, ?, ?, ?)",
                (user_id, email, name, now),
            )
            conn.commit()
            return {"id": user_id, "email": email, "name": name, "created_at": now}
    finally:
        conn.close()


def get_user_secret(
    user_id: str,
    secret_key: str,
    fernet_key: str,
    db_path: Path | None = None,
) -> str | None:
    """Get a single decrypted secret for a user."""
    conn = _get_conn(db_path)
    try:
        row = conn.execute(
            "SELECT value FROM user_secrets WHERE user_id = ? AND key = ?",
            (user_id, secret_key),
        ).fetchone()
        if not row:
            return None
        return decrypt_value(fernet_key, row["value"], key_name=secret_key)
    finally:
        conn.close()


def get_user_secrets(
    user_id: str,
    fernet_key: str,
    db_path: Path | None = None,
) -> dict[str, str]:
    """Get all decrypted secrets for a user."""
    conn = _get_conn(db_path)
    try:
        rows = conn.execute(
            "SELECT key, value FROM user_secrets WHERE user_id = ?",
            (user_id,),
        ).fetchall()
        result = {}
        skipped = 0
        for row in rows:
            val = decrypt_value(fernet_key, row["value"], key_name=row["key"])
            if val is not None:
                result[row["key"]] = val
            else:
                skipped += 1
        if skipped:
            logger.warning(
                "user_store.secrets_skipped",
                user_id=user_id,
                total=len(rows),
                skipped=skipped,
            )
        return result
    finally:
        conn.close()


def set_user_secret(
    user_id: str,
    secret_key: str,
    value: str,
    fernet_key: str,
    db_path: Path | None = None,
) -> None:
    """Encrypt and store a secret for a user."""
    conn = _get_conn(db_path)
    try:
        encrypted = encrypt_value(fernet_key, value)
        conn.execute(
            "INSERT INTO user_secrets (user_id, key, value) VALUES (?, ?, ?) "
            "ON CONFLICT(user_id, key) DO UPDATE SET value = excluded.value",
            (user_id, secret_key, encrypted),
        )
        conn.commit()
        logger.info("user_store.secret_saved", user_id=user_id, key=secret_key)
    finally:
        conn.close()


def delete_user_secret(
    user_id: str,
    secret_key: str,
    db_path: Path | None = None,
) -> None:
    """Remove a secret for a user."""
    conn = _get_conn(db_path)
    try:
        conn.execute(
            "DELETE FROM user_secrets WHERE user_id = ? AND key = ?",
            (user_id, secret_key),
        )
        conn.commit()
    finally:
        conn.close()
