"""Curriculum MCP tools — list guides, get chapters, progress, reviews, recommendations."""

from pathlib import Path


def _get_store():
    from coach_mcp.bootstrap import get_components

    components = get_components()
    paths = components.get("paths", {})
    data_dir = paths.get("data_dir", Path.home() / "coach")
    from curriculum.store import CurriculumStore

    return CurriculumStore(Path(data_dir) / "curriculum.db")


def _content_dirs():
    """Resolve content directories for chapter reading."""
    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    return [repo_root / "content" / "curriculum"]


def _read_chapter_content(chapter_id: str) -> str | None:
    parts = chapter_id.split("/", 1)
    if len(parts) != 2:
        return None
    guide_id, chapter_stem = parts
    filename = f"{chapter_stem}.md"
    for content_dir in _content_dirs():
        candidate = content_dir / guide_id / filename
        if candidate.is_file():
            return candidate.read_text(encoding="utf-8")
        if guide_id.startswith("industry-"):
            industry_name = guide_id[len("industry-") :]
            industries_dir = content_dir / "Industries"
            if industries_dir.is_dir():
                for subdir in industries_dir.iterdir():
                    if subdir.name.lower() == industry_name.lower():
                        candidate = subdir / filename
                        if candidate.is_file():
                            return candidate.read_text(encoding="utf-8")
    return None


def _list_guides(args: dict) -> dict:
    store = _get_store()
    category = args.get("category")
    track = args.get("track")
    guides = store.list_guides(category=category)
    if track:
        guides = [g for g in guides if g.get("track") == track]
    return {"guides": guides, "count": len(guides)}


def _get_chapter(args: dict) -> dict:
    chapter_id = args.get("chapter_id", "")
    if not chapter_id:
        return {"error": "chapter_id required"}
    store = _get_store()
    chapter = store.get_chapter(chapter_id)
    if not chapter:
        return {"error": f"Chapter not found: {chapter_id}"}
    content = _read_chapter_content(chapter_id)
    if content:
        chapter["content"] = content
    return chapter


def _get_progress(args: dict) -> dict:
    store = _get_store()
    stats = store.get_stats("")  # MCP is single-user context
    return stats.model_dump()


def _due_reviews(args: dict) -> dict:
    store = _get_store()
    limit = args.get("limit", 10)
    items = store.get_due_reviews("", limit=limit)
    return {"items": items, "count": len(items)}


def _recommend_next(args: dict) -> dict:
    import json

    store = _get_store()
    # 1. Continue last-read
    last = store.get_last_read_chapter("")
    if last:
        next_ch = store.get_next_chapter("", last["guide_id"])
        if next_ch:
            return {
                "guide_id": last["guide_id"],
                "chapter": next_ch,
                "reason": "Continue where you left off",
            }

    # 2. Next enrolled incomplete
    enrollments = store.get_enrollments("")
    for enrollment in enrollments:
        if enrollment.get("completed_at"):
            continue
        next_ch = store.get_next_chapter("", enrollment["guide_id"])
        if next_ch:
            guide = store.get_guide(enrollment["guide_id"])
            return {
                "guide_id": enrollment["guide_id"],
                "guide_title": guide["title"] if guide else "",
                "chapter": next_ch,
                "reason": "Continue enrolled guide",
            }

    # 3. Ready-to-start (prereqs completed)
    ready = store.get_ready_guides("")
    if ready:
        g = ready[0]
        return {
            "guide_id": g["id"],
            "guide_title": g["title"],
            "chapter": None,
            "reason": "Prerequisites complete — ready to start",
            "action": "enroll",
        }

    # 4. Entry-point (no prereqs)
    all_guides = store.list_guides()
    for g in all_guides:
        prereqs = g.get("prerequisites", [])
        if isinstance(prereqs, str):
            prereqs = json.loads(prereqs)
        if prereqs:
            continue
        if not store.is_enrolled("", g["id"]):
            return {
                "guide_id": g["id"],
                "guide_title": g["title"],
                "chapter": None,
                "reason": "Suggested entry point — no prerequisites",
                "action": "enroll",
            }

    return {"chapter": None, "reason": "No active reading session"}


def _skill_tree(args: dict) -> dict:
    store = _get_store()
    tree_data = store.get_tree_data("")
    edges = []
    for g in tree_data:
        for prereq_id in g.get("prerequisites", []):
            edges.append({"source": prereq_id, "target": g["id"]})
    return {"nodes": tree_data, "edges": edges}


TOOLS = [
    (
        "curriculum_list_guides",
        {
            "description": "List available curriculum guides with optional category filter. Returns guide metadata, chapter counts, and reading time estimates.",
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Filter by category",
                    "enum": [
                        "science",
                        "humanities",
                        "business",
                        "technology",
                        "industry",
                        "social_science",
                        "professional",
                    ],
                },
                "track": {
                    "type": "string",
                    "description": "Filter by skill tree track",
                    "enum": [
                        "foundations",
                        "natural_sciences",
                        "human_sciences",
                        "business_economics",
                        "technology",
                        "industry",
                    ],
                },
            },
            "required": [],
        },
        _list_guides,
    ),
    (
        "curriculum_get_chapter",
        {
            "description": "Get a specific curriculum chapter's content and metadata.",
            "type": "object",
            "properties": {
                "chapter_id": {
                    "type": "string",
                    "description": "Chapter ID (format: guide_id/chapter_stem)",
                },
            },
            "required": ["chapter_id"],
        },
        _get_chapter,
    ),
    (
        "curriculum_progress",
        {
            "description": "Get the user's learning progress — enrolled guides, completed chapters, reading time, review stats.",
            "type": "object",
            "properties": {},
            "required": [],
        },
        _get_progress,
    ),
    (
        "curriculum_due_reviews",
        {
            "description": "Get spaced repetition review items that are due. Returns questions from previously studied chapters.",
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Max items to return",
                    "default": 10,
                },
            },
            "required": [],
        },
        _due_reviews,
    ),
    (
        "curriculum_recommend_next",
        {
            "description": "Get a recommendation for what to study next based on current progress, enrollment, and prerequisite completion.",
            "type": "object",
            "properties": {},
            "required": [],
        },
        _recommend_next,
    ),
    (
        "curriculum_skill_tree",
        {
            "description": "Get the skill tree DAG: nodes (guides with progress/mastery/status) and edges (prerequisite relationships).",
            "type": "object",
            "properties": {},
            "required": [],
        },
        _skill_tree,
    ),
]
