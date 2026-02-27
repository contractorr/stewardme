"""Learning path MCP tools — gaps, paths, progress."""

from coach_mcp.bootstrap import get_components


def _get_lp_storage(c):
    from advisor.learning_paths import LearningPathStorage

    lp_dir = c["config"].get("learning_paths", {}).get("dir", "~/coach/learning_paths")
    return LearningPathStorage(lp_dir)


def _learning_gaps(args: dict) -> dict:
    """Analyze skill gaps (requires LLM — returns profile + journal context for Claude to reason over)."""
    c = get_components()

    # Return raw context for Claude Code to reason over (no LLM in MCP layer)
    profile_ctx = ""
    try:
        from profile.storage import ProfileStorage

        profile_path = c["config"].get("profile", {}).get("path", "~/coach/profile.yaml")
        ps = ProfileStorage(profile_path)
        p = ps.load()
        if p:
            profile_ctx = p.summary()
    except Exception:
        pass

    journal_ctx = c["search"].get_context_for_query(
        "skills goals career aspirations learning",
        max_entries=8,
        max_chars=4000,
    )

    return {
        "profile": profile_ctx,
        "journal_context": journal_ctx,
        "instruction": "Analyze skill gaps between current skills and aspirations. Identify critical gaps and recommend priority order.",
    }


def _learning_paths_list(args: dict) -> dict:
    """List all learning paths."""
    c = get_components()
    storage = _get_lp_storage(c)
    status = args.get("status")
    paths = storage.list_paths(status=status)
    return {"paths": paths, "count": len(paths)}


def _learning_path_get(args: dict) -> dict:
    """Get a specific learning path."""
    c = get_components()
    storage = _get_lp_storage(c)
    path = storage.get(args["path_id"])
    if not path:
        return {"error": "Learning path not found"}
    return path


def _learning_path_progress(args: dict) -> dict:
    """Update progress on a learning path."""
    c = get_components()
    storage = _get_lp_storage(c)
    path_id = args["path_id"]
    completed = args["completed_modules"]

    if storage.update_progress(path_id, completed):
        path = storage.get(path_id)
        return {"success": True, "path": path}
    return {"success": False, "error": "Learning path not found"}


def _learning_check_in(args: dict) -> dict:
    """Check in on a learning module. Returns updated path + context for Claude to reason over."""
    c = get_components()
    storage = _get_lp_storage(c)
    path_id = args["path_id"]
    action = args["action"]
    module_number = args.get("module_number")

    path = storage.get(path_id)
    if not path:
        return {"error": "Learning path not found"}

    if not module_number:
        module_number = path.get("completed_modules", 0) + 1

    result = storage.check_in(path_id, module_number, action)
    if not result:
        return {"error": "Check-in failed"}

    return {
        "success": True,
        "path": result,
        "action": action,
        "module_number": module_number,
        "needs_deep_dive": action == "deepen",
        "instruction": "If action is 'deepen', generate a deep-dive subsection for this module and present it to the user.",
    }


TOOLS = [
    (
        "learning_gaps",
        {
            "description": "Get profile and journal context for skill gap analysis. Returns raw context for reasoning.",
            "type": "object",
            "properties": {},
            "required": [],
        },
        _learning_gaps,
    ),
    (
        "learning_paths_list",
        {
            "description": "List all learning paths with progress tracking.",
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "description": "Filter by status: active, completed",
                    "enum": ["active", "completed"],
                },
            },
            "required": [],
        },
        _learning_paths_list,
    ),
    (
        "learning_path_get",
        {
            "description": "Get a specific learning path by ID with full content.",
            "type": "object",
            "properties": {
                "path_id": {"type": "string", "description": "Learning path ID"},
            },
            "required": ["path_id"],
        },
        _learning_path_get,
    ),
    (
        "learning_path_progress",
        {
            "description": "Update progress on a learning path by marking completed modules.",
            "type": "object",
            "properties": {
                "path_id": {"type": "string", "description": "Learning path ID"},
                "completed_modules": {
                    "type": "integer",
                    "description": "Number of completed modules",
                },
            },
            "required": ["path_id", "completed_modules"],
        },
        _learning_path_progress,
    ),
    (
        "learning_check_in",
        {
            "description": "Check in on a learning module with continue/deepen/skip. Returns updated path + context.",
            "type": "object",
            "properties": {
                "path_id": {"type": "string", "description": "Learning path ID"},
                "action": {
                    "type": "string",
                    "description": "Check-in action",
                    "enum": ["continue", "deepen", "skip"],
                },
                "module_number": {
                    "type": "integer",
                    "description": "Module number (defaults to current)",
                },
            },
            "required": ["path_id", "action"],
        },
        _learning_check_in,
    ),
]
