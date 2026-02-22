"""Base scraper and intelligence storage."""

import hashlib
import sqlite3
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import httpx
import structlog
from bs4 import BeautifulSoup

logger = structlog.get_logger().bind(source="intel_storage")

_ALLOWED_SCHEMES = {"http", "https"}
_INTERNAL_SCHEMES = {"research"}


def validate_url(url: str) -> bool:
    """Validate URL has allowed scheme and reasonable structure."""
    if not url:
        return False
    try:
        parsed = urlparse(url)
        # Internal schemes (research://) are always valid
        if parsed.scheme in _INTERNAL_SCHEMES:
            return True
        if parsed.scheme not in _ALLOWED_SCHEMES:
            return False
        if not parsed.netloc or "." not in parsed.netloc:
            return False
        return True
    except Exception:
        return False


@dataclass
class IntelItem:
    """Single intelligence item."""

    source: str
    title: str
    url: str
    summary: str
    content: Optional[str] = None
    published: Optional[datetime] = None
    tags: Optional[list[str]] = None
    content_hash: Optional[str] = None

    def compute_hash(self) -> str:
        """Compute content hash for deduplication."""
        text = f"{self.title.lower().strip()}|{self.summary.lower().strip()}"
        return hashlib.sha256(text.encode()).hexdigest()[:16]


class IntelStorage:
    """SQLite storage for intelligence items."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS intel_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    title TEXT NOT NULL,
                    url TEXT UNIQUE NOT NULL,
                    summary TEXT,
                    content TEXT,
                    published TIMESTAMP,
                    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tags TEXT,
                    content_hash TEXT
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_intel_source ON intel_items(source)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_intel_scraped ON intel_items(scraped_at)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_intel_hash ON intel_items(content_hash)
            """)
            # Add column if not exists (for existing DBs)
            try:
                conn.execute("ALTER TABLE intel_items ADD COLUMN content_hash TEXT")
            except sqlite3.OperationalError:
                pass  # Column already exists

    def save(self, item: IntelItem) -> bool:
        """Save intel item, skip if URL invalid/exists or content hash exists."""
        if not validate_url(item.url):
            logger.warning("Invalid URL rejected: %s", item.url[:100])
            return False

        content_hash = item.content_hash or item.compute_hash()

        # Check for hash-based duplicate
        if self.hash_exists(content_hash):
            logger.info("Duplicate content skipped (hash): %s", item.title[:50])
            return False

        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO intel_items
                    (source, title, url, summary, content, published, tags, content_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        item.source,
                        item.title,
                        item.url,
                        item.summary,
                        item.content,
                        item.published.isoformat() if item.published else None,
                        ",".join(item.tags) if item.tags else None,
                        content_hash,
                    ),
                )
                return conn.total_changes > 0
        except sqlite3.IntegrityError:
            logger.debug("Duplicate URL skipped: %s", item.url)
            return False
        except sqlite3.Error as e:
            logger.error("DB error saving item %s: %s", item.url, e)
            return False

    def hash_exists(self, content_hash: str, days: int = 7) -> bool:
        """Check if content hash exists in recent items."""
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                """
                SELECT 1 FROM intel_items
                WHERE content_hash = ?
                AND scraped_at >= datetime('now', ?)
                LIMIT 1
            """,
                (content_hash, f"-{days} days"),
            ).fetchone()
            return row is not None

    def get_recent(self, days: int = 7, limit: int = 50) -> list[dict]:
        """Get recent intel items."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT * FROM intel_items
                WHERE scraped_at >= datetime('now', ?)
                ORDER BY scraped_at DESC
                LIMIT ?
            """,
                (f"-{days} days", limit),
            )
            return [dict(row) for row in cursor.fetchall()]

    def search(self, query: str, limit: int = 20) -> list[dict]:
        """Simple text search in titles and summaries."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT * FROM intel_items
                WHERE title LIKE ? OR summary LIKE ?
                ORDER BY scraped_at DESC
                LIMIT ?
            """,
                (f"%{query}%", f"%{query}%", limit),
            )
            return [dict(row) for row in cursor.fetchall()]


class BaseScraper(ABC):
    """Async base class for intelligence scrapers."""

    def __init__(self, storage: IntelStorage, embedding_manager=None):
        self.storage = storage
        self.embedding_manager = embedding_manager
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={"User-Agent": "AI-Coach/1.0 (Personal Use)"},
        )

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Unique source identifier."""
        pass

    @abstractmethod
    async def scrape(self) -> list[IntelItem]:
        """Scrape and return intel items."""
        pass

    async def fetch_html(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse HTML asynchronously."""
        try:
            logger.debug("Fetching %s", url)
            response = await self.client.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except httpx.HTTPStatusError as e:
            logger.warning("HTTP %d fetching %s", e.response.status_code, url)
            return None
        except httpx.RequestError as e:
            logger.warning("Request error fetching %s: %s", url, e)
            return None

    async def save_items(self, items: list[IntelItem], semantic_dedup: bool = True) -> int:
        """Save items and return count of new items.

        Args:
            items: List of items to save
            semantic_dedup: Check for semantic duplicates via embeddings

        Returns:
            Count of new items saved
        """
        new_count = 0
        for item in items:
            # Semantic dedup check if embedding manager available
            if semantic_dedup and self.embedding_manager:
                content = f"{item.title} {item.summary}"
                if self.embedding_manager.find_similar(content, threshold=0.85):
                    logger.info("Semantic duplicate skipped: %s", item.title[:50])
                    continue

            if self.storage.save(item):
                new_count += 1
        return new_count

    async def close(self):
        """Close the async client."""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
