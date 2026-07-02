"""Flashcard deck routes — Anki .apkg import/export + SM-2 flashcard review."""

from pathlib import Path
from typing import Literal

import structlog
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from fastapi.responses import Response
from pydantic import BaseModel, Field

from curriculum.anki import AnkiCard, AnkiFormatError, build_apkg, parse_apkg
from curriculum.flashcards import FlashcardStore
from curriculum.models import Deck, Flashcard
from curriculum.store import CurriculumStore
from web.auth import get_current_user
from web.deps import get_user_paths
from web.user_store import log_event

logger = structlog.get_logger()
router = APIRouter(prefix="/api/curriculum", tags=["decks"])

MAX_APKG_BYTES = 50 * 1024 * 1024

RATING_TO_GRADE = {"again": 1, "hard": 3, "good": 4, "easy": 5}


# --- Request/response schemas (route-local; web/models.py is a guarded hotspot) ---


class DeckCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)


class FlashcardCreate(BaseModel):
    front: str = Field(..., min_length=1, max_length=4000)
    back: str = Field(default="", max_length=4000)
    tags: list[str] = Field(default_factory=list)


class FlashcardUpdate(BaseModel):
    front: str | None = Field(None, min_length=1, max_length=4000)
    back: str | None = Field(None, max_length=4000)


class FlashcardGradeRequest(BaseModel):
    rating: Literal["again", "hard", "good", "easy"] | None = None
    grade: int | None = Field(None, ge=0, le=5)


class FlashcardResponse(BaseModel):
    id: str
    deck_id: str = ""
    front: str = ""
    back: str = ""
    tags: list[str] = Field(default_factory=list)
    easiness_factor: float = 2.5
    interval_days: int = 1
    repetitions: int = 0
    next_review: str | None = None
    last_reviewed: str | None = None
    created_at: str | None = None


class DeckResponse(BaseModel):
    id: str
    title: str = ""
    description: str = ""
    source: str = "created"
    card_count: int = 0
    due_count: int = 0
    created_at: str | None = None


class DeckDetailResponse(DeckResponse):
    cards: list[FlashcardResponse] = Field(default_factory=list)


class DeckImportResponse(DeckResponse):
    skipped_empty: int = 0
    skipped_media: int = 0


def _db_path(user_id: str) -> Path:
    paths = get_user_paths(user_id)
    return Path(paths["data_dir"]) / "curriculum.db"


def _get_store(user_id: str) -> FlashcardStore:
    return FlashcardStore(_db_path(user_id))


def _shape_card(card: Flashcard) -> FlashcardResponse:
    return FlashcardResponse(
        id=card.id,
        deck_id=card.deck_id,
        front=card.front,
        back=card.back,
        tags=card.tags,
        easiness_factor=card.easiness_factor,
        interval_days=card.interval_days,
        repetitions=card.repetitions,
        next_review=card.next_review.isoformat() if card.next_review else None,
        last_reviewed=card.last_reviewed.isoformat() if card.last_reviewed else None,
        created_at=card.created_at.isoformat() if card.created_at else None,
    )


def _shape_deck(deck: Deck) -> dict:
    return {
        "id": deck.id,
        "title": deck.title,
        "description": deck.description,
        "source": deck.source.value,
        "card_count": deck.card_count,
        "due_count": deck.due_count,
        "created_at": deck.created_at.isoformat() if deck.created_at else None,
    }


@router.get("/decks", response_model=list[DeckResponse])
async def list_decks(user: dict = Depends(get_current_user)):
    store = _get_store(user["id"])
    return [DeckResponse(**_shape_deck(deck)) for deck in store.list_decks(user["id"])]


@router.post("/decks", response_model=DeckResponse, status_code=201)
async def create_deck(payload: DeckCreate, user: dict = Depends(get_current_user)):
    store = _get_store(user["id"])
    deck = store.create_deck(user["id"], payload.title.strip(), payload.description.strip())
    log_event(user["id"], "deck_created", {"deck_id": deck.id})
    return DeckResponse(**_shape_deck(deck))


@router.get("/decks/{deck_id}", response_model=DeckDetailResponse)
async def get_deck(deck_id: str, user: dict = Depends(get_current_user)):
    store = _get_store(user["id"])
    deck = store.get_deck(user["id"], deck_id)
    if deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    cards = store.list_cards(user["id"], deck_id)
    return DeckDetailResponse(**_shape_deck(deck), cards=[_shape_card(c) for c in cards])


@router.delete("/decks/{deck_id}", status_code=204)
async def delete_deck(deck_id: str, user: dict = Depends(get_current_user)):
    store = _get_store(user["id"])
    if not store.delete_deck(user["id"], deck_id):
        raise HTTPException(status_code=404, detail="Deck not found")


@router.post("/decks/import", response_model=DeckImportResponse, status_code=201)
async def import_deck(
    file: UploadFile = File(...),
    title: str | None = Form(default=None),
    user: dict = Depends(get_current_user),
):
    payload = await file.read()
    if len(payload) > MAX_APKG_BYTES:
        raise HTTPException(status_code=413, detail="Deck file exceeds the 50 MB limit")
    if not payload.startswith(b"PK"):
        raise HTTPException(
            status_code=400, detail="Not a valid .apkg file (corrupt or not a zip archive)."
        )

    try:
        result = parse_apkg(payload)
    except AnkiFormatError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    deck_name = (title or "").strip() or result.deck_name
    if deck_name in ("", "Default", "Imported deck") and file.filename:
        stem = Path(file.filename).stem.strip()
        deck_name = stem or deck_name or "Imported deck"

    store = _get_store(user["id"])
    deck = store.create_deck(user["id"], deck_name, source="imported")
    store.add_cards_bulk(
        user["id"],
        deck.id,
        [
            {
                "front": card.front,
                "back": card.back,
                "tags": card.tags,
                "anki_note_guid": card.guid,
                "easiness_factor": card.easiness_factor,
                "interval_days": card.interval_days,
                "repetitions": card.repetitions,
                "next_review": card.due_at,
            }
            for card in result.cards
        ],
    )
    deck = store.get_deck(user["id"], deck.id)
    log_event(user["id"], "deck_imported", {"deck_id": deck.id, "cards": deck.card_count})
    return DeckImportResponse(
        **_shape_deck(deck),
        skipped_empty=result.skipped_empty,
        skipped_media=result.skipped_media,
    )


@router.get("/decks/{deck_id}/export")
async def export_deck(deck_id: str, user: dict = Depends(get_current_user)):
    store = _get_store(user["id"])
    deck = store.get_deck(user["id"], deck_id)
    if deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    cards = store.list_cards(user["id"], deck_id, limit=100_000)
    apkg = build_apkg(
        deck.title,
        [AnkiCard(front=c.front, back=c.back, tags=c.tags, guid=c.anki_note_guid) for c in cards],
    )
    filename = f"{_safe_filename(deck.title)}.apkg"
    return Response(
        content=apkg,
        media_type="application/apkg",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/decks/{deck_id}/cards", response_model=FlashcardResponse, status_code=201)
async def add_card(deck_id: str, payload: FlashcardCreate, user: dict = Depends(get_current_user)):
    store = _get_store(user["id"])
    if store.get_deck(user["id"], deck_id) is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    card = store.add_card(
        user["id"], deck_id, payload.front.strip(), payload.back.strip(), payload.tags
    )
    return _shape_card(card)


@router.patch("/decks/{deck_id}/cards/{card_id}", response_model=FlashcardResponse)
async def update_card(
    deck_id: str,
    card_id: str,
    payload: FlashcardUpdate,
    user: dict = Depends(get_current_user),
):
    store = _get_store(user["id"])
    existing = store.get_card(user["id"], card_id)
    if existing is None or existing.deck_id != deck_id:
        raise HTTPException(status_code=404, detail="Card not found")
    card = store.update_card(user["id"], card_id, front=payload.front, back=payload.back)
    return _shape_card(card)


@router.delete("/decks/{deck_id}/cards/{card_id}", status_code=204)
async def delete_card(deck_id: str, card_id: str, user: dict = Depends(get_current_user)):
    store = _get_store(user["id"])
    existing = store.get_card(user["id"], card_id)
    if existing is None or existing.deck_id != deck_id:
        raise HTTPException(status_code=404, detail="Card not found")
    store.delete_card(user["id"], card_id)


@router.get("/review/flashcards/due", response_model=list[FlashcardResponse])
async def due_flashcards(
    limit: int = Query(default=20, ge=1, le=50),
    deck_id: str | None = Query(default=None),
    user: dict = Depends(get_current_user),
):
    store = _get_store(user["id"])
    cards = store.get_due_cards(user["id"], limit=limit, deck_id=deck_id)
    return [_shape_card(card) for card in cards]


@router.post("/review/flashcards/{card_id}/grade", response_model=FlashcardResponse)
async def grade_flashcard(
    card_id: str,
    payload: FlashcardGradeRequest,
    user: dict = Depends(get_current_user),
):
    if payload.rating is None and payload.grade is None:
        raise HTTPException(status_code=422, detail="Provide either rating or grade")
    grade = payload.grade if payload.grade is not None else RATING_TO_GRADE[payload.rating]
    store = _get_store(user["id"])
    card = store.grade_card(user["id"], card_id, grade)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    log_event(user["id"], "flashcard_graded", {"card_id": card_id, "grade": grade})
    return _shape_card(card)


@router.get("/review/export")
async def export_review_items(user: dict = Depends(get_current_user)):
    """Export the user's chapter review questions as an Anki deck."""
    store = CurriculumStore(_db_path(user["id"]))
    items = store.list_review_items(user["id"], include_pre_reading=False)
    cards = [
        AnkiCard(
            front=item["question"],
            back=item.get("expected_answer", ""),
            tags=[tag for tag in [item.get("guide_id", "").replace(" ", "_")] if tag],
        )
        for item in items
        if item.get("question")
    ]
    apkg = build_apkg("StewardMe reviews", cards)
    return Response(
        content=apkg,
        media_type="application/apkg",
        headers={"Content-Disposition": 'attachment; filename="stewardme-reviews.apkg"'},
    )


def _safe_filename(name: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in ("-", "_", " ") else "" for ch in name)
    return cleaned.strip().replace(" ", "-").lower() or "deck"
