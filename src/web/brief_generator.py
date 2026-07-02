"""Brief generation: assembles a persisted digest covering the window since the last brief.

Sections degrade independently: an LLM or search failure falls back to raw item
lists (or a quiet note) and never aborts the whole brief.
"""

from datetime import datetime, timedelta, timezone

import structlog

from web.brief_models import BriefConfig
from web.brief_store import BriefStore

logger = structlog.get_logger()

BRIEF_MAX_WINDOW_DAYS = 14
DEFAULT_FIRST_WINDOW_HOURS = 72
NOTHING_NEW = "Nothing new in this window."

SIGNALS_SYSTEM = (
    "You summarize a batch of news/intel items for a personal brief. Group related "
    "items by theme, keep it scannable markdown (short bullets, bold theme names), "
    "and never invent items that are not in the input."
)

JOURNAL_SYSTEM = (
    "You are a thoughtful personal advisor reviewing someone's recent journal "
    "entries. Produce short markdown with three parts: **Observations** (patterns "
    "you notice), **Feedback** (honest, kind), and **Suggestions** (2-3 concrete "
    "next actions). Ground everything in the entries; do not fabricate."
)

TOPIC_SYSTEM = (
    "You pick one concrete topic satisfying a standing instruction. Reply with "
    "the topic only - a short noun phrase, no quotes, no explanation."
)

CUSTOM_SYSTEM = (
    "You write one self-contained, well-organized markdown section for a personal "
    "brief, following the user's standing instruction. Be substantive but concise."
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _parse_ts(value) -> datetime | None:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
        except ValueError:
            return None
    return None


def _resolve_llm(user_id: str):
    """Return (llm, provider_name, api_key) or (None, None, None) when unavailable."""
    try:
        from llm import create_cheap_provider
        from web.deps_credentials import resolve_llm_credentials_for_user

        provider, api_key, _source = resolve_llm_credentials_for_user(user_id)
        if not api_key:
            return None, None, None
        return create_cheap_provider(provider=provider, api_key=api_key), provider, api_key
    except Exception as exc:
        logger.warning("brief.llm_unavailable", error=str(exc))
        return None, None, None


def _call_llm(llm, prompt: str, system: str, max_tokens: int = 900) -> str | None:
    if llm is None:
        return None
    try:
        response = llm.generate(
            messages=[{"role": "user", "content": prompt}],
            system=system,
            max_tokens=max_tokens,
        )
        text = (response or "").strip()
        return text or None
    except Exception as exc:
        logger.warning("brief.llm_call_failed", error=str(exc))
        return None


def _compute_window(store: BriefStore) -> tuple[datetime, datetime, bool]:
    """Return (period_start, period_end, capped)."""
    now = _utcnow()
    latest = store.get_latest()
    start = _parse_ts(latest["period_end"]) if latest else None
    if start is None:
        start = now - timedelta(hours=DEFAULT_FIRST_WINDOW_HOURS)
    capped = False
    floor = now - timedelta(days=BRIEF_MAX_WINDOW_DAYS)
    if start < floor:
        start = floor
        capped = True
    return start, now, capped


def _build_signals_section(user_id: str, since: datetime, llm, max_items: int) -> dict:
    items: list[dict] = []
    try:
        from web.deps_storage import get_user_intel_storage

        items = get_user_intel_storage(user_id).get_items_since(since, limit=max_items * 3)
    except Exception as exc:
        logger.warning("brief.signals_fetch_failed", error=str(exc))

    section = {"kind": "signals", "title": "What changed", "body": NOTHING_NEW, "items": []}
    if not items:
        return section

    section["items"] = [
        {
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "source": item.get("source", ""),
            "summary": (item.get("summary") or "")[:300],
        }
        for item in items[:max_items]
    ]
    listing = "\n".join(
        f"- [{item.get('source', '?')}] {item.get('title', '')}: {(item.get('summary') or '')[:220]}"
        for item in items
    )
    body = _call_llm(
        llm,
        f"Summarize these {len(items)} new items from my tracked sources:\n\n{listing}",
        SIGNALS_SYSTEM,
    )
    section["body"] = body or "\n".join(
        f"- {item.get('title', '')} ({item.get('source', '?')})" for item in items[:max_items]
    )
    return section


def _build_journal_section(user_id: str, since: datetime, llm, max_items: int) -> dict:
    section = {"kind": "journal", "title": "From your journal", "body": NOTHING_NEW, "items": []}

    entries: list[dict] = []
    try:
        from journal.storage import JournalStorage
        from storage_paths import get_user_paths

        storage = JournalStorage(get_user_paths(user_id)["journal_dir"])
        for entry in storage.list_entries(limit=40):
            created = _parse_ts(entry.get("created"))
            if created is None or created >= since:
                entries.append(entry)
            if len(entries) >= 15:
                break
    except Exception as exc:
        logger.warning("brief.journal_fetch_failed", error=str(exc))

    insights: list[dict] = []
    try:
        from web.deps_storage import get_insight_store

        insights = get_insight_store().get_active(limit=10)
    except Exception as exc:
        logger.warning("brief.insights_fetch_failed", error=str(exc))

    if not entries and not insights:
        return section

    section["items"] = [
        {"title": insight.get("title", ""), "detail": (insight.get("detail") or "")[:200]}
        for insight in insights[:max_items]
    ]

    entry_text = "\n\n".join(
        f"### {entry.get('title', 'Untitled')} ({entry.get('created', '')})\n"
        f"{(entry.get('preview') or '')[:500]}"
        for entry in entries
    )
    insight_text = "\n".join(
        f"- {insight.get('title', '')}: {(insight.get('detail') or '')[:150]}"
        for insight in insights
    )
    prompt = (
        f"Recent journal entries:\n{entry_text or '(none in this window)'}\n\n"
        f"Active detected insights:\n{insight_text or '(none)'}"
    )
    body = _call_llm(llm, prompt, JOURNAL_SYSTEM, max_tokens=1200)
    if body:
        section["body"] = body
    elif insights:
        section["body"] = "\n".join(
            f"- {insight.get('title', '')}" for insight in insights[:max_items]
        )
    elif entries:
        section["body"] = (
            f"{len(entries)} journal entries in this window. "
            "Add an LLM key to get observations and suggestions."
        )
    return section


def _build_custom_section(
    user_id: str, custom: dict, llm, provider, api_key, recent_topics: list[str]
) -> dict | None:
    instructions = (custom.get("instructions") or "").strip()
    if not instructions:
        return None

    title = (custom.get("title") or "").strip() or instructions[:60]
    section = {
        "kind": "custom",
        "title": title,
        "body": "",
        "sources": [],
        "researched": False,
        "topic": "",
    }

    avoid = "; ".join(recent_topics) if recent_topics else "(none yet)"
    topic = _call_llm(
        llm,
        f"Standing instruction: {instructions}\n\nTopics already covered recently "
        f"(pick something different): {avoid}",
        TOPIC_SYSTEM,
        max_tokens=60,
    )
    topic = (topic or "").strip().strip('"') or title
    section["topic"] = topic

    if custom.get("use_research"):
        try:
            from research import ResearchSynthesizer, WebSearchClient
            from web.deps_base import get_secret_key
            from web.user_store import get_user_secret

            tavily_key = None
            try:
                tavily_key = get_user_secret(user_id, "tavily_api_key", get_secret_key())
            except Exception:
                pass
            results = WebSearchClient(api_key=tavily_key).search(topic)
            if results:
                synthesizer = ResearchSynthesizer(api_key=api_key, provider=provider)
                section["body"] = synthesizer.synthesize(
                    topic, results, user_context=instructions, max_tokens=1500
                )
                section["sources"] = [
                    {"title": result.title, "url": result.url} for result in results[:6]
                ]
                section["researched"] = True
                return section
        except Exception as exc:
            logger.warning("brief.custom_research_failed", topic=topic, error=str(exc))

    body = _call_llm(
        llm,
        f"Standing instruction: {instructions}\n\nWrite this brief section on: {topic}",
        CUSTOM_SYSTEM,
        max_tokens=1500,
    )
    if not body:
        return None
    if custom.get("use_research"):
        body = "_Not web-researched this time._\n\n" + body
    section["body"] = body
    return section


def generate_brief(user_id: str, config: BriefConfig, store: BriefStore) -> dict:
    """Generate and persist the next brief for a user."""
    period_start, period_end, capped = _compute_window(store)
    llm, provider, api_key = _resolve_llm(user_id)

    sections: list[dict] = []
    if config.include_signals:
        sections.append(
            _build_signals_section(user_id, period_start, llm, config.max_items_per_section)
        )
    if config.include_journal:
        sections.append(
            _build_journal_section(user_id, period_start, llm, config.max_items_per_section)
        )

    recent_topics = store.recent_custom_topics()
    for custom in config.custom_sections:
        built = _build_custom_section(
            user_id, custom.model_dump(), llm, provider, api_key, recent_topics
        )
        if built:
            sections.append(built)
            if built.get("topic"):
                recent_topics.append(built["topic"])

    headline_parts = [
        section["title"]
        for section in sections
        if section.get("body") and section["body"] != NOTHING_NEW
    ]
    days = max(1, round((period_end - period_start).total_seconds() / 86400))
    summary = _call_llm(
        llm,
        "Write one plain sentence (max 25 words) summarizing this brief covering "
        f"the last {days} day(s). Sections with content: {', '.join(headline_parts) or 'none'}.",
        "You write a single friendly headline sentence for a personal brief. No markdown.",
        max_tokens=60,
    )
    if not summary:
        if headline_parts:
            summary = f"Covering the last {days} day(s): {', '.join(headline_parts)}."
        else:
            summary = f"All quiet over the last {days} day(s) - nothing new to report."
    if capped:
        summary += f" (Window capped at {BRIEF_MAX_WINDOW_DAYS} days.)"

    return store.save_brief(
        summary=summary,
        sections=sections,
        period_start=period_start.isoformat(),
        period_end=period_end.isoformat(),
    )
