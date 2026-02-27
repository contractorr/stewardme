"""Heartbeat MCP tools — list and dismiss notifications."""

from pathlib import Path

from coach_mcp.bootstrap import get_components


def _list_notifications(args: dict) -> dict:
    """List active heartbeat notifications."""
    c = get_components()
    config = c.get("config", {})
    paths_config = config.get("paths", {})
    db_path = Path(paths_config.get("intel_db", "~/coach/intel.db")).expanduser()

    from intelligence.heartbeat import ActionBriefStore

    store = ActionBriefStore(db_path)
    notifications = store.get_active(limit=args.get("limit", 20))
    return {"notifications": notifications, "count": len(notifications)}


def _dismiss_notification(args: dict) -> dict:
    """Dismiss a heartbeat notification by ID."""
    c = get_components()
    config = c.get("config", {})
    paths_config = config.get("paths", {})
    db_path = Path(paths_config.get("intel_db", "~/coach/intel.db")).expanduser()

    from intelligence.heartbeat import ActionBriefStore

    store = ActionBriefStore(db_path)
    ok = store.dismiss(args["notification_id"])
    return {"dismissed": ok, "notification_id": args["notification_id"]}


TOOLS = [
    (
        "heartbeat_notifications",
        {
            "description": "List active (undismissed) heartbeat notifications — intel items matched to goals by the proactive heartbeat pipeline.",
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Max notifications to return",
                    "default": 20,
                },
            },
            "required": [],
        },
        _list_notifications,
    ),
    (
        "heartbeat_dismiss",
        {
            "description": "Dismiss a heartbeat notification so it won't resurface.",
            "type": "object",
            "properties": {
                "notification_id": {
                    "type": "integer",
                    "description": "ID of the notification to dismiss",
                },
            },
            "required": ["notification_id"],
        },
        _dismiss_notification,
    ),
]
