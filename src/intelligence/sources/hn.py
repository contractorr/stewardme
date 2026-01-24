"""Hacker News scraper."""

import asyncio
from datetime import datetime
from typing import Optional

import httpx
from bs4 import BeautifulSoup

from intelligence.scraper import AsyncBaseScraper, BaseScraper, IntelItem, IntelStorage


class HackerNewsScraper(BaseScraper):
    """Scraper for Hacker News top stories."""

    API_BASE = "https://hacker-news.firebaseio.com/v0"

    def __init__(self, storage: IntelStorage, max_stories: int = 30):
        super().__init__(storage)
        self.max_stories = max_stories

    @property
    def source_name(self) -> str:
        return "hackernews"

    def scrape(self) -> list[IntelItem]:
        """Fetch top HN stories."""
        items = []

        try:
            # Get top story IDs
            response = self.client.get(f"{self.API_BASE}/topstories.json")
            story_ids = response.json()[:self.max_stories]

            for story_id in story_ids:
                item = self._fetch_story(story_id)
                if item:
                    items.append(item)

        except Exception:
            pass

        return items

    def _fetch_story(self, story_id: int) -> Optional[IntelItem]:
        """Fetch single story details."""
        try:
            response = self.client.get(f"{self.API_BASE}/item/{story_id}.json")
            data = response.json()

            if not data or data.get("type") != "story":
                return None

            # Build summary from available data
            summary_parts = []
            if data.get("score"):
                summary_parts.append(f"{data['score']} points")
            if data.get("descendants"):
                summary_parts.append(f"{data['descendants']} comments")
            if data.get("text"):
                # For Ask HN / Show HN posts
                from bs4 import BeautifulSoup
                text = BeautifulSoup(data["text"], "html.parser").get_text()[:300]
                summary_parts.append(text)

            return IntelItem(
                source=self.source_name,
                title=data.get("title", "Untitled"),
                url=data.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                summary=" | ".join(summary_parts) if summary_parts else "",
                published=datetime.fromtimestamp(data["time"]) if data.get("time") else None,
                tags=self._detect_tags(data.get("title", "")),
            )

        except Exception:
            return None

    def _detect_tags(self, title: str) -> list[str]:
        """Detect tags from title patterns."""
        tags = []
        title_lower = title.lower()

        if title.startswith("Ask HN:"):
            tags.append("ask-hn")
        elif title.startswith("Show HN:"):
            tags.append("show-hn")
        elif title.startswith("Tell HN:"):
            tags.append("tell-hn")

        # Topic detection
        topics = {
            "ai": ["ai", "llm", "gpt", "machine learning", "neural"],
            "startup": ["startup", "founder", "yc", "funding", "venture"],
            "programming": ["rust", "python", "javascript", "golang", "typescript"],
            "career": ["hiring", "job", "career", "interview", "salary"],
        }

        for tag, keywords in topics.items():
            if any(kw in title_lower for kw in keywords):
                tags.append(tag)

        return tags[:5]


class AsyncHackerNewsScraper(AsyncBaseScraper):
    """Async scraper for Hacker News top stories."""

    API_BASE = "https://hacker-news.firebaseio.com/v0"

    def __init__(self, storage: IntelStorage, max_stories: int = 30):
        super().__init__(storage)
        self.max_stories = max_stories

    @property
    def source_name(self) -> str:
        return "hackernews"

    async def scrape(self) -> list[IntelItem]:
        """Fetch top HN stories concurrently."""
        items = []

        try:
            response = await self.client.get(f"{self.API_BASE}/topstories.json")
            story_ids = response.json()[:self.max_stories]

            # Fetch stories concurrently with semaphore for rate limiting
            semaphore = asyncio.Semaphore(10)
            tasks = [self._fetch_story_limited(semaphore, sid) for sid in story_ids]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, IntelItem):
                    items.append(result)

        except Exception:
            pass

        return items

    async def _fetch_story_limited(self, semaphore: asyncio.Semaphore, story_id: int) -> Optional[IntelItem]:
        """Fetch story with rate limiting."""
        async with semaphore:
            return await self._fetch_story(story_id)

    async def _fetch_story(self, story_id: int) -> Optional[IntelItem]:
        """Fetch single story details."""
        try:
            response = await self.client.get(f"{self.API_BASE}/item/{story_id}.json")
            data = response.json()

            if not data or data.get("type") != "story":
                return None

            summary_parts = []
            if data.get("score"):
                summary_parts.append(f"{data['score']} points")
            if data.get("descendants"):
                summary_parts.append(f"{data['descendants']} comments")
            if data.get("text"):
                text = BeautifulSoup(data["text"], "html.parser").get_text()[:300]
                summary_parts.append(text)

            return IntelItem(
                source=self.source_name,
                title=data.get("title", "Untitled"),
                url=data.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                summary=" | ".join(summary_parts) if summary_parts else "",
                published=datetime.fromtimestamp(data["time"]) if data.get("time") else None,
                tags=self._detect_tags(data.get("title", "")),
            )

        except Exception:
            return None

    def _detect_tags(self, title: str) -> list[str]:
        """Detect tags from title patterns."""
        tags = []
        title_lower = title.lower()

        if title.startswith("Ask HN:"):
            tags.append("ask-hn")
        elif title.startswith("Show HN:"):
            tags.append("show-hn")
        elif title.startswith("Tell HN:"):
            tags.append("tell-hn")

        topics = {
            "ai": ["ai", "llm", "gpt", "machine learning", "neural"],
            "startup": ["startup", "founder", "yc", "funding", "venture"],
            "programming": ["rust", "python", "javascript", "golang", "typescript"],
            "career": ["hiring", "job", "career", "interview", "salary"],
        }

        for tag, keywords in topics.items():
            if any(kw in title_lower for kw in keywords):
                tags.append(tag)

        return tags[:5]
