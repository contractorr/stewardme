"""Signal detection engine — scans data sources, produces prioritized actionable signals."""

import hashlib
import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Optional

import structlog

logger = structlog.get_logger()


class SignalType(str, Enum):
    SENTIMENT_ALERT = "sentiment_alert"
    TOPIC_EMERGENCE = "topic_emergence"
    GOAL_STALE = "goal_stale"
    GOAL_COMPLETE_CANDIDATE = "goal_complete"
    DEADLINE_URGENT = "deadline_urgent"
    JOURNAL_GAP = "journal_gap"
    LEARNING_STALLED = "learning_stalled"
    RESEARCH_TRIGGER = "research_trigger"
    RECURRING_BLOCKER = "recurring_blocker"


@dataclass
class Signal:
    type: SignalType
    severity: int  # 1-10
    title: str
    detail: str
    suggested_actions: list[str]
    evidence: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    acknowledged: bool = False

    def signal_hash(self) -> str:
        """Dedup hash based on type + title."""
        text = f"{self.type.value}|{self.title}"
        return hashlib.sha256(text.encode()).hexdigest()[:16]


class SignalStore:
    """SQLite persistence for signals in existing intel.db."""

    def __init__(self, db_path: Path):
        self.db_path = Path(db_path).expanduser()
        self._init_tables()

    def _init_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS signals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    severity INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    detail TEXT,
                    evidence_json TEXT,
                    actions_json TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    acknowledged INTEGER DEFAULT 0,
                    signal_hash TEXT UNIQUE
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_signals_type ON signals(type)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_signals_ack ON signals(acknowledged)
            """)

    def save(self, signal: Signal) -> bool:
        """Save signal, skip if duplicate hash exists and is unacknowledged."""
        h = signal.signal_hash()
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Check for existing unacknowledged signal with same hash
                existing = conn.execute(
                    "SELECT id FROM signals WHERE signal_hash = ? AND acknowledged = 0",
                    (h,),
                ).fetchone()
                if existing:
                    return False

                # Delete old acknowledged version if any, then insert fresh
                conn.execute("DELETE FROM signals WHERE signal_hash = ?", (h,))
                conn.execute(
                    """INSERT INTO signals
                    (type, severity, title, detail, evidence_json, actions_json,
                     created_at, expires_at, acknowledged, signal_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        signal.type.value,
                        signal.severity,
                        signal.title,
                        signal.detail,
                        json.dumps(signal.evidence),
                        json.dumps(signal.suggested_actions),
                        signal.created_at.isoformat(),
                        signal.expires_at.isoformat() if signal.expires_at else None,
                        0,
                        h,
                    ),
                )
                return True
        except sqlite3.Error as e:
            logger.error("signal_save_error", error=str(e))
            return False

    def get_active(
        self,
        signal_type: Optional[str] = None,
        min_severity: int = 1,
        limit: int = 20,
    ) -> list[dict]:
        """Get active (unacknowledged, unexpired) signals."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            query = """
                SELECT * FROM signals
                WHERE acknowledged = 0
                AND (expires_at IS NULL OR expires_at > ?)
                AND severity >= ?
            """
            params: list = [datetime.now().isoformat(), min_severity]
            if signal_type:
                query += " AND type = ?"
                params.append(signal_type)
            query += " ORDER BY severity DESC, created_at DESC LIMIT ?"
            params.append(limit)
            rows = conn.execute(query, params).fetchall()
            return [self._row_to_dict(r) for r in rows]

    def acknowledge(self, signal_id: int) -> bool:
        """Mark signal as acknowledged."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE signals SET acknowledged = 1 WHERE id = ?", (signal_id,))
            return conn.total_changes > 0

    @staticmethod
    def _row_to_dict(row) -> dict:
        d = dict(row)
        d["evidence"] = json.loads(d.pop("evidence_json", "[]") or "[]")
        d["suggested_actions"] = json.loads(d.pop("actions_json", "[]") or "[]")
        return d


class SignalDetector:
    """Scans all data sources and produces prioritized signals."""

    def __init__(self, journal_storage, db_path: Path, config: Optional[dict] = None):
        self.storage = journal_storage
        self.db_path = Path(db_path).expanduser()
        self.config = config or {}
        self.agent_config = self.config.get("agent", {}).get("signals", {})
        self.store = SignalStore(self.db_path)

    def detect_all(self) -> list[Signal]:
        """Run all detectors, persist new signals, return active list."""
        signals = []
        detectors = [
            self._detect_sentiment,
            self._detect_goal_staleness,
            self._detect_goal_completion,
            self._detect_journal_gap,
            self._detect_topic_emergence,
            self._detect_deadlines,
            self._detect_learning_stalled,
            self._detect_research_triggers,
            self._detect_recurring_blockers,
        ]
        for detector in detectors:
            try:
                signals.extend(detector())
            except Exception as e:
                logger.warning("signal_detector_error", detector=detector.__name__, error=str(e))

        # Persist
        for s in signals:
            self.store.save(s)

        return sorted(signals, key=lambda s: s.severity, reverse=True)

    # --- Detectors ---

    def _detect_sentiment(self) -> list[Signal]:
        """Detect sustained negative mood (3+ consecutive negative days or avg < -0.3 over 7 days)."""
        try:
            from journal.sentiment import get_mood_history

            history = get_mood_history(self.storage, days=14)
        except Exception:
            return []

        if len(history) < 3:
            return []

        signals = []
        threshold = self.agent_config.get("sentiment_consecutive_negative", 3)

        # Check consecutive negative days
        consecutive_neg = 0
        neg_entries = []
        for entry in reversed(history):
            if entry["score"] < -0.2:
                consecutive_neg += 1
                neg_entries.append(entry.get("title", entry["date"]))
            else:
                break

        if consecutive_neg >= threshold:
            signals.append(
                Signal(
                    type=SignalType.SENTIMENT_ALERT,
                    severity=min(8, 5 + consecutive_neg),
                    title=f"Negative mood for {consecutive_neg} consecutive days",
                    detail=f"Sentiment has been negative for the last {consecutive_neg} entries. This may indicate burnout or sustained stress.",
                    suggested_actions=[
                        "Take a break or do something restorative",
                        "Review recent wins and accomplishments",
                        "Consider journaling about what's causing the stress",
                    ],
                    evidence=neg_entries[:5],
                    expires_at=datetime.now() + timedelta(days=3),
                )
            )

        # Check 7-day average
        recent_7d = [
            e
            for e in history
            if e["date"] >= (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        ]
        if len(recent_7d) >= 3:
            avg_score = sum(e["score"] for e in recent_7d) / len(recent_7d)
            if avg_score < -0.3:
                signals.append(
                    Signal(
                        type=SignalType.SENTIMENT_ALERT,
                        severity=7,
                        title=f"Weekly mood average is low ({avg_score:.2f})",
                        detail="Average sentiment over the past 7 days is significantly negative.",
                        suggested_actions=[
                            "Reflect on what's been weighing on you",
                            "Consider talking to someone about current challenges",
                        ],
                        evidence=[f"7-day avg: {avg_score:.2f} across {len(recent_7d)} entries"],
                        expires_at=datetime.now() + timedelta(days=7),
                    )
                )

        return signals

    def _detect_goal_staleness(self) -> list[Signal]:
        """Detect goals with no check-in past threshold."""
        try:
            from advisor.goals import GoalTracker

            tracker = GoalTracker(self.storage)
            stale = tracker.get_stale_goals()
        except Exception:
            return []

        signals = []
        for goal in stale:
            days = goal.get("days_since_check", 0)
            signals.append(
                Signal(
                    type=SignalType.GOAL_STALE,
                    severity=min(8, 4 + days // 7),
                    title=f"Goal stale: {goal['title']}",
                    detail=f"No check-in in {days} days (threshold: {goal.get('check_in_days', 14)}).",
                    suggested_actions=[
                        f"Check in on '{goal['title']}'",
                        "Update progress or pause if no longer relevant",
                    ],
                    evidence=[str(goal.get("path", ""))],
                    expires_at=datetime.now() + timedelta(days=7),
                )
            )
        return signals

    def _detect_goal_completion(self) -> list[Signal]:
        """Detect goals where all milestones are done but status != completed."""
        try:
            from advisor.goals import GoalTracker

            tracker = GoalTracker(self.storage)
            goals = tracker.get_goals(include_inactive=False)
        except Exception:
            return []

        signals = []
        for goal in goals:
            if goal["status"] != "active":
                continue
            try:
                progress = tracker.get_progress(goal["path"])
                if progress["total"] > 0 and progress["completed"] == progress["total"]:
                    signals.append(
                        Signal(
                            type=SignalType.GOAL_COMPLETE_CANDIDATE,
                            severity=6,
                            title=f"Goal ready to complete: {goal['title']}",
                            detail=f"All {progress['total']} milestones are done but goal is still marked active.",
                            suggested_actions=[
                                f"Mark '{goal['title']}' as completed",
                                "Celebrate the achievement!",
                            ],
                            evidence=[str(goal.get("path", ""))],
                        )
                    )
            except Exception:
                continue
        return signals

    def _detect_journal_gap(self) -> list[Signal]:
        """Detect no journal entries in 7+ days."""
        try:
            entries = self.storage.list_entries(limit=5)
        except Exception:
            return []

        if not entries:
            return [
                Signal(
                    type=SignalType.JOURNAL_GAP,
                    severity=5,
                    title="No journal entries found",
                    detail="Start journaling to get personalized coaching.",
                    suggested_actions=["Write a quick daily reflection"],
                )
            ]

        latest = entries[0]
        created = latest.get("created", "")
        if not created:
            return []

        try:
            dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            if dt.tzinfo:
                dt = dt.replace(tzinfo=None)
            days_ago = (datetime.now() - dt).days
        except (ValueError, OSError):
            return []

        if days_ago >= 7:
            return [
                Signal(
                    type=SignalType.JOURNAL_GAP,
                    severity=min(7, 4 + days_ago // 7),
                    title=f"No journal entries in {days_ago} days",
                    detail="Regular journaling helps track progress and detect patterns.",
                    suggested_actions=[
                        "Write a quick reflection on this week",
                        "Use a template: daily, weekly, or goal check-in",
                    ],
                    evidence=[f"Last entry: {created[:10]}"],
                    expires_at=datetime.now() + timedelta(days=3),
                )
            ]
        return []

    def _detect_topic_emergence(self) -> list[Signal]:
        """Detect emerging topics (high growth rate) not in active goals."""
        try:
            from pathlib import Path as P

            from journal import EmbeddingManager, JournalSearch
            from journal.trends import TrendDetector

            paths_config = self.config.get("paths", {})
            chroma_dir = P(paths_config.get("chroma_dir", "~/coach/chroma")).expanduser()
            embeddings = EmbeddingManager(chroma_dir)
            search = JournalSearch(self.storage, embeddings)
            detector = TrendDetector(search)
            emerging = detector.get_emerging_topics(threshold=0.3)
        except Exception:
            return []

        if not emerging:
            return []

        # Get active goal titles for filtering
        try:
            from advisor.goals import GoalTracker

            goal_titles = {g["title"].lower() for g in GoalTracker(self.storage).get_goals()}
        except Exception:
            goal_titles = set()

        signals = []
        for topic in emerging[:3]:
            topic_name = topic["topic"]
            # Skip if already tracked as a goal
            if any(topic_name.lower() in gt for gt in goal_titles):
                continue
            signals.append(
                Signal(
                    type=SignalType.TOPIC_EMERGENCE,
                    severity=min(7, 4 + int(topic["growth_rate"] * 5)),
                    title=f"Emerging topic: {topic_name}",
                    detail=f"Topic '{topic_name}' is growing ({topic['growth_rate']:+.0%}) across {topic['total_entries']} entries but isn't tracked as a goal.",
                    suggested_actions=[
                        f"Create a goal around '{topic_name}'",
                        f"Research '{topic_name}' in depth",
                    ],
                    evidence=topic.get("representative_titles", []),
                    expires_at=datetime.now() + timedelta(days=14),
                )
            )
        return signals

    def _detect_deadlines(self) -> list[Signal]:
        """Detect upcoming events/CFPs within 14 days."""
        try:
            from advisor.events import get_upcoming_events
            from intelligence.scraper import IntelStorage

            intel = IntelStorage(self.db_path)
            events = get_upcoming_events(intel, days=30, min_score=3.0)
        except Exception:
            return []

        warning_days = self.agent_config.get("deadline_warning_days", 14)
        signals = []
        for event in events[:5]:
            meta = event.get("_metadata", {})
            cfp = meta.get("cfp_deadline", "")
            if cfp:
                try:
                    deadline = datetime.fromisoformat(cfp)
                    days_until = (deadline - datetime.now()).days
                    if 0 < days_until <= warning_days:
                        signals.append(
                            Signal(
                                type=SignalType.DEADLINE_URGENT,
                                severity=min(9, 6 + (warning_days - days_until) // 3),
                                title=f"CFP closing in {days_until} days: {event['title'][:60]}",
                                detail=f"Call for proposals closes {cfp[:10]}.",
                                suggested_actions=[
                                    "Review submission requirements",
                                    "Draft proposal outline",
                                ],
                                evidence=[event.get("url", "")],
                                expires_at=deadline,
                            )
                        )
                except ValueError:
                    pass
        return signals

    def _detect_learning_stalled(self) -> list[Signal]:
        """Detect learning paths with no progress in 14+ days."""
        try:
            from advisor.learning_paths import LearningPathStorage

            lp_dir = self.config.get("learning_paths", {}).get("dir", "~/coach/learning_paths")
            lp_storage = LearningPathStorage(lp_dir)
            active = lp_storage.list_paths(status="active")
        except Exception:
            return []

        signals = []
        for path in active:
            updated = path.get("updated_at") or path.get("created_at", "")
            if not updated:
                continue
            try:
                updated_dt = datetime.fromisoformat(updated)
                days_stalled = (datetime.now() - updated_dt).days
                if days_stalled > 14:
                    signals.append(
                        Signal(
                            type=SignalType.LEARNING_STALLED,
                            severity=min(6, 3 + days_stalled // 14),
                            title=f"Learning stalled: {path.get('skill', 'Unknown')}",
                            detail=f"No progress in {days_stalled} days on '{path.get('skill', 'Unknown')}'.",
                            suggested_actions=[
                                f"Resume learning '{path.get('skill', '')}'",
                                "Adjust the learning path if it's too ambitious",
                            ],
                            evidence=[str(path.get("path", ""))],
                            expires_at=datetime.now() + timedelta(days=7),
                        )
                    )
            except ValueError:
                continue
        return signals

    def _detect_research_triggers(self) -> list[Signal]:
        """Detect topics mentioned 3+ times in 7 days with no existing research."""
        try:
            entries = self.storage.list_entries(limit=50)
        except Exception:
            return []

        threshold = self.agent_config.get("topic_mention_threshold", 3)
        cutoff = (datetime.now() - timedelta(days=7)).isoformat()

        # Count tag frequency in recent entries
        tag_counts: dict[str, int] = {}
        for entry in entries:
            if entry.get("created", "") < cutoff:
                continue
            for tag in entry.get("tags", []):
                tag_lower = tag.lower()
                tag_counts[tag_lower] = tag_counts.get(tag_lower, 0) + 1

        # Check for existing research on these topics
        research_entries = self.storage.list_entries(entry_type="research", limit=50)
        researched_topics = set()
        for r in research_entries:
            researched_topics.add(r.get("title", "").lower())
            for t in r.get("tags", []):
                researched_topics.add(t.lower())

        signals = []
        for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True):
            if count >= threshold and tag not in researched_topics:
                signals.append(
                    Signal(
                        type=SignalType.RESEARCH_TRIGGER,
                        severity=min(6, 3 + count),
                        title=f"Research opportunity: {tag}",
                        detail=f"Topic '{tag}' mentioned {count} times this week with no existing research.",
                        suggested_actions=[
                            f"Run deep research on '{tag}'",
                            f"Create a goal around '{tag}'",
                        ],
                        evidence=[f"{count} mentions in 7 days"],
                        expires_at=datetime.now() + timedelta(days=14),
                    )
                )
        return signals[:3]

    def _detect_recurring_blockers(self) -> list[Signal]:
        """Detect same negative keywords appearing in 3+ entries within 14 days."""
        try:
            from journal.sentiment import analyze_sentiment

            entries = self.storage.list_entries(limit=50)
        except Exception:
            return []

        cutoff = (datetime.now() - timedelta(days=14)).isoformat()
        blocker_words: dict[str, list[str]] = {}

        _BLOCKER_KEYWORDS = {
            "stuck",
            "blocked",
            "struggling",
            "frustrated",
            "confused",
            "overwhelmed",
            "procrastinating",
            "difficult",
            "impossible",
        }

        for entry in entries:
            if entry.get("created", "") < cutoff:
                continue
            try:
                post = self.storage.read(entry["path"])
                text = post.content.lower()
                sentiment = analyze_sentiment(post.content)
                if sentiment["score"] >= 0:
                    continue

                import re

                words = set(re.findall(r"\b[a-z]+\b", text))
                found = words & _BLOCKER_KEYWORDS
                for w in found:
                    if w not in blocker_words:
                        blocker_words[w] = []
                    blocker_words[w].append(entry.get("title", entry.get("created", "")[:10]))
            except Exception:
                continue

        signals = []
        for keyword, occurrences in blocker_words.items():
            if len(occurrences) >= 3:
                signals.append(
                    Signal(
                        type=SignalType.RECURRING_BLOCKER,
                        severity=min(8, 5 + len(occurrences)),
                        title=f"Recurring blocker: '{keyword}'",
                        detail=f"The word '{keyword}' appears in {len(occurrences)} negative entries over 14 days. This may indicate a persistent problem.",
                        suggested_actions=[
                            f"Reflect on what's causing you to feel '{keyword}'",
                            "Break the problem into smaller actionable steps",
                            "Consider seeking help or a different approach",
                        ],
                        evidence=occurrences[:5],
                        expires_at=datetime.now() + timedelta(days=7),
                    )
                )
        return signals
