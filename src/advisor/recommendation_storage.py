"""SQLite persistence for recommendations."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict


@dataclass
class Recommendation:
    """A single recommendation."""
    id: Optional[int] = None
    category: str = ""  # learning, career, entrepreneurial, investment
    title: str = ""
    description: str = ""
    rationale: str = ""
    score: float = 0.0
    created_at: Optional[str] = None
    status: str = "suggested"  # suggested, in_progress, completed, dismissed
    metadata: Optional[dict] = None
    embedding_hash: Optional[str] = None

    def to_dict(self) -> dict:
        d = asdict(self)
        d["metadata"] = json.dumps(d["metadata"]) if d["metadata"] else None
        return d


class RecommendationStorage:
    """SQLite storage for recommendations with deduplication."""

    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self._init_db()

    def _init_db(self):
        """Create recommendations table if not exists."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS recommendations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    rationale TEXT,
                    score REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'suggested',
                    metadata JSON,
                    embedding_hash TEXT
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_rec_category ON recommendations(category)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_rec_status ON recommendations(status)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_rec_hash ON recommendations(embedding_hash)
            """)

    def save(self, rec: Recommendation) -> int:
        """Save recommendation, return id."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("""
                INSERT INTO recommendations
                (category, title, description, rationale, score, status, metadata, embedding_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                rec.category,
                rec.title,
                rec.description,
                rec.rationale,
                rec.score,
                rec.status,
                json.dumps(rec.metadata) if rec.metadata else None,
                rec.embedding_hash,
            ))
            return cur.lastrowid

    def get(self, rec_id: int) -> Optional[Recommendation]:
        """Get recommendation by id."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM recommendations WHERE id = ?", (rec_id,)
            ).fetchone()
            if row:
                return self._row_to_rec(row)
        return None

    def update_status(self, rec_id: int, status: str) -> bool:
        """Update recommendation status."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                "UPDATE recommendations SET status = ? WHERE id = ?",
                (status, rec_id)
            )
            return cur.rowcount > 0

    def list_by_category(
        self,
        category: str,
        status: Optional[str] = None,
        limit: int = 10,
    ) -> list[Recommendation]:
        """List recommendations by category."""
        query = "SELECT * FROM recommendations WHERE category = ?"
        params = [category]
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY score DESC, created_at DESC LIMIT ?"
        params.append(limit)

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(query, params).fetchall()
            return [self._row_to_rec(r) for r in rows]

    def list_recent(
        self,
        days: int = 7,
        status: Optional[str] = None,
        limit: int = 20,
    ) -> list[Recommendation]:
        """List recent recommendations."""
        query = """
            SELECT * FROM recommendations
            WHERE created_at >= datetime('now', ?)
        """
        params = [f"-{days} days"]
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY score DESC, created_at DESC LIMIT ?"
        params.append(limit)

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(query, params).fetchall()
            return [self._row_to_rec(r) for r in rows]

    def hash_exists(self, embedding_hash: str, days: int = 30) -> bool:
        """Check if similar recommendation exists recently."""
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("""
                SELECT 1 FROM recommendations
                WHERE embedding_hash = ?
                AND created_at >= datetime('now', ?)
                LIMIT 1
            """, (embedding_hash, f"-{days} days")).fetchone()
            return row is not None

    def get_top_by_score(
        self,
        min_score: float = 6.0,
        limit: int = 5,
        exclude_status: Optional[list[str]] = None,
    ) -> list[Recommendation]:
        """Get top recommendations by score."""
        query = "SELECT * FROM recommendations WHERE score >= ?"
        params = [min_score]
        if exclude_status:
            placeholders = ",".join("?" * len(exclude_status))
            query += f" AND status NOT IN ({placeholders})"
            params.extend(exclude_status)
        query += " ORDER BY score DESC LIMIT ?"
        params.append(limit)

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(query, params).fetchall()
            return [self._row_to_rec(r) for r in rows]

    def _row_to_rec(self, row: sqlite3.Row) -> Recommendation:
        """Convert DB row to Recommendation."""
        return Recommendation(
            id=row["id"],
            category=row["category"],
            title=row["title"],
            description=row["description"],
            rationale=row["rationale"],
            score=row["score"],
            created_at=row["created_at"],
            status=row["status"],
            metadata=json.loads(row["metadata"]) if row["metadata"] else None,
            embedding_hash=row["embedding_hash"],
        )

    def add_feedback(
        self,
        rec_id: int,
        rating: int,
        comment: Optional[str] = None,
    ) -> bool:
        """Add user feedback to recommendation.

        Args:
            rec_id: Recommendation ID
            rating: 1-5 rating
            comment: Optional feedback comment

        Returns:
            True if updated
        """
        rec = self.get(rec_id)
        if not rec:
            return False

        metadata = rec.metadata or {}
        metadata["user_rating"] = rating
        metadata["feedback_at"] = datetime.now().isoformat()
        if comment:
            metadata["feedback_comment"] = comment

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE recommendations SET metadata = ? WHERE id = ?",
                (json.dumps(metadata), rec_id)
            )
        return True

    def get_feedback_stats(
        self,
        category: Optional[str] = None,
        days: int = 90,
    ) -> dict:
        """Get feedback statistics for scoring adjustment.

        Args:
            category: Filter by category
            days: Lookback period

        Returns:
            Dict with avg_rating, count, by_category
        """
        query = """
            SELECT category, metadata FROM recommendations
            WHERE metadata IS NOT NULL
            AND created_at >= datetime('now', ?)
        """
        params = [f"-{days} days"]
        if category:
            query += " AND category = ?"
            params.append(category)

        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(query, params).fetchall()

        ratings_by_cat = {}
        for row in rows:
            cat = row[0]
            try:
                meta = json.loads(row[1])
                if "user_rating" in meta:
                    if cat not in ratings_by_cat:
                        ratings_by_cat[cat] = []
                    ratings_by_cat[cat].append(meta["user_rating"])
            except (json.JSONDecodeError, TypeError):
                continue

        # Calculate stats
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
