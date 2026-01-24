"""Vector embeddings for intelligence items using ChromaDB."""

from pathlib import Path
from typing import Optional

import chromadb
from chromadb.config import Settings


class IntelEmbeddingManager:
    """Manages vector embeddings for intelligence items."""

    def __init__(self, chroma_dir: str | Path):
        self.chroma_dir = Path(chroma_dir).expanduser()
        self.chroma_dir.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=str(self.chroma_dir),
            settings=Settings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(
            name="intel",
            metadata={"hnsw:space": "cosine"},
        )

    def add_item(
        self,
        item_id: str,
        content: str,
        metadata: Optional[dict] = None,
    ) -> None:
        """Add or update intel item embedding."""
        self.collection.upsert(
            ids=[item_id],
            documents=[content],
            metadatas=[metadata or {}],
        )

    def add_items_batch(
        self,
        items: list[dict],
    ) -> int:
        """Add multiple items in batch.

        Args:
            items: List of dicts with id, content, metadata keys

        Returns:
            Number of items added
        """
        if not items:
            return 0

        ids = [item["id"] for item in items]
        documents = [item["content"] for item in items]
        metadatas = [item.get("metadata", {}) for item in items]

        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
        )
        return len(items)

    def remove_item(self, item_id: str) -> None:
        """Remove item from vector store."""
        try:
            self.collection.delete(ids=[item_id])
        except Exception:
            pass

    def query(
        self,
        query_text: str,
        n_results: int = 10,
        where: Optional[dict] = None,
    ) -> list[dict]:
        """Query similar intel items.

        Args:
            query_text: Search query
            n_results: Number of results to return
            where: Optional metadata filter

        Returns:
            List of matching items with scores
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where,
            include=["documents", "metadatas", "distances"],
        )

        items = []
        if results["ids"] and results["ids"][0]:
            for i, item_id in enumerate(results["ids"][0]):
                items.append({
                    "id": item_id,
                    "content": results["documents"][0][i] if results["documents"] else "",
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else 0,
                })

        return items

    def sync_from_storage(self, items: list[dict]) -> tuple[int, int]:
        """Sync embeddings from intel storage items.

        Args:
            items: List of dicts with id, content, metadata

        Returns:
            Tuple of (added, removed) counts
        """
        existing = set()
        try:
            existing_data = self.collection.get()
            existing = set(existing_data["ids"]) if existing_data["ids"] else set()
        except Exception:
            pass

        current_ids = {str(item["id"]) for item in items}

        # Add/update items
        added = 0
        for item in items:
            item_id = str(item["id"])
            self.add_item(item_id, item["content"], item.get("metadata"))
            if item_id not in existing:
                added += 1

        # Remove deleted items
        removed = 0
        for old_id in existing - current_ids:
            self.remove_item(old_id)
            removed += 1

        return added, removed

    def count(self) -> int:
        """Get total number of embedded items."""
        return self.collection.count()
