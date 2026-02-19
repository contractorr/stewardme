"""Profile MCP tools — get profile, update fields."""

from coach_mcp.bootstrap import get_components


def _get_profile_path(c):
    """Get profile path from config."""
    config = c["config"]
    path = config.get("profile", {}).get("path", "~/coach/profile.yaml")
    return path


def _profile_get(args: dict) -> dict:
    """Get current user profile."""
    c = get_components()
    from profile.storage import ProfileStorage

    ps = ProfileStorage(_get_profile_path(c))
    p = ps.load()
    if not p:
        return {"exists": False, "profile": None}
    return {
        "exists": True,
        "profile": p.model_dump(),
        "summary": p.summary(),
        "is_stale": p.is_stale(),
    }


def _profile_update_field(args: dict) -> dict:
    """Update a single profile field."""
    c = get_components()
    from profile.storage import ProfileStorage

    ps = ProfileStorage(_get_profile_path(c))
    field = args["field"]
    value = args["value"]

    # Parse list fields
    list_fields = {"interests", "languages_frameworks"}
    if field in list_fields and isinstance(value, str):
        value = [v.strip() for v in value.split(",")]

    try:
        p = ps.update_field(field, value)
        return {"success": True, "profile": p.model_dump()}
    except ValueError as e:
        return {"success": False, "error": str(e)}


TOOLS = [
    (
        "profile_get",
        {
            "description": "Get the user's professional profile including skills, interests, career stage, location, and aspirations.",
            "type": "object",
            "properties": {},
            "required": [],
        },
        _profile_get,
    ),
    (
        "profile_update_field",
        {
            "description": "Update a single field on the user's profile.",
            "type": "object",
            "properties": {
                "field": {
                    "type": "string",
                    "description": "Field name (skills, interests, career_stage, current_role, aspirations, location, languages_frameworks, learning_style, weekly_hours_available)",
                },
                "value": {
                    "description": "New value for the field. For list fields (interests, languages_frameworks), pass comma-separated string.",
                },
            },
            "required": ["field", "value"],
        },
        _profile_update_field,
    ),
]
