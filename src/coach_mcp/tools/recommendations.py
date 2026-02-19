"""Recommendations MCP tools — list, update status, rate."""

from coach_mcp.bootstrap import get_components


def _get_rec_storage():
    from advisor.recommendation_storage import RecommendationStorage
    from cli.utils import get_rec_db_path

    c = get_components()
    db_path = get_rec_db_path(c["config"])
    return RecommendationStorage(db_path)


def _list_recs(args: dict) -> dict:
    """List recent recommendations."""
    rec_storage = _get_rec_storage()
    limit = args.get("limit", 20)
    category = args.get("category")
    status = args.get("status")

    if category:
        recs = rec_storage.list_by_category(category, status=status, limit=limit)
    else:
        recs = rec_storage.list_recent(days=90, status=status, limit=limit)

    return {
        "recommendations": [
            {
                "id": r.id,
                "category": r.category,
                "title": r.title,
                "description": r.description,
                "rationale": r.rationale,
                "score": r.score,
                "status": r.status,
                "created_at": r.created_at,
            }
            for r in recs
        ],
        "count": len(recs),
    }


def _update_status(args: dict) -> dict:
    """Update recommendation status."""
    rec_storage = _get_rec_storage()
    rec_id = args["rec_id"]
    status = args["status"]

    success = rec_storage.update_status(rec_id, status)
    return {"success": success, "rec_id": rec_id, "status": status}


def _rate(args: dict) -> dict:
    """Rate a recommendation's usefulness."""
    rec_storage = _get_rec_storage()
    rec_id = args["rec_id"]
    rating = args["rating"]
    comment = args.get("comment")

    success = rec_storage.add_feedback(rec_id, rating, comment=comment)
    return {"success": success, "rec_id": rec_id, "rating": rating}


TOOLS = [
    (
        "recommendations_list",
        {
            "description": "List recent recommendations, optionally filtered by category or status.",
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "description": "Max results", "default": 20},
                "category": {
                    "type": "string",
                    "description": "Filter: learning, career, entrepreneurial, investment",
                },
                "status": {
                    "type": "string",
                    "description": "Filter by status",
                    "enum": ["suggested", "in_progress", "completed", "dismissed"],
                },
            },
            "required": [],
        },
        _list_recs,
    ),
    (
        "recommendations_update_status",
        {
            "description": "Update a recommendation's status.",
            "type": "object",
            "properties": {
                "rec_id": {"type": "integer", "description": "Recommendation ID"},
                "status": {
                    "type": "string",
                    "enum": ["suggested", "in_progress", "completed", "dismissed"],
                    "description": "New status",
                },
            },
            "required": ["rec_id", "status"],
        },
        _update_status,
    ),
    (
        "recommendations_rate",
        {
            "description": "Rate a recommendation's usefulness (1-5).",
            "type": "object",
            "properties": {
                "rec_id": {"type": "integer", "description": "Recommendation ID"},
                "rating": {
                    "type": "integer",
                    "description": "Rating from 1 to 5",
                    "minimum": 1,
                    "maximum": 5,
                },
                "comment": {"type": "string", "description": "Optional feedback comment"},
            },
            "required": ["rec_id", "rating"],
        },
        _rate,
    ),
]
