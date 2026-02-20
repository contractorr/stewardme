"""Tests for user_store: user CRUD, secrets CRUD, isolation."""

from cryptography.fernet import Fernet

from web.user_store import (
    delete_user_secret,
    get_or_create_user,
    get_user_secret,
    get_user_secrets,
    init_db,
    set_user_secret,
)


def test_create_user(tmp_path):
    db = tmp_path / "users.db"
    init_db(db)
    user = get_or_create_user("u1", email="a@b.com", name="Alice", db_path=db)
    assert user["id"] == "u1"
    assert user["email"] == "a@b.com"


def test_idempotent_upsert(tmp_path):
    db = tmp_path / "users.db"
    init_db(db)
    get_or_create_user("u1", email="a@b.com", name="Alice", db_path=db)
    user = get_or_create_user("u1", email="new@b.com", name="Alice2", db_path=db)
    assert user["email"] == "new@b.com"
    assert user["name"] == "Alice2"


def test_set_get_secret(tmp_path):
    db = tmp_path / "users.db"
    fernet_key = Fernet.generate_key().decode()
    init_db(db)
    get_or_create_user("u1", db_path=db)

    set_user_secret("u1", "llm_api_key", "sk-abc", fernet_key, db)
    val = get_user_secret("u1", "llm_api_key", fernet_key, db)
    assert val == "sk-abc"


def test_get_all_secrets(tmp_path):
    db = tmp_path / "users.db"
    fernet_key = Fernet.generate_key().decode()
    init_db(db)
    get_or_create_user("u1", db_path=db)

    set_user_secret("u1", "key_a", "val_a", fernet_key, db)
    set_user_secret("u1", "key_b", "val_b", fernet_key, db)

    secrets = get_user_secrets("u1", fernet_key, db)
    assert secrets == {"key_a": "val_a", "key_b": "val_b"}


def test_overwrite_secret(tmp_path):
    db = tmp_path / "users.db"
    fernet_key = Fernet.generate_key().decode()
    init_db(db)
    get_or_create_user("u1", db_path=db)

    set_user_secret("u1", "key", "v1", fernet_key, db)
    set_user_secret("u1", "key", "v2", fernet_key, db)
    assert get_user_secret("u1", "key", fernet_key, db) == "v2"


def test_delete_secret(tmp_path):
    db = tmp_path / "users.db"
    fernet_key = Fernet.generate_key().decode()
    init_db(db)
    get_or_create_user("u1", db_path=db)

    set_user_secret("u1", "key", "val", fernet_key, db)
    delete_user_secret("u1", "key", db)
    assert get_user_secret("u1", "key", fernet_key, db) is None


def test_secrets_isolation(tmp_path):
    """User A's secrets invisible to User B."""
    db = tmp_path / "users.db"
    fernet_key = Fernet.generate_key().decode()
    init_db(db)
    get_or_create_user("alice", db_path=db)
    get_or_create_user("bob", db_path=db)

    set_user_secret("alice", "api_key", "sk-alice", fernet_key, db)
    set_user_secret("bob", "api_key", "sk-bob", fernet_key, db)

    assert get_user_secret("alice", "api_key", fernet_key, db) == "sk-alice"
    assert get_user_secret("bob", "api_key", fernet_key, db) == "sk-bob"
    assert get_user_secrets("alice", fernet_key, db) == {"api_key": "sk-alice"}


def test_missing_secret_returns_none(tmp_path):
    db = tmp_path / "users.db"
    fernet_key = Fernet.generate_key().decode()
    init_db(db)
    get_or_create_user("u1", db_path=db)
    assert get_user_secret("u1", "nonexistent", fernet_key, db) is None
