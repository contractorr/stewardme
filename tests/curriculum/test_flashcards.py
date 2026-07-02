"""Tests for the flashcard deck store."""

from datetime import datetime, timedelta

import pytest

from curriculum.flashcards import FlashcardStore
from curriculum.store import CurriculumStore

USER = "user-123"
OTHER = "user-456"


@pytest.fixture
def store(tmp_path):
    return FlashcardStore(tmp_path / "curriculum.db")


def test_create_and_list_decks(store):
    deck = store.create_deck(USER, "Spanish", "Vocab deck")
    decks = store.list_decks(USER)
    assert [d.id for d in decks] == [deck.id]
    assert decks[0].title == "Spanish"
    assert decks[0].card_count == 0
    assert decks[0].due_count == 0


def test_add_card_is_due_immediately(store):
    deck = store.create_deck(USER, "Deck")
    store.add_card(USER, deck.id, "front", "back", tags=["x"])
    fetched = store.get_deck(USER, deck.id)
    assert fetched.card_count == 1
    assert fetched.due_count == 1
    due = store.get_due_cards(USER)
    assert len(due) == 1
    assert due[0].front == "front"
    assert due[0].tags == ["x"]


def test_bulk_add_preserves_scheduling(store):
    deck = store.create_deck(USER, "Imported", source="imported")
    future = datetime.utcnow() + timedelta(days=10)
    count = store.add_cards_bulk(
        USER,
        deck.id,
        [
            {"front": "due now", "back": "a"},
            {
                "front": "due later",
                "back": "b",
                "easiness_factor": 2.1,
                "interval_days": 30,
                "repetitions": 7,
                "next_review": future,
            },
        ],
    )
    assert count == 2
    due = store.get_due_cards(USER)
    assert [card.front for card in due] == ["due now"]
    later = next(c for c in store.list_cards(USER, deck.id) if c.front == "due later")
    assert later.easiness_factor == pytest.approx(2.1)
    assert later.interval_days == 30
    assert later.repetitions == 7


def test_grade_card_success_reschedules(store):
    deck = store.create_deck(USER, "Deck")
    card = store.add_card(USER, deck.id, "q", "a")
    graded = store.grade_card(USER, card.id, 4)
    assert graded.repetitions == 1
    assert graded.next_review > datetime.utcnow()
    assert store.count_due(USER) == 0


def test_grade_card_failure_keeps_card_due(store):
    deck = store.create_deck(USER, "Deck")
    card = store.add_card(USER, deck.id, "q", "a")
    graded = store.grade_card(USER, card.id, 1)
    assert graded.repetitions == 0
    assert store.count_due(USER) == 1


def test_easy_pushes_further_out_than_good(store):
    deck = store.create_deck(USER, "Deck")
    good = store.add_card(USER, deck.id, "g", "")
    easy = store.add_card(USER, deck.id, "e", "")
    for _ in range(3):
        good = store.grade_card(USER, good.id, 4)
        easy = store.grade_card(USER, easy.id, 5)
    assert easy.next_review > good.next_review


def test_update_and_delete_card(store):
    deck = store.create_deck(USER, "Deck")
    card = store.add_card(USER, deck.id, "old", "old back")
    updated = store.update_card(USER, card.id, front="new")
    assert updated.front == "new"
    assert updated.back == "old back"
    assert store.delete_card(USER, card.id)
    assert store.get_card(USER, card.id) is None


def test_delete_deck_cascades_to_cards(store):
    deck = store.create_deck(USER, "Deck")
    store.add_card(USER, deck.id, "q", "a")
    assert store.delete_deck(USER, deck.id)
    assert store.list_decks(USER) == []
    assert store.count_due(USER) == 0


def test_user_isolation(store):
    deck = store.create_deck(USER, "Mine")
    store.add_card(USER, deck.id, "q", "a")
    assert store.list_decks(OTHER) == []
    assert store.get_deck(OTHER, deck.id) is None
    assert store.get_due_cards(OTHER) == []
    assert not store.delete_deck(OTHER, deck.id)
    # still intact for the owner
    assert store.get_deck(USER, deck.id) is not None


def test_due_cards_filtered_by_deck(store):
    deck_a = store.create_deck(USER, "A")
    deck_b = store.create_deck(USER, "B")
    store.add_card(USER, deck_a.id, "a-card", "")
    store.add_card(USER, deck_b.id, "b-card", "")
    due_a = store.get_due_cards(USER, deck_id=deck_a.id)
    assert [card.front for card in due_a] == ["a-card"]


def test_coexists_with_curriculum_store_in_same_db(tmp_path):
    db_path = tmp_path / "curriculum.db"
    curriculum = CurriculumStore(db_path)
    flashcards = FlashcardStore(db_path)
    deck = flashcards.create_deck(USER, "Deck")
    flashcards.add_card(USER, deck.id, "q", "a")
    # Re-opening either store must not lose data or fight over schema version.
    CurriculumStore(db_path)
    assert FlashcardStore(db_path).get_deck(USER, deck.id).card_count == 1
    assert curriculum.list_guides() == []
