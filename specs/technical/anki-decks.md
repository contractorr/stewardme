---
id: anki-decks
category: tracked_module
status: experimental
implements:
- anki-decks
code_paths:
- src/curriculum/anki.py
- src/curriculum/flashcards.py
- src/web/routes/decks.py
- web/src/app/(dashboard)/learn/decks
- tests/curriculum/test_anki.py
- tests/curriculum/test_flashcards.py
- tests/web/test_deck_routes.py
last_reviewed: '2026-07-02'
---

# Anki Decks — Technical Spec

## Overview

Flashcard decks with Anki `.apkg` import/export, reviewed through the existing SM-2 engine
(`curriculum/spaced_repetition.py`). Decks and cards live in the per-user `curriculum.db`
alongside chapter review items, but in their own tables so the guide-joined review queries are
untouched. A dedicated flashcard queue is merged with the chapter review count at the API layer.

## Dependencies

**Depends on:** `curriculum.spaced_repetition`, `curriculum.store` (shared DB file + `db.wal_connect`),
`beautifulsoup4` (HTML → text), stdlib `zipfile`/`sqlite3`/`json`.
**Depended on by:** `web.routes.decks`.

## Data Model (curriculum.db, schema v8)

```sql
CREATE TABLE decks (
    id TEXT PRIMARY KEY,            -- uuid4 hex
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    source TEXT NOT NULL DEFAULT 'created',   -- 'created' | 'imported'
    anki_deck_id INTEGER,           -- original Anki deck id when imported
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE flashcards (
    id TEXT PRIMARY KEY,            -- uuid4 hex
    deck_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    front TEXT NOT NULL,
    back TEXT NOT NULL DEFAULT '',
    tags TEXT NOT NULL DEFAULT '[]',           -- JSON list
    anki_note_guid TEXT NOT NULL DEFAULT '',
    easiness_factor REAL NOT NULL DEFAULT 2.5,
    interval_days INTEGER NOT NULL DEFAULT 1,
    repetitions INTEGER NOT NULL DEFAULT 0,
    next_review TIMESTAMP,          -- NULL/past ⇒ due
    last_reviewed TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (deck_id) REFERENCES decks(id)
);
CREATE INDEX idx_flashcards_deck ON flashcards(user_id, deck_id);
CREATE INDEX idx_flashcards_due ON flashcards(user_id, next_review);
```

Migration lives in `CurriculumStore._init_db` (v7 → v8, `CREATE TABLE IF NOT EXISTS`).

## Components

### `curriculum/flashcards.py` — `FlashcardStore`

Wraps the same DB file as `CurriculumStore` (constructed with the identical path).

```python
class FlashcardStore:
    def __init__(self, db_path: str | Path): ...
    def create_deck(self, user_id, title, description="", source="created", anki_deck_id=None) -> Deck
    def list_decks(self, user_id) -> list[Deck]            # includes card_count, due_count
    def get_deck(self, user_id, deck_id) -> Deck | None
    def delete_deck(self, user_id, deck_id) -> bool        # cascades to flashcards
    def add_card(self, user_id, deck_id, front, back, tags=None, *,
                 easiness_factor=2.5, interval_days=1, repetitions=0,
                 next_review=None, anki_note_guid="") -> Flashcard
    def add_cards_bulk(self, user_id, deck_id, cards: list[dict]) -> int
    def update_card(self, user_id, card_id, front=None, back=None) -> Flashcard | None
    def delete_card(self, user_id, card_id) -> bool
    def list_cards(self, user_id, deck_id, limit=500, offset=0) -> list[Flashcard]
    def get_due_cards(self, user_id, limit=20, deck_id=None) -> list[Flashcard]
    def count_due(self, user_id) -> int
    def grade_card(self, user_id, card_id, grade: int) -> Flashcard | None  # sm2_update + reschedule
```

Pydantic models `Deck` and `Flashcard` in `curriculum/models.py`. Grade mapping for
Anki-style buttons happens at the route layer: `again=1, hard=3, good=4, easy=5`.
`grade_card` sets `next_review = now + interval_days` on success and `now` (due immediately)
on failure (`grade < 3`), mirroring `store.grade_review` semantics.

### `curriculum/anki.py` — apkg codec (pure functions, stdlib only)

```python
@dataclass
class AnkiCard:      # normalized import/export unit
    front: str
    back: str
    tags: list[str]
    guid: str = ""
    easiness_factor: float = 2.5
    interval_days: int = 1
    repetitions: int = 0
    due_at: datetime | None = None

@dataclass
class AnkiImportResult:
    deck_name: str
    cards: list[AnkiCard]
    skipped_empty: int
    skipped_media: int

def parse_apkg(data: bytes) -> AnkiImportResult      # raises AnkiFormatError
def build_apkg(deck_name: str, cards: list[AnkiCard]) -> bytes
```

**Import:** open zip in memory; prefer `collection.anki21`, fall back to `collection.anki2`;
if only `collection.anki21b` exists raise `AnkiFormatError` with the re-export hint. Copy the
member to a temp file and open with `sqlite3`. Read `col` (models/decks JSON, `crt`), `notes`
(fields split on `\x1f`), `cards`. Per card: substitute `{{Field}}` into the notetype's
`qfmt`/`afmt` (strip `{{FrontSide}}`, conditionals, and `{{cloze:...}}` handled by blanking
`{{c1::...}}` spans on the front and revealing on the back); HTML → text via BeautifulSoup
(`<br>`/`<div>`/`<li>` become newlines); `[sound:...]`/`<img>` references dropped and counted.
Scheduling: `easiness_factor = max(1.3, factor/1000)` when `factor > 0`; `interval_days =
max(1, ivl)` (negative learning-step ivl ⇒ 1); `repetitions = reps`; `due_at` from `crt +
due*86400` for review cards (`type == 2`), otherwise `None` (due now). Only the first card
per note per template ordinal is kept for cloze notes with multiple ordinals — each ordinal
becomes its own flashcard.

**Export:** writes a fresh `collection.anki2` (Anki schema 11: `col`, `notes`, `cards`,
`revlog`, `graves` + indexes) with one Basic notetype (Front/Back) and one deck, zips it with
an empty `media` manifest (`{}`). IDs are epoch-ms-based and deterministic per call ordering;
`guid` reuses the stored `anki_note_guid` or derives one from the card id so re-imports into
Anki dedupe. Cards export as new (queue/type 0, due = ordinal).

### `web/routes/decks.py`

`router = APIRouter(prefix="/api/curriculum", tags=["decks"])`, all endpoints
`Depends(get_current_user)`, store built per request from `get_user_paths(user_id)["data_dir"]
/ "curriculum.db"`.

| Endpoint | Behavior |
| --- | --- |
| `GET /decks` | list decks with counts |
| `POST /decks` | create deck (`DeckCreate`: title 1..200, description ≤ 2000) |
| `GET /decks/{deck_id}` | deck + first 500 cards |
| `DELETE /decks/{deck_id}` | delete deck + cards, 404 if not owner |
| `POST /decks/import` | multipart `.apkg` (≤ 50 MB); validates zip magic `PK`; 400 on parse errors with `AnkiFormatError` message |
| `GET /decks/{deck_id}/export` | `Response` with `application/apkg` bytes + `Content-Disposition` |
| `POST /decks/{deck_id}/cards` | add card (`FlashcardCreate`: front 1..4000, back ≤ 4000) |
| `PATCH /decks/{deck_id}/cards/{card_id}` | edit front/back |
| `DELETE /decks/{deck_id}/cards/{card_id}` | delete card |
| `GET /review/flashcards/due` | due cards (limit ≤ 50, optional `deck_id`) |
| `POST /review/flashcards/{card_id}/grade` | body `{"rating": "again\|hard\|good\|easy"}` or `{"grade": 0..5}` |
| `GET /review/export` | user's chapter `review_items` (quiz/teachback) as `.apkg` |

Registered in `web/routes/__init__.py` `ROUTERS`.

## Error Paths

- Corrupt zip / missing collection member / undecodable DB → `AnkiFormatError` → HTTP 400.
- `collection.anki21b`-only export → 400 with re-export guidance.
- Oversized upload (> 50 MB) → 413.
- Cross-user deck/card access → 404 (never 403, matching library convention).
- Grade outside 0–5 or unknown rating → 422 (Pydantic validation).

## Frontend

- `web/src/app/(dashboard)/learn/decks/page.tsx` — deck list, import (file input → FormData),
  create, export (blob download), delete.
- `web/src/app/(dashboard)/learn/decks/review/page.tsx` — flashcard session: front → reveal →
  Again/Hard/Good/Easy, per-session cap 20.
- Types in `web/src/types/decks.ts`; Learn page gains a compact Flashcards card when decks exist.

## Validation

```
uv run pytest tests/curriculum/test_anki.py tests/curriculum/test_flashcards.py tests/web/test_deck_routes.py -q
```
