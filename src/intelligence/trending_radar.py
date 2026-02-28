"""Cross-source topic convergence — surfaces topics appearing across multiple scraped sources."""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path

import structlog

from db import wal_connect

logger = structlog.get_logger().bind(source="trending_radar")

STOPWORDS = frozenset(
    {
        "the",
        "and",
        "for",
        "are",
        "but",
        "not",
        "you",
        "all",
        "can",
        "her",
        "was",
        "one",
        "our",
        "out",
        "has",
        "had",
        "how",
        "its",
        "may",
        "new",
        "now",
        "old",
        "see",
        "way",
        "who",
        "did",
        "get",
        "let",
        "say",
        "she",
        "too",
        "use",
        "with",
        "this",
        "that",
        "have",
        "from",
        "they",
        "been",
        "will",
        "more",
        "when",
        "what",
        "some",
        "than",
        "them",
        "into",
        "only",
        "very",
        "just",
        "also",
        "about",
        "would",
        "there",
        "their",
        "which",
        "could",
        "other",
        "after",
        "first",
        "never",
        "where",
        "those",
        "every",
        "being",
        "these",
        "should",
        "because",
        "through",
        "before",
        "between",
        "using",
        "show",
        "shows",
        "based",
        "make",
        "made",
        "like",
        "does",
        "here",
        "most",
        "over",
        "such",
        "take",
        "well",
        "back",
        "then",
        "work",
        "year",
        "years",
        "really",
        "still",
        "need",
        "know",
        "want",
        "look",
        "think",
        "good",
        "much",
        "even",
        "same",
        "each",
        "many",
        "help",
        "something",
        "anything",
        "everything",
        "another",
        "things",
        "thing",
        "today",
        "best",
        "part",
        "long",
        "going",
        "getting",
        "making",
        "trying",
        "looking",
        "working",
        "building",
        "why",
        "what",
        "asks",
        "ask",
        "asked",
    }
)

_TERM_RE = re.compile(r"[a-z][a-z0-9\-]{2,}")


def _extract_title_terms(title: str) -> set[str]:
    """Extract meaningful lowercase tokens from a title, filtered against stopwords."""
    tokens = _TERM_RE.findall(title.lower())
    return {t for t in tokens if t not in STOPWORDS and len(t) >= 3}


class TrendingRadar:
    """Aggregates topics across intel sources by frequency, source diversity, and recency."""

    MAX_ROWS = 20

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path).expanduser()
        self._init_db()

    def _init_db(self):
        with wal_connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS trending_radar (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    computed_at TEXT NOT NULL,
                    snapshot_json TEXT NOT NULL
                )
                """
            )

    def compute(
        self,
        days: int = 7,
        min_sources: int = 2,
        max_topics: int = 15,
        weights: dict | None = None,
    ) -> dict:
        """Compute trending topics from recent intel items.

        Scoring: 0.4*norm_freq + 0.4*norm_diversity + 0.2*avg_recency
        Gate: topic must appear in >= min_sources distinct sources.
        """
        w = weights or {"freq": 0.4, "diversity": 0.4, "recency": 0.2}
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        now = datetime.now()

        with wal_connect(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT id, source, title, url, summary, scraped_at, tags
                FROM intel_items
                WHERE scraped_at >= ?
                ORDER BY scraped_at DESC
                LIMIT 2000
                """,
                (cutoff,),
            ).fetchall()

        if not rows:
            return {
                "computed_at": now.isoformat(),
                "days": days,
                "min_sources": min_sources,
                "total_items_scanned": 0,
                "topics": [],
            }

        # Build topic → items mapping
        topic_items: dict[str, list[dict]] = {}
        all_sources: set[str] = set()

        for row in rows:
            item_id, source, title, url, summary, scraped_at, tags_str = row
            all_sources.add(source)

            item = {
                "id": item_id,
                "source": source,
                "title": title,
                "url": url,
                "summary": (summary or "")[:200],
                "scraped_at": scraped_at,
            }

            # Collect terms from tags + title
            terms: set[str] = set()
            if tags_str:
                for tag in tags_str.split(","):
                    tag = tag.strip().lower()
                    if tag and tag not in STOPWORDS and len(tag) >= 3:
                        terms.add(tag)
            terms |= _extract_title_terms(title)

            for term in terms:
                topic_items.setdefault(term, []).append(item)

        total_active_sources = len(all_sources)

        # Score each topic
        max_item_count = max((len(items) for items in topic_items.values()), default=1)
        scored: list[dict] = []

        for topic, items in topic_items.items():
            sources = {i["source"] for i in items}
            if len(sources) < min_sources:
                continue

            norm_freq = len(items) / max_item_count if max_item_count else 0
            norm_diversity = len(sources) / total_active_sources if total_active_sources else 0

            # Recency: linear decay over `days` window
            recency_scores = []
            for i in items:
                try:
                    scraped = datetime.fromisoformat(i["scraped_at"])
                    hours_since = (now - scraped).total_seconds() / 3600
                    recency_scores.append(max(0.0, 1.0 - hours_since / (days * 24)))
                except (ValueError, TypeError):
                    recency_scores.append(0.0)
            avg_recency = sum(recency_scores) / len(recency_scores) if recency_scores else 0

            score = (
                w.get("freq", 0.4) * norm_freq
                + w.get("diversity", 0.4) * norm_diversity
                + w.get("recency", 0.2) * avg_recency
            )

            # Top-3 representative items (most recent, deduplicated by URL)
            seen_urls: set[str] = set()
            rep_items = []
            for i in sorted(items, key=lambda x: x["scraped_at"], reverse=True):
                if i["url"] not in seen_urls:
                    seen_urls.add(i["url"])
                    rep_items.append(i)
                if len(rep_items) >= 3:
                    break

            scored.append(
                {
                    "topic": topic,
                    "score": round(score, 3),
                    "item_count": len(items),
                    "source_count": len(sources),
                    "sources": sorted(sources),
                    "avg_recency": round(avg_recency, 3),
                    "items": rep_items,
                }
            )

        scored.sort(key=lambda x: x["score"], reverse=True)
        topics = scored[:max_topics]

        return {
            "computed_at": now.isoformat(),
            "days": days,
            "min_sources": min_sources,
            "total_items_scanned": len(rows),
            "topics": topics,
        }

    def refresh(self, **kwargs) -> dict:
        """Compute and persist a snapshot. Prunes old rows beyond MAX_ROWS."""
        snapshot = self.compute(**kwargs)
        with wal_connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO trending_radar (computed_at, snapshot_json) VALUES (?, ?)",
                (snapshot["computed_at"], json.dumps(snapshot)),
            )
            conn.execute(
                """
                DELETE FROM trending_radar
                WHERE id NOT IN (
                    SELECT id FROM trending_radar ORDER BY id DESC LIMIT ?
                )
                """,
                (self.MAX_ROWS,),
            )
        logger.info(
            "trending_radar.refreshed",
            topics=len(snapshot["topics"]),
            items_scanned=snapshot["total_items_scanned"],
        )
        return snapshot

    def load(self) -> dict | None:
        """Load most recent snapshot from DB, or None."""
        with wal_connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT snapshot_json FROM trending_radar ORDER BY id DESC LIMIT 1"
            ).fetchone()
        if not row:
            return None
        try:
            return json.loads(row[0])
        except (json.JSONDecodeError, TypeError):
            return None

    def get_or_compute(self, **kwargs) -> dict:
        """Return cached snapshot if available, otherwise compute fresh."""
        cached = self.load()
        if cached:
            return cached
        return self.refresh(**kwargs)
