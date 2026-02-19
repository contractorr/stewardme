"""Simple keyword-based sentiment analysis for journal entries."""

import re
from datetime import datetime, timedelta

# Lexicon-based sentiment (no external deps needed)
_POSITIVE = {
    "great", "good", "excellent", "happy", "excited", "proud", "accomplished",
    "progress", "success", "win", "awesome", "fantastic", "love", "enjoy",
    "productive", "motivated", "inspired", "grateful", "thankful", "confident",
    "breakthrough", "solved", "achieved", "improved", "optimistic", "energized",
    "satisfied", "fun", "rewarding", "thriving", "focused", "clear",
}

_NEGATIVE = {
    "bad", "terrible", "frustrated", "stuck", "blocked", "stressed", "anxious",
    "overwhelmed", "exhausted", "burned", "burnout", "failed", "struggling",
    "confused", "worried", "disappointed", "tired", "difficult", "hard",
    "impossible", "lost", "behind", "procrastinating", "unmotivated", "drained",
    "angry", "annoyed", "boring", "painful", "hopeless", "doubt",
}


def analyze_sentiment(text: str) -> dict:
    """Analyze sentiment of text using keyword matching.

    Returns:
        {score: float (-1 to 1), label: str, positive_count: int, negative_count: int}
    """
    words = set(re.findall(r'\b[a-z]+\b', text.lower()))
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


def get_mood_history(journal_storage, days: int = 30) -> list[dict]:
    """Get mood timeline from journal entries.

    Returns list of {date, score, label, title} sorted by date.
    """
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    entries = journal_storage.list_entries(limit=200)

    timeline = []
    for entry in entries:
        created = entry.get("created", "")
        if created < cutoff:
            continue

        post = journal_storage.read(entry["path"])
        # Use frontmatter mood if already computed
        if post.get("mood"):
            sentiment = post["mood"]
        else:
            sentiment = analyze_sentiment(post.content)

        timeline.append({
            "date": created[:10],
            "score": sentiment.get("score", 0),
            "label": sentiment.get("label", "neutral"),
            "title": entry.get("title", ""),
        })

    timeline.sort(key=lambda x: x["date"])
    return timeline
