"""Semantic search across journal entries."""

from pathlib import Path
from typing import Optional

import frontmatter

from .storage import JournalStorage
from .embeddings import EmbeddingManager


class JournalSearch:
    """Unified search interface combining semantic and keyword search."""

    def __init__(self, storage: JournalStorage, embeddings: EmbeddingManager):
        self.storage = storage
        self.embeddings = embeddings

    def semantic_search(
        self,
        query: str,
        n_results: int = 5,
        entry_type: Optional[str] = None,
    ) -> list[dict]:
        """Search using semantic similarity.

        Args:
            query: Natural language query
            n_results: Max results to return
            entry_type: Optional filter by entry type

        Returns:
            List of matching entries with relevance scores
        """
        # Fall back to keyword search if no embeddings
        if self.embeddings is None:
            return self.keyword_search(query, limit=n_results, entry_type=entry_type)

        where = {"type": entry_type} if entry_type else None
        results = self.embeddings.query(query, n_results=n_results, where=where)

        # Enrich with full entry data
        enriched = []
        for r in results:
            try:
                path = Path(r["id"])
                if path.exists():
                    post = frontmatter.load(path)
                    enriched.append({
                        "path": path,
                        "title": post.get("title", path.stem),
                        "type": post.get("type"),
                        "created": post.get("created"),
                        "tags": post.get("tags", []),
                        "content": post.content,
                        "relevance": 1 - r["distance"],  # Convert distance to similarity
                    })
            except (OSError, ValueError):
                continue

        return enriched

    def keyword_search(
        self,
        keyword: str,
        entry_type: Optional[str] = None,
        limit: int = 20,
    ) -> list[dict]:
        """Simple keyword search in content."""
        entries = self.storage.list_entries(entry_type=entry_type, limit=limit * 2)
        matches = []

        keyword_lower = keyword.lower()
        for entry in entries:
            try:
                post = frontmatter.load(entry["path"])
                if keyword_lower in post.content.lower():
                    matches.append({
                        "path": entry["path"],
                        "title": entry["title"],
                        "type": entry["type"],
                        "created": entry["created"],
                        "tags": entry["tags"],
                        "content": post.content,
                    })
                    if len(matches) >= limit:
                        break
            except (OSError, ValueError):
                continue

        return matches

    def get_context_for_query(
        self,
        query: str,
        max_entries: int = 5,
        max_chars: int = 8000,
    ) -> str:
        """Get relevant journal context for RAG.

        Args:
            query: User question/query
            max_entries: Max entries to include
            max_chars: Max total characters

        Returns:
            Formatted context string for LLM
        """
        results = self.semantic_search(query, n_results=max_entries)

        if not results:
            return "No relevant journal entries found."

        context_parts = []
        total_chars = 0

        for r in results:
            entry_text = f"""
--- Entry: {r['title']} ({r['type']}) ---
Date: {r['created']}
Tags: {', '.join(r['tags']) if r['tags'] else 'none'}

{r['content']}
"""
            if total_chars + len(entry_text) > max_chars:
                # Truncate last entry if needed
                remaining = max_chars - total_chars
                if remaining > 200:
                    context_parts.append(entry_text[:remaining] + "...[truncated]")
                break

            context_parts.append(entry_text)
            total_chars += len(entry_text)

        return "\n".join(context_parts)

    def sync_embeddings(self) -> tuple[int, int]:
        """Sync all journal entries to embedding store."""
        entries = self.storage.get_all_content()
        return self.embeddings.sync_from_storage(entries)
