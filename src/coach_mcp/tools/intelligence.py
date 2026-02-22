"""Intelligence MCP tools — search, recent items, trigger scrape."""

from coach_mcp.bootstrap import get_components


def _search(args: dict) -> dict:
    """Semantic search over scraped intelligence."""
    c = get_components()
    query = args["query"]
    limit = args.get("limit", 10)

    results = c["intel_search"].semantic_search(query, n_results=limit)

    return {
        "results": [
            {
                "id": r.get("id"),
                "source": r.get("source", ""),
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "summary": (r.get("summary") or "")[:500],
                "scraped_at": r.get("scraped_at", ""),
                "score": r.get("score"),
            }
            for r in results
        ],
        "count": len(results),
    }


def _get_recent(args: dict) -> dict:
    """Get recent intelligence items."""
    c = get_components()
    days = args.get("days", 7)
    limit = args.get("limit", 50)
    source = args.get("source")

    items = c["intel_storage"].get_recent(days=days, limit=limit)

    # Filter by source if specified
    if source:
        items = [i for i in items if i.get("source") == source]

    return {
        "items": [
            {
                "id": i.get("id"),
                "source": i.get("source", ""),
                "title": i.get("title", ""),
                "url": i.get("url", ""),
                "summary": (i.get("summary") or "")[:500],
                "scraped_at": i.get("scraped_at", ""),
            }
            for i in items
        ],
        "count": len(items),
    }


def _scrape_now(args: dict) -> dict:
    """Trigger all scrapers immediately."""
    c = get_components()

    from intelligence.scheduler import IntelScheduler

    scheduler = IntelScheduler(
        storage=c["intel_storage"],
        config=c["config"].get("intelligence", {}),
        journal_storage=c["storage"],
        embeddings=c["embeddings"],
        full_config=c["config"],
    )

    results = scheduler.run_now()

    # Sync intel embeddings after scrape
    synced = c["intel_search"].sync_embeddings()

    return {
        "scrape_results": results,
        "embeddings_synced": {"added": synced[0], "removed": synced[1]},
    }


def _events_upcoming(args: dict) -> dict:
    """Get upcoming events ranked by relevance."""
    c = get_components()
    from advisor.events import get_upcoming_events

    profile = None
    try:
        from profile.storage import ProfileStorage

        profile_path = c["config"].get("profile", {}).get("path", "~/coach/profile.yaml")
        ps = ProfileStorage(profile_path)
        profile = ps.load()
    except Exception:
        pass

    days = args.get("days", 90)
    limit = args.get("limit", 20)
    events = get_upcoming_events(c["intel_storage"], profile=profile, days=days, limit=limit)

    return {
        "events": [
            {
                "title": e.get("title", ""),
                "url": e.get("url", ""),
                "score": e.get("_score", 0),
                "event_date": e.get("_metadata", {}).get("event_date", ""),
                "location": e.get("_metadata", {}).get("location", ""),
                "cfp_deadline": e.get("_metadata", {}).get("cfp_deadline", ""),
                "online": e.get("_metadata", {}).get("online", False),
            }
            for e in events
        ],
        "count": len(events),
    }


TOOLS = [
    (
        "intel_search",
        {
            "description": "Semantic search over scraped intelligence articles and items.",
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "limit": {"type": "integer", "description": "Max results", "default": 10},
            },
            "required": ["query"],
        },
        _search,
    ),
    (
        "intel_get_recent",
        {
            "description": "Get recently scraped intelligence items, optionally filtered by source.",
            "type": "object",
            "properties": {
                "days": {"type": "integer", "description": "Lookback days", "default": 7},
                "limit": {"type": "integer", "description": "Max items", "default": 50},
                "source": {
                    "type": "string",
                    "description": "Filter by source (hackernews, reddit, rss, etc.)",
                },
            },
            "required": [],
        },
        _get_recent,
    ),
    (
        "intel_scrape_now",
        {
            "description": "Trigger all configured scrapers immediately and sync embeddings.",
            "type": "object",
            "properties": {},
            "required": [],
        },
        _scrape_now,
    ),
    (
        "events_upcoming",
        {
            "description": "Get upcoming tech events (conferences, meetups, workshops) ranked by relevance to user profile.",
            "type": "object",
            "properties": {
                "days": {
                    "type": "integer",
                    "description": "Lookback/forward window in days",
                    "default": 90,
                },
                "limit": {"type": "integer", "description": "Max events to return", "default": 20},
            },
            "required": [],
        },
        _events_upcoming,
    ),
]
