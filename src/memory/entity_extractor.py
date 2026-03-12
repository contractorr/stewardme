"""Regex-based named entity extraction for memory fact text."""

import re

# Common sentence starters / generic words to skip
_SKIP_WORDS = frozenset(
    {
        "user",
        "the",
        "they",
        "their",
        "this",
        "that",
        "these",
        "those",
        "has",
        "have",
        "had",
        "was",
        "were",
        "been",
        "being",
        "will",
        "would",
        "could",
        "should",
        "might",
        "may",
        "also",
        "just",
        "very",
        "really",
        "about",
        "some",
        "new",
        "recently",
        "currently",
        "previously",
        "often",
        "after",
        "before",
        "since",
        "during",
        "while",
    }
)

# Multi-word proper nouns: 2+ consecutive Title-Case words
_PROPER_NOUN_RE = re.compile(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b")

# Standalone acronyms: 2+ uppercase letters (not inside a word)
_ACRONYM_RE = re.compile(r"\b([A-Z]{2,})\b")

# Single title-case word: proper noun anywhere in text (3+ chars)
_SINGLE_PROPER_RE = re.compile(r"\b([A-Z][a-z]{2,})\b")


def extract_entities(text: str) -> list[tuple[str, str]]:
    """Extract named entities from fact text via regex patterns.

    Returns deduplicated list of (original_name, normalized) tuples sorted by normalized.
    No LLM calls, no external dependencies — O(n) on input length.
    """
    if not text or not text.strip():
        return []

    # Map normalized -> original (first occurrence wins)
    entities: dict[str, str] = {}

    # Multi-word proper nouns: "Machine Learning", "San Francisco"
    for match in _PROPER_NOUN_RE.finditer(text):
        name = match.group(1).strip()
        normalized = name.lower()
        if not any(w in _SKIP_WORDS for w in normalized.split()):
            entities.setdefault(normalized, name)

    # Standalone acronyms: "AWS", "ML", "API"
    for match in _ACRONYM_RE.finditer(text):
        acronym = match.group(1)
        if len(acronym) >= 2:
            entities.setdefault(acronym.lower(), acronym)

    # Single proper nouns anywhere: "Python", "Django"
    for match in _SINGLE_PROPER_RE.finditer(text):
        word = match.group(1)
        normalized = word.lower()
        if normalized not in _SKIP_WORDS and len(word) >= 3:
            entities.setdefault(normalized, word)

    return sorted(
        ((orig, norm) for norm, orig in entities.items()),
        key=lambda t: t[1],
    )
