"""Base scraper and intelligence storage."""

import asyncio
import logging
import sqlite3
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


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
                    tags TEXT
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_intel_source ON intel_items(source)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_intel_scraped ON intel_items(scraped_at)
            """)

    def save(self, item: IntelItem) -> bool:
        """Save intel item, skip if URL exists."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR IGNORE INTO intel_items
                    (source, title, url, summary, content, published, tags)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    item.source,
                    item.title,
                    item.url,
                    item.summary,
                    item.content,
                    item.published.isoformat() if item.published else None,
                    ",".join(item.tags) if item.tags else None,
                ))
                return conn.total_changes > 0
        except sqlite3.IntegrityError:
            logger.debug("Duplicate URL skipped: %s", item.url)
            return False
        except sqlite3.Error as e:
            logger.error("DB error saving item %s: %s", item.url, e)
            return False

    def get_recent(self, days: int = 7, limit: int = 50) -> list[dict]:
        """Get recent intel items."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM intel_items
                WHERE scraped_at >= datetime('now', ?)
                ORDER BY scraped_at DESC
                LIMIT ?
            """, (f"-{days} days", limit))
            return [dict(row) for row in cursor.fetchall()]

    def search(self, query: str, limit: int = 20) -> list[dict]:
        """Simple text search in titles and summaries."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM intel_items
                WHERE title LIKE ? OR summary LIKE ?
                ORDER BY scraped_at DESC
                LIMIT ?
            """, (f"%{query}%", f"%{query}%", limit))
            return [dict(row) for row in cursor.fetchall()]


class BaseScraper(ABC):
    """Base class for intelligence scrapers."""

    def __init__(self, storage: IntelStorage):
        self.storage = storage
        self.client = httpx.Client(
            timeout=30.0,
            headers={"User-Agent": "AI-Coach/1.0 (Personal Use)"},
        )

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Unique source identifier."""
        pass

    @abstractmethod
    def scrape(self) -> list[IntelItem]:
        """Scrape and return intel items."""
        pass

    def fetch_html(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse HTML."""
        try:
            logger.debug("Fetching %s", url)
            response = self.client.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except httpx.HTTPStatusError as e:
            logger.warning("HTTP %d fetching %s", e.response.status_code, url)
            return None
        except httpx.RequestError as e:
            logger.warning("Request error fetching %s: %s", url, e)
            return None

    def save_items(self, items: list[IntelItem]) -> int:
        """Save items and return count of new items."""
        new_count = 0
        for item in items:
            if self.storage.save(item):
                new_count += 1
        return new_count


class AsyncBaseScraper(ABC):
    """Async base class for intelligence scrapers."""

    def __init__(self, storage: IntelStorage):
        self.storage = storage
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

    async def save_items(self, items: list[IntelItem]) -> int:
        """Save items and return count of new items."""
        new_count = 0
        for item in items:
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
