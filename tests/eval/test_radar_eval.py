"""Tests for eval/radar.py — trending radar evaluation."""

import json
import sqlite3
from datetime import datetime, timedelta

import pytest

from eval.radar import (
    RadarEvalReport,
    _check_cross_source,
    _check_personalization,
    _check_temporal_validity,
    _score_coherence,
    run_radar_eval,
)
from intelligence.search import ProfileTerms


@pytest.fixture
def snapshot():
    """A well-formed trending radar snapshot."""
    now = datetime.now()
    return {
        "computed_at": now.isoformat(),
        "days": 7,
        "min_source_families": 2,
        "min_items": 4,
        "total_items_scanned": 100,
        "topics": [
            {
                "topic": "machine learning",
                "score": 0.8,
                "item_count": 10,
                "source_count": 3,
                "sources": ["hackernews", "rss:blog", "reddit"],
                "source_families": ["aggregator", "rss", "reddit"],
                "velocity": 2.1,
                "items": [
                    {
                        "source": "hackernews",
                        "title": "New ML Framework for PyTorch",
                        "url": "https://hn.com/1",
                        "scraped_at": now.isoformat(),
                    },
                    {
                        "source": "rss:blog",
                        "title": "TensorFlow vs PyTorch in 2026",
                        "url": "https://blog.com/1",
                        "scraped_at": now.isoformat(),
                    },
                    {
                        "source": "reddit",
                        "title": "ML Pipeline Best Practices",
                        "url": "https://reddit.com/1",
                        "scraped_at": now.isoformat(),
                    },
                ],
            },
            {
                "topic": "rust lang",
                "score": 0.6,
                "item_count": 5,
                "source_count": 2,
                "sources": ["hackernews", "github_trending"],
                "source_families": ["aggregator", "github"],
                "velocity": 1.5,
                "items": [
                    {
                        "source": "hackernews",
                        "title": "Rust 2.0 Released",
                        "url": "https://hn.com/2",
                        "scraped_at": now.isoformat(),
                    },
                    {
                        "source": "github_trending",
                        "title": "Rust Web Framework",
                        "url": "https://gh.com/1",
                        "scraped_at": now.isoformat(),
                    },
                ],
            },
        ],
    }


@pytest.fixture
def radar_db(tmp_path, snapshot):
    """DB with a trending_radar snapshot."""
    db_path = tmp_path / "intel.db"
    conn = sqlite3.connect(str(db_path))
    conn.execute("""
        CREATE TABLE trending_radar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            computed_at TEXT NOT NULL,
            snapshot_json TEXT NOT NULL
        )
    """)
    conn.execute(
        "INSERT INTO trending_radar (computed_at, snapshot_json) VALUES (?, ?)",
        (snapshot["computed_at"], json.dumps(snapshot)),
    )
    conn.commit()
    conn.close()
    return db_path


class TestCheckCrossSource:
    def test_all_pass(self, snapshot):
        result = _check_cross_source(snapshot, min_families=2)
        assert result["passed"] is True
        assert result["violation_count"] == 0

    def test_violation(self, snapshot):
        # Require 4 families — both topics fail
        result = _check_cross_source(snapshot, min_families=4)
        assert result["passed"] is False
        assert result["violation_count"] == 2

    def test_empty_topics(self):
        result = _check_cross_source({"topics": []})
        assert result["passed"] is True
        assert result["total_topics"] == 0


class TestCheckTemporalValidity:
    def test_fresh_snapshot(self, snapshot):
        result = _check_temporal_validity(snapshot)
        assert result["passed"] is True
        assert result["snapshot_fresh"] is True

    def test_stale_snapshot(self, snapshot):
        snapshot["computed_at"] = (datetime.now() - timedelta(hours=100)).isoformat()
        result = _check_temporal_validity(snapshot, max_age_hours=48)
        assert result["passed"] is False
        assert result["snapshot_fresh"] is False

    def test_invalid_computed_at(self):
        result = _check_temporal_validity({"computed_at": "not-a-date"})
        assert result["passed"] is False


class TestCheckPersonalization:
    def test_with_matching_profile(self, snapshot):
        terms = ProfileTerms(
            skills=["python", "pytorch"],
            interests=["machine learning"],
        )
        result = _check_personalization(snapshot, terms)
        assert result["total_topics"] == 2
        # ML topic should be relevant
        ml_result = next(r for r in result["results"] if r["topic"] == "machine learning")
        assert ml_result["relevant"] is True
        assert len(ml_result["matches"]) > 0

    def test_empty_profile(self, snapshot):
        terms = ProfileTerms()
        result = _check_personalization(snapshot, terms)
        assert result["passed"] is True
        assert result["reason"] == "no profile terms provided"


class TestScoreCoherence:
    def test_with_mock_llm(self, snapshot):
        mock_llm = type(
            "MockLLM",
            (),
            {"generate": lambda self, **kw: '{"coherence": 4, "reasoning": "good grouping"}'},
        )()
        result = _score_coherence(snapshot["topics"][0], mock_llm)
        assert result["coherence"] == 4
        assert "skipped" not in result

    def test_llm_failure(self, snapshot):
        mock_llm = type(
            "MockLLM",
            (),
            {"generate": lambda self, **kw: (_ for _ in ()).throw(RuntimeError("fail"))},
        )()
        result = _score_coherence(snapshot["topics"][0], mock_llm)
        assert result["skipped"] is True


class TestRunRadarEval:
    def test_full_structural(self, radar_db):
        report = run_radar_eval(radar_db)
        assert isinstance(report, RadarEvalReport)
        assert report.summary["passed"] is True
        assert report.summary["topics_evaluated"] == 2

    def test_no_table(self, tmp_path):
        db = tmp_path / "empty.db"
        conn = sqlite3.connect(str(db))
        conn.close()
        report = run_radar_eval(db)
        assert report.summary["passed"] is False

    def test_no_snapshots(self, tmp_path):
        db = tmp_path / "empty.db"
        conn = sqlite3.connect(str(db))
        conn.execute(
            "CREATE TABLE trending_radar (id INTEGER PRIMARY KEY, computed_at TEXT, snapshot_json TEXT)"
        )
        conn.close()
        report = run_radar_eval(db)
        assert report.summary["passed"] is False

    def test_to_dict(self, radar_db):
        report = run_radar_eval(radar_db)
        d = report.to_dict()
        assert "cross_source" in d
        assert "summary" in d

    def test_with_profile(self, radar_db):
        terms = ProfileTerms(skills=["pytorch"], interests=["machine learning"])
        report = run_radar_eval(radar_db, profile_terms=terms)
        assert report.personalization.get("total_topics") == 2
