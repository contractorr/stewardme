"""Crunchbase scraper for startup funding and market data."""

from datetime import datetime
from typing import Optional

import httpx
import structlog

from cli.retry import http_retry
from intelligence.scraper import BaseScraper, IntelItem, IntelStorage
from intelligence.utils import detect_tags
from shared_types import IntelSource

logger = structlog.get_logger().bind(source="crunchbase")


class CrunchbaseScraper(BaseScraper):
    """Async scraper for Crunchbase API (requires API key)."""

    API_BASE = "https://api.crunchbase.com/api/v4"

    def __init__(
        self,
        storage: IntelStorage,
        api_key: str,
        limit: int = 30,
    ):
        super().__init__(storage)
        self.api_key = api_key
        self.limit = limit
        self.client.headers["X-cb-user-key"] = api_key

    @property
    def source_name(self) -> str:
        return IntelSource.CRUNCHBASE

    async def scrape(self) -> list[IntelItem]:
        """Fetch recent funding rounds from Crunchbase."""
        items = []

        # Fetch recent funding rounds
        funding_items = await self._fetch_funding_rounds()
        items.extend(funding_items)

        # Fetch recent acquisitions
        acq_items = await self._fetch_acquisitions()
        items.extend(acq_items)

        logger.info("Scraped %d items from Crunchbase", len(items))
        return items

    @http_retry(exceptions=(httpx.HTTPStatusError, httpx.ConnectError, httpx.RequestError))
    async def _fetch_funding_rounds(self) -> list[IntelItem]:
        """Fetch recent funding rounds."""
        url = f"{self.API_BASE}/searches/funding_rounds"
        payload = {
            "field_ids": [
                "identifier",
                "funded_organization_identifier",
                "announced_on",
                "money_raised",
                "investment_type",
                "investor_identifiers",
                "short_description",
            ],
            "order": [{"field_id": "announced_on", "sort": "desc"}],
            "limit": self.limit,
        }

        try:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return self._parse_funding_rounds(data.get("entities", []))
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            logger.warning("Failed to fetch Crunchbase funding: %s", e)
            return []

    @http_retry(exceptions=(httpx.HTTPStatusError, httpx.ConnectError, httpx.RequestError))
    async def _fetch_acquisitions(self) -> list[IntelItem]:
        """Fetch recent acquisitions."""
        url = f"{self.API_BASE}/searches/acquisitions"
        payload = {
            "field_ids": [
                "identifier",
                "acquiree_identifier",
                "acquirer_identifier",
                "announced_on",
                "price",
                "short_description",
            ],
            "order": [{"field_id": "announced_on", "sort": "desc"}],
            "limit": self.limit // 2,
        }

        try:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return self._parse_acquisitions(data.get("entities", []))
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            logger.warning("Failed to fetch Crunchbase acquisitions: %s", e)
            return []

    def _parse_funding_rounds(self, entities: list) -> list[IntelItem]:
        """Parse funding round entities."""
        items = []
        for entity in entities:
            item = self._parse_funding_round(entity)
            if item:
                items.append(item)
        return items

    def _parse_funding_round(self, entity: dict) -> Optional[IntelItem]:
        """Parse single funding round."""
        try:
            props = entity.get("properties", {})
            uuid = entity.get("uuid", "")

            # Get company info
            org = props.get("funded_organization_identifier", {})
            company = org.get("value", "Unknown Company")
            org_uuid = org.get("uuid", "")

            # Investment type and amount
            inv_type = props.get("investment_type", "funding")
            money = props.get("money_raised", {})
            amount = money.get("value_usd")
            amount_str = f"${amount:,.0f}" if amount else "undisclosed"

            title = f"{company} raises {amount_str} ({inv_type})"

            # URL
            url = f"https://www.crunchbase.com/funding_round/{uuid}" if uuid else ""

            # Date
            announced = props.get("announced_on")
            published = None
            if announced:
                try:
                    published = datetime.fromisoformat(announced)
                except ValueError:
                    pass

            # Investors
            investors = props.get("investor_identifiers", [])
            investor_names = [i.get("value", "") for i in investors[:3]]
            desc = props.get("short_description", "")

            summary_parts = [amount_str, inv_type]
            if investor_names:
                summary_parts.append(f"from {', '.join(investor_names)}")
            if desc:
                summary_parts.append(desc[:200])

            # Tags
            tags = ["funding", inv_type]
            if amount and amount >= 100_000_000:
                tags.append("mega-round")
            elif amount and amount >= 10_000_000:
                tags.append("significant")
            tags.extend(detect_tags(company))
            tags = list(dict.fromkeys(tags))[:8]

            return IntelItem(
                source=self.source_name,
                title=title,
                url=url,
                summary=" | ".join(summary_parts),
                content=desc,
                published=published,
                tags=tags,
            )

        except (KeyError, TypeError, ValueError) as e:
            logger.debug("Failed to parse funding round: %s", e)
            return None

    def _parse_acquisitions(self, entities: list) -> list[IntelItem]:
        """Parse acquisition entities."""
        items = []
        for entity in entities:
            item = self._parse_acquisition(entity)
            if item:
                items.append(item)
        return items

    def _parse_acquisition(self, entity: dict) -> Optional[IntelItem]:
        """Parse single acquisition."""
        try:
            props = entity.get("properties", {})
            uuid = entity.get("uuid", "")

            # Get companies
            acquiree = props.get("acquiree_identifier", {}).get("value", "Unknown")
            acquirer = props.get("acquirer_identifier", {}).get("value", "Unknown")

            # Price
            price = props.get("price", {}).get("value_usd")
            price_str = f"${price:,.0f}" if price else "undisclosed"

            title = f"{acquirer} acquires {acquiree}"

            # URL
            url = f"https://www.crunchbase.com/acquisition/{uuid}" if uuid else ""

            # Date
            announced = props.get("announced_on")
            published = None
            if announced:
                try:
                    published = datetime.fromisoformat(announced)
                except ValueError:
                    pass

            desc = props.get("short_description", "")
            summary = f"{price_str} | {desc[:300]}" if desc else price_str

            # Tags
            tags = ["acquisition", "m&a"]
            if price and price >= 1_000_000_000:
                tags.append("billion-dollar")
            tags.extend(detect_tags(acquiree))
            tags = list(dict.fromkeys(tags))[:8]

            return IntelItem(
                source=self.source_name,
                title=title,
                url=url,
                summary=summary,
                content=desc,
                published=published,
                tags=tags,
            )

        except (KeyError, TypeError, ValueError) as e:
            logger.debug("Failed to parse acquisition: %s", e)
            return None
