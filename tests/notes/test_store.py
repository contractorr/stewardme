"""Tests for the notes store lifecycle."""

import pytest

from notes.polisher import PolishResult
from notes.store import NotesStore

USER = "user-123"
OTHER = "user-456"


@pytest.fixture
def store(tmp_path):
    return NotesStore(tmp_path / "notes.db")


def _result():
    return PolishResult(
        polished_markdown="# Clean\n\nText.",
        corrections=[{"type": "spelling", "original": "teh", "corrected": "the", "reason": "typo"}],
        diff="--- original\n+++ polished\n-teh\n+the",
    )


def test_create_pending_keeps_original(store):
    note = store.create_pending(USER, "My note", "teh original", _result(), "<h1>Clean</h1>")
    assert note.status == "pending"
    fetched = store.get_note(USER, note.id)
    assert fetched.original_text == "teh original"
    assert fetched.diff
    assert fetched.polished_html == "<h1>Clean</h1>"
    assert fetched.corrections[0]["type"] == "spelling"


def test_accept_discards_original_and_diff(store):
    note = store.create_pending(USER, "n", "original text", _result(), "<p>html</p>")
    accepted = store.accept(USER, note.id)
    assert accepted.status == "accepted"
    assert accepted.original_text is None
    assert accepted.diff == ""
    assert accepted.accepted_at is not None
    assert accepted.polished_html == "<p>html</p>"
    # the original is unrecoverable from the DB
    assert store.get_note(USER, note.id).original_text is None


def test_accept_is_idempotent(store):
    note = store.create_pending(USER, "n", "orig", _result(), "<p>x</p>")
    store.accept(USER, note.id)
    again = store.accept(USER, note.id)
    assert again.status == "accepted"


def test_delete_pending_note(store):
    note = store.create_pending(USER, "n", "orig", _result(), "<p>x</p>")
    assert store.delete(USER, note.id)
    assert store.get_note(USER, note.id) is None
    assert store.list_notes(USER) == []


def test_list_filters_by_status_and_omits_bodies(store):
    pending = store.create_pending(USER, "p", "orig", _result(), "<p>1</p>")
    accepted = store.create_pending(USER, "a", "orig2", _result(), "<p>2</p>")
    store.accept(USER, accepted.id)
    assert [n.id for n in store.list_notes(USER, status="pending")] == [pending.id]
    assert [n.id for n in store.list_notes(USER, status="accepted")] == [accepted.id]
    summary = store.list_notes(USER)[0]
    assert summary.polished_html == ""
    assert summary.original_text is None


def test_user_isolation(store):
    note = store.create_pending(USER, "n", "orig", _result(), "<p>x</p>")
    assert store.get_note(OTHER, note.id) is None
    assert store.accept(OTHER, note.id) is None
    assert not store.delete(OTHER, note.id)
    assert store.get_note(USER, note.id) is not None
