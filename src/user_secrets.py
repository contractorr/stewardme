"""Encrypted per-user secret storage."""

import structlog

from crypto_utils import decrypt_value, encrypt_value
from user_crud import _get_conn

logger = structlog.get_logger()


def get_user_secret(user_id: str, secret_key: str, fernet_key: str, db_path=None) -> str | None:
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


def get_user_secrets(user_id: str, fernet_key: str, db_path=None) -> dict[str, str]:
    """Get all decrypted secrets for a user."""
    conn = _get_conn(db_path)
    try:
        rows = conn.execute(
            "SELECT key, value FROM user_secrets WHERE user_id = ?", (user_id,)
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
    user_id: str, secret_key: str, value: str, fernet_key: str, db_path=None
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


def delete_user_secret(user_id: str, secret_key: str, db_path=None) -> None:
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
