"""Reflection prompts MCP tool."""

from coach_mcp.bootstrap import get_components


def _get_reflection_prompts(args: dict) -> dict:
    """Generate coaching reflection questions from journal + goals context."""
    c = get_components()
    days = args.get("days", 14)

    journal_ctx = c["rag"].get_recent_entries(days=days)
    goal_entries = c["storage"].list_entries(entry_type="goal", limit=10)
    goal_ctx = ""
    for g in goal_entries:
        post = c["storage"].read(g["path"])
        status = post.get("status", "active")
        goal_ctx += f"- {g['title']} ({status})\n"

    return {
        "journal_context": journal_ctx,
        "goal_context": goal_ctx or "(No goals set)",
        "instruction": "Generate 3-5 targeted coaching questions based on the journal context and goal status. Reference specific entries and goals.",
    }


TOOLS = [
    (
        "get_reflection_prompts",
        {
            "description": "Get journal + goals context for generating coaching reflection questions. Returns raw context for Claude to reason over.",
            "type": "object",
            "properties": {
                "days": {"type": "integer", "description": "Lookback days for journal context", "default": 14},
            },
            "required": [],
        },
        _get_reflection_prompts,
    ),
]
