"""Curriculum / Learn routes — guides, chapters, progress, reviews, quizzes."""

from pathlib import Path

import structlog
from fastapi import APIRouter, Depends, HTTPException, Query, status

from curriculum.models import (
    BloomLevel,
    ChapterStatus,
    ProgressUpdate,
    QuizSubmission,
    ReviewGradeRequest,
)
from curriculum.question_generator import QuestionGenerator
from curriculum.scanner import CurriculumScanner
from curriculum.store import CurriculumStore
from web.auth import get_current_user
from web.deps import get_config, get_user_paths
from web.user_store import log_event

logger = structlog.get_logger()
router = APIRouter(prefix="/api/curriculum", tags=["curriculum"])


def _content_dirs() -> list[Path]:
    """Resolve built-in + extra content directories."""
    # Built-in content: content/curriculum/ relative to repo root
    # Repo root = 3 levels up from src/web/routes/
    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    dirs = [repo_root / "content" / "curriculum"]

    config = get_config()
    if hasattr(config, "curriculum") and config.curriculum.extra_content_dirs:
        for d in config.curriculum.extra_content_dirs:
            dirs.append(Path(d).expanduser().resolve())
    return dirs


def _get_store(user_id: str) -> CurriculumStore:
    paths = get_user_paths(user_id)
    return CurriculumStore(Path(paths["data_dir"]) / "curriculum.db")


def _chapter_content_path(chapter_id: str) -> Path | None:
    """Resolve chapter markdown file from content dirs.

    chapter_id format: guide_id/chapter_stem
    """
    parts = chapter_id.split("/", 1)
    if len(parts) != 2:
        return None

    guide_id, chapter_stem = parts
    filename = f"{chapter_stem}.md"

    for content_dir in _content_dirs():
        # Direct guide dir (e.g., content/curriculum/01-philosophy-guide/)
        candidate = content_dir / guide_id / filename
        if candidate.is_file():
            return candidate

        # Industry guides (content/curriculum/Industries/Name/)
        if guide_id.startswith("industry-"):
            industry_name = guide_id[len("industry-") :]
            # Search Industries/ subdirs case-insensitively
            industries_dir = content_dir / "Industries"
            if industries_dir.is_dir():
                for subdir in industries_dir.iterdir():
                    if subdir.name.lower() == industry_name.lower():
                        candidate = subdir / filename
                        if candidate.is_file():
                            return candidate
    return None


# --- Endpoints ---


@router.get("/guides")
async def list_guides(
    category: str | None = Query(None),
    user: dict = Depends(get_current_user),
):
    user_id = user["id"]
    store = _get_store(user_id)

    # Auto-sync catalog if empty
    guides = store.list_guides(category=category, user_id=user_id)
    if not guides:
        _sync_catalog(store)
        guides = store.list_guides(category=category, user_id=user_id)

    return guides


@router.get("/guides/{guide_id}")
async def get_guide(
    guide_id: str,
    user: dict = Depends(get_current_user),
):
    store = _get_store(user["id"])
    guide = store.get_guide(guide_id, user_id=user["id"])
    if not guide:
        # Try sync first
        _sync_catalog(store)
        guide = store.get_guide(guide_id, user_id=user["id"])
    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")
    return guide


@router.get("/guides/{guide_id}/chapters/{chapter_id:path}")
async def get_chapter(
    guide_id: str,
    chapter_id: str,
    user: dict = Depends(get_current_user),
):
    store = _get_store(user["id"])

    # chapter_id comes in as the part after guide_id, reconstruct full id
    full_chapter_id = f"{guide_id}/{chapter_id}"
    chapter = store.get_chapter(full_chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    # Read content
    content_path = _chapter_content_path(full_chapter_id)
    if not content_path:
        raise HTTPException(status_code=404, detail="Chapter content file not found")

    content = content_path.read_text(encoding="utf-8")

    # Get progress
    progress = store.get_chapter_progress(user["id"], full_chapter_id)

    # Compute prev/next
    guide = store.get_guide(guide_id, user_id=user["id"])
    prev_chapter = None
    next_chapter = None
    if guide and guide.get("chapters"):
        chapters_list = guide["chapters"]
        for i, ch in enumerate(chapters_list):
            if ch["id"] == full_chapter_id:
                if i > 0:
                    prev_chapter = chapters_list[i - 1]["id"]
                if i < len(chapters_list) - 1:
                    next_chapter = chapters_list[i + 1]["id"]
                break

    return {
        **chapter,
        "content": content,
        "progress": progress,
        "prev_chapter": prev_chapter,
        "next_chapter": next_chapter,
    }


@router.post("/guides/{guide_id}/enroll", status_code=status.HTTP_201_CREATED)
async def enroll_guide(
    guide_id: str,
    user: dict = Depends(get_current_user),
):
    store = _get_store(user["id"])
    guide = store.get_guide(guide_id)
    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")

    store.enroll(user["id"], guide_id)
    log_event("curriculum_enrolled", user["id"], {"guide_id": guide_id})
    return {"status": "enrolled", "guide_id": guide_id}


@router.post("/progress")
async def update_progress(
    body: ProgressUpdate,
    user: dict = Depends(get_current_user),
):
    store = _get_store(user["id"])
    result = store.update_progress(
        user_id=user["id"],
        chapter_id=body.chapter_id,
        guide_id=body.guide_id,
        status=body.status.value if body.status else None,
        reading_time_seconds=body.reading_time_seconds,
        scroll_position=body.scroll_position,
    )

    if body.status == ChapterStatus.COMPLETED:
        log_event(
            "chapter_completed",
            user["id"],
            {
                "chapter_id": body.chapter_id,
                "guide_id": body.guide_id,
            },
        )

    return result


@router.get("/review/due")
async def get_due_reviews(
    guide_id: str | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
    user: dict = Depends(get_current_user),
):
    store = _get_store(user["id"])
    return store.get_due_reviews(user["id"], limit=limit, guide_id=guide_id)


@router.post("/review/{review_id}/grade")
async def grade_review(
    review_id: str,
    body: ReviewGradeRequest,
    user: dict = Depends(get_current_user),
):
    store = _get_store(user["id"])
    item = store.get_review_item(review_id)
    if not item:
        raise HTTPException(status_code=404, detail="Review item not found")

    # If self-grade provided, use it directly
    if body.self_grade is not None:
        grade = max(0, min(5, body.self_grade))
    else:
        # LLM grading
        try:
            gen = QuestionGenerator()
            bloom = BloomLevel(item["bloom_level"])
            result = await gen.grade_answer(
                question=item["question"],
                expected_answer=item["expected_answer"],
                student_answer=body.answer,
                bloom_level=bloom,
            )
            grade = result.grade
        except Exception:
            grade = 3  # default if grading fails

    updated = store.grade_review(review_id, grade)
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to update review")

    log_event(
        "review_graded",
        user["id"],
        {
            "review_id": review_id,
            "grade": grade,
        },
    )
    return {"review": updated, "grade": grade}


@router.post("/quiz/{chapter_id:path}/generate")
async def generate_quiz(
    chapter_id: str,
    user: dict = Depends(get_current_user),
):
    store = _get_store(user["id"])
    chapter = store.get_chapter(chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    # Check if questions already exist
    existing = store.get_review_items_for_chapter(user["id"], chapter_id)
    if existing:
        return {"questions": existing, "cached": True}

    # Read content
    content_path = _chapter_content_path(chapter_id)
    if not content_path:
        raise HTTPException(status_code=404, detail="Chapter content not found")
    content = content_path.read_text(encoding="utf-8")

    # Get guide title
    guide = store.get_guide(chapter["guide_id"])
    guide_title = guide["title"] if guide else ""

    gen = QuestionGenerator()
    items = await gen.generate_questions(
        content=content,
        chapter_title=chapter["title"],
        guide_title=guide_title,
        count=5,
        content_hash=chapter["content_hash"],
        chapter_id=chapter_id,
        guide_id=chapter["guide_id"],
        user_id=user["id"],
    )

    if items:
        store.add_review_items(items)

    return {"questions": [i.model_dump() for i in items], "cached": False}


@router.post("/quiz/{chapter_id:path}/submit")
async def submit_quiz(
    chapter_id: str,
    body: QuizSubmission,
    user: dict = Depends(get_current_user),
):
    store = _get_store(user["id"])
    results = []

    for question_id, answer in body.answers.items():
        item = store.get_review_item(question_id)
        if not item:
            continue

        gen = QuestionGenerator()
        bloom = BloomLevel(item["bloom_level"])
        grade_result = await gen.grade_answer(
            question=item["question"],
            expected_answer=item["expected_answer"],
            student_answer=answer,
            bloom_level=bloom,
        )

        store.grade_review(question_id, grade_result.grade)
        results.append(
            {
                "question_id": question_id,
                "grade": grade_result.grade,
                "feedback": grade_result.feedback,
                "correct_points": grade_result.correct_points,
                "missing_points": grade_result.missing_points,
            }
        )

    log_event(
        "quiz_completed",
        user["id"],
        {
            "chapter_id": chapter_id,
            "avg_grade": sum(r["grade"] for r in results) / len(results) if results else 0,
        },
    )
    return {"results": results}


@router.get("/stats")
async def get_stats(user: dict = Depends(get_current_user)):
    store = _get_store(user["id"])
    stats = store.get_stats(user["id"])
    return stats.model_dump()


@router.post("/sync")
async def sync_content(user: dict = Depends(get_current_user)):
    store = _get_store(user["id"])
    count = _sync_catalog(store)
    return {"synced_guides": count}


@router.get("/next")
async def get_next_recommendation(
    user: dict = Depends(get_current_user),
):
    """Get advisor-recommended next chapter to study."""
    store = _get_store(user["id"])

    # Simple heuristic: continue last read guide, or suggest enrolled guide with most progress
    last = store.get_last_read_chapter(user["id"])
    if last:
        next_ch = store.get_next_chapter(user["id"], last["guide_id"])
        if next_ch:
            return {
                "guide_id": last["guide_id"],
                "guide_title": last.get("guide_title", ""),
                "chapter": next_ch,
                "reason": "Continue where you left off",
            }

    # Check enrolled guides
    enrollments = store.get_enrollments(user["id"])
    for enrollment in enrollments:
        if enrollment.get("completed_at"):
            continue
        next_ch = store.get_next_chapter(user["id"], enrollment["guide_id"])
        if next_ch:
            guide = store.get_guide(enrollment["guide_id"])
            return {
                "guide_id": enrollment["guide_id"],
                "guide_title": guide["title"] if guide else "",
                "chapter": next_ch,
                "reason": "Continue enrolled guide",
            }

    return {
        "guide_id": None,
        "chapter": None,
        "reason": "No active guides — enroll in one to get started",
    }


def _sync_catalog(store: CurriculumStore) -> int:
    """Run scanner and sync results into store."""
    scanner = CurriculumScanner(_content_dirs())
    guides, chapters = scanner.scan()
    if guides:
        store.sync_catalog(guides, chapters)
    return len(guides)
