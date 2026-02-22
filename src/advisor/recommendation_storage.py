"""Markdown-based persistence for recommendations."""

import json
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import frontmatter

from shared_types import RecommendationStatus


@dataclass
class Recommendation:
    """A single recommendation."""

    id: Optional[str] = None
    category: str = ""
    title: str = ""
    description: str = ""
    rationale: str = ""
    score: float = 0.0
    created_at: Optional[str] = None
    status: str = RecommendationStatus.SUGGESTED
    metadata: Optional[dict] = None
    embedding_hash: Optional[str] = None


def _slug(text: str) -> str:
    """Generate filename-safe slug."""
    s = re.sub(r"[^\w\s-]", "", text.lower().strip())
    return re.sub(r"[\s_]+", "-", s)[:40]


class RecommendationStorage:
    """Markdown file storage for recommendations."""

    def __init__(self, path: Path, dedup_window_days: int = 30):
        self.dir = Path(path)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.dedup_window_days = dedup_window_days

    def save(self, rec: Recommendation) -> str:
        """Save recommendation as markdown file. Returns id."""
        rec_id = rec.id or uuid.uuid4().hex[:8]
        now = rec.created_at or datetime.now().isoformat()
        date_prefix = now[:10]

        filename = f"{date_prefix}_{rec.category}_{_slug(rec.title)}_{rec_id}.md"
        filepath = self.dir / filename

        post = frontmatter.Post("")
        post.metadata = {
            "id": rec_id,
            "category": str(rec.category),
            "title": str(rec.title),
            "score": float(rec.score),
            "status": str(rec.status),
            "created_at": str(now),
            "embedding_hash": str(rec.embedding_hash) if rec.embedding_hash else None,
        }
        if rec.metadata:
            post.metadata["metadata"] = rec.metadata

        body_parts = []
        if rec.description:
            body_parts.append(rec.description)
        if rec.rationale:
            body_parts.append(f"\n## Rationale\n\n{rec.rationale}")
        if rec.metadata and rec.metadata.get("action_plan"):
            body_parts.append(f"\n## Action Plan\n\n{rec.metadata['action_plan']}")
        post.content = "\n".join(body_parts)

        filepath.write_text(frontmatter.dumps(post))
        return rec_id

    def get(self, rec_id) -> Optional[Recommendation]:
        """Get recommendation by id."""
        rec_id = str(rec_id)
        for f in self.dir.glob("*.md"):
            rec = self._read_file(f)
            if rec and str(rec.id) == rec_id:
                return rec
        return None

    def update_status(self, rec_id, status: str) -> bool:
        """Update recommendation status."""
        rec_id = str(rec_id)
        for f in self.dir.glob("*.md"):
            post = frontmatter.load(f)
            if str(post.metadata.get("id")) == rec_id:
                post.metadata["status"] = status
                f.write_text(frontmatter.dumps(post))
                return True
        return False

    def list_by_category(
        self, category: str, status: Optional[str] = None, limit: int = 10
    ) -> list[Recommendation]:
        """List recommendations by category."""
        recs = [r for r in self._all() if r.category == category]
        if status:
            recs = [r for r in recs if r.status == status]
        recs.sort(key=lambda r: r.score, reverse=True)
        return recs[:limit]

    def list_recent(
        self, days: int = 7, status: Optional[str] = None, limit: int = 20
    ) -> list[Recommendation]:
        """List recent recommendations."""
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        recs = [r for r in self._all() if (r.created_at or "") >= cutoff]
        if status:
            recs = [r for r in recs if r.status == status]
        recs.sort(key=lambda r: r.score, reverse=True)
        return recs[:limit]

    def hash_exists(self, embedding_hash: str, days: int | None = None) -> bool:
        """Check if similar recommendation exists recently."""
        days = days if days is not None else self.dedup_window_days
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        for r in self._all():
            if r.embedding_hash == embedding_hash and (r.created_at or "") >= cutoff:
                return True
        return False

    def get_top_by_score(
        self,
        min_score: float = 6.0,
        limit: int = 5,
        exclude_status: Optional[list[str]] = None,
    ) -> list[Recommendation]:
        """Get top recommendations by score."""
        exclude = set(exclude_status or [])
        recs = [r for r in self._all() if r.score >= min_score and r.status not in exclude]
        recs.sort(key=lambda r: r.score, reverse=True)
        return recs[:limit]

    def add_feedback(self, rec_id, rating: int, comment: Optional[str] = None) -> bool:
        """Add user feedback to recommendation."""
        rec_id = str(rec_id)
        for f in self.dir.glob("*.md"):
            post = frontmatter.load(f)
            if str(post.metadata.get("id")) == rec_id:
                meta = post.metadata.get("metadata") or {}
                meta["user_rating"] = rating
                meta["feedback_at"] = datetime.now().isoformat()
                if comment:
                    meta["feedback_comment"] = comment
                post.metadata["metadata"] = meta
                f.write_text(frontmatter.dumps(post))
                return True
        return False

    def get_feedback_stats(self, category: Optional[str] = None, days: int = 90) -> dict:
        """Get feedback statistics."""
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        ratings_by_cat: dict[str, list] = {}

        for r in self._all():
            if (r.created_at or "") < cutoff:
                continue
            if category and r.category != category:
                continue
            if r.metadata and "user_rating" in r.metadata:
                ratings_by_cat.setdefault(r.category, []).append(r.metadata["user_rating"])

        all_ratings = []
        by_category = {}
        for cat, ratings in ratings_by_cat.items():
            avg = sum(ratings) / len(ratings)
            by_category[cat] = {"avg_rating": avg, "count": len(ratings)}
            all_ratings.extend(ratings)

        return {
            "avg_rating": sum(all_ratings) / len(all_ratings) if all_ratings else 3.0,
            "count": len(all_ratings),
            "by_category": by_category,
        }

    def _all(self) -> list[Recommendation]:
        """Read all recommendations from disk."""
        recs = []
        for f in sorted(self.dir.glob("*.md"), reverse=True):
            rec = self._read_file(f)
            if rec:
                recs.append(rec)
        return recs

    def _read_file(self, path: Path) -> Optional[Recommendation]:
        """Parse a recommendation markdown file."""
        try:
            post = frontmatter.load(path)
            m = post.metadata

            # Extract description and rationale from body
            body = post.content
            description = body.split("\n## Rationale")[0].strip() if body else ""
            rationale = ""
            if "## Rationale" in body:
                rationale = body.split("## Rationale")[-1].split("## Action Plan")[0].strip()

            meta = m.get("metadata")
            if isinstance(meta, str):
                meta = json.loads(meta)

            # Reconstruct action_plan into metadata
            if "## Action Plan" in body:
                action_plan = body.split("## Action Plan")[-1].strip()
                meta = meta or {}
                meta["action_plan"] = action_plan

            return Recommendation(
                id=str(m.get("id", "")),
                category=m.get("category", ""),
                title=m.get("title", ""),
                description=description,
                rationale=rationale,
                score=float(m.get("score", 0)),
                created_at=m.get("created_at"),
                status=m.get("status", "suggested"),
                metadata=meta,
                embedding_hash=m.get("embedding_hash"),
            )
        except Exception:
            return None
