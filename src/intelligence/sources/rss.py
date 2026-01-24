"""RSS feed scraper."""

import logging
from datetime import datetime
from time import mktime
from typing import Optional
from urllib.parse import urlparse

import feedparser
from bs4 import BeautifulSoup

from intelligence.scraper import AsyncBaseScraper, BaseScraper, IntelItem, IntelStorage
from intelligence.utils import detect_tags

logger = logging.getLogger(__name__)


def _extract_name(url: str) -> str:
    """Extract readable name from URL."""
    domain = urlparse(url).netloc
    return domain.replace("www.", "").split(".")[0]


class RSSFeedScraper(BaseScraper):
    """Scraper for RSS/Atom feeds."""

    def __init__(self, storage: IntelStorage, feed_url: str, name: Optional[str] = None):
        super().__init__(storage)
        self.feed_url = feed_url
        self._name = name or _extract_name(feed_url)

    @property
    def source_name(self) -> str:
        return f"rss:{self._name}"

    def scrape(self) -> list[IntelItem]:
        """Parse RSS feed and return items."""
        logger.debug("Parsing RSS feed: %s", self.feed_url)
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

            summary = BeautifulSoup(summary, "html.parser").get_text()[:500]
            title = entry.get("title", "Untitled")

            # Get tags from feed entry categories + detect from title
            tags = _extract_entry_tags(entry)
            tags.extend(detect_tags(title))
            tags = list(dict.fromkeys(tags))[:5]  # Dedupe, limit to 5

            items.append(IntelItem(
                source=self.source_name,
                title=title,
                url=entry.get("link", ""),
                summary=summary,
                published=published,
                tags=tags,
            ))

        logger.info("Scraped %d items from %s", len(items), self._name)
        return items


def _extract_entry_tags(entry) -> list[str]:
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
        self._name = name or _extract_name(feed_url)

    @property
    def source_name(self) -> str:
        return f"rss:{self._name}"

    async def scrape(self) -> list[IntelItem]:
        """Parse RSS feed asynchronously."""
        try:
            logger.debug("Fetching RSS feed: %s", self.feed_url)
            response = await self.client.get(self.feed_url)
            response.raise_for_status()
            content = response.text
        except Exception as e:
            logger.warning("Failed to fetch RSS %s: %s", self.feed_url, e)
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
            title = entry.get("title", "Untitled")

            tags = _extract_entry_tags(entry)
            tags.extend(detect_tags(title))
            tags = list(dict.fromkeys(tags))[:5]

            items.append(IntelItem(
                source=self.source_name,
                title=title,
                url=entry.get("link", ""),
                summary=summary,
                published=published,
                tags=tags,
            ))

        logger.info("Scraped %d items from %s", len(items), self._name)
        return items
