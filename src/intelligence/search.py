"""Semantic and keyword search for intelligence items."""

import sqlite3
from pathlib import Path
from typing import Optional

from .embeddings import IntelEmbeddingManager
from .scraper import IntelStorage


class IntelSearch:
    """Combined semantic and keyword search for intel items."""

    def __init__(
        self,
        storage: IntelStorage,
        embedding_manager: Optional[IntelEmbeddingManager] = None,
    ):
        self.storage = storage
        self.embeddings = embedding_manager

    def semantic_search(
        self,
        query: str,
        n_results: int = 10,
        source_filter: Optional[str] = None,
    ) -> list[dict]:
        """Search using vector similarity.

        Falls back to keyword search if embeddings not available.
        """
        if not self.embeddings:
            return self.keyword_search(query, limit=n_results)

        where = {"source": source_filter} if source_filter else None
        results = self.embeddings.query(query, n_results=n_results, where=where)

        # Enrich results with full item data from storage
        enriched = []
        for result in results:
            try:
                item_id = int(result["id"])
                item = self._get_item_by_id(item_id)
                if item:
                    item["score"] = 1 - result["distance"]  # Convert distance to similarity
                    enriched.append(item)
            except (ValueError, TypeError):
                continue

        return enriched

    def keyword_search(
        self,
        query: str,
        limit: int = 20,
        source_filter: Optional[str] = None,
    ) -> list[dict]:
        """Simple keyword search in titles and summaries."""
        return self.storage.search(query, limit=limit)

    def hybrid_search(
        self,
        query: str,
        n_results: int = 10,
        semantic_weight: float = 0.7,
    ) -> list[dict]:
        """Combine semantic and keyword search results.

        Args:
            query: Search query
            n_results: Max results to return
            semantic_weight: Weight for semantic results (0-1)

        Returns:
            Merged and ranked results
        """
        semantic_results = self.semantic_search(query, n_results=n_results * 2)
        keyword_results = self.keyword_search(query, limit=n_results * 2)

        # Score fusion: combine results by URL
        scores = {}
        items = {}

        for i, item in enumerate(semantic_results):
            url = item.get("url", "")
            if url:
                rank_score = 1.0 / (i + 1)
                scores[url] = scores.get(url, 0) + rank_score * semantic_weight
                items[url] = item

        for i, item in enumerate(keyword_results):
            url = item.get("url", "")
            if url:
                rank_score = 1.0 / (i + 1)
                scores[url] = scores.get(url, 0) + rank_score * (1 - semantic_weight)
                if url not in items:
                    items[url] = item

        # Sort by combined score
        sorted_urls = sorted(scores.keys(), key=lambda u: scores[u], reverse=True)
        return [items[url] for url in sorted_urls[:n_results]]

    def get_context_for_query(
        self,
        query: str,
        max_items: int = 5,
        max_chars: int = 3000,
    ) -> str:
        """Get intel context string for RAG.

        Args:
            query: User query
            max_items: Maximum items to include
            max_chars: Character limit for context

        Returns:
            Formatted context string
        """
        if self.embeddings:
            results = self.hybrid_search(query, n_results=max_items * 2)
        else:
            results = self.keyword_search(query, limit=max_items * 2)

        if not results:
            # Fallback to recent items
            results = self.storage.get_recent(days=7, limit=max_items)

        if not results:
            return "No external intelligence available."

        context_parts = []
        total_chars = 0

        for item in results[:max_items]:
            source = item.get("source", "unknown")
            title = item.get("title", "Untitled")
            summary = item.get("summary", "")[:200]
            url = item.get("url", "")

            entry = f"- [{source}] {title}"
            if summary:
                entry += f": {summary}"
            if url:
                entry += f" ({url})"

            if total_chars + len(entry) > max_chars:
                break

            context_parts.append(entry)
            total_chars += len(entry)

        return "\n".join(context_parts) if context_parts else "No relevant intelligence found."

    def sync_embeddings(self) -> tuple[int, int]:
        """Sync all intel items to vector store.

        Returns:
            Tuple of (added, removed) counts
        """
        if not self.embeddings:
            return 0, 0

        # Get all items from storage
        with sqlite3.connect(self.storage.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT id, source, title, url, summary, content, tags
                FROM intel_items
            """)
            rows = cursor.fetchall()

        # Prepare for embedding
        items = []
        for row in rows:
            content = f"{row['title']}\n{row['summary'] or ''}\n{row['content'] or ''}"
            items.append({
                "id": str(row["id"]),
                "content": content,
                "metadata": {
                    "source": row["source"],
                    "url": row["url"],
                    "tags": row["tags"] or "",
                },
            })

        return self.embeddings.sync_from_storage(items)

    def _get_item_by_id(self, item_id: int) -> Optional[dict]:
        """Fetch single item by ID."""
        try:
            with sqlite3.connect(self.storage.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    "SELECT * FROM intel_items WHERE id = ?",
                    (item_id,),
                )
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception:
            return None
