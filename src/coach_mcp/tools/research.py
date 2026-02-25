"""Research MCP tools — topic suggestions, trigger deep research."""

from coach_mcp.bootstrap import get_components


def _get_scheduler():
    from intelligence.scheduler import IntelScheduler

    c = get_components()
    return IntelScheduler(
        storage=c["intel_storage"],
        config=c["config"].get("intelligence", {}),
        journal_storage=c["storage"],
        embeddings=c["embeddings"],
        full_config=c["config"],
    )


def _topics(args: dict) -> dict:
    """Auto-suggested research topics from journal/goals."""
    scheduler = _get_scheduler()
    topics = scheduler.get_research_topics()

    return {
        "topics": topics,
        "count": len(topics),
    }


def _run(args: dict) -> dict:
    """Trigger deep research (uses configured LLM for synthesis)."""
    scheduler = _get_scheduler()
    topic = args.get("topic")

    results = scheduler.run_research_now(topic=topic)

    return {
        "reports": [
            {
                "topic": r.get("topic", ""),
                "title": r.get("title", ""),
                "summary": (r.get("summary") or r.get("content", ""))[:1000],
                "sources_count": len(r.get("sources", [])),
                "saved_path": str(r.get("saved_path", "")),
            }
            for r in results
        ],
        "count": len(results),
    }


TOOLS = [
    (
        "research_topics",
        {
            "description": "[Experimental] Get auto-suggested research topics based on journal entries and goals.",
            "type": "object",
            "properties": {},
            "required": [],
        },
        _topics,
    ),
    (
        "research_run",
        {
            "description": "[Experimental] Run deep research on a topic (or auto-select). Uses configured LLM for synthesis.",
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "Specific topic to research (auto-selects if omitted)",
                },
            },
            "required": [],
        },
        _run,
    ),
]
