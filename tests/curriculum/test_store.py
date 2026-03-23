"""Tests for curriculum SQLite store."""

import uuid
from datetime import datetime

import pytest

from curriculum.models import (
    BloomLevel,
    Chapter,
    DifficultyLevel,
    Guide,
    GuideCategory,
    ReviewItem,
)
from curriculum.store import CurriculumStore


@pytest.fixture
def store(tmp_path):
    return CurriculumStore(tmp_path / "curriculum.db")


@pytest.fixture
def sample_guide():
    return Guide(
        id="01-philosophy-guide",
        title="Philosophy",
        category=GuideCategory.HUMANITIES,
        difficulty=DifficultyLevel.INTRODUCTORY,
        source_dir="/content/01-philosophy-guide",
        chapter_count=3,
        total_word_count=5000,
        total_reading_time_minutes=20,
        has_glossary=True,
        prerequisites=[],
    )


@pytest.fixture
def sample_chapters():
    return [
        Chapter(
            id="01-philosophy-guide/01-introduction",
            guide_id="01-philosophy-guide",
            title="Introduction to Philosophy",
            filename="01-introduction.md",
            order=0,
            word_count=2000,
            reading_time_minutes=8,
            content_hash="abc123",
        ),
        Chapter(
            id="01-philosophy-guide/02-logic",
            guide_id="01-philosophy-guide",
            title="Logic and Reasoning",
            filename="02-logic.md",
            order=1,
            word_count=2500,
            reading_time_minutes=10,
            content_hash="def456",
        ),
        Chapter(
            id="01-philosophy-guide/03-glossary",
            guide_id="01-philosophy-guide",
            title="Glossary",
            filename="03-glossary.md",
            order=2,
            word_count=500,
            reading_time_minutes=2,
            is_glossary=True,
            content_hash="ghi789",
        ),
    ]


def test_sync_catalog(store, sample_guide, sample_chapters):
    store.sync_catalog([sample_guide], sample_chapters)
    guides = store.list_guides()
    assert len(guides) == 1
    assert guides[0]["id"] == "01-philosophy-guide"


def test_get_guide_with_chapters(store, sample_guide, sample_chapters):
    store.sync_catalog([sample_guide], sample_chapters)
    guide = store.get_guide("01-philosophy-guide")
    assert guide is not None
    assert len(guide["chapters"]) == 3


def test_enrollment(store, sample_guide, sample_chapters):
    store.sync_catalog([sample_guide], sample_chapters)
    user_id = "test-user"

    assert not store.is_enrolled(user_id, "01-philosophy-guide")
    store.enroll(user_id, "01-philosophy-guide")
    assert store.is_enrolled(user_id, "01-philosophy-guide")

    enrollments = store.get_enrollments(user_id)
    assert len(enrollments) == 1


def test_progress_tracking(store, sample_guide, sample_chapters):
    store.sync_catalog([sample_guide], sample_chapters)
    user_id = "test-user"

    # Start reading
    result = store.update_progress(
        user_id=user_id,
        chapter_id="01-philosophy-guide/01-introduction",
        guide_id="01-philosophy-guide",
        status="in_progress",
    )
    assert result["status"] == "in_progress"
    assert result["started_at"] is not None

    # Complete
    result = store.update_progress(
        user_id=user_id,
        chapter_id="01-philosophy-guide/01-introduction",
        guide_id="01-philosophy-guide",
        status="completed",
    )
    assert result["status"] == "completed"
    assert result["completed_at"] is not None


def test_reading_time_accumulates(store, sample_guide, sample_chapters):
    store.sync_catalog([sample_guide], sample_chapters)
    user_id = "test-user"

    store.update_progress(
        user_id=user_id,
        chapter_id="01-philosophy-guide/01-introduction",
        guide_id="01-philosophy-guide",
        status="in_progress",
        reading_time_seconds=30,
    )
    store.update_progress(
        user_id=user_id,
        chapter_id="01-philosophy-guide/01-introduction",
        guide_id="01-philosophy-guide",
        reading_time_seconds=45,
    )
    progress = store.get_chapter_progress(user_id, "01-philosophy-guide/01-introduction")
    assert progress["reading_time_seconds"] == 75


def test_guide_auto_complete(store, sample_guide, sample_chapters):
    store.sync_catalog([sample_guide], sample_chapters)
    user_id = "test-user"
    store.enroll(user_id, "01-philosophy-guide")

    # Complete non-glossary chapters
    for ch_id in ["01-philosophy-guide/01-introduction", "01-philosophy-guide/02-logic"]:
        store.update_progress(
            user_id=user_id,
            chapter_id=ch_id,
            guide_id="01-philosophy-guide",
            status="completed",
        )

    # Guide should be auto-completed (glossary not required)
    enrollments = store.get_enrollments(user_id)
    assert enrollments[0]["completed_at"] is not None


def test_review_items(store, sample_guide, sample_chapters):
    store.sync_catalog([sample_guide], sample_chapters)
    user_id = "test-user"
    now = datetime.utcnow()

    items = [
        ReviewItem(
            id=uuid.uuid4().hex[:16],
            user_id=user_id,
            chapter_id="01-philosophy-guide/01-introduction",
            guide_id="01-philosophy-guide",
            question="What is philosophy?",
            expected_answer="The study of fundamental questions about existence, knowledge, values.",
            bloom_level=BloomLevel.REMEMBER,
            next_review=now,
            created_at=now,
            content_hash="abc123",
        ),
    ]
    store.add_review_items(items)

    due = store.get_due_reviews(user_id)
    assert len(due) == 1
    assert due[0]["question"] == "What is philosophy?"


def test_grade_review_updates_schedule(store, sample_guide, sample_chapters):
    store.sync_catalog([sample_guide], sample_chapters)
    user_id = "test-user"
    now = datetime.utcnow()
    item_id = uuid.uuid4().hex[:16]

    items = [
        ReviewItem(
            id=item_id,
            user_id=user_id,
            chapter_id="01-philosophy-guide/01-introduction",
            guide_id="01-philosophy-guide",
            question="Test question",
            expected_answer="Test answer",
            bloom_level=BloomLevel.REMEMBER,
            next_review=now,
            created_at=now,
            content_hash="abc123",
        ),
    ]
    store.add_review_items(items)

    updated = store.grade_review(item_id, 5)
    assert updated is not None
    assert updated["repetitions"] == 1
    assert updated["interval_days"] == 1


def test_stats(store, sample_guide, sample_chapters):
    store.sync_catalog([sample_guide], sample_chapters)
    user_id = "test-user"
    store.enroll(user_id, "01-philosophy-guide")

    stats = store.get_stats(user_id)
    assert stats.guides_enrolled == 1
    assert stats.total_chapters == 3
    assert stats.chapters_completed == 0


def test_next_chapter(store, sample_guide, sample_chapters):
    store.sync_catalog([sample_guide], sample_chapters)
    user_id = "test-user"

    # First chapter should be next
    nxt = store.get_next_chapter(user_id, "01-philosophy-guide")
    assert nxt is not None
    assert nxt["id"] == "01-philosophy-guide/01-introduction"

    # Complete first, next should be second
    store.update_progress(
        user_id=user_id,
        chapter_id="01-philosophy-guide/01-introduction",
        guide_id="01-philosophy-guide",
        status="completed",
    )
    nxt = store.get_next_chapter(user_id, "01-philosophy-guide")
    assert nxt["id"] == "01-philosophy-guide/02-logic"


def test_list_guides_with_progress(store, sample_guide, sample_chapters):
    store.sync_catalog([sample_guide], sample_chapters)
    user_id = "test-user"
    store.enroll(user_id, "01-philosophy-guide")
    store.update_progress(
        user_id=user_id,
        chapter_id="01-philosophy-guide/01-introduction",
        guide_id="01-philosophy-guide",
        status="completed",
    )

    guides = store.list_guides(user_id=user_id)
    assert guides[0]["enrolled"]
    assert guides[0]["chapters_completed"] == 1
    assert guides[0]["progress_pct"] > 0


def test_count_due_reviews(store, sample_guide, sample_chapters):
    store.sync_catalog([sample_guide], sample_chapters)
    user_id = "test-user"

    assert store.count_due_reviews(user_id) == 0

    items = [
        ReviewItem(
            id=uuid.uuid4().hex[:16],
            user_id=user_id,
            chapter_id="01-philosophy-guide/01-introduction",
            guide_id="01-philosophy-guide",
            question="Q1",
            expected_answer="A1",
            bloom_level=BloomLevel.REMEMBER,
            next_review=datetime.utcnow(),
            created_at=datetime.utcnow(),
            content_hash="abc",
        ),
    ]
    store.add_review_items(items)
    assert store.count_due_reviews(user_id) == 1


def test_get_chapter_metadata(store, sample_guide, sample_chapters):
    store.sync_catalog([sample_guide], sample_chapters)
    ch = store.get_chapter("01-philosophy-guide/01-introduction")
    assert ch is not None
    assert ch["title"] == "Introduction to Philosophy"
    assert ch["word_count"] == 2000
