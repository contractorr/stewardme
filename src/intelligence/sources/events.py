"""Event scraper — confs.tech JSON API + RSS feeds for tech events."""

import asyncio
import json
from datetime import datetime
from typing import Optional

import structlog

from intelligence.scraper import BaseScraper, IntelItem, IntelStorage
from shared_types import IntelSource

logger = structlog.get_logger()

CONFS_TECH_API = "https://raw.githubusercontent.com/tech-conferences/confs.tech/main/conferences"
CURRENT_YEAR = datetime.now().year


class EventScraper(BaseScraper):
    """Scrape tech events from confs.tech and RSS feeds."""

    def __init__(
        self,
        storage: IntelStorage,
        topics: Optional[list[str]] = None,
        location_filter: Optional[str] = None,
        rss_feeds: Optional[list[str]] = None,
        embedding_manager=None,
    ):
        super().__init__(storage, embedding_manager)
        self.topics = topics or ["javascript", "python", "devops", "data", "general"]
        self.location_filter = (location_filter or "").lower()
        self.rss_feeds = rss_feeds or []

    @property
    def source_name(self) -> str:
        return IntelSource.EVENTS

    async def scrape(self) -> list[IntelItem]:
        """Scrape events from all configured sources."""
        tasks = [self._scrape_confs_tech()]
        for url in self.rss_feeds:
            tasks.append(self._scrape_rss_events(url))
        results = await asyncio.gather(*tasks, return_exceptions=True)

        items = []
        for result in results:
            if isinstance(result, list):
                items.extend(result)
            elif isinstance(result, Exception):
                logger.warning("event_scrape_error", error=str(result))
        return items

    async def _scrape_confs_tech(self) -> list[IntelItem]:
        """Scrape confs.tech GitHub JSON data."""
        items = []
        for year in [CURRENT_YEAR, CURRENT_YEAR + 1]:
            for topic in self.topics:
                url = f"{CONFS_TECH_API}/{year}/{topic}.json"
                try:
                    response = await self.client.get(url)
                    if response.status_code != 200:
                        continue
                    events = response.json()
                    for event in events:
                        item = self._parse_confs_tech_event(event, topic)
                        if item:
                            items.append(item)
                except Exception as e:
                    logger.debug("confs_tech_fetch_failed", topic=topic, year=year, error=str(e))
        return items

    def _parse_confs_tech_event(self, event: dict, topic: str) -> Optional[IntelItem]:
        """Parse a confs.tech event into IntelItem."""
        name = event.get("name", "")
        url = event.get("url", "")
        if not name or not url:
            return None

        city = event.get("city", "")
        country = event.get("country", "")
        location = f"{city}, {country}" if city else country
        start_date = event.get("startDate", "")
        end_date = event.get("endDate", "")
        cfp_url = event.get("cfpUrl", "")
        cfp_end = event.get("cfpEndDate", "")
        online = event.get("online", False)

        # Location filter
        if self.location_filter and not online:
            loc_lower = location.lower()
            if self.location_filter not in loc_lower and country.lower() not in self.location_filter:
                return None

        # Build summary
        parts = [f"Date: {start_date}"]
        if end_date and end_date != start_date:
            parts[0] = f"Date: {start_date} to {end_date}"
        if location:
            parts.append(f"Location: {location}")
        if online:
            parts.append("Online")
        if cfp_end:
            parts.append(f"CFP deadline: {cfp_end}")
        summary = " | ".join(parts)

        tags = ["event", topic]
        if online:
            tags.append("online")
        if cfp_url:
            tags.append("cfp-open")

        # Parse date
        published = None
        if start_date:
            try:
                published = datetime.fromisoformat(start_date)
            except ValueError:
                pass

        # Store extra metadata in content as JSON
        metadata = {
            "event_date": start_date,
            "end_date": end_date,
            "location": location,
            "cfp_deadline": cfp_end,
            "cfp_url": cfp_url,
            "registration_url": url,
            "event_type": "conference",
            "online": online,
            "topic": topic,
        }

        return IntelItem(
            source=IntelSource.CONFS_TECH,
            title=name,
            url=url,
            summary=summary,
            content=json.dumps(metadata),
            published=published,
            tags=tags,
        )

    async def _scrape_rss_events(self, feed_url: str) -> list[IntelItem]:
        """Scrape events from RSS feed."""
        try:
            import feedparser

            response = await self.client.get(feed_url)
            if response.status_code != 200:
                return []

            feed = feedparser.parse(response.text)
            items = []
            for entry in feed.entries[:30]:
                title = entry.get("title", "")
                link = entry.get("link", "")
                description = entry.get("summary", entry.get("description", ""))[:300]
                published = None
                if entry.get("published_parsed"):
                    try:
                        published = datetime(*entry.published_parsed[:6])
                    except (TypeError, ValueError):
                        pass

                if title and link:
                    items.append(IntelItem(
                        source=IntelSource.EVENTS,
                        title=title,
                        url=link,
                        summary=description,
                        published=published,
                        tags=["event", "rss"],
                    ))
            return items
        except Exception as e:
            logger.warning("rss_events_failed", url=feed_url, error=str(e))
            return []
