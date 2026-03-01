"""SQLite persistence for prediction ledger — lives in intel.db."""

import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

import structlog

from db import wal_connect

logger = structlog.get_logger()


@dataclass
class Prediction:
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    recommendation_id: str = ""
    category: str = ""
    claim_text: str = ""
    confidence: float = 0.5
    confidence_bucket: str = "Medium"
    source_intel_ids: str = "[]"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    evaluation_due: str = ""
    outcome: str = "pending"
    outcome_at: Optional[str] = None
    outcome_notes: Optional[str] = None
    outcome_source: Optional[str] = None


class PredictionStore:
    """SQLite persistence for predictions in existing intel.db."""

    def __init__(self, db_path: Path):
        self.db_path = Path(db_path).expanduser()
        self._init_tables()

    def _init_tables(self):
        with wal_connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id TEXT PRIMARY KEY,
                    recommendation_id TEXT,
                    category TEXT NOT NULL,
                    claim_text TEXT NOT NULL,
                    confidence REAL NOT NULL DEFAULT 0.5,
                    confidence_bucket TEXT NOT NULL DEFAULT 'Medium',
                    source_intel_ids TEXT DEFAULT '[]',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    evaluation_due TIMESTAMP NOT NULL,
                    outcome TEXT NOT NULL DEFAULT 'pending'
                        CHECK(outcome IN ('pending','confirmed','rejected','expired','skipped')),
                    outcome_at TIMESTAMP,
                    outcome_notes TEXT,
                    outcome_source TEXT
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_pred_due ON predictions(evaluation_due)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_pred_outcome ON predictions(outcome)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_pred_category ON predictions(category)")

    def save(self, prediction: Prediction) -> str:
        """Insert prediction, return id."""
        try:
            with wal_connect(self.db_path) as conn:
                conn.execute(
                    """INSERT INTO predictions
                    (id, recommendation_id, category, claim_text, confidence,
                     confidence_bucket, source_intel_ids, created_at, evaluation_due,
                     outcome, outcome_at, outcome_notes, outcome_source)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        prediction.id,
                        prediction.recommendation_id,
                        prediction.category,
                        prediction.claim_text,
                        prediction.confidence,
                        prediction.confidence_bucket,
                        prediction.source_intel_ids,
                        prediction.created_at,
                        prediction.evaluation_due,
                        prediction.outcome,
                        prediction.outcome_at,
                        prediction.outcome_notes,
                        prediction.outcome_source,
                    ),
                )
                return prediction.id
        except sqlite3.Error as e:
            logger.error("prediction_save_error", error=str(e))
            return prediction.id

    def get_pending(self, category: Optional[str] = None, limit: int = 20) -> list[dict]:
        """Get pending predictions, optionally filtered by category."""
        with wal_connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            query = "SELECT * FROM predictions WHERE outcome = 'pending'"
            params: list = []
            if category:
                query += " AND category = ?"
                params.append(category)
            query += " ORDER BY evaluation_due ASC LIMIT ?"
            params.append(limit)
            return [self._row_to_dict(r) for r in conn.execute(query, params).fetchall()]

    def get_review_due(self, limit: int = 3) -> list[dict]:
        """Get predictions past their evaluation_due date."""
        now = datetime.now().isoformat()
        with wal_connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """SELECT * FROM predictions
                WHERE outcome = 'pending' AND evaluation_due <= ?
                ORDER BY evaluation_due ASC LIMIT ?""",
                (now, limit),
            ).fetchall()
            return [self._row_to_dict(r) for r in rows]

    def record_outcome(self, prediction_id: str, outcome: str, notes: Optional[str] = None) -> bool:
        """Record outcome for a prediction."""
        if outcome not in ("confirmed", "rejected", "expired", "skipped"):
            return False
        try:
            with wal_connect(self.db_path) as conn:
                conn.execute(
                    """UPDATE predictions
                    SET outcome = ?, outcome_at = ?, outcome_notes = ?, outcome_source = 'manual_review'
                    WHERE id = ? AND outcome = 'pending'""",
                    (outcome, datetime.now().isoformat(), notes, prediction_id),
                )
                return conn.total_changes > 0
        except sqlite3.Error as e:
            logger.error("prediction_outcome_error", error=str(e))
            return False

    def get_all(
        self,
        category: Optional[str] = None,
        outcome: Optional[str] = None,
        limit: int = 50,
    ) -> list[dict]:
        """Get all predictions with optional filters."""
        with wal_connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            query = "SELECT * FROM predictions WHERE 1=1"
            params: list = []
            if category:
                query += " AND category = ?"
                params.append(category)
            if outcome:
                query += " AND outcome = ?"
                params.append(outcome)
            query += " ORDER BY created_at DESC LIMIT ?"
            params.append(limit)
            return [self._row_to_dict(r) for r in conn.execute(query, params).fetchall()]

    def get_stats(self) -> dict:
        """Aggregate stats: per-category counts, per-bucket accuracy."""
        with wal_connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT * FROM predictions").fetchall()

        total = len(rows)
        by_outcome: dict[str, int] = {}
        by_category: dict[str, dict] = {}
        by_bucket: dict[str, dict] = {}

        for row in rows:
            r = self._row_to_dict(row)
            outcome = r["outcome"]
            cat = r["category"]
            bucket = r["confidence_bucket"]

            by_outcome[outcome] = by_outcome.get(outcome, 0) + 1

            if cat not in by_category:
                by_category[cat] = {"total": 0, "confirmed": 0, "rejected": 0}
            by_category[cat]["total"] += 1
            if outcome in ("confirmed", "rejected"):
                by_category[cat][outcome] += 1

            if bucket not in by_bucket:
                by_bucket[bucket] = {"total": 0, "confirmed": 0, "rejected": 0}
            by_bucket[bucket]["total"] += 1
            if outcome in ("confirmed", "rejected"):
                by_bucket[bucket][outcome] += 1

        # Compute accuracy
        for group in (by_category, by_bucket):
            for v in group.values():
                denom = v["confirmed"] + v["rejected"]
                v["accuracy"] = v["confirmed"] / denom if denom > 0 else None

        review_due = sum(
            1
            for r in rows
            if dict(r)["outcome"] == "pending"
            and dict(r)["evaluation_due"] <= datetime.now().isoformat()
        )

        return {
            "total": total,
            "by_outcome": by_outcome,
            "by_category": by_category,
            "by_confidence_bucket": by_bucket,
            "review_due": review_due,
        }

    @staticmethod
    def _row_to_dict(row) -> dict:
        return dict(row)
