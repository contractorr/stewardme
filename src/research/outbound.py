"""Outbound query hygiene and audit logging for research web searches.

Research topics are derived from journal themes and goals, so raw candidate
queries can contain personal, first-person text. Nothing leaves the machine
without passing ``sanitize_outbound_query`` and being recorded by
``OutboundLogger`` first.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import structlog

logger = structlog.get_logger()

# Queries containing any of these are dropped outright — emotional/personal
# content has no business in a web search. Guardrail, not NLP.
FEELINGS_VOCAB = {
    "feel",
    "feels",
    "felt",
    "feeling",
    "feelings",
    "anxious",
    "anxiety",
    "worried",
    "worry",
    "worrying",
    "scared",
    "afraid",
    "fear",
    "fears",
    "stressed",
    "stress",
    "burnout",
    "burned",
    "exhausted",
    "depressed",
    "depression",
    "overwhelmed",
    "lonely",
    "sad",
    "angry",
    "frustrated",
    "ashamed",
    "guilty",
    "hopeless",
    "insecure",
    "crying",
    "therapy",
    "therapist",
}

FIRST_PERSON = {
    "i",
    "i'm",
    "im",
    "i've",
    "ive",
    "i'd",
    "me",
    "my",
    "mine",
    "myself",
    "we",
    "our",
    "ours",
    "us",
    "ourselves",
}

# Removed when reducing a sentence-like query to its content-word core.
_FUNCTION_WORDS = {
    "a",
    "an",
    "the",
    "and",
    "or",
    "but",
    "if",
    "then",
    "so",
    "to",
    "of",
    "for",
    "in",
    "on",
    "at",
    "by",
    "with",
    "about",
    "from",
    "as",
    "is",
    "am",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "do",
    "does",
    "did",
    "have",
    "has",
    "had",
    "will",
    "would",
    "can",
    "could",
    "should",
    "must",
    "might",
    "that",
    "this",
    "these",
    "those",
    "it",
    "its",
    "what",
    "when",
    "where",
    "how",
    "why",
    "who",
    "not",
    "no",
    "really",
    "more",
    "want",
    "wants",
    "wanted",
    "need",
    "needs",
    "think",
    "keep",
    "get",
    "getting",
    "learn",
    "understand",
    "know",
    "like",
}

MAX_QUERY_WORDS = 10


def sanitize_outbound_query(query: str, max_words: int = MAX_QUERY_WORDS) -> str | None:
    """Reduce a candidate query to a topic/entity phrase, or drop it.

    Returns the sanitized query, or ``None`` when the query must not be
    sent (empty, or contains feelings vocabulary).
    """
    text = (query or "").strip()
    if not text:
        return None

    words = re.findall(r"[A-Za-z0-9][\w'+#.&-]*", text)
    pairs = [(w, w.lower().strip("'.")) for w in words]
    if any(lw in FEELINGS_VOCAB for _, lw in pairs):
        return None

    kept = [(w, lw) for w, lw in pairs if lw not in FIRST_PERSON]
    sentence_like = len(kept) != len(pairs) or len(pairs) > max_words
    if sentence_like:
        # Approximate the noun-phrase core: content words only.
        kept = [(w, lw) for w, lw in kept if lw not in _FUNCTION_WORDS]

    result = [w for w, _ in kept[:max_words]]
    if not result:
        return None
    return " ".join(result)


class OutboundLogger:
    """Append-only JSONL audit log of every query sent to a search provider.

    Recording happens before the query is issued; IO errors propagate so an
    unloggable query is never sent.
    """

    def __init__(self, log_path: Path | None = None):
        self._log_path = Path(log_path) if log_path else None

    @property
    def log_path(self) -> Path:
        if self._log_path is None:
            from storage_paths import get_coach_home

            self._log_path = get_coach_home() / "research" / "outbound_log.jsonl"
        return self._log_path

    def record(self, query: str, provider: str) -> dict:
        """Persist and return an audit entry for a query about to be sent."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "query": query,
            "provider": provider,
        }
        path = self.log_path
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return entry
