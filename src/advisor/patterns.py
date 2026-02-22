"""Higher-level pattern recognition — synthesizes signals into coaching insights."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional

import structlog

logger = structlog.get_logger()


@dataclass
class Pattern:
    type: str  # burnout, blind_spot, blocker_cycle, momentum
    confidence: float  # 0-1
    summary: str
    evidence: list[str] = field(default_factory=list)
    coaching_prompt: str = ""


class PatternDetector:
    """Detects high-level behavioral patterns from journal + goals data."""

    def __init__(self, journal_storage, embeddings=None, config: Optional[dict] = None):
        self.storage = journal_storage
        self.embeddings = embeddings
        self.config = config or {}

    def detect_all(self, lookback_days: int = 30) -> list[Pattern]:
        """Run all pattern detectors and return findings."""
        patterns = []
        detectors = [
            self._detect_burnout,
            self._detect_blind_spots,
            self._detect_momentum,
            self._detect_blocker_cycle,
        ]
        for detector in detectors:
            try:
                result = detector(lookback_days)
                if result:
                    patterns.append(result)
            except Exception as e:
                logger.warning("pattern_detector_error", detector=detector.__name__, error=str(e))
        return sorted(patterns, key=lambda p: p.confidence, reverse=True)

    def _detect_burnout(self, lookback_days: int) -> Optional[Pattern]:
        """3+ consecutive negative sentiment days + declining entry frequency."""
        try:
            from journal.sentiment import get_mood_history

            history = get_mood_history(self.storage, days=lookback_days)
        except Exception:
            return None

        if len(history) < 5:
            return None

        # Check consecutive negative streak from most recent
        consecutive_neg = 0
        for entry in reversed(history):
            if entry["score"] < -0.2:
                consecutive_neg += 1
            else:
                break

        if consecutive_neg < 3:
            return None

        # Check declining entry frequency (compare last 2 weeks)
        mid = (datetime.now() - timedelta(days=lookback_days // 2)).strftime("%Y-%m-%d")
        first_half = [e for e in history if e["date"] < mid]
        second_half = [e for e in history if e["date"] >= mid]

        freq_declining = len(second_half) < len(first_half) * 0.7 if first_half else False
        confidence = min(1.0, 0.5 + consecutive_neg * 0.1 + (0.2 if freq_declining else 0))

        evidence = [f"{consecutive_neg} consecutive negative days"]
        if freq_declining:
            evidence.append(f"Entry frequency dropped: {len(first_half)} -> {len(second_half)}")

        # Find recent positive entries for coaching
        recent_wins = [e["title"] for e in history if e["score"] > 0.2][-3:]

        coaching = "I notice a pattern of sustained negative mood"
        if freq_declining:
            coaching += " combined with less frequent journaling"
        coaching += ". This can signal burnout."
        if recent_wins:
            coaching += f" Remember your recent wins: {', '.join(recent_wins)}."
        coaching += " What's one small thing you could do today to recharge?"

        return Pattern(
            type="burnout",
            confidence=confidence,
            summary=f"Possible burnout: {consecutive_neg} consecutive negative days"
            + (" with declining activity" if freq_declining else ""),
            evidence=evidence,
            coaching_prompt=coaching,
        )

    def _detect_blind_spots(self, lookback_days: int) -> Optional[Pattern]:
        """Active goals with zero related journal entries (low embedding similarity)."""
        if not self.embeddings:
            return None

        try:
            from advisor.goals import GoalTracker

            tracker = GoalTracker(self.storage)
            goals = tracker.get_goals(include_inactive=False)
        except Exception:
            return None

        if not goals:
            return None

        blind_spots = []
        for goal in goals:
            if goal["status"] != "active":
                continue
            goal_text = f"{goal['title']} {goal.get('content', '')}"
            try:
                results = self.embeddings.query(goal_text, n_results=3)
                if not results:
                    blind_spots.append(goal["title"])
                    continue

                # Check if any result is recent and relevant
                cutoff = (datetime.now() - timedelta(days=lookback_days)).isoformat()
                recent_relevant = [
                    r
                    for r in results
                    if r.get("metadata", {}).get("created", "") >= cutoff
                    and r.get("distance", 1.0) < 0.7  # similarity > 0.3
                ]
                if not recent_relevant:
                    blind_spots.append(goal["title"])
            except Exception:
                continue

        if not blind_spots:
            return None

        return Pattern(
            type="blind_spot",
            confidence=min(1.0, 0.4 + len(blind_spots) * 0.2),
            summary=f"{len(blind_spots)} active goal(s) with no recent journal mentions",
            evidence=[f"Unmentioned: {g}" for g in blind_spots],
            coaching_prompt=f"You haven't written about {', '.join(blind_spots[:3])} recently. "
            "Are these goals still relevant? If so, what's one step you could take this week?",
        )

    def _detect_momentum(self, lookback_days: int) -> Optional[Pattern]:
        """3+ consecutive positive days + active goal progress."""
        try:
            from journal.sentiment import get_mood_history

            history = get_mood_history(self.storage, days=lookback_days)
        except Exception:
            return None

        if len(history) < 3:
            return None

        # Check consecutive positive streak
        consecutive_pos = 0
        for entry in reversed(history):
            if entry["score"] > 0.2:
                consecutive_pos += 1
            else:
                break

        if consecutive_pos < 3:
            return None

        # Check goal progress
        progressing_goals = []
        try:
            from advisor.goals import GoalTracker

            tracker = GoalTracker(self.storage)
            goals = tracker.get_goals(include_inactive=False)
            for goal in goals:
                if goal["status"] == "active" and goal.get("days_since_check", 999) < 7:
                    progressing_goals.append(goal["title"])
        except Exception:
            pass

        confidence = min(1.0, 0.4 + consecutive_pos * 0.1 + len(progressing_goals) * 0.15)

        evidence = [f"{consecutive_pos} consecutive positive days"]
        if progressing_goals:
            evidence.append(
                f"Active goals with recent check-ins: {', '.join(progressing_goals[:3])}"
            )

        coaching = f"You're on a {consecutive_pos}-day positive streak!"
        if progressing_goals:
            coaching += f" Great progress on {', '.join(progressing_goals[:2])}."
        coaching += " This is a good time to tackle something ambitious or set a stretch goal."

        return Pattern(
            type="momentum",
            confidence=confidence,
            summary=f"Positive momentum: {consecutive_pos}-day streak"
            + (f" with {len(progressing_goals)} goals progressing" if progressing_goals else ""),
            evidence=evidence,
            coaching_prompt=coaching,
        )

    def _detect_blocker_cycle(self, lookback_days: int) -> Optional[Pattern]:
        """Same negative keywords across 3+ entries in 14 days."""
        try:
            import re

            from journal.sentiment import analyze_sentiment

            entries = self.storage.list_entries(limit=50)
        except Exception:
            return None

        cutoff = (datetime.now() - timedelta(days=min(lookback_days, 14))).isoformat()

        _BLOCKER_KEYWORDS = {
            "stuck",
            "blocked",
            "struggling",
            "frustrated",
            "confused",
            "overwhelmed",
            "procrastinating",
            "impossible",
        }

        keyword_entries: dict[str, list[str]] = {}
        for entry in entries:
            if entry.get("created", "") < cutoff:
                continue
            try:
                post = self.storage.read(entry["path"])
                sentiment = analyze_sentiment(post.content)
                if sentiment["score"] >= 0:
                    continue
                words = set(re.findall(r"\b[a-z]+\b", post.content.lower()))
                for w in words & _BLOCKER_KEYWORDS:
                    keyword_entries.setdefault(w, []).append(
                        entry.get("title", entry.get("created", "")[:10])
                    )
            except Exception:
                continue

        # Find most recurring blocker
        worst = None
        worst_count = 0
        for kw, entries_list in keyword_entries.items():
            if len(entries_list) >= 3 and len(entries_list) > worst_count:
                worst = kw
                worst_count = len(entries_list)

        if not worst:
            return None

        return Pattern(
            type="blocker_cycle",
            confidence=min(1.0, 0.4 + worst_count * 0.15),
            summary=f"Recurring blocker: '{worst}' in {worst_count} entries",
            evidence=keyword_entries[worst][:5],
            coaching_prompt=f"I notice '{worst}' keeps coming up in your journal. "
            "This might be a systemic issue worth addressing directly. "
            "What would it take to break through this? Could you try a completely different approach?",
        )
