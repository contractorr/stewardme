"""SQLite persistence for flashcard decks (Anki import/export + SM-2 review)."""

import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path

import structlog

from db import ensure_schema_version, wal_connect

from .models import Deck, DeckSource, Flashcard
from .spaced_repetition import sm2_update

logger = structlog.get_logger()

FLASHCARD_SCHEMA_VERSION = 8


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


class FlashcardStore:
    """Deck + flashcard persistence in the per-user curriculum DB file."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with wal_connect(self.db_path) as conn:
            create_flashcard_tables(conn)
            ensure_schema_version(conn, FLASHCARD_SCHEMA_VERSION)
            conn.commit()

    # --- Decks ---

    def create_deck(
        self,
        user_id: str,
        title: str,
        description: str = "",
        source: str = "created",
        anki_deck_id: int | None = None,
    ) -> Deck:
        deck_id = uuid.uuid4().hex
        now = datetime.utcnow().isoformat()
        with wal_connect(self.db_path) as conn:
            conn.execute(
                """INSERT INTO decks (id, user_id, title, description, source, anki_deck_id, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (deck_id, user_id, title, description, source, anki_deck_id, now),
            )
            conn.commit()
        return Deck(
            id=deck_id,
            user_id=user_id,
            title=title,
            description=description,
            source=DeckSource(source),
            anki_deck_id=anki_deck_id,
            created_at=_parse_dt(now),
        )

    def list_decks(self, user_id: str) -> list[Deck]:
        now = datetime.utcnow().isoformat()
        with wal_connect(self.db_path, row_factory=True) as conn:
            rows = conn.execute(
                """SELECT d.*,
                       (SELECT COUNT(*) FROM flashcards f
                        WHERE f.deck_id = d.id AND f.user_id = d.user_id) AS card_count,
                       (SELECT COUNT(*) FROM flashcards f
                        WHERE f.deck_id = d.id AND f.user_id = d.user_id
                        AND (f.next_review IS NULL OR f.next_review <= ?)) AS due_count
                   FROM decks d WHERE d.user_id = ?
                   ORDER BY d.created_at DESC""",
                (now, user_id),
            ).fetchall()
            return [self._row_to_deck(dict(row)) for row in rows]

    def get_deck(self, user_id: str, deck_id: str) -> Deck | None:
        now = datetime.utcnow().isoformat()
        with wal_connect(self.db_path, row_factory=True) as conn:
            row = conn.execute(
                """SELECT d.*,
                       (SELECT COUNT(*) FROM flashcards f
                        WHERE f.deck_id = d.id AND f.user_id = d.user_id) AS card_count,
                       (SELECT COUNT(*) FROM flashcards f
                        WHERE f.deck_id = d.id AND f.user_id = d.user_id
                        AND (f.next_review IS NULL OR f.next_review <= ?)) AS due_count
                   FROM decks d WHERE d.user_id = ? AND d.id = ?""",
                (now, user_id, deck_id),
            ).fetchone()
            return self._row_to_deck(dict(row)) if row else None

    def delete_deck(self, user_id: str, deck_id: str) -> bool:
        with wal_connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM decks WHERE user_id = ? AND id = ?", (user_id, deck_id)
            )
            if cursor.rowcount == 0:
                return False
            conn.execute(
                "DELETE FROM flashcards WHERE user_id = ? AND deck_id = ?", (user_id, deck_id)
            )
            conn.commit()
            return True

    # --- Cards ---

    def add_card(
        self,
        user_id: str,
        deck_id: str,
        front: str,
        back: str = "",
        tags: list[str] | None = None,
        *,
        easiness_factor: float = 2.5,
        interval_days: int = 1,
        repetitions: int = 0,
        next_review: datetime | None = None,
        anki_note_guid: str = "",
    ) -> Flashcard:
        card_id = uuid.uuid4().hex
        now = datetime.utcnow()
        due = next_review if next_review is not None else now
        with wal_connect(self.db_path) as conn:
            conn.execute(
                """INSERT INTO flashcards
                   (id, deck_id, user_id, front, back, tags, anki_note_guid,
                    easiness_factor, interval_days, repetitions, next_review, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    card_id,
                    deck_id,
                    user_id,
                    front,
                    back,
                    json.dumps(tags or []),
                    anki_note_guid,
                    max(1.3, easiness_factor),
                    max(1, interval_days),
                    max(0, repetitions),
                    due.isoformat(),
                    now.isoformat(),
                ),
            )
            conn.commit()
        return Flashcard(
            id=card_id,
            deck_id=deck_id,
            user_id=user_id,
            front=front,
            back=back,
            tags=tags or [],
            anki_note_guid=anki_note_guid,
            easiness_factor=max(1.3, easiness_factor),
            interval_days=max(1, interval_days),
            repetitions=max(0, repetitions),
            next_review=due,
            created_at=now,
        )

    def add_cards_bulk(self, user_id: str, deck_id: str, cards: list[dict]) -> int:
        """Insert many cards at once (used by .apkg import)."""
        now = datetime.utcnow()
        rows = []
        for card in cards:
            due = card.get("next_review") or now
            rows.append(
                (
                    uuid.uuid4().hex,
                    deck_id,
                    user_id,
                    card.get("front", ""),
                    card.get("back", ""),
                    json.dumps(card.get("tags") or []),
                    card.get("anki_note_guid", ""),
                    max(1.3, float(card.get("easiness_factor", 2.5))),
                    max(1, int(card.get("interval_days", 1))),
                    max(0, int(card.get("repetitions", 0))),
                    due.isoformat(),
                    now.isoformat(),
                )
            )
        with wal_connect(self.db_path) as conn:
            conn.executemany(
                """INSERT INTO flashcards
                   (id, deck_id, user_id, front, back, tags, anki_note_guid,
                    easiness_factor, interval_days, repetitions, next_review, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                rows,
            )
            conn.commit()
        return len(rows)

    def update_card(
        self,
        user_id: str,
        card_id: str,
        front: str | None = None,
        back: str | None = None,
    ) -> Flashcard | None:
        with wal_connect(self.db_path) as conn:
            if front is not None:
                conn.execute(
                    "UPDATE flashcards SET front = ? WHERE user_id = ? AND id = ?",
                    (front, user_id, card_id),
                )
            if back is not None:
                conn.execute(
                    "UPDATE flashcards SET back = ? WHERE user_id = ? AND id = ?",
                    (back, user_id, card_id),
                )
            conn.commit()
        return self.get_card(user_id, card_id)

    def delete_card(self, user_id: str, card_id: str) -> bool:
        with wal_connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM flashcards WHERE user_id = ? AND id = ?", (user_id, card_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    def get_card(self, user_id: str, card_id: str) -> Flashcard | None:
        with wal_connect(self.db_path, row_factory=True) as conn:
            row = conn.execute(
                "SELECT * FROM flashcards WHERE user_id = ? AND id = ?", (user_id, card_id)
            ).fetchone()
            return self._row_to_card(dict(row)) if row else None

    def list_cards(
        self, user_id: str, deck_id: str, limit: int = 500, offset: int = 0
    ) -> list[Flashcard]:
        with wal_connect(self.db_path, row_factory=True) as conn:
            rows = conn.execute(
                """SELECT * FROM flashcards WHERE user_id = ? AND deck_id = ?
                   ORDER BY created_at ASC, id ASC LIMIT ? OFFSET ?""",
                (user_id, deck_id, limit, offset),
            ).fetchall()
            return [self._row_to_card(dict(row)) for row in rows]

    # --- Review ---

    def get_due_cards(
        self, user_id: str, limit: int = 20, deck_id: str | None = None
    ) -> list[Flashcard]:
        now = datetime.utcnow().isoformat()
        params: list[object] = [user_id, now]
        query = """SELECT * FROM flashcards
                   WHERE user_id = ? AND (next_review IS NULL OR next_review <= ?)"""
        if deck_id:
            query += " AND deck_id = ?"
            params.append(deck_id)
        query += """ ORDER BY
                     CASE WHEN next_review IS NULL THEN 0 ELSE 1 END,
                     next_review ASC, created_at ASC LIMIT ?"""
        params.append(limit)
        with wal_connect(self.db_path, row_factory=True) as conn:
            rows = conn.execute(query, tuple(params)).fetchall()
            return [self._row_to_card(dict(row)) for row in rows]

    def count_due(self, user_id: str) -> int:
        now = datetime.utcnow().isoformat()
        with wal_connect(self.db_path) as conn:
            row = conn.execute(
                """SELECT COUNT(*) FROM flashcards
                   WHERE user_id = ? AND (next_review IS NULL OR next_review <= ?)""",
                (user_id, now),
            ).fetchone()
            return int(row[0])

    def grade_card(self, user_id: str, card_id: str, grade: int) -> Flashcard | None:
        card = self.get_card(user_id, card_id)
        if card is None:
            return None
        result = sm2_update(
            easiness_factor=card.easiness_factor,
            interval_days=card.interval_days,
            repetitions=card.repetitions,
            grade=grade,
        )
        now = datetime.utcnow()
        if grade < 3:
            next_review = now  # failed cards stay due immediately
        else:
            next_review = now + timedelta(days=result.interval_days)
        with wal_connect(self.db_path) as conn:
            conn.execute(
                """UPDATE flashcards SET easiness_factor = ?, interval_days = ?,
                   repetitions = ?, next_review = ?, last_reviewed = ?
                   WHERE user_id = ? AND id = ?""",
                (
                    result.easiness_factor,
                    result.interval_days,
                    result.repetitions,
                    next_review.isoformat(),
                    now.isoformat(),
                    user_id,
                    card_id,
                ),
            )
            conn.commit()
        return self.get_card(user_id, card_id)

    # --- Row mapping ---

    @staticmethod
    def _row_to_deck(row: dict) -> Deck:
        return Deck(
            id=row["id"],
            user_id=row["user_id"],
            title=row["title"],
            description=row.get("description", ""),
            source=DeckSource(row.get("source", "created")),
            anki_deck_id=row.get("anki_deck_id"),
            card_count=row.get("card_count", 0),
            due_count=row.get("due_count", 0),
            created_at=_parse_dt(row.get("created_at")),
        )

    @staticmethod
    def _row_to_card(row: dict) -> Flashcard:
        try:
            tags = json.loads(row.get("tags") or "[]")
        except json.JSONDecodeError:
            tags = []
        return Flashcard(
            id=row["id"],
            deck_id=row["deck_id"],
            user_id=row["user_id"],
            front=row["front"],
            back=row.get("back", ""),
            tags=tags,
            anki_note_guid=row.get("anki_note_guid", ""),
            easiness_factor=row.get("easiness_factor", 2.5),
            interval_days=row.get("interval_days", 1),
            repetitions=row.get("repetitions", 0),
            next_review=_parse_dt(row.get("next_review")),
            last_reviewed=_parse_dt(row.get("last_reviewed")),
            created_at=_parse_dt(row.get("created_at")),
        )


def create_flashcard_tables(conn) -> None:
    """Create deck/flashcard tables (shared with CurriculumStore's v8 migration)."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS decks (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            source TEXT NOT NULL DEFAULT 'created',
            anki_deck_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS flashcards (
            id TEXT PRIMARY KEY,
            deck_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            front TEXT NOT NULL,
            back TEXT NOT NULL DEFAULT '',
            tags TEXT NOT NULL DEFAULT '[]',
            anki_note_guid TEXT NOT NULL DEFAULT '',
            easiness_factor REAL NOT NULL DEFAULT 2.5,
            interval_days INTEGER NOT NULL DEFAULT 1,
            repetitions INTEGER NOT NULL DEFAULT 0,
            next_review TIMESTAMP,
            last_reviewed TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (deck_id) REFERENCES decks(id)
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_flashcards_deck ON flashcards(user_id, deck_id)")
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_flashcards_due ON flashcards(user_id, next_review)"
    )
