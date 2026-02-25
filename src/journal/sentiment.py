"""Simple keyword-based sentiment analysis for journal entries."""

import re

# Lexicon-based sentiment (no external deps needed)
_POSITIVE = {
    "great",
    "good",
    "excellent",
    "happy",
    "excited",
    "proud",
    "accomplished",
    "progress",
    "success",
    "win",
    "awesome",
    "fantastic",
    "love",
    "enjoy",
    "productive",
    "motivated",
    "inspired",
    "grateful",
    "thankful",
    "confident",
    "breakthrough",
    "solved",
    "achieved",
    "improved",
    "optimistic",
    "energized",
    "satisfied",
    "fun",
    "rewarding",
    "thriving",
    "focused",
    "clear",
}

_NEGATIVE = {
    "bad",
    "terrible",
    "frustrated",
    "stuck",
    "blocked",
    "stressed",
    "anxious",
    "overwhelmed",
    "exhausted",
    "burned",
    "burnout",
    "failed",
    "struggling",
    "confused",
    "worried",
    "disappointed",
    "tired",
    "difficult",
    "hard",
    "impossible",
    "lost",
    "behind",
    "procrastinating",
    "unmotivated",
    "drained",
    "angry",
    "annoyed",
    "boring",
    "painful",
    "hopeless",
    "doubt",
}


def analyze_sentiment(text: str) -> dict:
    """Analyze sentiment of text using keyword matching.

    Returns:
        {score: float (-1 to 1), label: str, positive_count: int, negative_count: int}
    """
    words = set(re.findall(r"\b[a-z]+\b", text.lower()))
    pos = len(words & _POSITIVE)
    neg = len(words & _NEGATIVE)
    total = pos + neg

    if total == 0:
        score = 0.0
        label = "neutral"
    else:
        score = (pos - neg) / total
        if score > 0.2:
            label = "positive"
        elif score < -0.2:
            label = "negative"
        else:
            label = "mixed"

    return {
        "score": round(score, 2),
        "label": label,
        "positive_count": pos,
        "negative_count": neg,
    }
