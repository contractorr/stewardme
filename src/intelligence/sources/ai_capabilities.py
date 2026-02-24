"""AI capabilities scraper — METR evals, Chatbot Arena, HELM benchmarks."""

from datetime import datetime
from typing import Optional

import httpx
import structlog

from cli.retry import http_retry
from intelligence.scraper import BaseScraper, IntelItem, IntelStorage
from shared_types import IntelSource

logger = structlog.get_logger().bind(source="ai_capabilities")

_DEFAULT_TAGS = ["ai-capabilities", "benchmarks"]


class AICapabilitiesScraper(BaseScraper):
    """Scrapes AI capability benchmarks from METR, Chatbot Arena, and HELM."""

    METR_API = "https://api.github.com/repos/METR/autonomy-evals/releases"
    CHATBOT_ARENA_URL = "https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard"
    HELM_URL = "https://crfm.stanford.edu/helm/latest/"

    def __init__(
        self,
        storage: IntelStorage,
        sources: Optional[list[str]] = None,
        max_items_per_source: int = 10,
    ):
        super().__init__(storage)
        self.enabled_sources = sources or ["metr", "chatbot_arena", "helm"]
        self.max_items = max_items_per_source

    @property
    def source_name(self) -> str:
        return IntelSource.AI_CAPABILITIES

    @http_retry(exceptions=(httpx.HTTPStatusError, httpx.ConnectError, httpx.RequestError))
    async def scrape(self) -> list[IntelItem]:
        """Scrape all enabled AI capability sources."""
        items: list[IntelItem] = []

        if "metr" in self.enabled_sources:
            items.extend(await self._scrape_metr())

        if "chatbot_arena" in self.enabled_sources:
            items.extend(await self._scrape_chatbot_arena())

        if "helm" in self.enabled_sources:
            items.extend(await self._scrape_helm())

        logger.info("Scraped %d AI capability items", len(items))
        return items

    async def _scrape_metr(self) -> list[IntelItem]:
        """Fetch METR autonomy eval releases from GitHub API."""
        items = []
        try:
            response = await self.client.get(
                self.METR_API,
                headers={"Accept": "application/vnd.github+json"},
            )
            response.raise_for_status()
            releases = response.json()[: self.max_items]

            for rel in releases:
                published = None
                if rel.get("published_at"):
                    try:
                        published = datetime.fromisoformat(
                            rel["published_at"].replace("Z", "+00:00")
                        )
                    except (ValueError, TypeError):
                        pass

                body = (rel.get("body") or "")[:500]
                items.append(
                    IntelItem(
                        source=self.source_name,
                        title=f"METR Eval: {rel.get('name') or rel.get('tag_name', 'unknown')}",
                        url=rel.get("html_url", "https://github.com/METR/autonomy-evals"),
                        summary=body if body else f"Release {rel.get('tag_name', '')}",
                        published=published,
                        tags=_DEFAULT_TAGS + ["metr", "autonomy"],
                    )
                )
        except httpx.RequestError as e:
            logger.warning("METR scrape failed: %s", e)

        return items

    async def _scrape_chatbot_arena(self) -> list[IntelItem]:
        """Scrape Chatbot Arena leaderboard from HuggingFace."""
        items = []
        try:
            soup = await self.fetch_html(self.CHATBOT_ARENA_URL)
            if not soup:
                return items

            # Extract model rankings from the leaderboard page
            # HF spaces render dynamically; we extract whatever static content is available
            title_el = soup.find("title")
            page_title = title_el.get_text(strip=True) if title_el else "Chatbot Arena"

            # Look for table rows or model cards
            rows = soup.select("table tr, .model-row, [class*='leaderboard']")
            if rows:
                summaries = []
                for row in rows[: self.max_items]:
                    text = row.get_text(separator=" ", strip=True)[:200]
                    if text:
                        summaries.append(text)

                if summaries:
                    items.append(
                        IntelItem(
                            source=self.source_name,
                            title="Chatbot Arena Leaderboard Update",
                            url=self.CHATBOT_ARENA_URL,
                            summary="; ".join(summaries[:5]),
                            published=datetime.now(),
                            tags=_DEFAULT_TAGS + ["chatbot-arena", "rankings"],
                        )
                    )
            else:
                # Fallback: store page as single item
                text = soup.get_text(separator=" ", strip=True)[:500]
                if text:
                    items.append(
                        IntelItem(
                            source=self.source_name,
                            title=f"Chatbot Arena: {page_title}",
                            url=self.CHATBOT_ARENA_URL,
                            summary=text,
                            published=datetime.now(),
                            tags=_DEFAULT_TAGS + ["chatbot-arena", "rankings"],
                        )
                    )
        except httpx.RequestError as e:
            logger.warning("Chatbot Arena scrape failed: %s", e)

        return items

    async def _scrape_helm(self) -> list[IntelItem]:
        """Scrape HELM benchmark results from Stanford CRFM."""
        items = []
        try:
            soup = await self.fetch_html(self.HELM_URL)
            if not soup:
                return items

            # Extract benchmark results — HELM pages have structured tables
            tables = soup.select("table")
            if tables:
                for table in tables[:3]:
                    caption = table.find("caption")
                    caption_text = caption.get_text(strip=True) if caption else "HELM Benchmark"

                    rows = table.select("tr")
                    row_texts = []
                    for row in rows[:8]:
                        cells = row.find_all(["td", "th"])
                        text = " | ".join(c.get_text(strip=True) for c in cells)
                        if text:
                            row_texts.append(text)

                    if row_texts:
                        items.append(
                            IntelItem(
                                source=self.source_name,
                                title=f"HELM: {caption_text}",
                                url=self.HELM_URL,
                                summary="\n".join(row_texts[:5]),
                                published=datetime.now(),
                                tags=_DEFAULT_TAGS + ["helm", "stanford"],
                            )
                        )
            else:
                # Fallback: grab page summary
                text = soup.get_text(separator=" ", strip=True)[:500]
                if text:
                    items.append(
                        IntelItem(
                            source=self.source_name,
                            title="HELM Benchmark Results",
                            url=self.HELM_URL,
                            summary=text,
                            published=datetime.now(),
                            tags=_DEFAULT_TAGS + ["helm", "stanford"],
                        )
                    )
        except httpx.RequestError as e:
            logger.warning("HELM scrape failed: %s", e)

        return items
