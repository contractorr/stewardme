"""RAG retrieval combining journal and intelligence sources."""

import sqlite3
from pathlib import Path
from typing import Optional

import structlog

from intelligence.search import IntelSearch
from journal.search import JournalSearch

logger = structlog.get_logger()


class RAGRetriever:
    """Retrieves relevant context for LLM queries."""

    def __init__(
        self,
        journal_search: JournalSearch,
        intel_db_path: Optional[Path] = None,
        intel_search: Optional[IntelSearch] = None,
        max_context_chars: int = 8000,
        journal_weight: float = 0.7,
        profile_path: Optional[str] = None,
        users_db_path: Optional[Path] = None,
        user_id: Optional[str] = None,
    ):
        self.journal = journal_search
        self.intel_db_path = Path(intel_db_path).expanduser() if intel_db_path else None
        self.intel_search = intel_search
        self.max_context_chars = max_context_chars
        self.journal_weight = journal_weight
        self._profile_path = profile_path or "~/coach/profile.yaml"
        self._users_db_path = users_db_path
        self._user_id = user_id

    def get_profile_context(self, structured: bool = False) -> str:
        """Load user profile summary for LLM context injection.

        Args:
            structured: If True, return multi-section structured format
                        optimized for recommendation prompts. If False,
                        return compact one-line summary.
        """
        try:
            from profile.storage import ProfileStorage

            ps = ProfileStorage(self._profile_path)
            profile = ps.load()
            if profile:
                if structured:
                    return f"\n{profile.structured_summary()}\n"
                return f"\nUSER PROFILE: {profile.summary()}\n"
        except Exception as e:
            logger.debug("profile_load_skipped", error=str(e))
        return ""

    def get_profile_keywords(self) -> list[str]:
        """Extract key terms from profile for intel query augmentation."""
        try:
            from profile.storage import ProfileStorage

            ps = ProfileStorage(self._profile_path)
            profile = ps.load()
            if not profile:
                return []

            keywords = []
            if profile.skills:
                keywords.extend(s.name for s in profile.skills[:8])
            keywords.extend(profile.languages_frameworks[:6])
            keywords.extend(profile.technologies_watching[:6])
            keywords.extend(profile.industries_watching[:4])
            keywords.extend(profile.interests[:4])
            # Extract key terms from active projects
            for p in profile.active_projects[:3]:
                keywords.extend(p.lower().split()[:3])
            return [k.lower().strip() for k in keywords if k.strip()]
        except Exception:
            return []

    def get_journal_context(
        self,
        query: str,
        max_entries: int = 5,
        max_chars: int = 6000,
        entry_type: Optional[str] = None,
    ) -> str:
        """Get relevant journal entries for query."""
        return self.journal.get_context_for_query(
            query=query,
            max_entries=max_entries,
            max_chars=max_chars,
        )

    def _load_profile_terms(self):
        """Load profile and build ProfileTerms for intel filtering."""
        try:
            from profile.storage import ProfileStorage

            from intelligence.search import ProfileTerms

            ps = ProfileStorage(self._profile_path)
            profile = ps.load()
            if not profile:
                return ProfileTerms()

            # Extract goal keywords from free-text goal fields
            import re

            goal_keywords = []
            for text in [profile.goals_short_term, profile.goals_long_term, profile.aspirations]:
                if text:
                    # Extract meaningful words (3+ chars, skip stopwords)
                    words = re.findall(r"[a-z][a-z0-9\-]+", text.lower())
                    stopwords = {
                        "the", "and", "for", "that", "with", "this", "from", "have",
                        "will", "are", "was", "been", "being", "would", "could", "should",
                        "into", "about", "more", "some", "than", "also", "just", "over",
                        "such", "want", "like", "get", "make", "see", "know", "take",
                        "next", "year", "years", "month", "months", "within", "achieve",
                    }
                    goal_keywords.extend(w for w in words if len(w) > 2 and w not in stopwords)

            # Extract project keywords
            project_keywords = []
            for p in profile.active_projects:
                words = re.findall(r"[a-z][a-z0-9\-]+", p.lower())
                project_keywords.extend(w for w in words if len(w) > 2)

            return ProfileTerms(
                skills=[s.name for s in profile.skills],
                tech=profile.languages_frameworks + profile.technologies_watching,
                interests=profile.interests + profile.industries_watching,
                goal_keywords=goal_keywords[:20],  # cap to avoid noise
                project_keywords=project_keywords[:10],
            )
        except Exception as e:
            logger.debug("profile_terms_load_failed", error=str(e))
            from intelligence.search import ProfileTerms

            return ProfileTerms()

    def get_filtered_intel_context(
        self,
        query: str,
        max_items: int = 5,
        max_chars: int = 3000,
        min_relevance: float = 0.05,
    ) -> str:
        """Get intel context filtered and annotated by profile relevance.

        Two-stage pipeline:
        1. Broad retrieval using profile-augmented query
        2. Re-rank by profile term overlap, filter below threshold, annotate matches

        Falls back to standard get_intel_context if IntelSearch not available
        or profile is empty.
        """
        if not self.intel_search:
            return self.get_intel_context(query, max_items=max_items, max_chars=max_chars)

        profile_terms = self._load_profile_terms()

        return self.intel_search.get_filtered_context_for_query(
            query=query,
            profile_terms=profile_terms,
            max_items=max_items,
            max_chars=max_chars,
            min_relevance=min_relevance,
        )

    def get_intel_context(
        self,
        query: str,
        max_items: int = 5,
        max_chars: int = 3000,
    ) -> str:
        """Get relevant intelligence items for query.

        Uses semantic search if IntelSearch is configured, falls back to keyword search.
        """
        # Use semantic search if available
        if self.intel_search:
            return self.intel_search.get_context_for_query(
                query=query,
                max_items=max_items,
                max_chars=max_chars,
            )

        # Fallback to basic keyword search
        if not self.intel_db_path or not self.intel_db_path.exists():
            return "No external intelligence available yet."

        try:
            with sqlite3.connect(self.intel_db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    """
                    SELECT title, source, summary, url, scraped_at
                    FROM intel_items
                    WHERE title LIKE ? OR summary LIKE ?
                    ORDER BY scraped_at DESC
                    LIMIT ?
                """,
                    (f"%{query}%", f"%{query}%", max_items * 2),
                )

                items = cursor.fetchall()

                if not items:
                    cursor = conn.execute(
                        """
                        SELECT title, source, summary, url, scraped_at
                        FROM intel_items
                        ORDER BY scraped_at DESC
                        LIMIT ?
                    """,
                        (max_items,),
                    )
                    items = cursor.fetchall()

            if not items:
                return "No external intelligence available."

            context_parts = []
            total_chars = 0

            for item in items[:max_items]:
                entry = f"- [{item['source']}] {item['title']}: {item['summary'][:200]}"
                if total_chars + len(entry) > max_chars:
                    break
                context_parts.append(entry)
                total_chars += len(entry)

            return "\n".join(context_parts) if context_parts else "No relevant intelligence found."

        except sqlite3.OperationalError:
            return "No external intelligence available."

    def compute_dynamic_weight(self, user_id: Optional[str] = None) -> float:
        """Compute journal_weight from engagement data.

        Formula: base(0.7) + 0.15 * (journal_ratio - 0.5), clamped [0.5, 0.85].
        Returns default 0.7 when <10 events in last 30 days.
        """
        uid = user_id or self._user_id
        if not uid or not self._users_db_path:
            return self.journal_weight

        try:
            with sqlite3.connect(str(self._users_db_path)) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(
                    """
                    SELECT target_type, event_type, COUNT(*) as cnt
                    FROM engagement_events
                    WHERE user_id = ? AND created_at >= datetime('now', '-30 days')
                    GROUP BY target_type, event_type
                    """,
                    (uid,),
                ).fetchall()

            total = sum(r["cnt"] for r in rows)
            if total < 10:
                return self.journal_weight

            positive_events = {"opened", "saved", "acted_on", "feedback_useful"}
            journal_score = sum(
                r["cnt"]
                for r in rows
                if r["target_type"] == "journal" and r["event_type"] in positive_events
            )
            intel_score = sum(
                r["cnt"]
                for r in rows
                if r["target_type"] == "intel" and r["event_type"] in positive_events
            )
            denom = journal_score + intel_score
            if denom == 0:
                return self.journal_weight

            journal_ratio = journal_score / denom
            weight = 0.7 + 0.15 * (journal_ratio - 0.5)
            return max(0.5, min(0.85, weight))
        except Exception as e:
            logger.debug("dynamic_weight_fallback", error=str(e))
            return self.journal_weight

    def get_combined_context(
        self,
        query: str,
        journal_weight: Optional[float] = None,
    ) -> tuple[str, str]:
        """Get both journal and intel context.

        Args:
            query: User query
            journal_weight: Proportion of context budget for journal (0-1)

        Returns:
            Tuple of (journal_context, intel_context)
        """
        if journal_weight is not None:
            weight = journal_weight
        elif self._users_db_path and self._user_id:
            weight = self.compute_dynamic_weight()
        else:
            weight = self.journal_weight
        total_chars = self.max_context_chars
        journal_chars = int(total_chars * weight)
        intel_chars = total_chars - journal_chars

        journal_ctx = self.get_journal_context(query, max_chars=journal_chars)
        intel_ctx = self.get_intel_context(query, max_chars=intel_chars)

        return journal_ctx, intel_ctx

    def get_ai_capabilities_context(self, query: str, max_chars: int = 1500) -> str:
        """Get AI capability context combining static KB + recent intel.

        Args:
            query: User query to match against AI capability intel
            max_chars: Max total characters for combined context

        Returns:
            Combined context string with KB summary + relevant scraped items
        """
        from advisor.ai_capabilities_kb import render_summary

        parts = []
        # Static KB summary (~500 chars)
        summary = render_summary()
        parts.append(summary)
        remaining = max_chars - len(summary) - 20

        # Recent AI capabilities intel from scraper
        if remaining > 100:
            ai_intel = self.get_intel_context(
                query + " AI capabilities benchmarks model performance",
                max_items=5,
                max_chars=remaining,
            )
            if ai_intel and "No" not in ai_intel[:10]:
                parts.append(ai_intel)

        return "\n\n".join(parts)

    def get_recent_entries(self, days: int = 7, max_chars: int = 6000) -> str:
        """Get recent journal entries for weekly review."""
        # For weekly review, use recency-based retrieval
        entries = self.journal.storage.list_entries(limit=20)

        from datetime import datetime, timedelta

        cutoff = datetime.now() - timedelta(days=days)

        recent = []
        total_chars = 0

        for entry in entries:
            try:
                created = entry.get("created")
                if created:
                    entry_date = datetime.fromisoformat(created.replace("Z", "+00:00"))
                    if entry_date.replace(tzinfo=None) < cutoff:
                        continue

                post = self.journal.storage.read(entry["path"])
                entry_text = f"""
--- {entry["title"]} ({entry["type"]}) ---
{post.content}
"""
                if total_chars + len(entry_text) > max_chars:
                    break

                recent.append(entry_text)
                total_chars += len(entry_text)

            except (OSError, ValueError) as e:
                logger.warning(
                    "journal_entry_read_failed", path=str(entry.get("path")), error=str(e)
                )
                continue

        if not recent:
            return "No journal entries from the past week."

        return "\n".join(recent)

    def get_research_context(
        self,
        query: str,
        max_entries: int = 3,
        max_chars: int = 4000,
    ) -> str:
        """Get relevant research reports for query.

        Args:
            query: User query to match against research
            max_entries: Max research entries to include
            max_chars: Max total characters

        Returns:
            Formatted research context string
        """
        # Search research entries via journal
        research_entries = self.journal.storage.list_entries(
            entry_type="research",
            limit=max_entries * 2,
        )

        if not research_entries:
            return ""

        # Use semantic search if available to rank by relevance
        if hasattr(self.journal, "semantic_search"):
            results = self.journal.semantic_search(
                query,
                n_results=max_entries,
                entry_type="research",
            )
            if results:
                context_parts = []
                total_chars = 0
                for r in results:
                    text = (
                        f"[Research: {r.get('title', 'Unknown')}]\n{r.get('content', '')[:1500]}\n"
                    )
                    if total_chars + len(text) > max_chars:
                        break
                    context_parts.append(text)
                    total_chars += len(text)
                return "\n".join(context_parts) if context_parts else ""

        # Fallback: return most recent research
        context_parts = []
        total_chars = 0

        for entry in research_entries[:max_entries]:
            try:
                post = self.journal.storage.read(entry["path"])
                text = f"[Research: {entry['title']}]\n{post.content[:1500]}\n"
                if total_chars + len(text) > max_chars:
                    break
                context_parts.append(text)
                total_chars += len(text)
            except (OSError, ValueError) as e:
                logger.warning(
                    "research_entry_read_failed", path=str(entry.get("path")), error=str(e)
                )
                continue

        return "\n".join(context_parts) if context_parts else ""

    def get_full_context(
        self,
        query: str,
        include_research: bool = True,
    ) -> tuple[str, str, str]:
        """Get journal, intel, and research context.

        Returns:
            Tuple of (journal_context, intel_context, research_context)
        """
        journal_ctx, intel_ctx = self.get_combined_context(query)
        research_ctx = self.get_research_context(query) if include_research else ""
        return journal_ctx, intel_ctx, research_ctx
