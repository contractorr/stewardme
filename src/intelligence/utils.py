"""Shared utilities for intelligence module."""

import structlog
from typing import Optional

logger = structlog.get_logger()


# Topic detection keywords - shared across scrapers
TOPIC_KEYWORDS = {
    "ai": ["ai", "llm", "gpt", "machine learning", "neural", "chatgpt", "claude"],
    "startup": ["startup", "founder", "yc", "funding", "venture", "series a"],
    "programming": ["rust", "python", "javascript", "golang", "typescript", "kotlin"],
    "career": ["hiring", "job", "career", "interview", "salary", "remote"],
    "security": ["security", "vulnerability", "breach", "hack", "privacy"],
    "crypto": ["crypto", "bitcoin", "ethereum", "blockchain", "web3"],
}


def detect_tags(title: str, prefixes: Optional[dict[str, str]] = None) -> list[str]:
    """Detect tags from title patterns.

    Args:
        title: Article/post title
        prefixes: Optional dict mapping prefix patterns to tags (e.g., {"Ask HN:": "ask-hn"})

    Returns:
        List of detected tags (max 5)
    """
    tags = []
    title_lower = title.lower()

    # Check prefix patterns
    if prefixes:
        for prefix, tag in prefixes.items():
            if title.startswith(prefix):
                tags.append(tag)
                break

    # Topic detection
    for tag, keywords in TOPIC_KEYWORDS.items():
        if any(kw in title_lower for kw in keywords):
            tags.append(tag)

    return tags[:5]


# HN-specific prefixes
HN_PREFIXES = {
    "Ask HN:": "ask-hn",
    "Show HN:": "show-hn",
    "Tell HN:": "tell-hn",
    "Launch HN:": "launch-hn",
}


def detect_hn_tags(title: str) -> list[str]:
    """Detect tags for Hacker News posts."""
    return detect_tags(title, prefixes=HN_PREFIXES)
