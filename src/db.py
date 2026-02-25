"""Shared SQLite helpers — WAL mode, row_factory defaults."""

import sqlite3
from pathlib import Path


def wal_connect(db_path: str | Path, row_factory: bool = False) -> sqlite3.Connection:
    """Open SQLite connection with WAL journal mode.

    Args:
        db_path: Path to database file.
        row_factory: If True, set conn.row_factory = sqlite3.Row.
    """
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    if row_factory:
        conn.row_factory = sqlite3.Row
    return conn
