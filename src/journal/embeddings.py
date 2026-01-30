"""Vector embedding operations using ChromaDB."""

from pathlib import Path
from typing import Optional

import chromadb
from chromadb.config import Settings


class EmbeddingManager:
    """Manages vector embeddings for journal entries."""

    def __init__(self, chroma_dir: str | Path):
        self.chroma_dir = Path(chroma_dir).expanduser()
        self.chroma_dir.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=str(self.chroma_dir),
            settings=Settings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(
            name="journal",
            metadata={"hnsw:space": "cosine"},
        )

    def add_entry(
        self,
        entry_id: str,
        content: str,
        metadata: Optional[dict] = None,
    ) -> None:
        """Add or update entry embedding."""
        # Sanitize metadata - ChromaDB only accepts str, int, float, bool, None
        clean_meta = {}
        if metadata:
            for k, v in metadata.items():
                if isinstance(v, list):
                    clean_meta[k] = ",".join(str(x) for x in v) if v else ""
                elif isinstance(v, (str, int, float, bool)) or v is None:
                    clean_meta[k] = v
                else:
                    clean_meta[k] = str(v)

        # ChromaDB requires non-empty metadata or None
        self.collection.upsert(
            ids=[entry_id],
            documents=[content],
            metadatas=[clean_meta] if clean_meta else None,
        )

    def remove_entry(self, entry_id: str) -> None:
        """Remove entry from vector store."""
        try:
            self.collection.delete(ids=[entry_id])
        except Exception:
            pass

    def query(
        self,
        query_text: str,
        n_results: int = 5,
        where: Optional[dict] = None,
    ) -> list[dict]:
        """Query similar entries.

        Args:
            query_text: Search query
            n_results: Number of results to return
            where: Optional metadata filter

        Returns:
            List of matching entries with scores
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where,
            include=["documents", "metadatas", "distances"],
        )

        entries = []
        if results["ids"] and results["ids"][0]:
            for i, entry_id in enumerate(results["ids"][0]):
                entries.append({
                    "id": entry_id,
                    "content": results["documents"][0][i] if results["documents"] else "",
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else 0,
                })

        return entries

    def sync_from_storage(self, entries: list[dict]) -> tuple[int, int]:
        """Sync embeddings from storage entries.

        Args:
            entries: List of dicts with id, content, metadata

        Returns:
            Tuple of (added, removed) counts
        """
        # Get existing IDs
        existing = set()
        try:
            existing_data = self.collection.get()
            existing = set(existing_data["ids"]) if existing_data["ids"] else set()
        except Exception:
            pass

        current_ids = {e["id"] for e in entries}

        # Add/update entries
        added = 0
        for entry in entries:
            self.add_entry(entry["id"], entry["content"], entry.get("metadata"))
            if entry["id"] not in existing:
                added += 1

        # Remove deleted entries
        removed = 0
        for old_id in existing - current_ids:
            self.remove_entry(old_id)
            removed += 1

        return added, removed

    def count(self) -> int:
        """Get total number of embedded entries."""
        return self.collection.count()
