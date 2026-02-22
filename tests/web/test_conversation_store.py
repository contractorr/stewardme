"""Tests for conversation_store: CRUD, isolation, message ordering."""

from web.conversation_store import (
    add_message,
    conversation_belongs_to,
    create_conversation,
    delete_conversation,
    get_conversation,
    get_messages,
    list_conversations,
    update_timestamp,
)
from web.user_store import get_or_create_user, init_db


def _setup(tmp_path):
    db = tmp_path / "users.db"
    init_db(db)
    get_or_create_user("u1", email="a@b.com", db_path=db)
    return db


def test_create_and_list(tmp_path):
    db = _setup(tmp_path)
    cid = create_conversation("u1", "Hello world", db_path=db)
    assert cid
    convs = list_conversations("u1", db_path=db)
    assert len(convs) == 1
    assert convs[0]["title"] == "Hello world"
    assert convs[0]["message_count"] == 0


def test_title_truncated(tmp_path):
    db = _setup(tmp_path)
    long = "x" * 200
    create_conversation("u1", long, db_path=db)
    convs = list_conversations("u1", db_path=db)
    assert len(convs[0]["title"]) <= 80


def test_add_and_get_messages(tmp_path):
    db = _setup(tmp_path)
    cid = create_conversation("u1", "test", db_path=db)
    add_message(cid, "user", "hi", db_path=db)
    add_message(cid, "assistant", "hello", db_path=db)

    msgs = get_messages(cid, db_path=db)
    assert len(msgs) == 2
    assert msgs[0]["role"] == "user"
    assert msgs[1]["role"] == "assistant"
    assert msgs[1]["content"] == "hello"


def test_get_messages_limit(tmp_path):
    db = _setup(tmp_path)
    cid = create_conversation("u1", "test", db_path=db)
    for i in range(10):
        add_message(cid, "user", f"msg {i}", db_path=db)

    msgs = get_messages(cid, limit=3, db_path=db)
    assert len(msgs) == 3
    # Should be the last 3 messages, oldest first
    assert msgs[0]["content"] == "msg 7"
    assert msgs[2]["content"] == "msg 9"


def test_get_conversation_with_messages(tmp_path):
    db = _setup(tmp_path)
    cid = create_conversation("u1", "test", db_path=db)
    add_message(cid, "user", "q", db_path=db)
    add_message(cid, "assistant", "a", db_path=db)

    conv = get_conversation(cid, "u1", db_path=db)
    assert conv is not None
    assert conv["title"] == "test"
    assert len(conv["messages"]) == 2


def test_get_conversation_wrong_user(tmp_path):
    db = _setup(tmp_path)
    get_or_create_user("u2", db_path=db)
    cid = create_conversation("u1", "private", db_path=db)

    assert get_conversation(cid, "u2", db_path=db) is None


def test_delete_conversation(tmp_path):
    db = _setup(tmp_path)
    cid = create_conversation("u1", "doomed", db_path=db)
    add_message(cid, "user", "bye", db_path=db)

    assert delete_conversation(cid, "u1", db_path=db) is True
    assert list_conversations("u1", db_path=db) == []


def test_delete_wrong_user(tmp_path):
    db = _setup(tmp_path)
    get_or_create_user("u2", db_path=db)
    cid = create_conversation("u1", "test", db_path=db)

    assert delete_conversation(cid, "u2", db_path=db) is False
    assert len(list_conversations("u1", db_path=db)) == 1


def test_conversation_belongs_to(tmp_path):
    db = _setup(tmp_path)
    get_or_create_user("u2", db_path=db)
    cid = create_conversation("u1", "test", db_path=db)

    assert conversation_belongs_to(cid, "u1", db_path=db) is True
    assert conversation_belongs_to(cid, "u2", db_path=db) is False
    assert conversation_belongs_to("nonexistent", "u1", db_path=db) is False


def test_list_conversations_sorted_by_recency(tmp_path):
    db = _setup(tmp_path)
    c1 = create_conversation("u1", "first", db_path=db)
    c2 = create_conversation("u1", "second", db_path=db)
    # Update c1 to make it more recent
    update_timestamp(c1, db_path=db)

    convs = list_conversations("u1", db_path=db)
    assert convs[0]["id"] == c1
    assert convs[1]["id"] == c2


def test_message_count_in_list(tmp_path):
    db = _setup(tmp_path)
    cid = create_conversation("u1", "test", db_path=db)
    add_message(cid, "user", "q1", db_path=db)
    add_message(cid, "assistant", "a1", db_path=db)
    add_message(cid, "user", "q2", db_path=db)

    convs = list_conversations("u1", db_path=db)
    assert convs[0]["message_count"] == 3


def test_user_isolation(tmp_path):
    db = _setup(tmp_path)
    get_or_create_user("u2", db_path=db)
    create_conversation("u1", "u1 conv", db_path=db)
    create_conversation("u2", "u2 conv", db_path=db)

    assert len(list_conversations("u1", db_path=db)) == 1
    assert len(list_conversations("u2", db_path=db)) == 1
    assert list_conversations("u1", db_path=db)[0]["title"] == "u1 conv"
