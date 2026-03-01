"""Prediction ledger MCP tools — list, review-due, stats."""

from pathlib import Path

from coach_mcp.bootstrap import get_components


def _list_predictions(args: dict) -> dict:
    c = get_components()
    config = c.get("config", {})
    db_path = Path(config.get("paths", {}).get("intel_db", "~/coach/intel.db")).expanduser()

    from predictions.store import PredictionStore

    store = PredictionStore(db_path)
    preds = store.get_all(
        category=args.get("category"),
        outcome=args.get("status"),
        limit=args.get("limit", 20),
    )
    return {"predictions": preds, "count": len(preds)}


def _review_predictions(args: dict) -> dict:
    c = get_components()
    config = c.get("config", {})
    db_path = Path(config.get("paths", {}).get("intel_db", "~/coach/intel.db")).expanduser()

    from predictions.store import PredictionStore

    store = PredictionStore(db_path)
    due = store.get_review_due(limit=3)
    return {"predictions": due, "count": len(due)}


def _prediction_stats(args: dict) -> dict:
    c = get_components()
    config = c.get("config", {})
    db_path = Path(config.get("paths", {}).get("intel_db", "~/coach/intel.db")).expanduser()

    from predictions.store import PredictionStore

    store = PredictionStore(db_path)
    return store.get_stats()


TOOLS = [
    (
        "predictions_list",
        {
            "description": "List predictions with optional filters by status and category.",
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "description": "Filter by outcome status",
                    "enum": ["pending", "confirmed", "rejected", "expired", "skipped"],
                },
                "category": {
                    "type": "string",
                    "description": "Filter by category",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max predictions to return",
                    "default": 20,
                },
            },
            "required": [],
        },
        _list_predictions,
    ),
    (
        "predictions_review",
        {
            "description": "Get predictions that are past their evaluation due date and need review.",
            "type": "object",
            "properties": {},
            "required": [],
        },
        _review_predictions,
    ),
    (
        "predictions_stats",
        {
            "description": "Get prediction accuracy statistics: per-category counts, per-confidence-bucket accuracy.",
            "type": "object",
            "properties": {},
            "required": [],
        },
        _prediction_stats,
    ),
]
