"""Local drop-folder ingest source.

External pipelines (e.g. a scheduled task reading Gmail through a
connector) drop `.md` or `.json` files into a directory; StewardMe ingests
them as intel items without holding any credentials itself. Content arriving
this way is external, untrusted input — it is wrapped in
``<untrusted_external_content>`` downstream at context assembly like every
other scraped source.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import structlog

from intelligence.scraper import BaseScraper, IntelItem

logger = structlog.get_logger()

SUPPORTED_SUFFIXES = {".md", ".json"}
MAX_CONTENT_CHARS = 50_000
SUMMARY_CHARS = 500


def _default_dropbox_dir() -> Path:
    from storage_paths import get_coach_home

    return get_coach_home() / "intel_dropbox"


def _parse_published(value) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(str(value))
    except ValueError:
        return None


class LocalDropScraper(BaseScraper):
    """Ingests locally dropped .md/.json files as intel items."""

    def __init__(self, storage, dropbox_dir: str | Path | None = None, **kwargs):
        super().__init__(storage, **kwargs)
        self.dropbox_dir = Path(dropbox_dir).expanduser() if dropbox_dir else _default_dropbox_dir()

    @property
    def source_name(self) -> str:
        return "local_drop"

    async def scrape(self) -> list[IntelItem]:
        if not self.dropbox_dir.is_dir():
            return []

        items: list[IntelItem] = []
        for path in sorted(self.dropbox_dir.iterdir()):
            if not path.is_file() or path.suffix.lower() not in SUPPORTED_SUFFIXES:
                continue
            try:
                if path.suffix.lower() == ".md":
                    item = self._parse_markdown(path)
                else:
                    item = self._parse_json(path)
            except Exception as exc:
                # Malformed files are skipped (left in place for the
                # producer to fix), never a crash.
                logger.warning("local_drop_file_skipped", file=path.name, error=str(exc))
                continue

            items.append(item)
            self._move_to_processed(path)

        return items

    # ── Parsing ─────────────────────────────────────────────────────

    def _parse_markdown(self, path: Path) -> IntelItem:
        import frontmatter

        post = frontmatter.loads(path.read_text(encoding="utf-8"))
        content = post.content.strip()
        if not content:
            raise ValueError("empty markdown body")

        title = post.get("title") or self._first_heading(content) or path.stem
        return self._build_item(
            title=str(title),
            url=post.get("url"),
            source=post.get("source"),
            published=post.get("published") or post.get("date"),
            content=content,
        )

    def _parse_json(self, path: Path) -> IntelItem:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("top-level JSON must be an object")
        missing = [key for key in ("title", "source", "content") if not data.get(key)]
        if missing:
            raise ValueError(f"missing required fields: {', '.join(missing)}")
        return self._build_item(
            title=str(data["title"]),
            url=data.get("url"),
            source=data["source"],
            published=data.get("published_at"),
            content=str(data["content"]),
        )

    @staticmethod
    def _first_heading(content: str) -> str | None:
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                return stripped.lstrip("#").strip() or None
        return None

    def _build_item(self, *, title, url, source, published, content) -> IntelItem:
        content = content[:MAX_CONTENT_CHARS]
        tags = ["local_drop"]
        if source:
            tags.append(f"origin:{source}")

        item = IntelItem(
            source=self.source_name,
            title=title,
            url=url or "",
            summary=content[:SUMMARY_CHARS],
            content=content,
            published=_parse_published(published),
            tags=tags,
        )
        if not url:
            # No URL: dedup on content hash alone via an internal unique URL.
            item.content_hash = item.compute_hash()
            item.url = f"localdrop://{item.content_hash}"
        return item

    # ── File lifecycle ──────────────────────────────────────────────

    def _move_to_processed(self, path: Path) -> Path:
        """Move an ingested file to processed/ — never delete."""
        processed_dir = self.dropbox_dir / "processed"
        processed_dir.mkdir(exist_ok=True)
        target = processed_dir / path.name
        counter = 1
        while target.exists():
            target = processed_dir / f"{path.stem}-{counter}{path.suffix}"
            counter += 1
        path.rename(target)
        return target
