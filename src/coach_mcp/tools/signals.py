"""Signal MCP tools — list and acknowledge detected signals."""

from pathlib import Path

from coach_mcp.bootstrap import get_components


def _list_signals(args: dict) -> dict:
    """List active signals, optionally filtered by type/severity."""
    c = get_components()
    config = c.get("config", {})
    paths_config = config.get("paths", {})
    db_path = Path(paths_config.get("intel_db", "~/coach/intel.db")).expanduser()

    from advisor.signals import SignalStore

    store = SignalStore(db_path)
    signals = store.get_active(
        signal_type=args.get("type"),
        min_severity=args.get("min_severity", 1),
        limit=args.get("limit", 20),
    )
    return {"signals": signals, "count": len(signals)}


def _acknowledge_signal(args: dict) -> dict:
    """Mark a signal as acknowledged so it won't resurface."""
    c = get_components()
    config = c.get("config", {})
    paths_config = config.get("paths", {})
    db_path = Path(paths_config.get("intel_db", "~/coach/intel.db")).expanduser()

    from advisor.signals import SignalStore

    store = SignalStore(db_path)
    ok = store.acknowledge(args["signal_id"])
    return {"acknowledged": ok, "signal_id": args["signal_id"]}


TOOLS = [
    (
        "signals_list",
        {
            "description": "List active (unacknowledged) signals by type and severity. Signals detect stale goals, deadlines, emerging topics, etc.",
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "description": "Filter by signal type",
                    "enum": [
                        "topic_emergence",
                        "goal_stale",
                        "goal_complete",
                        "deadline_urgent",
                        "journal_gap",
                        "learning_stalled",
                        "research_trigger",
                        "recurring_blocker",
                        "prediction_review_due",
                    ],
                },
                "min_severity": {
                    "type": "integer",
                    "description": "Minimum severity (1-10)",
                    "default": 1,
                },
                "limit": {
                    "type": "integer",
                    "description": "Max signals to return",
                    "default": 20,
                },
            },
            "required": [],
        },
        _list_signals,
    ),
    (
        "signals_acknowledge",
        {
            "description": "Acknowledge a signal to mark it as acted on. Prevents it from resurfacing.",
            "type": "object",
            "properties": {
                "signal_id": {
                    "type": "integer",
                    "description": "ID of the signal to acknowledge",
                },
            },
            "required": ["signal_id"],
        },
        _acknowledge_signal,
    ),
]
