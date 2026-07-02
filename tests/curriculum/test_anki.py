"""Tests for the Anki .apkg codec."""

import io
import json
import sqlite3
import tempfile
import zipfile
from datetime import datetime, timedelta

import pytest

from curriculum.anki import (
    AnkiCard,
    AnkiFormatError,
    build_apkg,
    html_to_text,
    parse_apkg,
)


def _make_collection_bytes(notes, cards, models=None, decks=None, crt=None):
    """Build a minimal collection.anki2 SQLite file and return its bytes."""
    if crt is None:
        crt = int(datetime(2024, 1, 1).timestamp())
    if models is None:
        models = {
            "1000": {
                "id": 1000,
                "name": "Basic",
                "type": 0,
                "flds": [{"name": "Front", "ord": 0}, {"name": "Back", "ord": 1}],
                "tmpls": [
                    {
                        "name": "Card 1",
                        "ord": 0,
                        "qfmt": "{{Front}}",
                        "afmt": '{{FrontSide}}<hr id="answer">{{Back}}',
                    }
                ],
            }
        }
    if decks is None:
        decks = {
            "1": {"id": 1, "name": "Default"},
            "2000": {"id": 2000, "name": "Spanish Vocabulary"},
        }

    with tempfile.NamedTemporaryFile(suffix=".anki2", delete=False) as tmp:
        path = tmp.name
    conn = sqlite3.connect(path)
    conn.executescript("""
        CREATE TABLE col (id, crt, mod, scm, ver, dty, usn, ls,
                          conf, models, decks, dconf, tags);
        CREATE TABLE notes (id, guid, mid, mod, usn, tags, flds, sfld, csum, flags, data);
        CREATE TABLE cards (id, nid, did, ord, mod, usn, type, queue, due,
                            ivl, factor, reps, lapses, left, odue, odid, flags, data);
    """)
    conn.execute(
        "INSERT INTO col VALUES (1, ?, 0, 0, 11, 0, 0, 0, '{}', ?, ?, '{}', '{}')",
        (crt, json.dumps(models), json.dumps(decks)),
    )
    for note in notes:
        conn.execute(
            "INSERT INTO notes VALUES (?, ?, ?, 0, -1, ?, ?, '', 0, 0, '')",
            (
                note["id"],
                note.get("guid", f"g{note['id']}"),
                note.get("mid", 1000),
                note.get("tags", ""),
                note["flds"],
            ),
        )
    for card in cards:
        conn.execute(
            "INSERT INTO cards VALUES (?, ?, ?, ?, 0, -1, ?, 0, ?, ?, ?, ?, 0, 0, 0, 0, 0, '')",
            (
                card["id"],
                card["nid"],
                card.get("did", 2000),
                card.get("ord", 0),
                card.get("type", 0),
                card.get("due", 0),
                card.get("ivl", 0),
                card.get("factor", 0),
                card.get("reps", 0),
            ),
        )
    conn.commit()
    conn.close()
    data = open(path, "rb").read()
    import os

    os.unlink(path)
    return data


def _make_apkg(notes, cards, member="collection.anki2", **kwargs):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr(member, _make_collection_bytes(notes, cards, **kwargs))
        archive.writestr("media", "{}")
    return buffer.getvalue()


# --- html_to_text ---


def test_html_to_text_plain_passthrough():
    text, media = html_to_text("hello world")
    assert text == "hello world"
    assert media == 0


def test_html_to_text_flattens_markup_and_counts_media():
    html = '<div>What is <b>gravity</b>?<br>See <img src="pic.jpg"> [sound:audio.mp3]</div>'
    text, media = html_to_text(html)
    assert "gravity" in text
    assert "img" not in text
    assert media == 2


def test_html_to_text_list_items_become_lines():
    text, _ = html_to_text("<ul><li>one</li><li>two</li></ul>")
    assert "one" in text.splitlines()[0]
    assert any("two" in line for line in text.splitlines())


# --- import ---


def test_parse_apkg_basic_roundtrip_fields():
    apkg = _make_apkg(
        notes=[{"id": 1, "flds": "hola\x1fhello", "tags": "vocab"}],
        cards=[{"id": 10, "nid": 1}],
    )
    result = parse_apkg(apkg)
    assert result.deck_name == "Spanish Vocabulary"
    assert len(result.cards) == 1
    card = result.cards[0]
    assert card.front == "hola"
    assert card.back.endswith("hello")
    assert "vocab" in card.tags


def test_parse_apkg_preserves_scheduling_state():
    crt = int(datetime(2024, 1, 1).timestamp())
    apkg = _make_apkg(
        notes=[{"id": 1, "flds": "q\x1fa"}],
        cards=[{"id": 10, "nid": 1, "type": 2, "due": 400, "ivl": 30, "factor": 2100, "reps": 7}],
        crt=crt,
    )
    card = parse_apkg(apkg).cards[0]
    assert card.easiness_factor == pytest.approx(2.1)
    assert card.interval_days == 30
    assert card.repetitions == 7
    assert card.due_at == datetime.fromtimestamp(crt) + timedelta(days=400)


def test_parse_apkg_new_cards_have_no_due_date_and_default_ease():
    apkg = _make_apkg(
        notes=[{"id": 1, "flds": "q\x1fa"}],
        cards=[{"id": 10, "nid": 1, "type": 0, "factor": 0, "ivl": 0}],
    )
    card = parse_apkg(apkg).cards[0]
    assert card.due_at is None
    assert card.easiness_factor == 2.5
    assert card.interval_days == 1


def test_parse_apkg_skips_empty_fronts():
    apkg = _make_apkg(
        notes=[{"id": 1, "flds": "\x1fonly back"}, {"id": 2, "flds": "front\x1fback"}],
        cards=[{"id": 10, "nid": 1}, {"id": 11, "nid": 2}],
    )
    result = parse_apkg(apkg)
    assert len(result.cards) == 1
    assert result.skipped_empty == 1


def test_parse_apkg_cloze_cards():
    models = {
        "3000": {
            "id": 3000,
            "name": "Cloze",
            "type": 1,
            "flds": [{"name": "Text", "ord": 0}, {"name": "Extra", "ord": 1}],
            "tmpls": [
                {"name": "Cloze", "ord": 0, "qfmt": "{{cloze:Text}}", "afmt": "{{cloze:Text}}"}
            ],
        }
    }
    apkg = _make_apkg(
        notes=[{"id": 1, "mid": 3000, "flds": "The capital of France is {{c1::Paris}}.\x1f"}],
        cards=[{"id": 10, "nid": 1, "ord": 0}],
        models=models,
    )
    card = parse_apkg(apkg).cards[0]
    assert "[...]" in card.front
    assert "Paris" not in card.front
    assert "Paris" in card.back


def test_parse_apkg_rejects_garbage():
    with pytest.raises(AnkiFormatError):
        parse_apkg(b"definitely not a zip file")


def test_parse_apkg_rejects_new_format_with_hint():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("collection.anki21b", b"zstd-compressed")
    with pytest.raises(AnkiFormatError, match="older Anki versions"):
        parse_apkg(buffer.getvalue())


def test_parse_apkg_rejects_zip_without_collection():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("random.txt", "nope")
    with pytest.raises(AnkiFormatError, match="No Anki collection"):
        parse_apkg(buffer.getvalue())


def test_parse_apkg_prefers_anki21_member():
    apkg = _make_apkg(
        notes=[{"id": 1, "flds": "q21\x1fa"}],
        cards=[{"id": 10, "nid": 1}],
        member="collection.anki21",
    )
    assert parse_apkg(apkg).cards[0].front == "q21"


# --- export + roundtrip ---


def test_build_apkg_roundtrips_through_parse():
    cards = [
        AnkiCard(front="What is SM-2?", back="A spaced repetition algorithm", tags=["srs"]),
        AnkiCard(front="Line one\nLine two", back=""),
    ]
    apkg = build_apkg("My Deck", cards)
    result = parse_apkg(apkg)
    assert result.deck_name == "My Deck"
    assert len(result.cards) == 2
    fronts = {card.front for card in result.cards}
    assert "What is SM-2?" in fronts
    assert any("Line one" in front and "Line two" in front for front in fronts)
    backs = {card.back for card in result.cards}
    assert any("spaced repetition algorithm" in back for back in backs)


def test_build_apkg_empty_deck_is_valid():
    result = parse_apkg(build_apkg("Empty", []))
    assert result.cards == []


def test_build_apkg_collection_passes_anki_schema_smoke_check():
    apkg = build_apkg("Deck", [AnkiCard(front="q", back="a")])
    with zipfile.ZipFile(io.BytesIO(apkg)) as archive:
        assert "collection.anki2" in archive.namelist()
        assert json.loads(archive.read("media")) == {}
        with tempfile.NamedTemporaryFile(suffix=".anki2") as tmp:
            tmp.write(archive.read("collection.anki2"))
            tmp.flush()
            conn = sqlite3.connect(tmp.name)
            ver = conn.execute("SELECT ver FROM col").fetchone()[0]
            models = json.loads(conn.execute("SELECT models FROM col").fetchone()[0])
            note_count = conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
            card_count = conn.execute("SELECT COUNT(*) FROM cards").fetchone()[0]
            conn.close()
    assert ver == 11
    assert note_count == 1
    assert card_count == 1
    model = next(iter(models.values()))
    assert [f["name"] for f in model["flds"]] == ["Front", "Back"]
