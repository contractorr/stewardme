"""Cross-source topic convergence — surfaces topics appearing across multiple scraped sources."""

import json
import math
import re
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

import structlog

from db import wal_connect

logger = structlog.get_logger().bind(source="trending_radar")

STOPWORDS = frozenset(
    {
        # Articles, pronouns, prepositions, conjunctions
        "a",
        "an",
        "at",
        "be",
        "by",
        "do",
        "go",
        "if",
        "in",
        "it",
        "me",
        "my",
        "no",
        "of",
        "on",
        "or",
        "so",
        "to",
        "up",
        "us",
        "we",
        "the",
        "and",
        "for",
        "are",
        "but",
        "not",
        "you",
        "your",
        "all",
        "can",
        "is",
        "her",
        "his",
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
        "while",
        "during",
        "without",
        "within",
        "against",
        "along",
        "above",
        "below",
        "under",
        "since",
        "until",
        "upon",
        # Common verbs / verb forms
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
        "really",
        "still",
        "need",
        "know",
        "want",
        "look",
        "think",
        "much",
        "even",
        "same",
        "each",
        "many",
        "help",
        "come",
        "came",
        "goes",
        "gone",
        "going",
        "getting",
        "making",
        "trying",
        "looking",
        "working",
        "building",
        "become",
        "becomes",
        "start",
        "starts",
        "started",
        "bring",
        "brings",
        "keep",
        "keeps",
        "turn",
        "turns",
        "move",
        "moves",
        "run",
        "runs",
        "running",
        "says",
        "said",
        "told",
        "tells",
        "gives",
        "given",
        "finds",
        "found",
        "puts",
        "read",
        "reads",
        "write",
        "writes",
        "learn",
        "learned",
        "used",
        "needs",
        "wants",
        "built",
        "create",
        "created",
        "creates",
        "update",
        "updated",
        "adds",
        "added",
        "inside",
        # Generic nouns too common in tech news to be meaningful
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
        "people",
        "world",
        "time",
        "times",
        "data",
        "code",
        "tool",
        "tools",
        "app",
        "apps",
        "system",
        "systems",
        "user",
        "users",
        "team",
        "teams",
        "company",
        "companies",
        "product",
        "products",
        "project",
        "projects",
        "platform",
        "service",
        "services",
        "feature",
        "features",
        "issue",
        "issues",
        "release",
        "releases",
        "version",
        "support",
        "report",
        "reports",
        "list",
        "guide",
        # Generic adjectives / adverbs
        "good",
        "great",
        "better",
        "simple",
        "easy",
        "fast",
        "free",
        "full",
        "high",
        "large",
        "small",
        "open",
        "real",
        "right",
        "top",
        "big",
        "next",
        "last",
        "own",
        "early",
        "late",
        "hard",
        "soft",
        "available",
        "popular",
        "common",
        "major",
        "minor",
        "latest",
        "recent",
        "possible",
        # Filler / meta
        "work",
        "year",
        "years",
        "why",
        "asks",
        "ask",
        "asked",
        "yet",
        "already",
        "across",
        "around",
        "among",
        "toward",
        "towards",
        "via",
        "per",
        "vs",
        "etc",
        "via",
        "instead",
        "day",
        "days",
        "week",
        "weeks",
        "month",
        "months",
        "hour",
        "hours",
        "way",
        "ways",
        "case",
        "cases",
        "point",
        "points",
        "level",
        "number",
        "line",
        "lines",
        "step",
        "steps",
        "change",
        "changes",
        "end",
        "set",
        "idea",
        "ideas",
        "result",
        "results",
        "career",
        "job",
        "jobs",
        "site",
        "blog",
        "post",
        "source",
        "problem",
        "model",
        "models",
        "state",
        "power",
        "reading",
        "review",
    }
)

# Bigrams where either word is one of these are always junk
_BIGRAM_STOPWORDS = frozenset(
    {
        "the", "and", "for", "are", "but", "not", "you", "your", "all", "can",
        "is", "was", "one", "our", "out", "has", "had", "how", "its", "may",
        "new", "now", "old", "see", "who", "did", "get", "let", "say", "she",
        "too", "use", "with", "this", "that", "have", "from", "they", "been",
        "will", "more", "when", "what", "some", "than", "them", "into", "only",
        "very", "just", "also", "about", "would", "there", "their", "which",
        "could", "other", "after", "first", "never", "where", "those", "every",
        "being", "these", "should", "because", "through", "before", "between",
        "while", "during", "without", "within", "against", "along", "above",
        "below", "under", "since", "until", "upon", "via", "per", "vs",
    }
)

_TOKEN_RE = re.compile(r"[a-z][a-z0-9\-]{1,}")

# Source family grouping — collapse granular source names for diversity scoring
_SOURCE_FAMILIES = {
    "hackernews": "aggregator",
    "producthunt": "aggregator",
    "github_trending": "github",
}


def _source_family(source: str) -> str:
    """Map a raw source name to its family for diversity scoring."""
    if source in _SOURCE_FAMILIES:
        return _SOURCE_FAMILIES[source]
    if source.startswith("rss:"):
        return "rss"
    return source


def _extract_title_terms(title: str) -> set[str]:
    """Extract meaningful tokens and bigrams from a title.

    Returns individual non-stopword tokens (min 4 chars) plus adjacent bigrams
    formed from consecutive non-stopword tokens where neither word is a
    preposition/article. Bigrams like 'machine learning' or 'ai agents' emerge
    naturally; collocation detection later promotes statistically significant
    ones and drops redundant unigrams.
    """
    tokens = _TOKEN_RE.findall(title.lower())
    # Split into runs of non-stopword tokens
    runs: list[list[str]] = []
    current: list[str] = []
    for tok in tokens:
        if tok in STOPWORDS:
            if current:
                runs.append(current)
                current = []
        else:
            current.append(tok)
    if current:
        runs.append(current)

    terms: set[str] = set()
    for run in runs:
        # Add individual tokens (min 4 chars to drop "won", "stop", "life", etc.)
        for tok in run:
            if len(tok) >= 4:
                terms.add(tok)
        # Add bigrams — both components must be non-trivial
        for a, b in zip(run, run[1:]):
            if a in _BIGRAM_STOPWORDS or b in _BIGRAM_STOPWORDS:
                continue
            if len(a) < 2 or len(b) < 2:
                continue
            terms.add(f"{a} {b}")
    return terms


# ---------------------------------------------------------------------------
# Dunning log-likelihood ratio for corpus-level bigram collocation detection
# Adapted from amueller/word_cloud (MIT license)
# ---------------------------------------------------------------------------


def _ll(k: int, n: int, x: float) -> float:
    """Log-likelihood helper."""
    if x <= 0:
        x = 1e-10
    if x >= 1:
        x = 1 - 1e-10
    return math.log(x) * k + math.log(1 - x) * (n - k)


def _dunning_score(c12: int, c1: int, c2: int, n: int) -> float:
    """Dunning log-likelihood ratio. Higher = stronger collocation."""
    if n <= c1 or n <= c2 or c1 == 0:
        return 0.0
    p = c2 / n
    p1 = c12 / c1
    p2 = (c2 - c12) / (n - c1) if n > c1 else 0
    return -2 * (
        _ll(c12, c1, p) + _ll(c2 - c12, n - c1, p) - _ll(c12, c1, p1) - _ll(c2 - c12, n - c1, p2)
    )


def _detect_collocations(titles: list[str], threshold: float = 15.0) -> dict[str, float]:
    """Find statistically significant bigrams across a corpus of titles.

    Returns {bigram_string: score} for bigrams above the threshold.
    """
    # Tokenize all titles, filter stopwords
    tokenized = []
    for t in titles:
        toks = [w for w in _TOKEN_RE.findall(t.lower()) if w not in STOPWORDS and len(w) >= 2]
        tokenized.append(toks)

    all_words = [w for toks in tokenized for w in toks]
    n = len(all_words)
    if n < 4:
        return {}

    unigram_counts = Counter(all_words)
    bigram_counts: Counter = Counter()
    for toks in tokenized:
        for a, b in zip(toks, toks[1:]):
            bigram_counts[(a, b)] += 1

    collocations = {}
    for (a, b), c12 in bigram_counts.items():
        if c12 < 2:
            continue
        score = _dunning_score(c12, unigram_counts[a], unigram_counts[b], n)
        if score > threshold:
            collocations[f"{a} {b}"] = score
    return collocations


# ---------------------------------------------------------------------------
# Velocity scoring — two-window comparison
# ---------------------------------------------------------------------------


def _velocity_score(
    items: list[dict], now: datetime, total_days: int = 7, hot_hours: int = 24
) -> float:
    """Compare recent mention rate vs baseline rate.

    Uses published date when available (actual article date), falls back to
    scraped_at. Returns >1.0 if accelerating, <1.0 if decelerating.
    Returns 1.0 (neutral) when time spread is too small to be meaningful.
    """
    timestamps: list[datetime] = []
    cutoff_recent = now - timedelta(hours=hot_hours)
    recent, baseline = 0, 0

    for item in items:
        # Prefer published date over scraped_at
        ts_str = item.get("published") or item.get("scraped_at")
        try:
            t = datetime.fromisoformat(ts_str)
        except (ValueError, TypeError):
            continue
        timestamps.append(t)
        if t >= cutoff_recent:
            recent += 1
        else:
            baseline += 1

    # If all items have timestamps within a narrow window (< 2 hours),
    # velocity is meaningless — likely a batch scrape
    if len(timestamps) >= 2:
        spread = max(timestamps) - min(timestamps)
        if spread < timedelta(hours=2):
            return 1.0  # neutral

    baseline_days = total_days - hot_hours / 24
    baseline_rate = baseline / baseline_days if baseline_days > 0 else 0
    recent_rate = recent / (hot_hours / 24)

    if baseline_rate == 0:
        return min(recent_rate * 2.0, 5.0)  # cap brand-new boost
    return min(recent_rate / baseline_rate, 5.0)


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
        min_source_families: int = 2,
        min_items: int = 4,
        max_topics: int = 15,
        weights: dict | None = None,
        # Legacy compat — ignored, use min_source_families
        min_sources: int | None = None,
    ) -> dict:
        """Compute trending topics from recent intel items.

        Pipeline:
        1. Extract phrases (RAKE-style stopword splitting) + detect collocations
        2. Gate: topic must appear in >= min_source_families distinct source
           families AND have >= min_items total mentions
        3. Score: 0.35*sublinear_freq + 0.35*diversity + 0.3*velocity
           Diversity uses source families (all rss:* = one family) so
           cross-ecosystem convergence is valued over blog-to-blog overlap.
        """
        w = weights or {"freq": 0.35, "diversity": 0.35, "velocity": 0.3}
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        now = datetime.now()

        with wal_connect(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT id, source, title, url, summary, scraped_at, tags, published
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
                "min_source_families": min_source_families,
                "min_items": min_items,
                "total_items_scanned": 0,
                "topics": [],
            }

        # Detect statistically significant bigram collocations across all titles
        all_titles = [row[2] for row in rows]
        collocations = _detect_collocations(all_titles, threshold=15.0)

        # Build topic → items mapping using phrase extraction
        topic_items: dict[str, list[dict]] = {}
        all_families: set[str] = set()

        for row in rows:
            item_id, source, title, url, summary, scraped_at, tags_str, published = row
            family = _source_family(source)
            all_families.add(family)

            item = {
                "id": item_id,
                "source": source,
                "source_family": family,
                "title": title,
                "url": url,
                "summary": (summary or "")[:200],
                "scraped_at": scraped_at,
                "published": published,
            }

            # Collect phrases from tags + title
            terms: set[str] = set()
            if tags_str:
                for tag in tags_str.split(","):
                    tag = tag.strip().lower()
                    if tag and tag not in STOPWORDS and len(tag) >= 4:
                        terms.add(tag)
            terms |= _extract_title_terms(title)

            # Also add any detected collocations present in this title
            title_lower = title.lower()
            for bigram in collocations:
                if bigram in title_lower:
                    terms.add(bigram)

            for term in terms:
                topic_items.setdefault(term, []).append(item)

        # Deduplicate: if a statistically significant collocation (e.g. "machine learning")
        # exists as a topic, remove its constituent unigrams to avoid double-counting.
        significant_bigrams = {t for t in topic_items if t in collocations}
        unigram_parts: set[str] = set()
        for ct in significant_bigrams:
            for part in ct.split():
                unigram_parts.add(part)
        for part in unigram_parts:
            if part in topic_items:
                del topic_items[part]

        total_active_families = len(all_families)

        # Score each topic — gate on source families AND min item count
        max_item_count = max((len(items) for items in topic_items.values()), default=1)
        scored: list[dict] = []

        for topic, items in topic_items.items():
            if len(items) < min_items:
                continue
            families = {i["source_family"] for i in items}
            if len(families) < min_source_families:
                continue

            # Sublinear TF: 1+log(count) dampens high-frequency generic terms
            norm_freq = (
                (1 + math.log(len(items))) / (1 + math.log(max_item_count))
                if max_item_count > 0
                else 0
            )
            norm_diversity = len(families) / total_active_families if total_active_families else 0

            # Velocity: compare recent mention rate vs baseline
            velocity = _velocity_score(items, now, total_days=days)
            norm_velocity = min(velocity / 5.0, 1.0)

            score = (
                w.get("freq", 0.35) * norm_freq
                + w.get("diversity", 0.35) * norm_diversity
                + w.get("velocity", 0.3) * norm_velocity
            )

            # Top-3 representative items (most recent, deduplicated by URL)
            seen_urls: set[str] = set()
            rep_items = []
            for i in sorted(items, key=lambda x: x["scraped_at"], reverse=True):
                if i["url"] not in seen_urls:
                    seen_urls.add(i["url"])
                    rep_items.append({
                        k: v for k, v in i.items() if k != "source_family"
                    })
                if len(rep_items) >= 3:
                    break

            raw_sources = sorted({i["source"] for i in items})
            scored.append(
                {
                    "topic": topic,
                    "score": round(score, 3),
                    "item_count": len(items),
                    "source_count": len(raw_sources),
                    "sources": raw_sources,
                    "source_families": sorted(families),
                    "velocity": round(velocity, 2),
                    "items": rep_items,
                }
            )

        scored.sort(key=lambda x: x["score"], reverse=True)
        topics = scored[:max_topics]

        return {
            "computed_at": now.isoformat(),
            "days": days,
            "min_source_families": min_source_families,
            "min_items": min_items,
            "total_items_scanned": len(rows),
            "topics": topics,
        }

    # ------------------------------------------------------------------
    # LLM-based trending: send recent articles to LLM for summarisation
    # ------------------------------------------------------------------

    _LLM_SYSTEM = (
        "You are a tech news analyst. You receive a batch of recent articles "
        "scraped from multiple sources (Hacker News, Reddit, RSS blogs, GitHub Trending, etc). "
        "Your job is to identify 5-10 specific, newsworthy developments that are getting "
        "cross-source attention.\n\n"
        "Rules:\n"
        "- Focus on SPECIFIC events, releases, companies, or developments — not broad "
        "categories like 'AI' or 'security' or 'programming'.\n"
        "- Each trend must be backed by at least 2 articles from different sources.\n"
        "- Rank by significance and cross-source convergence.\n"
        "- Return ONLY valid JSON — no markdown, no commentary.\n\n"
        "Return a JSON array of objects with these fields:\n"
        '  "topic": short descriptive label (5-10 words, like a headline),\n'
        '  "summary": one sentence explaining what happened and why it matters,\n'
        '  "article_ids": list of article ID numbers that discuss this development\n'
    )

    def compute_llm(self, llm, days: int = 7, max_topics: int = 10) -> dict:
        """Use an LLM to identify specific trending developments from recent intel.

        Args:
            llm: An LLMProvider instance (cheap tier recommended).
            days: Look-back window.
            max_topics: Max trends to return.

        Returns:
            Snapshot dict in the same format as compute(), with richer topic labels
            and summaries. Falls back to NLP compute() on any LLM failure.
        """
        now = datetime.now()
        cutoff = (now - timedelta(days=days)).isoformat()

        with wal_connect(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT id, source, title, url, summary, scraped_at, published
                FROM intel_items
                WHERE scraped_at >= ?
                ORDER BY scraped_at DESC
                LIMIT 500
                """,
                (cutoff,),
            ).fetchall()

        if not rows:
            return {
                "computed_at": now.isoformat(),
                "days": days,
                "total_items_scanned": 0,
                "method": "llm",
                "topics": [],
            }

        # Build article list for the prompt and an ID→item lookup
        items_by_id: dict[int, dict] = {}
        article_lines: list[str] = []
        for row in rows:
            item_id, source, title, url, summary, scraped_at, published = row
            items_by_id[item_id] = {
                "id": item_id,
                "source": source,
                "title": title,
                "url": url,
                "summary": (summary or "")[:200],
                "scraped_at": scraped_at,
                "published": published,
            }
            short_summary = (f" — {summary[:120]}" if summary else "")
            article_lines.append(f"[{item_id}] ({source}) {title}{short_summary}")

        prompt_body = (
            f"Here are {len(rows)} articles from the last {days} days:\n\n"
            + "\n".join(article_lines)
        )

        try:
            raw = llm.generate(
                messages=[{"role": "user", "content": prompt_body}],
                system=self._LLM_SYSTEM,
                max_tokens=2000,
            )

            # Strip markdown fences if present
            text = raw.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1] if "\n" in text else text[3:]
                if text.endswith("```"):
                    text = text[:-3]
                text = text.strip()

            llm_topics = json.loads(text)
            if not isinstance(llm_topics, list):
                raise ValueError("Expected JSON array")

        except Exception as e:
            logger.warning("trending_radar.llm_failed", error=str(e))
            return self.compute(days=days, max_topics=max_topics)

        # Convert LLM output to snapshot format
        topics: list[dict] = []
        for entry in llm_topics[:max_topics]:
            topic_label = entry.get("topic", "")
            summary_text = entry.get("summary", "")
            article_ids = entry.get("article_ids", [])

            # Resolve article IDs to items
            matched_items = [items_by_id[aid] for aid in article_ids if aid in items_by_id]
            if len(matched_items) < 2:
                continue

            sources = sorted({i["source"] for i in matched_items})
            families = sorted({_source_family(i["source"]) for i in matched_items})

            # Build representative items (up to 3)
            rep_items = []
            seen_urls: set[str] = set()
            for item in matched_items:
                if item["url"] not in seen_urls:
                    seen_urls.add(item["url"])
                    rep_items.append({
                        k: v for k, v in item.items() if k != "source_family"
                    })
                if len(rep_items) >= 3:
                    break

            topics.append({
                "topic": topic_label,
                "summary": summary_text,
                "item_count": len(matched_items),
                "source_count": len(sources),
                "sources": sources,
                "source_families": families,
                "items": rep_items,
            })

        return {
            "computed_at": now.isoformat(),
            "days": days,
            "total_items_scanned": len(rows),
            "method": "llm",
            "topics": topics,
        }

    def refresh(self, llm=None, **kwargs) -> dict:
        """Compute and persist a snapshot. Prunes old rows beyond MAX_ROWS.

        If an LLM provider is passed, uses LLM-based summarisation.
        Otherwise falls back to NLP-based compute().
        """
        if llm:
            snapshot = self.compute_llm(
                llm,
                days=kwargs.get("days", 7),
                max_topics=kwargs.get("max_topics", 10),
            )
        else:
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
            method=snapshot.get("method", "nlp"),
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

    def get_or_compute(self, llm=None, **kwargs) -> dict:
        """Return cached snapshot if available, otherwise compute fresh."""
        cached = self.load()
        if cached:
            return cached
        return self.refresh(llm=llm, **kwargs)
