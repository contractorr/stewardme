"""Goals MCP tools — list, add, check-in, status, milestones."""

from pathlib import Path

from coach_mcp.bootstrap import get_components


def _get_tracker():
    from advisor.goals import GoalTracker

    c = get_components()
    return GoalTracker(c["storage"])


def _list_goals(args: dict) -> dict:
    """List goals with staleness info, progress, milestones."""
    tracker = _get_tracker()
    include_inactive = args.get("include_inactive", False)
    goals = tracker.get_goals(include_inactive=include_inactive)

    enriched = []
    for g in goals:
        goal_path = Path(g["path"])
        progress = tracker.get_progress(goal_path)
        enriched.append({
            "path": str(goal_path),
            "filename": goal_path.name,
            "title": g["title"],
            "status": g["status"],
            "created": g["created"],
            "last_checked": g["last_checked"],
            "check_in_days": g["check_in_days"],
            "days_since_check": g["days_since_check"],
            "is_stale": g["is_stale"],
            "tags": g["tags"],
            "progress": progress,
            "preview": g["content"],
        })

    return {"goals": enriched, "count": len(enriched)}


def _add_goal(args: dict) -> dict:
    """Create goal journal entry with goal metadata."""
    from coach_mcp.tools.journal import _create

    goal_args = {
        "content": args.get("description", ""),
        "entry_type": "goal",
        "title": args["title"],
        "tags": args.get("tags", []),
    }
    result = _create(goal_args)

    # Set check_in_days if non-default
    check_days = args.get("check_days", 14)
    if check_days != 14 and "path" in result:
        import frontmatter

        filepath = Path(result["path"])
        post = frontmatter.load(filepath)
        post["check_in_days"] = check_days
        with open(filepath, "w") as f:
            f.write(frontmatter.dumps(post))

    return result


def _check_in(args: dict) -> dict:
    """Record a check-in for a goal."""
    tracker = _get_tracker()
    goal_path = Path(args["goal_path"])
    notes = args.get("notes")

    success = tracker.check_in_goal(goal_path, notes=notes)
    return {"success": success, "goal_path": str(goal_path)}


def _update_status(args: dict) -> dict:
    """Set goal status."""
    tracker = _get_tracker()
    goal_path = Path(args["goal_path"])
    status = args["status"]

    success = tracker.update_goal_status(goal_path, status)
    return {"success": success, "goal_path": str(goal_path), "status": status}


def _add_milestone(args: dict) -> dict:
    """Add milestone to a goal."""
    tracker = _get_tracker()
    goal_path = Path(args["goal_path"])
    title = args["title"]

    success = tracker.add_milestone(goal_path, title)
    progress = tracker.get_progress(goal_path) if success else None
    return {"success": success, "goal_path": str(goal_path), "progress": progress}


def _complete_milestone(args: dict) -> dict:
    """Mark milestone as done."""
    tracker = _get_tracker()
    goal_path = Path(args["goal_path"])
    milestone_index = args["milestone_index"]

    success = tracker.complete_milestone(goal_path, milestone_index)
    progress = tracker.get_progress(goal_path) if success else None
    return {"success": success, "goal_path": str(goal_path), "progress": progress}


TOOLS = [
    (
        "goals_list",
        {
            "description": "List all goals with staleness info, progress, and milestones.",
            "type": "object",
            "properties": {
                "include_inactive": {
                    "type": "boolean",
                    "description": "Include completed/abandoned goals",
                    "default": False,
                },
            },
            "required": [],
        },
        _list_goals,
    ),
    (
        "goals_add",
        {
            "description": "Create a new goal with optional milestones tracking.",
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Goal title"},
                "description": {"type": "string", "description": "Goal description/body"},
                "check_days": {
                    "type": "integer",
                    "description": "Days between expected check-ins",
                    "default": 14,
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Tags for the goal",
                },
            },
            "required": ["title"],
        },
        _add_goal,
    ),
    (
        "goals_check_in",
        {
            "description": "Record a check-in on a goal, optionally with notes.",
            "type": "object",
            "properties": {
                "goal_path": {
                    "type": "string",
                    "description": "Full path to the goal file",
                },
                "notes": {"type": "string", "description": "Check-in notes"},
            },
            "required": ["goal_path"],
        },
        _check_in,
    ),
    (
        "goals_update_status",
        {
            "description": "Update goal status (active/paused/completed/abandoned).",
            "type": "object",
            "properties": {
                "goal_path": {"type": "string", "description": "Full path to the goal file"},
                "status": {
                    "type": "string",
                    "enum": ["active", "paused", "completed", "abandoned"],
                    "description": "New status",
                },
            },
            "required": ["goal_path", "status"],
        },
        _update_status,
    ),
    (
        "goals_add_milestone",
        {
            "description": "Add a milestone to a goal for progress tracking.",
            "type": "object",
            "properties": {
                "goal_path": {"type": "string", "description": "Full path to the goal file"},
                "title": {"type": "string", "description": "Milestone title"},
            },
            "required": ["goal_path", "title"],
        },
        _add_milestone,
    ),
    (
        "goals_complete_milestone",
        {
            "description": "Mark a goal milestone as completed.",
            "type": "object",
            "properties": {
                "goal_path": {"type": "string", "description": "Full path to the goal file"},
                "milestone_index": {
                    "type": "integer",
                    "description": "0-based index of the milestone",
                },
            },
            "required": ["goal_path", "milestone_index"],
        },
        _complete_milestone,
    ),
]
