"""Mood tracking MCP tool."""

from coach_mcp.bootstrap import get_components


def _get_mood(args: dict) -> dict:
    """Get mood timeline from journal entries."""
    from journal.sentiment import get_mood_history

    c = get_components()
    days = args.get("days", 30)
    timeline = get_mood_history(c["storage"], days=days)

    scores = [e["score"] for e in timeline]
    avg = sum(scores) / len(scores) if scores else 0

    return {
        "timeline": timeline,
        "count": len(timeline),
        "average_score": round(avg, 2),
    }


TOOLS = [
    (
        "mood_timeline",
        {
            "description": "Get mood/sentiment timeline from journal entries. Returns scored entries over time.",
            "type": "object",
            "properties": {
                "days": {"type": "integer", "description": "Lookback days", "default": 30},
            },
            "required": [],
        },
        _get_mood,
    ),
]
