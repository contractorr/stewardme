"""RSS feed scraper."""

from datetime import datetime
from time import mktime
from typing import Optional
from urllib.parse import urlparse

import feedparser
import httpx
import structlog
from bs4 import BeautifulSoup

from cli.retry import http_retry
from intelligence.scraper import BaseScraper, IntelItem, IntelStorage
from intelligence.utils import detect_tags
from shared_types import IntelSource

logger = structlog.get_logger().bind(source="rss")


def _extract_name(url: str) -> str:
    """Extract readable name from URL."""
    domain = urlparse(url).netloc
    return domain.replace("www.", "").split(".")[0]


def _extract_entry_tags(entry) -> list[str]:
    """Extract tags/categories from feed entry."""
    tags = []
    if hasattr(entry, "tags"):
        tags = [t.term for t in entry.tags if hasattr(t, "term")][:5]
    return tags


class RSSFeedScraper(BaseScraper):
    """Async scraper for RSS/Atom feeds."""

    def __init__(self, storage: IntelStorage, feed_url: str, name: Optional[str] = None):
        super().__init__(storage)
        self.feed_url = feed_url
        self._name = name or _extract_name(feed_url)

    @property
    def source_name(self) -> str:
        return f"{IntelSource.RSS}:{self._name}"

    @http_retry(exceptions=(httpx.HTTPStatusError, httpx.ConnectError, httpx.RequestError))
    async def scrape(self) -> list[IntelItem]:
        """Parse RSS feed asynchronously."""
        try:
            logger.debug("Fetching RSS feed: %s", self.feed_url)
            response = await self.client.get(self.feed_url)
            response.raise_for_status()
            content = response.text
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
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
