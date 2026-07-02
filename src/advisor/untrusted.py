"""Provenance tagging and guards for untrusted external (scraped) content.

Scraped third-party content (HN, Reddit, RSS, web search, …) flows into
advisor prompts. This module wraps that content in an explicit
``<untrusted_external_content>`` envelope so prompts can carry a standing
rule that it is data, never instructions, and provides the code-level guard
used by the agentic orchestrator to block outbound tool calls steered by
that content.
"""

from __future__ import annotations

import re

UNTRUSTED_TAG = "untrusted_external_content"
OPEN_TAG_PREFIX = f"<{UNTRUSTED_TAG}"
CLOSE_TAG = f"</{UNTRUSTED_TAG}>"

# Any literal open/close wrapper tag inside scraped text — escaped so content
# can neither break out of the wrapper nor spoof a new one.
_TAG_BREAKOUT_RE = re.compile(rf"</?\s*{UNTRUSTED_TAG}[^>]*>", re.IGNORECASE)

_OPEN_TAG_RE = re.compile(rf"<{UNTRUSTED_TAG}(?:\s[^>]*)?>")

# Retriever no-data placeholders — trusted strings, not scraped content.
_PLACEHOLDER_PREFIXES = (
    "No external intelligence",
    "No relevant intelligence",
)


def neutralize_breakouts(text: str) -> str:
    """Entity-escape literal wrapper tags inside untrusted text."""
    return _TAG_BREAKOUT_RE.sub(
        lambda m: m.group(0).replace("<", "&lt;").replace(">", "&gt;"), text
    )


def wrap_untrusted(text: str, source: str = "intel") -> str:
    """Wrap scraped content in the untrusted-content envelope.

    Empty strings, retriever placeholders, and already-wrapped text are
    returned unchanged.
    """
    if not text or not text.strip():
        return text
    stripped = text.strip()
    if stripped.startswith(OPEN_TAG_PREFIX) and stripped.endswith(CLOSE_TAG):
        return text
    if stripped.startswith(_PLACEHOLDER_PREFIXES):
        return text
    safe_source = re.sub(r"[^A-Za-z0-9_.:-]", "_", source or "unknown")
    body = neutralize_breakouts(text)
    return f'<{UNTRUSTED_TAG} source="{safe_source}">\n{body}\n</{UNTRUSTED_TAG}>'


def strip_untrusted_tags(text: str) -> str:
    """Remove wrapper tags, keeping content.

    Used before line-level operations (rerank, decomposed-retrieval merge)
    that would otherwise reorder or deduplicate the tag lines; callers must
    re-wrap the result.
    """
    return _TAG_BREAKOUT_RE.sub("", text).strip("\n")


def ensure_closed(text: str) -> str:
    """Append missing closing tags (wrapper truncated by token budget)."""
    if not text:
        return text
    opens = len(_OPEN_TAG_RE.findall(text))
    closes = text.count(CLOSE_TAG)
    if opens > closes:
        return text + ("\n" + CLOSE_TAG) * (opens - closes)
    return text


def _words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def contains_verbatim_span(
    candidate: str,
    untrusted_texts: list[str],
    span_words: int = 8,
) -> bool:
    """True if candidate shares >= span_words consecutive words with any untrusted text.

    Deliberately blunt: a word-level n-gram match catches copy-through of
    scraped content into outbound tool arguments, but misses paraphrases and
    can false-positive on long common phrases. That tradeoff is accepted for
    a simple, auditable guard.
    """
    cand_words = _words(candidate)
    if len(cand_words) < span_words:
        return False
    cand_grams = {
        tuple(cand_words[i : i + span_words]) for i in range(len(cand_words) - span_words + 1)
    }
    for text in untrusted_texts:
        words = _words(text)
        for i in range(len(words) - span_words + 1):
            if tuple(words[i : i + span_words]) in cand_grams:
                return True
    return False
