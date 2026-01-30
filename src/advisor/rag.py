"""RAG retrieval combining journal and intelligence sources."""

import sqlite3
from typing import Optional
from pathlib import Path

from journal.search import JournalSearch
from intelligence.search import IntelSearch


class RAGRetriever:
    """Retrieves relevant context for LLM queries."""

    def __init__(
        self,
        journal_search: JournalSearch,
        intel_db_path: Optional[Path] = None,
        intel_search: Optional[IntelSearch] = None,
    ):
        self.journal = journal_search
        self.intel_db_path = Path(intel_db_path).expanduser() if intel_db_path else None
        self.intel_search = intel_search

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
                cursor = conn.execute("""
                    SELECT title, source, summary, url, scraped_at
                    FROM intel_items
                    WHERE title LIKE ? OR summary LIKE ?
                    ORDER BY scraped_at DESC
                    LIMIT ?
                """, (f"%{query}%", f"%{query}%", max_items * 2))

                items = cursor.fetchall()

                if not items:
                    cursor = conn.execute("""
                        SELECT title, source, summary, url, scraped_at
                        FROM intel_items
                        ORDER BY scraped_at DESC
                        LIMIT ?
                    """, (max_items,))
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

        except Exception:
            return "No external intelligence available."

    def get_combined_context(
        self,
        query: str,
        journal_weight: float = 0.7,
    ) -> tuple[str, str]:
        """Get both journal and intel context.

        Args:
            query: User query
            journal_weight: Proportion of context budget for journal (0-1)

        Returns:
            Tuple of (journal_context, intel_context)
        """
        total_chars = 8000
        journal_chars = int(total_chars * journal_weight)
        intel_chars = total_chars - journal_chars

        journal_ctx = self.get_journal_context(query, max_chars=journal_chars)
        intel_ctx = self.get_intel_context(query, max_chars=intel_chars)

        return journal_ctx, intel_ctx

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
--- {entry['title']} ({entry['type']}) ---
{post.content}
"""
                if total_chars + len(entry_text) > max_chars:
                    break

                recent.append(entry_text)
                total_chars += len(entry_text)

            except Exception:
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
        if hasattr(self.journal, 'semantic_search'):
            results = self.journal.semantic_search(
                query,
                n_results=max_entries,
                entry_type="research",
            )
            if results:
                context_parts = []
                total_chars = 0
                for r in results:
                    text = f"[Research: {r.get('title', 'Unknown')}]\n{r.get('content', '')[:1500]}\n"
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
            except Exception:
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
