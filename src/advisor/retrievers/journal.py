"""Journal context retriever."""

from __future__ import annotations

from typing import Optional

import structlog

from journal.search import JournalSearch

logger = structlog.get_logger()


class JournalRetriever:
    """Retrieves context from journal entries."""

    def __init__(self, journal_search: JournalSearch, cache=None):
        self._search = journal_search
        self.cache = cache

    @property
    def search(self) -> JournalSearch:
        """Expose underlying JournalSearch (for rag.search.storage compat)."""
        return self._search

    def get_journal_context(
        self,
        query: str,
        max_entries: int = 5,
        max_chars: int = 6000,
        entry_type: Optional[str] = None,
    ) -> str:
        """Get relevant journal entries for query."""
        if self.cache:
            key = self.cache.make_key(
                "journal", query, max_entries=max_entries, max_chars=max_chars
            )
            cached = self.cache.get(key)
            if cached is not None:
                return cached

        result = self._search.get_context_for_query(
            query=query,
            max_entries=max_entries,
            max_chars=max_chars,
        )

        if self.cache:
            self.cache.set(key, result)
        return result

    def get_recent_entries(self, days: int = 7, max_chars: int = 6000) -> str:
        """Get recent journal entries for weekly review."""
        entries = self._search.storage.list_entries(limit=20)

        from datetime import datetime, timedelta, timezone

        cutoff = datetime.now(timezone.utc) - timedelta(days=days)

        recent = []
        total_chars = 0

        for entry in entries:
            try:
                created = entry.get("created")
                if created:
                    entry_date = datetime.fromisoformat(created.replace("Z", "+00:00"))
                    if entry_date.tzinfo is None:
                        entry_date = entry_date.replace(tzinfo=timezone.utc)
                    if entry_date < cutoff:
                        continue

                post = self._search.storage.read(entry["path"])
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
        """Get relevant research reports for query."""
        research_entries = self._search.storage.list_entries(
            entry_type="research",
            limit=max_entries * 2,
        )

        if not research_entries:
            return ""

        if hasattr(self._search, "semantic_search"):
            results = self._search.semantic_search(
                query,
                n_results=max_entries,
                entry_type="research",
            )
            if results:
                context_parts = []
                total_chars = 0
                for r in results:
                    label = r.get("title", "Unknown")
                    if r.get("change_summary"):
                        label = f"{label} — {r.get('change_summary')}"
                    text = f"[Research: {label}]\n{r.get('content', '')[:1500]}\n"
                    if total_chars + len(text) > max_chars:
                        break
                    context_parts.append(text)
                    total_chars += len(text)
                return "\n".join(context_parts) if context_parts else ""

        context_parts = []
        total_chars = 0

        for entry in research_entries[:max_entries]:
            try:
                post = self._search.storage.read(entry["path"])
                label = entry["title"]
                if post.get("change_summary"):
                    label = f"{label} — {post.get('change_summary')}"
                text = f"[Research: {label}]\n{post.content[:1500]}\n"
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
