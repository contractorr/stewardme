"""Goals CRUD routes wrapping advisor/goals.py."""

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status

from advisor.goals import GoalTracker
from journal.storage import JournalStorage
from web.auth import get_current_user
from web.deps import get_coach_paths
from web.models import GoalCheckIn, GoalCreate, GoalStatusUpdate, MilestoneAdd, MilestoneComplete

router = APIRouter(prefix="/api/goals", tags=["goals"])


def _get_tracker() -> GoalTracker:
    paths = get_coach_paths()
    storage = JournalStorage(paths["journal_dir"])
    return GoalTracker(storage)


def _get_storage() -> JournalStorage:
    paths = get_coach_paths()
    return JournalStorage(paths["journal_dir"])


@router.get("")
async def list_goals(
    include_inactive: bool = False,
    user: dict = Depends(get_current_user),
):
    tracker = _get_tracker()
    goals = tracker.get_goals(include_inactive=include_inactive)
    # Convert Path objects to strings for JSON
    for g in goals:
        g["path"] = str(g["path"])
    return goals


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_goal(
    body: GoalCreate,
    user: dict = Depends(get_current_user),
):
    from advisor.goals import get_goal_defaults

    storage = _get_storage()
    try:
        filepath = storage.create(
            content=body.content,
            entry_type="goal",
            title=body.title,
            tags=body.tags,
            metadata=get_goal_defaults(),
        )
        return {"path": str(filepath), "title": body.title}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{filepath:path}/check-in")
async def check_in(
    filepath: str,
    body: GoalCheckIn,
    user: dict = Depends(get_current_user),
):
    tracker = _get_tracker()
    success = tracker.check_in_goal(Path(filepath), notes=body.notes)
    if not success:
        raise HTTPException(status_code=404, detail="Goal not found")
    return {"ok": True}


@router.put("/{filepath:path}/status")
async def update_status(
    filepath: str,
    body: GoalStatusUpdate,
    user: dict = Depends(get_current_user),
):
    tracker = _get_tracker()
    success = tracker.update_goal_status(Path(filepath), body.status)
    if not success:
        raise HTTPException(status_code=404, detail="Goal not found")
    return {"ok": True}


@router.post("/{filepath:path}/milestones")
async def add_milestone(
    filepath: str,
    body: MilestoneAdd,
    user: dict = Depends(get_current_user),
):
    tracker = _get_tracker()
    success = tracker.add_milestone(Path(filepath), body.title)
    if not success:
        raise HTTPException(status_code=404, detail="Goal not found")
    return {"ok": True}


@router.post("/{filepath:path}/milestones/complete")
async def complete_milestone(
    filepath: str,
    body: MilestoneComplete,
    user: dict = Depends(get_current_user),
):
    tracker = _get_tracker()
    success = tracker.complete_milestone(Path(filepath), body.milestone_index)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid milestone")
    return {"ok": True}


@router.get("/{filepath:path}/progress")
async def get_progress(
    filepath: str,
    user: dict = Depends(get_current_user),
):
    tracker = _get_tracker()
    return tracker.get_progress(Path(filepath))
