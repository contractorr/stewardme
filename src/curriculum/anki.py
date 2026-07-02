"""Anki .apkg import/export codec (stdlib + BeautifulSoup only).

An .apkg file is a zip archive containing an Anki SQLite collection
(``collection.anki2`` for the legacy schema, ``collection.anki21`` for the
2.1 scheduler, ``collection.anki21b`` for the newer zstd-compressed format)
plus a ``media`` JSON manifest. Import supports the two SQLite variants;
export writes a fresh ``collection.anki2`` with a single Basic notetype so
the deck opens in any Anki version.
"""

import hashlib
import io
import json
import re
import sqlite3
import tempfile
import time
import zipfile
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path

import structlog
from bs4 import BeautifulSoup

logger = structlog.get_logger()

FIELD_SEPARATOR = "\x1f"
MIN_EASINESS = 1.3
CARD_TYPE_REVIEW = 2

_SOUND_RE = re.compile(r"\[sound:[^\]]*\]")
_CLOZE_RE = re.compile(r"\{\{c(\d+)::(.*?)(?:::(.*?))?\}\}", re.DOTALL)
_FIELD_REF_RE = re.compile(r"\{\{(?:type:|hint:|text:)?([^#^/{}]+?)\}\}")
_SECTION_RE = re.compile(r"\{\{([#^])([^{}]+?)\}\}(.*?)\{\{/\2\}\}", re.DOTALL)


class AnkiFormatError(ValueError):
    """Raised when an .apkg file cannot be parsed."""


@dataclass
class AnkiCard:
    """Normalized flashcard used for both import and export."""

    front: str
    back: str = ""
    tags: list[str] = field(default_factory=list)
    guid: str = ""
    easiness_factor: float = 2.5
    interval_days: int = 1
    repetitions: int = 0
    due_at: datetime | None = None


@dataclass
class AnkiImportResult:
    deck_name: str
    cards: list[AnkiCard]
    skipped_empty: int = 0
    skipped_media: int = 0


# --- HTML → text -----------------------------------------------------------


def html_to_text(html: str) -> tuple[str, int]:
    """Flatten Anki card HTML to readable plain text.

    Returns (text, media_reference_count). ``<br>`` and block elements become
    newlines; images and ``[sound:...]`` references are dropped and counted.
    """
    media_count = len(_SOUND_RE.findall(html))
    html = _SOUND_RE.sub("", html)
    if "<" not in html:
        return html.strip(), media_count

    soup = BeautifulSoup(html, "html.parser")
    media_count += len(soup.find_all(("img", "audio", "video", "object", "embed")))
    for tag in soup.find_all(("img", "audio", "video", "object", "embed", "script", "style")):
        tag.decompose()
    for br in soup.find_all("br"):
        br.replace_with("\n")
    for block in soup.find_all(("div", "p", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6")):
        block.append("\n")
    text = soup.get_text()
    # Collapse runs of blank lines while preserving intentional breaks.
    lines = [line.strip() for line in text.split("\n")]
    cleaned: list[str] = []
    for line in lines:
        if line or (cleaned and cleaned[-1]):
            cleaned.append(line)
    return "\n".join(cleaned).strip(), media_count


# --- Template rendering (import) -------------------------------------------


def _apply_sections(template: str, fields: dict[str, str]) -> str:
    """Resolve {{#Field}}...{{/Field}} and {{^Field}}...{{/Field}} blocks."""
    while True:
        match = _SECTION_RE.search(template)
        if not match:
            return template
        kind, name, body = match.groups()
        value = fields.get(name.strip(), "")
        keep = bool(value.strip()) if kind == "#" else not value.strip()
        template = template[: match.start()] + (body if keep else "") + template[match.end() :]


def _substitute_fields(template: str, fields: dict[str, str]) -> str:
    template = template.replace("{{FrontSide}}", "")
    template = _apply_sections(template, fields)

    def _replace(match: re.Match) -> str:
        name = match.group(1).strip()
        if ":" in name:  # unknown filter chain, e.g. {{kanji:Field}}
            name = name.rsplit(":", 1)[-1].strip()
        return fields.get(name, "")

    return _FIELD_REF_RE.sub(_replace, template)


def _render_cloze(text: str, ordinal: int) -> tuple[str, str]:
    """Return (front, back) for a cloze note at the given card ordinal."""
    target = ordinal + 1

    def _front(match: re.Match) -> str:
        number = int(match.group(1))
        hint = match.group(3)
        if number == target:
            return f"[...{hint}]" if hint else "[...]"
        return match.group(2)

    def _back(match: re.Match) -> str:
        return match.group(2)

    return _CLOZE_RE.sub(_front, text), _CLOZE_RE.sub(_back, text)


# --- Import -----------------------------------------------------------------


def parse_apkg(data: bytes) -> AnkiImportResult:
    """Parse an .apkg archive into normalized cards.

    Raises:
        AnkiFormatError: if the archive or its collection cannot be read.
    """
    try:
        archive = zipfile.ZipFile(io.BytesIO(data))
        names = set(archive.namelist())
    except zipfile.BadZipFile as exc:
        raise AnkiFormatError("Not a valid .apkg file (corrupt or not a zip archive).") from exc

    member = None
    for candidate in ("collection.anki21", "collection.anki2"):
        if candidate in names:
            member = candidate
            break
    if member is None:
        if "collection.anki21b" in names:
            raise AnkiFormatError(
                "This deck uses Anki's newest export format. Re-export it from Anki "
                'with "Support older Anki versions" enabled and try again.'
            )
        raise AnkiFormatError("No Anki collection found inside the archive.")

    with tempfile.NamedTemporaryFile(suffix=".anki2") as tmp:
        tmp.write(archive.read(member))
        tmp.flush()
        conn = sqlite3.connect(tmp.name)
        try:
            return _parse_collection(conn)
        except sqlite3.DatabaseError as exc:
            raise AnkiFormatError(f"Could not read the Anki collection: {exc}") from exc
        finally:
            conn.close()


def _parse_collection(conn: sqlite3.Connection) -> AnkiImportResult:
    row = conn.execute("SELECT crt, models, decks FROM col LIMIT 1").fetchone()
    if row is None:
        raise AnkiFormatError("The Anki collection is empty.")
    crt, models_json, decks_json = row
    try:
        models = json.loads(models_json or "{}")
        decks = json.loads(decks_json or "{}")
    except json.JSONDecodeError as exc:
        raise AnkiFormatError("The Anki collection metadata is malformed.") from exc

    notes: dict[int, tuple[int, list[str], list[str], str]] = {}
    for nid, guid, mid, flds, tags in conn.execute("SELECT id, guid, mid, flds, tags FROM notes"):
        notes[nid] = (mid, flds.split(FIELD_SEPARATOR), tags.split(), guid)

    deck_card_counts: dict[int, int] = {}
    cards: list[AnkiCard] = []
    skipped_empty = 0
    skipped_media = 0

    card_rows = conn.execute(
        "SELECT nid, did, ord, type, due, ivl, factor, reps FROM cards ORDER BY id"
    ).fetchall()
    for nid, did, ordinal, ctype, due, ivl, factor, reps in card_rows:
        note = notes.get(nid)
        if note is None:
            continue
        mid, field_values, tags, guid = note
        model = models.get(str(mid), {})
        front_html, back_html = _render_note(model, field_values, ordinal)

        front, media_front = html_to_text(front_html)
        back, media_back = html_to_text(back_html)
        skipped_media += media_front + media_back
        if not front.strip():
            skipped_empty += 1
            continue

        deck_card_counts[did] = deck_card_counts.get(did, 0) + 1
        card_tags = list(tags)
        deck_name = _deck_name(decks, did)
        if deck_name and "::" in deck_name:
            card_tags.append(deck_name.split("::")[-1].strip().replace(" ", "_"))

        cards.append(
            AnkiCard(
                front=front,
                back=back,
                tags=card_tags,
                guid=guid,
                easiness_factor=max(MIN_EASINESS, factor / 1000) if factor > 0 else 2.5,
                interval_days=max(1, ivl),
                repetitions=max(0, reps),
                due_at=(
                    datetime.fromtimestamp(crt) + timedelta(days=due)
                    if ctype == CARD_TYPE_REVIEW
                    else None
                ),
            )
        )

    deck_name = "Imported deck"
    if deck_card_counts:
        main_did = max(deck_card_counts, key=lambda did: deck_card_counts[did])
        deck_name = _deck_name(decks, main_did) or deck_name
        deck_name = deck_name.split("::")[0].strip() or "Imported deck"

    return AnkiImportResult(
        deck_name=deck_name,
        cards=cards,
        skipped_empty=skipped_empty,
        skipped_media=skipped_media,
    )


def _deck_name(decks: dict, did: int) -> str:
    entry = decks.get(str(did)) or {}
    return str(entry.get("name", ""))


def _render_note(model: dict, field_values: list[str], ordinal: int) -> tuple[str, str]:
    field_names = [f.get("name", "") for f in model.get("flds", [])]
    fields = {
        name: field_values[i] if i < len(field_values) else "" for i, name in enumerate(field_names)
    }

    if model.get("type") == 1:  # cloze notetype
        text = field_values[0] if field_values else ""
        front, back = _render_cloze(text, ordinal)
        extra = field_values[1] if len(field_values) > 1 else ""
        if extra.strip():
            back = f"{back}\n{extra}"
        return front, back

    templates = model.get("tmpls", [])
    template = None
    for tmpl in templates:
        if tmpl.get("ord") == ordinal:
            template = tmpl
            break
    if template is None and templates:
        template = templates[0]

    if template:
        front = _substitute_fields(template.get("qfmt", ""), fields)
        back = _substitute_fields(template.get("afmt", ""), fields)
        if front.strip():
            return front, back

    # Fallback: Anki's first field is the front, the remaining fields form the back.
    front = field_values[0] if field_values else ""
    back = "\n".join(value for value in field_values[1:] if value.strip())
    return front, back


# --- Export -----------------------------------------------------------------

_APKG_SCHEMA = """
CREATE TABLE col (
    id integer primary key, crt integer not null, mod integer not null,
    scm integer not null, ver integer not null, dty integer not null,
    usn integer not null, ls integer not null, conf text not null,
    models text not null, decks text not null, dconf text not null,
    tags text not null
);
CREATE TABLE notes (
    id integer primary key, guid text not null, mid integer not null,
    mod integer not null, usn integer not null, tags text not null,
    flds text not null, sfld integer not null, csum integer not null,
    flags integer not null, data text not null
);
CREATE TABLE cards (
    id integer primary key, nid integer not null, did integer not null,
    ord integer not null, mod integer not null, usn integer not null,
    type integer not null, queue integer not null, due integer not null,
    ivl integer not null, factor integer not null, reps integer not null,
    lapses integer not null, left integer not null, odue integer not null,
    odid integer not null, flags integer not null, data text not null
);
CREATE TABLE revlog (
    id integer primary key, cid integer not null, usn integer not null,
    ease integer not null, ivl integer not null, lastIvl integer not null,
    factor integer not null, time integer not null, type integer not null
);
CREATE TABLE graves (usn integer not null, oid integer not null, type integer not null);
CREATE INDEX ix_notes_usn ON notes (usn);
CREATE INDEX ix_cards_usn ON cards (usn);
CREATE INDEX ix_revlog_usn ON revlog (usn);
CREATE INDEX ix_cards_nid ON cards (nid);
CREATE INDEX ix_cards_sched ON cards (did, queue, due);
CREATE INDEX ix_revlog_cid ON revlog (cid);
CREATE INDEX ix_notes_csum ON notes (csum);
"""

_CARD_CSS = (
    ".card { font-family: arial; font-size: 20px; text-align: center; "
    "color: black; background-color: white; }"
)
_LATEX_PRE = (
    "\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n"
    "\\usepackage[utf8]{inputenc}\n\\usepackage{amssymb,amsmath}\n"
    "\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n"
)


def _guid_for(seed: str) -> str:
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    return digest[:10]


def _checksum(text: str) -> int:
    return int(hashlib.sha1(text.encode("utf-8")).hexdigest()[:8], 16)


def _text_to_html(text: str) -> str:
    from html import escape

    return escape(text).replace("\n", "<br>")


def build_apkg(deck_name: str, cards: list[AnkiCard]) -> bytes:
    """Build an .apkg archive containing the given cards as new cards."""
    now = int(time.time())
    now_ms = now * 1000
    model_id = now_ms
    deck_id = now_ms + 1

    model = {
        "id": model_id,
        "name": "Basic",
        "type": 0,
        "mod": now,
        "usn": -1,
        "sortf": 0,
        "did": deck_id,
        "tmpls": [
            {
                "name": "Card 1",
                "ord": 0,
                "qfmt": "{{Front}}",
                "afmt": '{{FrontSide}}<hr id="answer">{{Back}}',
                "bqfmt": "",
                "bafmt": "",
                "did": None,
                "bfont": "",
                "bsize": 0,
            }
        ],
        "flds": [
            {
                "name": "Front",
                "ord": 0,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "Back",
                "ord": 1,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
        ],
        "css": _CARD_CSS,
        "latexPre": _LATEX_PRE,
        "latexPost": "\\end{document}",
        "latexsvg": False,
        "req": [[0, "any", [0]]],
        "vers": [],
        "tags": [],
    }
    deck = {
        "id": deck_id,
        "name": deck_name or "Exported deck",
        "mod": now,
        "usn": -1,
        "lrnToday": [0, 0],
        "revToday": [0, 0],
        "newToday": [0, 0],
        "timeToday": [0, 0],
        "collapsed": False,
        "browserCollapsed": False,
        "desc": "",
        "dyn": 0,
        "conf": 1,
        "extendNew": 0,
        "extendRev": 0,
    }
    default_deck = dict(deck, id=1, name="Default", conf=1)
    dconf = {
        "1": {
            "id": 1,
            "name": "Default",
            "replayq": True,
            "timer": 0,
            "maxTaken": 60,
            "usn": -1,
            "mod": 0,
            "autoplay": True,
            "lapse": {"leechFails": 8, "minInt": 1, "delays": [10], "leechAction": 0, "mult": 0},
            "rev": {
                "perDay": 100,
                "fuzz": 0.05,
                "ivlFct": 1,
                "maxIvl": 36500,
                "ease4": 1.3,
                "bury": True,
                "minSpace": 1,
            },
            "new": {
                "perDay": 20,
                "delays": [1, 10],
                "separate": True,
                "ints": [1, 4, 7],
                "initialFactor": 2500,
                "bury": True,
                "order": 1,
            },
        }
    }
    conf = {
        "nextPos": 1,
        "estTimes": True,
        "activeDecks": [1],
        "sortType": "noteFld",
        "timeLim": 0,
        "sortBackwards": False,
        "addToCur": True,
        "curDeck": 1,
        "newBury": True,
        "newSpread": 0,
        "dueCounts": True,
        "curModel": str(model_id),
        "collapseTime": 1200,
    }

    with tempfile.NamedTemporaryFile(suffix=".anki2", delete=False) as tmp:
        db_path = Path(tmp.name)
    try:
        conn = sqlite3.connect(str(db_path))
        try:
            conn.executescript(_APKG_SCHEMA)
            conn.execute(
                "INSERT INTO col VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    1,
                    now,
                    now_ms,
                    now_ms,
                    11,
                    0,
                    0,
                    0,
                    json.dumps(conf),
                    json.dumps({str(model_id): model}),
                    json.dumps({"1": default_deck, str(deck_id): deck}),
                    json.dumps(dconf),
                    "{}",
                ),
            )
            for index, card in enumerate(cards):
                note_id = now_ms + 2 + index * 2
                card_id = note_id + 1
                front_html = _text_to_html(card.front)
                back_html = _text_to_html(card.back)
                fields = f"{front_html}{FIELD_SEPARATOR}{back_html}"
                guid = card.guid or _guid_for(f"{deck_name}:{card.front}:{card.back}")
                tags = " ".join(tag.replace(" ", "_") for tag in card.tags)
                if tags:
                    tags = f" {tags} "
                conn.execute(
                    "INSERT INTO notes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        note_id,
                        guid,
                        model_id,
                        now,
                        -1,
                        tags,
                        fields,
                        card.front,
                        _checksum(front_html),
                        0,
                        "",
                    ),
                )
                conn.execute(
                    "INSERT INTO cards VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        card_id,
                        note_id,
                        deck_id,
                        0,
                        now,
                        -1,
                        0,
                        0,
                        index,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        "",
                    ),
                )
            conn.commit()
        finally:
            conn.close()

        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.write(db_path, "collection.anki2")
            archive.writestr("media", "{}")
        return buffer.getvalue()
    finally:
        db_path.unlink(missing_ok=True)
