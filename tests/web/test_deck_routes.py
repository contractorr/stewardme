"""Tests for flashcard deck routes (Anki import/export + review)."""

import io
import zipfile

from curriculum.anki import AnkiCard, build_apkg


def _create_deck(client, headers, title="Test Deck"):
    response = client.post("/api/curriculum/decks", headers=headers, json={"title": title})
    assert response.status_code == 201
    return response.json()


def test_deck_crud_flow(client, auth_headers):
    deck = _create_deck(client, auth_headers)
    assert deck["title"] == "Test Deck"
    assert deck["card_count"] == 0

    listing = client.get("/api/curriculum/decks", headers=auth_headers).json()
    assert any(d["id"] == deck["id"] for d in listing)

    card = client.post(
        f"/api/curriculum/decks/{deck['id']}/cards",
        headers=auth_headers,
        json={"front": "What is RAG?", "back": "Retrieval-augmented generation"},
    )
    assert card.status_code == 201

    detail = client.get(f"/api/curriculum/decks/{deck['id']}", headers=auth_headers).json()
    assert detail["card_count"] == 1
    assert detail["cards"][0]["front"] == "What is RAG?"

    patched = client.patch(
        f"/api/curriculum/decks/{deck['id']}/cards/{card.json()['id']}",
        headers=auth_headers,
        json={"front": "What is RAG, really?"},
    )
    assert patched.status_code == 200
    assert patched.json()["front"] == "What is RAG, really?"

    deleted = client.delete(f"/api/curriculum/decks/{deck['id']}", headers=auth_headers)
    assert deleted.status_code == 204
    assert (
        client.get(f"/api/curriculum/decks/{deck['id']}", headers=auth_headers).status_code == 404
    )


def test_import_apkg_creates_deck_with_cards(client, auth_headers):
    apkg = build_apkg("History", [AnkiCard(front="When was 1066?", back="The Norman conquest")])
    response = client.post(
        "/api/curriculum/decks/import",
        headers=auth_headers,
        files={"file": ("history.apkg", apkg, "application/octet-stream")},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "History"
    assert body["card_count"] == 1
    assert body["source"] == "imported"

    due = client.get("/api/curriculum/review/flashcards/due", headers=auth_headers).json()
    assert any(card["front"] == "When was 1066?" for card in due)


def test_import_rejects_non_zip(client, auth_headers):
    response = client.post(
        "/api/curriculum/decks/import",
        headers=auth_headers,
        files={"file": ("bad.apkg", b"not a zip", "application/octet-stream")},
    )
    assert response.status_code == 400


def test_import_rejects_new_format_with_hint(client, auth_headers):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("collection.anki21b", b"zstd")
    response = client.post(
        "/api/curriculum/decks/import",
        headers=auth_headers,
        files={"file": ("new.apkg", buffer.getvalue(), "application/octet-stream")},
    )
    assert response.status_code == 400
    assert "older Anki versions" in response.json()["detail"]


def test_export_roundtrip(client, auth_headers):
    deck = _create_deck(client, auth_headers, title="Export Me")
    client.post(
        f"/api/curriculum/decks/{deck['id']}/cards",
        headers=auth_headers,
        json={"front": "front text", "back": "back text"},
    )
    response = client.get(f"/api/curriculum/decks/{deck['id']}/export", headers=auth_headers)
    assert response.status_code == 200
    assert "attachment" in response.headers["content-disposition"]

    reimport = client.post(
        "/api/curriculum/decks/import",
        headers=auth_headers,
        files={"file": ("export-me.apkg", response.content, "application/octet-stream")},
    )
    assert reimport.status_code == 201
    detail = client.get(
        f"/api/curriculum/decks/{reimport.json()['id']}", headers=auth_headers
    ).json()
    assert detail["cards"][0]["front"] == "front text"
    assert "back text" in detail["cards"][0]["back"]


def test_grade_flashcard_with_rating(client, auth_headers):
    deck = _create_deck(client, auth_headers)
    card = client.post(
        f"/api/curriculum/decks/{deck['id']}/cards",
        headers=auth_headers,
        json={"front": "q", "back": "a"},
    ).json()

    good = client.post(
        f"/api/curriculum/review/flashcards/{card['id']}/grade",
        headers=auth_headers,
        json={"rating": "good"},
    )
    assert good.status_code == 200
    assert good.json()["repetitions"] == 1

    due = client.get("/api/curriculum/review/flashcards/due", headers=auth_headers).json()
    assert all(c["id"] != card["id"] for c in due)

    again = client.post(
        f"/api/curriculum/review/flashcards/{card['id']}/grade",
        headers=auth_headers,
        json={"rating": "again"},
    )
    assert again.json()["repetitions"] == 0
    due = client.get("/api/curriculum/review/flashcards/due", headers=auth_headers).json()
    assert any(c["id"] == card["id"] for c in due)


def test_grade_requires_rating_or_grade(client, auth_headers):
    deck = _create_deck(client, auth_headers)
    card = client.post(
        f"/api/curriculum/decks/{deck['id']}/cards",
        headers=auth_headers,
        json={"front": "q"},
    ).json()
    response = client.post(
        f"/api/curriculum/review/flashcards/{card['id']}/grade",
        headers=auth_headers,
        json={},
    )
    assert response.status_code == 422


def test_decks_are_user_isolated(client, auth_headers, auth_headers_b):
    deck = _create_deck(client, auth_headers)
    assert (
        client.get(f"/api/curriculum/decks/{deck['id']}", headers=auth_headers_b).status_code == 404
    )
    assert (
        client.delete(f"/api/curriculum/decks/{deck['id']}", headers=auth_headers_b).status_code
        == 404
    )
    listing = client.get("/api/curriculum/decks", headers=auth_headers_b).json()
    assert all(d["id"] != deck["id"] for d in listing)


def test_review_export_returns_apkg(client, auth_headers):
    response = client.get("/api/curriculum/review/export", headers=auth_headers)
    assert response.status_code == 200
    assert response.content.startswith(b"PK")
