"""Dev.to scraper for trending developer articles."""

from datetime import datetime
from typing import Optional

import httpx
import structlog

from cli.retry import http_retry
from intelligence.scraper import BaseScraper, IntelItem, IntelStorage
from intelligence.utils import detect_tags
from shared_types import IntelSource

logger = structlog.get_logger().bind(source="devto")


class DevToScraper(BaseScraper):
    """Async scraper for Dev.to articles."""

    API_BASE = "https://dev.to/api/articles"

    def __init__(
        self,
        storage: IntelStorage,
        per_page: int = 30,
        top_period: str = "week",
    ):
        super().__init__(storage)
        self.per_page = per_page
        self.top_period = top_period  # week, month, year, infinity

    @property
    def source_name(self) -> str:
        return IntelSource.DEVTO

    @http_retry(exceptions=(httpx.HTTPStatusError, httpx.ConnectError, httpx.RequestError))
    async def scrape(self) -> list[IntelItem]:
        """Fetch trending articles from Dev.to."""
        items = []

        # Fetch top articles
        params = {"per_page": self.per_page, "top": self.top_period}
        try:
            response = await self.client.get(self.API_BASE, params=params)
            response.raise_for_status()
            articles = response.json()
            items = [self._parse_article(a) for a in articles]
            items = [i for i in items if i is not None]
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            logger.warning("Failed to fetch Dev.to: %s", e)

        logger.info("Scraped %d articles from Dev.to", len(items))
        return items

    def _parse_article(self, article: dict) -> Optional[IntelItem]:
        """Parse single Dev.to article."""
        try:
            title = article.get("title", "")
            if not title:
                return None

            url = article.get("url", "")
            description = article.get("description", "")[:500]

            # Stats
            reactions = article.get("public_reactions_count", 0)
            comments = article.get("comments_count", 0)
            reading_time = article.get("reading_time_minutes", 0)

            summary_parts = []
            if reactions:
                summary_parts.append(f"{reactions} reactions")
            if comments:
                summary_parts.append(f"{comments} comments")
            if reading_time:
                summary_parts.append(f"{reading_time} min read")
            if description:
                summary_parts.append(description)

            # Published
            pub_str = article.get("published_at")
            published = None
            if pub_str:
                try:
                    published = datetime.fromisoformat(pub_str.replace("Z", "+00:00"))
                except ValueError:
                    pass

            # Tags
            tags = article.get("tag_list", [])[:5]
            tags.extend(detect_tags(title))
            if reactions > 500:
                tags.append("popular")
            tags = list(dict.fromkeys(tags))[:8]

            # Author
            user = article.get("user", {})
            author = user.get("name", user.get("username", ""))

            return IntelItem(
                source=self.source_name,
                title=title,
                url=url,
                summary=" | ".join(summary_parts),
                content=f"By {author}. {description}" if author else description,
                published=published,
                tags=tags,
            )

        except (KeyError, TypeError, ValueError) as e:
            logger.debug("Failed to parse Dev.to article: %s", e)
            return None
