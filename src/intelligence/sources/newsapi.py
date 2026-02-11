"""NewsAPI scraper for aggregated tech news."""

from datetime import datetime, timedelta
from typing import Optional

import httpx
import structlog

from cli.retry import http_retry
from intelligence.scraper import BaseScraper, IntelItem, IntelStorage
from intelligence.utils import detect_tags
from shared_types import IntelSource

logger = structlog.get_logger().bind(source="newsapi")

# Default search queries for tech/startup news
DEFAULT_QUERIES = [
    "startup funding",
    "artificial intelligence",
    "tech layoffs",
    "software engineering",
]


class NewsAPIScraper(BaseScraper):
    """Async scraper for NewsAPI (requires API key)."""

    API_BASE = "https://newsapi.org/v2"

    def __init__(
        self,
        storage: IntelStorage,
        api_key: str,
        queries: Optional[list[str]] = None,
        page_size: int = 20,
        days_back: int = 7,
    ):
        super().__init__(storage)
        self.api_key = api_key
        self.queries = queries or DEFAULT_QUERIES
        self.page_size = page_size
        self.days_back = days_back

    @property
    def source_name(self) -> str:
        return IntelSource.NEWSAPI

    async def scrape(self) -> list[IntelItem]:
        """Fetch news from multiple queries."""
        items = []
        seen_urls = set()

        for query in self.queries:
            query_items = await self._fetch_query(query)
            # Dedupe by URL
            for item in query_items:
                if item.url not in seen_urls:
                    seen_urls.add(item.url)
                    items.append(item)

        logger.info("Scraped %d articles from NewsAPI", len(items))
        return items

    @http_retry(exceptions=(httpx.HTTPStatusError, httpx.ConnectError, httpx.RequestError))
    async def _fetch_query(self, query: str) -> list[IntelItem]:
        """Fetch articles for single query."""
        url = f"{self.API_BASE}/everything"
        from_date = (datetime.now() - timedelta(days=self.days_back)).strftime("%Y-%m-%d")

        params = {
            "q": query,
            "apiKey": self.api_key,
            "language": "en",
            "sortBy": "relevancy",
            "pageSize": self.page_size,
            "from": from_date,
        }

        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("status") != "ok":
                logger.warning("NewsAPI error: %s", data.get("message"))
                return []

            return self._parse_articles(data.get("articles", []), query)
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            logger.warning("Failed to fetch NewsAPI query '%s': %s", query, e)
            return []

    def _parse_articles(self, articles: list, query: str) -> list[IntelItem]:
        """Parse article list."""
        items = []
        for article in articles:
            item = self._parse_article(article, query)
            if item:
                items.append(item)
        return items

    def _parse_article(self, article: dict, query: str) -> Optional[IntelItem]:
        """Parse single article."""
        try:
            title = article.get("title", "")
            if not title or title == "[Removed]":
                return None

            url = article.get("url", "")
            if not url:
                return None

            description = article.get("description", "") or ""
            content = article.get("content", "") or ""

            # Source
            source = article.get("source", {}).get("name", "")

            # Summary
            summary_parts = []
            if source:
                summary_parts.append(source)
            if description:
                summary_parts.append(description[:300])

            # Published date
            pub_str = article.get("publishedAt")
            published = None
            if pub_str:
                try:
                    published = datetime.fromisoformat(pub_str.replace("Z", "+00:00"))
                except ValueError:
                    pass

            # Tags
            tags = [query.split()[0]]  # First word of query
            if source:
                tags.append(source.lower().replace(" ", "-"))
            tags.extend(detect_tags(title))
            tags = list(dict.fromkeys(tags))[:8]

            # Content (truncated)
            full_content = content[:1000] if content else description

            return IntelItem(
                source=self.source_name,
                title=title,
                url=url,
                summary=" | ".join(summary_parts),
                content=full_content,
                published=published,
                tags=tags,
            )

        except (KeyError, TypeError, ValueError) as e:
            logger.debug("Failed to parse NewsAPI article: %s", e)
            return None

    @http_retry(exceptions=(httpx.HTTPStatusError, httpx.ConnectError, httpx.RequestError))
    async def fetch_top_headlines(self, category: str = "technology") -> list[IntelItem]:
        """Fetch top headlines (alternative endpoint)."""
        url = f"{self.API_BASE}/top-headlines"
        params = {
            "apiKey": self.api_key,
            "category": category,
            "language": "en",
            "pageSize": self.page_size,
        }

        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("status") != "ok":
                return []

            return self._parse_articles(data.get("articles", []), category)
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            logger.warning("Failed to fetch top headlines: %s", e)
            return []
