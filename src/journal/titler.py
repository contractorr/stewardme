"""LLM-based title generation for journal entries."""

import structlog

logger = structlog.get_logger()

_SYSTEM = "You generate concise journal entry titles. Output ONLY the title, nothing else."
_PROMPT = (
    "Generate a brief title (3-8 words) for this journal entry. "
    "No quotes, no punctuation at the end.\n\n{content}"
)


def generate_title(content: str, llm_provider=None) -> str | None:
    """Generate a short title from entry content using cheap LLM.

    Returns title string, or None if generation fails (caller should fallback).
    """
    if not llm_provider:
        return None

    # Don't bother for very short content
    if len(content.strip()) < 20:
        return None

    try:
        # Truncate content to save tokens
        snippet = content[:1000]
        result = llm_provider.generate(
            messages=[{"role": "user", "content": _PROMPT.format(content=snippet)}],
            system=_SYSTEM,
            max_tokens=30,
        )
        title = result.strip().strip('"').strip("'").strip(".")
        if title and len(title) < 100:
            return title
    except Exception as e:
        logger.debug("title_generation_failed", error=str(e))

    return None
