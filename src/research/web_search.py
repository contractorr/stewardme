"""Web search abstraction for research."""

import logging
import os
import time
from dataclasses import dataclass
from typing import Optional

import httpx

logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """Single search result."""
    title: str
    url: str
    content: str
    score: float = 0.0


class WebSearchClient:
    """Abstract web search client (Tavily implementation)."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        provider: str = "tavily",
        max_results: int = 8,
        max_content_chars: int = 3000,
    ):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        self.provider = provider
        self.max_results = max_results
        self.max_content_chars = max_content_chars
        self.client = httpx.Client(timeout=30.0)

        # Rate limiting
        self._last_request = 0.0
        self._min_interval = 1.0  # seconds between requests

    def search(self, query: str, search_depth: str = "advanced") -> list[SearchResult]:
        """Search for a topic and return results.

        Args:
            query: Search query
            search_depth: "basic" or "advanced"

        Returns:
            List of SearchResult with extracted content
        """
        if not self.api_key:
            logger.warning("No TAVILY_API_KEY configured, returning empty results")
            return []

        self._rate_limit()

        if self.provider == "tavily":
            return self._tavily_search(query, search_depth)
        else:
            logger.error("Unknown search provider: %s", self.provider)
            return []

    def _rate_limit(self):
        """Enforce rate limiting between requests."""
        elapsed = time.time() - self._last_request
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)
        self._last_request = time.time()

    def _tavily_search(self, query: str, search_depth: str) -> list[SearchResult]:
        """Execute Tavily API search."""
        try:
            response = self.client.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": self.api_key,
                    "query": query,
                    "search_depth": search_depth,
                    "include_answer": True,
                    "include_raw_content": False,
                    "max_results": self.max_results,
                },
            )
            response.raise_for_status()
            data = response.json()

            results = []
            for item in data.get("results", []):
                content = item.get("content", "")[:self.max_content_chars]
                results.append(SearchResult(
                    title=item.get("title", "Untitled"),
                    url=item.get("url", ""),
                    content=content,
                    score=item.get("score", 0.0),
                ))

            logger.info("Tavily search for '%s' returned %d results", query, len(results))
            return results

        except httpx.HTTPStatusError as e:
            logger.error("Tavily API error %d: %s", e.response.status_code, e.response.text)
            return []
        except httpx.RequestError as e:
            logger.error("Tavily request failed: %s", e)
            return []
        except Exception as e:
            logger.error("Unexpected error in Tavily search: %s", e)
            return []

    def close(self):
        """Close the HTTP client."""
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class AsyncWebSearchClient:
    """Async version of web search client."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        provider: str = "tavily",
        max_results: int = 8,
        max_content_chars: int = 3000,
    ):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        self.provider = provider
        self.max_results = max_results
        self.max_content_chars = max_content_chars
        self.client = httpx.AsyncClient(timeout=30.0)

    async def search(self, query: str, search_depth: str = "advanced") -> list[SearchResult]:
        """Async search for a topic."""
        if not self.api_key:
            logger.warning("No TAVILY_API_KEY configured")
            return []

        if self.provider == "tavily":
            return await self._tavily_search(query, search_depth)
        return []

    async def _tavily_search(self, query: str, search_depth: str) -> list[SearchResult]:
        """Execute async Tavily API search."""
        try:
            response = await self.client.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": self.api_key,
                    "query": query,
                    "search_depth": search_depth,
                    "include_answer": True,
                    "include_raw_content": False,
                    "max_results": self.max_results,
                },
            )
            response.raise_for_status()
            data = response.json()

            results = []
            for item in data.get("results", []):
                content = item.get("content", "")[:self.max_content_chars]
                results.append(SearchResult(
                    title=item.get("title", "Untitled"),
                    url=item.get("url", ""),
                    content=content,
                    score=item.get("score", 0.0),
                ))

            return results

        except Exception as e:
            logger.error("Async Tavily search failed: %s", e)
            return []

    async def close(self):
        """Close async client."""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
