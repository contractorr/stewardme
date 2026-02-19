"""Project discovery MCP tools."""

from coach_mcp.bootstrap import get_components


def _projects_discover(args: dict) -> dict:
    """Find matching open-source issues."""
    c = get_components()
    from advisor.projects import get_matching_issues

    profile = None
    try:
        from profile.storage import ProfileStorage
        profile_path = c["config"].get("profile", {}).get("path", "~/coach/profile.yaml")
        ps = ProfileStorage(profile_path)
        profile = ps.load()
    except Exception:
        pass

    limit = args.get("limit", 20)
    days = args.get("days", 14)
    issues = get_matching_issues(c["intel_storage"], profile=profile, limit=limit, days=days)

    return {
        "issues": [
            {
                "title": i.get("title", ""),
                "url": i.get("url", ""),
                "summary": i.get("summary", "")[:300],
                "match_score": i.get("_match_score", 0),
            }
            for i in issues
        ],
        "count": len(issues),
    }


def _projects_ideas(args: dict) -> dict:
    """Get journal context for side-project idea generation (no LLM in MCP layer)."""
    c = get_components()

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
        "frustration problem idea project build wish", max_entries=10, max_chars=5000,
    )

    return {
        "profile": profile_ctx,
        "journal_context": journal_ctx,
        "instruction": "Generate side-project ideas based on the user's pain points, interests, and skills from journal entries.",
    }


def _projects_list(args: dict) -> dict:
    """List tracked project opportunities."""
    c = get_components()
    days = args.get("days", 14)
    items = c["intel_storage"].get_recent(days=days, limit=50)
    issues = [i for i in items if i.get("source") == "github_issues"]

    return {
        "issues": [
            {
                "title": i.get("title", ""),
                "url": i.get("url", ""),
                "summary": i.get("summary", "")[:300],
                "scraped_at": i.get("scraped_at", ""),
            }
            for i in issues
        ],
        "count": len(issues),
    }


TOOLS = [
    (
        "projects_discover",
        {
            "description": "Find open-source issues matching user's skills and interests.",
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "description": "Max issues", "default": 20},
                "days": {"type": "integer", "description": "Lookback window in days", "default": 14},
            },
            "required": [],
        },
        _projects_discover,
    ),
    (
        "projects_ideas",
        {
            "description": "Get context for generating side-project ideas from journal pain points.",
            "type": "object",
            "properties": {},
            "required": [],
        },
        _projects_ideas,
    ),
    (
        "projects_list",
        {
            "description": "List tracked project opportunities from GitHub issue scraping.",
            "type": "object",
            "properties": {
                "days": {"type": "integer", "description": "Lookback days", "default": 14},
            },
            "required": [],
        },
        _projects_list,
    ),
]
