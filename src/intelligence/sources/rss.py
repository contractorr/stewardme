"""RSS feed scraper."""

from datetime import datetime
from typing import Optional
from time import mktime

import feedparser
from bs4 import BeautifulSoup

from intelligence.scraper import AsyncBaseScraper, BaseScraper, IntelItem, IntelStorage


class RSSFeedScraper(BaseScraper):
    """Scraper for RSS/Atom feeds."""

    def __init__(self, storage: IntelStorage, feed_url: str, name: Optional[str] = None):
        super().__init__(storage)
        self.feed_url = feed_url
        self._name = name or self._extract_name(feed_url)

    def _extract_name(self, url: str) -> str:
        """Extract readable name from URL."""
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        return domain.replace("www.", "").split(".")[0]

    @property
    def source_name(self) -> str:
        return f"rss:{self._name}"

    def scrape(self) -> list[IntelItem]:
        """Parse RSS feed and return items."""
        feed = feedparser.parse(self.feed_url)
        items = []

        for entry in feed.entries[:20]:  # Limit per feed
            published = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = datetime.fromtimestamp(mktime(entry.published_parsed))

            # Get summary or truncated content
            summary = ""
            if hasattr(entry, "summary"):
                summary = entry.summary[:500]
            elif hasattr(entry, "content"):
                summary = entry.content[0].value[:500] if entry.content else ""

            # Strip HTML tags from summary
            from bs4 import BeautifulSoup
            summary = BeautifulSoup(summary, "html.parser").get_text()[:500]

            items.append(IntelItem(
                source=self.source_name,
                title=entry.get("title", "Untitled"),
                url=entry.get("link", ""),
                summary=summary,
                published=published,
                tags=self._extract_tags(entry),
            ))

        return items

    def _extract_tags(self, entry) -> list[str]:
        """Extract tags/categories from feed entry."""
        tags = []
        if hasattr(entry, "tags"):
            tags = [t.term for t in entry.tags if hasattr(t, "term")][:5]
        return tags


class AsyncRSSFeedScraper(AsyncBaseScraper):
    """Async scraper for RSS/Atom feeds."""

    def __init__(self, storage: IntelStorage, feed_url: str, name: Optional[str] = None):
        super().__init__(storage)
        self.feed_url = feed_url
        self._name = name or self._extract_name(feed_url)

    def _extract_name(self, url: str) -> str:
        """Extract readable name from URL."""
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        return domain.replace("www.", "").split(".")[0]

    @property
    def source_name(self) -> str:
        return f"rss:{self._name}"

    async def scrape(self) -> list[IntelItem]:
        """Parse RSS feed asynchronously."""
        try:
            response = await self.client.get(self.feed_url)
            response.raise_for_status()
            content = response.text
        except Exception:
            return []

        # feedparser is sync but parsing is fast
        feed = feedparser.parse(content)
        items = []

        for entry in feed.entries[:20]:
            published = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = datetime.fromtimestamp(mktime(entry.published_parsed))

            summary = ""
            if hasattr(entry, "summary"):
                summary = entry.summary[:500]
            elif hasattr(entry, "content"):
                summary = entry.content[0].value[:500] if entry.content else ""

            summary = BeautifulSoup(summary, "html.parser").get_text()[:500]

            items.append(IntelItem(
                source=self.source_name,
                title=entry.get("title", "Untitled"),
                url=entry.get("link", ""),
                summary=summary,
                published=published,
                tags=self._extract_tags(entry),
            ))

        return items

    def _extract_tags(self, entry) -> list[str]:
        """Extract tags/categories from feed entry."""
        tags = []
        if hasattr(entry, "tags"):
            tags = [t.term for t in entry.tags if hasattr(t, "term")][:5]
        return tags
