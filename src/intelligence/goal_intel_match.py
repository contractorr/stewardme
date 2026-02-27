"""Goal-Intel matching — keyword scoring + optional LLM eval for active goals."""

import json
import os
import re
import sqlite3
from pathlib import Path

import frontmatter
import structlog

from db import wal_connect

from .scraper import IntelStorage
from .search import ProfileTerms, score_profile_relevance

logger = structlog.get_logger()

# Stopwords to filter from goal content
_STOPWORDS = frozenset(
    "a an the and or but in on at to for of is it by be as do if my me we he she "
    "they this that with from not has have had was were will can could should would "
    "may might shall into more than also been being about after before between each "
    "few most other some such no nor only own same so too very just because how what "
    "when where which while who whom why all any both during through until above below "
    "again further then once here there these those am are its let get got use used "
    "using want need make made like going go take work things over".split()
)

# Urgency thresholds
_URGENCY_HIGH = 0.15
_URGENCY_MEDIUM = 0.08
_URGENCY_LOW = 0.04


class GoalIntelMatchStore:
    """SQLite persistence for goal-intel matches in intel.db."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path).expanduser()
        self._init_db()

    def _init_db(self):
        with wal_connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS goal_intel_matches (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    goal_path   TEXT NOT NULL,
                    goal_title  TEXT NOT NULL,
                    url         TEXT NOT NULL,
                    title       TEXT NOT NULL,
                    summary     TEXT,
                    score       REAL NOT NULL,
                    urgency     TEXT NOT NULL,
                    match_reasons TEXT NOT NULL,
                    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_gim_goal_path ON goal_intel_matches(goal_path)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_gim_created ON goal_intel_matches(created_at)"
            )
            # Phase 3: add llm_evaluated column (idempotent migration)
            try:
                conn.execute(
                    "ALTER TABLE goal_intel_matches ADD COLUMN llm_evaluated INTEGER NOT NULL DEFAULT 0"
                )
            except sqlite3.OperationalError:
                pass  # column already exists

    def save_matches(self, matches: list[dict]) -> int:
        """Save matches with 7-day dedup on (goal_path, url). Returns count inserted."""
        if not matches:
            return 0
        inserted = 0
        with wal_connect(self.db_path) as conn:
            for m in matches:
                # 7-day dedup
                existing = conn.execute(
                    """SELECT id FROM goal_intel_matches
                       WHERE goal_path = ? AND url = ?
                       AND created_at > datetime('now', '-7 days')""",
                    (m["goal_path"], m["url"]),
                ).fetchone()
                if existing:
                    continue
                conn.execute(
                    """INSERT INTO goal_intel_matches
                       (goal_path, goal_title, url, title, summary, score, urgency, match_reasons, llm_evaluated)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        m["goal_path"],
                        m["goal_title"],
                        m["url"],
                        m["title"],
                        m.get("summary", ""),
                        m["score"],
                        m["urgency"],
                        json.dumps(m["match_reasons"]),
                        int(m.get("llm_evaluated", 0)),
                    ),
                )
                inserted += 1
        logger.info("goal_intel_matches.saved", inserted=inserted, total=len(matches))
        return inserted

    def get_matches(
        self,
        goal_paths: list[str] | None = None,
        min_urgency: str | None = None,
        limit: int = 20,
    ) -> list[dict]:
        """Get matches ordered by urgency tier then score desc."""
        urgency_order = {"high": 1, "medium": 2, "low": 3}

        query = "SELECT * FROM goal_intel_matches WHERE 1=1"
        params: list = []

        if goal_paths:
            placeholders = ",".join("?" for _ in goal_paths)
            query += f" AND goal_path IN ({placeholders})"
            params.extend(goal_paths)

        if min_urgency and min_urgency in urgency_order:
            allowed = [u for u, v in urgency_order.items() if v <= urgency_order[min_urgency]]
            placeholders = ",".join("?" for _ in allowed)
            query += f" AND urgency IN ({placeholders})"
            params.extend(allowed)

        query += """
            ORDER BY
                CASE urgency WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END,
                score DESC
            LIMIT ?
        """
        params.append(limit)

        with wal_connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(query, params).fetchall()

        results = []
        for row in rows:
            d = dict(row)
            d["match_reasons"] = json.loads(d["match_reasons"])
            d["created_at"] = str(d["created_at"]) if d["created_at"] else ""
            results.append(d)
        return results

    def cleanup_old(self, days: int = 30) -> int:
        """Delete matches older than given days. Returns count deleted."""
        with wal_connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM goal_intel_matches WHERE created_at < datetime('now', ?)",
                (f"-{days} days",),
            )
            count = cursor.rowcount
        if count:
            logger.info("goal_intel_matches.cleanup", deleted=count, threshold_days=days)
        return count


class GoalIntelMatcher:
    """Keyword-based matching of intel items to user goals. Zero LLM cost."""

    def __init__(self, intel_storage: IntelStorage):
        self.intel_storage = intel_storage

    def _extract_goal_keywords(self, goal: dict) -> list[str]:
        """Extract keywords from goal title, content, and tags."""
        parts: list[str] = []

        # Title
        title = goal.get("title", "")
        if title:
            parts.append(title)

        # Tags
        tags = goal.get("tags", [])
        if tags:
            parts.extend(tags)

        # Full content from file if path available
        goal_path = goal.get("path")
        if goal_path:
            try:
                post = frontmatter.load(str(goal_path))
                body = post.content or ""
                if body:
                    parts.append(body[:1000])
                # Also get tags from frontmatter if not already in goal dict
                fm_tags = post.metadata.get("tags", [])
                if fm_tags:
                    parts.extend(fm_tags)
            except Exception:
                pass

        text = " ".join(parts).lower()
        tokens = set(re.findall(r"[a-z][a-z0-9\-]+", text))
        filtered = [t for t in tokens if t not in _STOPWORDS and len(t) > 2]
        # Cap at 30 terms, prefer longer (more specific) terms first
        filtered.sort(key=len, reverse=True)
        return filtered[:30]

    @staticmethod
    def _score_to_urgency(score: float) -> str | None:
        """Map score to urgency tier. Returns None if below threshold."""
        if score >= _URGENCY_HIGH:
            return "high"
        if score >= _URGENCY_MEDIUM:
            return "medium"
        if score >= _URGENCY_LOW:
            return "low"
        return None

    def match_goal(self, goal: dict, intel_items: list[dict]) -> list[dict]:
        """Score intel items against a single goal. Returns matches above threshold."""
        keywords = self._extract_goal_keywords(goal)
        if not keywords:
            return []

        # Populate both skills and goal_keywords for effective max ~0.45
        profile = ProfileTerms(skills=keywords, goal_keywords=keywords)

        matches = []
        goal_path = str(goal.get("path", ""))
        goal_title = goal.get("title", "")

        for item in intel_items:
            score, reasons = score_profile_relevance(item, profile)
            urgency = self._score_to_urgency(score)
            if not urgency:
                continue
            matches.append(
                {
                    "goal_path": goal_path,
                    "goal_title": goal_title,
                    "url": item.get("url", ""),
                    "title": item.get("title", ""),
                    "summary": (item.get("summary") or "")[:300],
                    "score": round(score, 4),
                    "urgency": urgency,
                    "match_reasons": reasons,
                }
            )

        matches.sort(key=lambda m: m["score"], reverse=True)
        return matches

    def match_all_goals(
        self, goals: list[dict], days: int = 7, limit: int = 100
    ) -> list[dict]:
        """Match all goals against recent intel. Single DB call for intel."""
        intel_items = self.intel_storage.get_recent(days=days, limit=500)
        if not intel_items:
            logger.debug("goal_intel_match.no_intel", days=days)
            return []

        all_matches: list[dict] = []
        for goal in goals:
            goal_matches = self.match_goal(goal, intel_items)
            all_matches.extend(goal_matches)

        # Sort by score desc, cap at limit
        all_matches.sort(key=lambda m: m["score"], reverse=True)
        logger.info(
            "goal_intel_match.complete",
            goals=len(goals),
            intel_items=len(intel_items),
            matches=len(all_matches[:limit]),
        )
        return all_matches[:limit]


class GoalIntelLLMEvaluator:
    """LLM-based refinement of keyword matches — drops false positives, adjusts urgency."""

    BATCH_SIZE = 20

    _SYSTEM_PROMPT = (
        "You evaluate whether news items are genuinely relevant to user goals. "
        "Be strict — keyword matches often produce false positives. "
        "For each item, judge relevance and urgency."
    )

    def __init__(self, provider=None):
        self._provider = provider  # inject for tests

    @staticmethod
    def is_available() -> bool:
        """Check if any LLM API key is configured."""
        from llm.factory import _PROVIDER_ENV_KEYS

        return any(os.getenv(v) for v in _PROVIDER_ENV_KEYS.values())

    def _get_provider(self):
        if self._provider:
            return self._provider
        from llm.factory import create_cheap_provider

        return create_cheap_provider()

    def _build_prompt(self, batch: list[dict]) -> str:
        """Build numbered evaluation prompt grouped by goal."""
        # Group by goal_title for context
        by_goal: dict[str, list[tuple[int, dict]]] = {}
        for idx, m in enumerate(batch):
            gt = m.get("goal_title", "Unknown")
            by_goal.setdefault(gt, []).append((idx, m))

        lines: list[str] = []
        for goal_title, items in by_goal.items():
            lines.append(f'GOAL: "{goal_title}"')
            for idx, m in items:
                lines.append(
                    f'{idx + 1}. [Title] "{m.get("title", "")}" '
                    f'| [Summary] "{(m.get("summary") or "")[:200]}"'
                )
            lines.append("")

        lines.append("For each item respond EXACTLY:")
        for idx in range(len(batch)):
            lines.append(f"ITEM_{idx + 1}_RELEVANT: yes|no")
            lines.append(f"ITEM_{idx + 1}_URGENCY: high|medium|low|drop")
        lines.append('"drop" means false positive — remove entirely.')
        return "\n".join(lines)

    def _parse_response(self, text: str, batch: list[dict]) -> list[dict]:
        """Parse LLM response, return surviving matches with updated urgency."""
        results: dict[int, dict] = {}  # 1-indexed
        for line in text.strip().splitlines():
            line = line.strip()
            m = re.match(r"ITEM_(\d+)_(RELEVANT|URGENCY):\s*(\S+)", line, re.IGNORECASE)
            if not m:
                continue
            idx = int(m.group(1))
            field = m.group(2).upper()
            value = m.group(3).lower()
            results.setdefault(idx, {})[field] = value

        surviving: list[dict] = []
        for i, match in enumerate(batch):
            item_data = results.get(i + 1, {})
            relevant = item_data.get("RELEVANT", "yes")
            urgency = item_data.get("URGENCY", match["urgency"])

            if relevant == "no" or urgency == "drop":
                continue

            if urgency in ("high", "medium", "low"):
                match["urgency"] = urgency
            match["llm_evaluated"] = 1
            surviving.append(match)

        return surviving

    def evaluate(self, matches: list[dict]) -> list[dict]:
        """LLM-refine batches of matches. Fallback: return unchanged on error."""
        if not matches:
            return matches

        provider = self._get_provider()
        all_surviving: list[dict] = []

        for start in range(0, len(matches), self.BATCH_SIZE):
            batch = matches[start : start + self.BATCH_SIZE]
            try:
                user_prompt = self._build_prompt(batch)
                response = provider.generate(
                    messages=[
                        {"role": "system", "content": self._SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt},
                    ],
                    max_tokens=1000,
                )
                surviving = self._parse_response(response, batch)
                all_surviving.extend(surviving)
            except Exception as e:
                logger.warning(
                    "goal_intel_llm_eval.batch_failed",
                    error=str(e),
                    batch_start=start,
                    batch_size=len(batch),
                )
                # Fallback: keep batch unchanged (no llm_evaluated flag)
                all_surviving.extend(batch)

        logger.info(
            "goal_intel_llm_eval.complete",
            input=len(matches),
            output=len(all_surviving),
            dropped=len(matches) - len(all_surviving),
        )
        return all_surviving
