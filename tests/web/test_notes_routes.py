"""Tests for note polish routes."""

import pytest

from notes.polisher import NotePolisher, PolishResult, compute_diff
from web.routes import notes as notes_routes


class FakePolisher(NotePolisher):
    def __init__(self):  # no LLM
        self.llm = None

    def polish(self, text: str) -> PolishResult:
        polished = "# Polished\n\nThe fixed text."
        return PolishResult(
            polished_markdown=polished,
            corrections=[
                {"type": "spelling", "original": "teh", "corrected": "the", "reason": "typo"}
            ],
            diff=compute_diff(text, polished),
        )


@pytest.fixture
def fake_polisher(monkeypatch):
    monkeypatch.setattr(notes_routes, "_build_polisher", lambda user_id: FakePolisher())


def _polish(client, headers, text="teh messy note"):
    response = client.post(
        "/api/notes/polish", headers=headers, json={"text": text, "title": "My Note"}
    )
    assert response.status_code == 201
    return response.json()


def test_polish_returns_pending_note_with_diff(client, auth_headers, fake_polisher):
    note = _polish(client, auth_headers)
    assert note["status"] == "pending"
    assert note["title"] == "My Note"
    assert note["original_text"] == "teh messy note"
    assert "<h1>Polished</h1>" in note["polished_html"]
    assert note["corrections"][0]["type"] == "spelling"
    assert "-teh messy note" in note["diff"]


def test_accept_stores_html_and_discards_original(client, auth_headers, fake_polisher):
    note = _polish(client, auth_headers)
    accepted = client.post(f"/api/notes/{note['id']}/accept", headers=auth_headers)
    assert accepted.status_code == 200
    body = accepted.json()
    assert body["status"] == "accepted"
    assert body["original_text"] is None
    assert body["diff"] == ""
    assert "<h1>Polished</h1>" in body["polished_html"]

    # original is gone from every endpoint
    fetched = client.get(f"/api/notes/{note['id']}", headers=auth_headers).json()
    assert fetched["original_text"] is None


def test_discard_deletes_note(client, auth_headers, fake_polisher):
    note = _polish(client, auth_headers)
    assert client.post(f"/api/notes/{note['id']}/discard", headers=auth_headers).status_code == 204
    assert client.get(f"/api/notes/{note['id']}", headers=auth_headers).status_code == 404
    listing = client.get("/api/notes", headers=auth_headers).json()
    assert all(n["id"] != note["id"] for n in listing)


def test_list_filters_by_status(client, auth_headers, fake_polisher):
    pending = _polish(client, auth_headers, text="one")
    accepted = _polish(client, auth_headers, text="two")
    client.post(f"/api/notes/{accepted['id']}/accept", headers=auth_headers)

    pending_list = client.get("/api/notes?status=pending", headers=auth_headers).json()
    accepted_list = client.get("/api/notes?status=accepted", headers=auth_headers).json()
    assert any(n["id"] == pending["id"] for n in pending_list)
    assert all(n["id"] != accepted["id"] for n in pending_list)
    assert any(n["id"] == accepted["id"] for n in accepted_list)


def test_notes_are_user_isolated(client, auth_headers, auth_headers_b, fake_polisher):
    note = _polish(client, auth_headers)
    assert client.get(f"/api/notes/{note['id']}", headers=auth_headers_b).status_code == 404
    assert client.post(f"/api/notes/{note['id']}/accept", headers=auth_headers_b).status_code == 404
    assert (
        client.post(f"/api/notes/{note['id']}/discard", headers=auth_headers_b).status_code == 404
    )


def test_polish_rejects_blank_text(client, auth_headers, fake_polisher):
    response = client.post("/api/notes/polish", headers=auth_headers, json={"text": "   "})
    assert response.status_code == 422


def test_polish_requires_llm_key(client, auth_headers, monkeypatch):
    monkeypatch.setattr(
        notes_routes, "resolve_llm_credentials_for_user", lambda user_id: (None, None, None)
    )
    response = client.post("/api/notes/polish", headers=auth_headers, json={"text": "some note"})
    assert response.status_code == 400


def test_polish_error_persists_nothing(client, auth_headers, monkeypatch):
    class ExplodingPolisher(FakePolisher):
        def polish(self, text):
            from notes.polisher import NotePolishError

            raise NotePolishError("The language model returned an unusable response")

    monkeypatch.setattr(notes_routes, "_build_polisher", lambda user_id: ExplodingPolisher())
    response = client.post("/api/notes/polish", headers=auth_headers, json={"text": "some note"})
    assert response.status_code == 502
    listing = client.get("/api/notes", headers=auth_headers).json()
    assert listing == []
