"""Trending radar evaluation — structural checks + optional LLM coherence."""

from __future__ import annotations

import json
import logging
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path

from eval.response import _parse_judge_response
from intelligence.search import ProfileTerms, score_profile_relevance

logger = logging.getLogger(__name__)

COHERENCE_PROMPT = """You are an evaluation judge. Given a trending topic label and representative items, score how semantically coherent the grouping is.

**Topic label:** {topic}

**Representative items:**
{items}

Score 1-5:
- 5: All items clearly about the same specific topic
- 3: Loosely related, some thematic overlap
- 1: Unrelated items grouped together

Respond in JSON only:
{{"coherence": <1-5>, "reasoning": "<brief explanation>"}}"""


# ---------------------------------------------------------------------------
# Structural checks (no LLM)
# ---------------------------------------------------------------------------


def _check_cross_source(snapshot: dict, min_families: int = 2) -> dict:
    """Each topic should have >= min_families source families."""
    violations = []
    total = 0
    for t in snapshot.get("topics", []):
        total += 1
        families = t.get("source_families", [])
        if len(families) < min_families:
            violations.append({"topic": t["topic"], "families": families, "count": len(families)})
    return {
        "total_topics": total,
        "violations": violations,
        "violation_count": len(violations),
        "passed": len(violations) == 0,
    }


def _check_temporal_validity(snapshot: dict, max_age_hours: int = 48) -> dict:
    """Snapshot should be recent and topics should have items within the window."""
    computed_at = snapshot.get("computed_at", "")
    try:
        ts = datetime.fromisoformat(computed_at)
    except (ValueError, TypeError):
        return {"passed": False, "reason": "invalid computed_at", "computed_at": computed_at}

    age_hours = (datetime.now() - ts).total_seconds() / 3600
    snapshot_fresh = age_hours <= max_age_hours

    days_window = snapshot.get("days", 7)
    stale_topics = []
    for t in snapshot.get("topics", []):
        items = t.get("items", [])
        if not items:
            continue
        # Check if all items are outside the window
        cutoff = (datetime.now() - timedelta(days=days_window)).isoformat()
        all_stale = all((item.get("scraped_at") or "") < cutoff for item in items)
        if all_stale:
            stale_topics.append(t["topic"])

    return {
        "passed": snapshot_fresh and len(stale_topics) == 0,
        "computed_at": computed_at,
        "age_hours": round(age_hours, 1),
        "snapshot_fresh": snapshot_fresh,
        "stale_topics": stale_topics,
    }


def _check_personalization(snapshot: dict, profile_terms: ProfileTerms) -> dict:
    """Topics flagged relevant should contain profile-matching content."""
    if profile_terms.is_empty:
        return {"passed": True, "reason": "no profile terms provided", "results": []}

    results = []
    for t in snapshot.get("topics", []):
        # Score each representative item against profile
        item_scores = []
        for item in t.get("items", []):
            score, matches = score_profile_relevance(item, profile_terms)
            item_scores.append({"score": score, "matches": matches})

        max_score = max((s["score"] for s in item_scores), default=0.0)
        all_matches = []
        for s in item_scores:
            all_matches.extend(s["matches"])

        results.append(
            {
                "topic": t["topic"],
                "max_relevance": round(max_score, 4),
                "matches": sorted(set(all_matches)),
                "relevant": max_score > 0.1,
            }
        )

    relevant_count = sum(1 for r in results if r["relevant"])
    return {
        "passed": True,  # informational, not a hard pass/fail
        "relevant_topics": relevant_count,
        "total_topics": len(results),
        "results": results,
    }


# ---------------------------------------------------------------------------
# LLM coherence check (optional)
# ---------------------------------------------------------------------------


def _score_coherence(topic: dict, llm) -> dict:
    """LLM-as-judge: score semantic coherence of a topic's items."""
    items_text = "\n".join(
        f"- [{item.get('source', '?')}] {item.get('title', '(no title)')}"
        for item in topic.get("items", [])
    )
    prompt = COHERENCE_PROMPT.format(topic=topic["topic"], items=items_text)

    try:
        raw = llm.generate(
            messages=[{"role": "user", "content": prompt}],
            system="You are an evaluation judge. Respond only in valid JSON.",
            max_tokens=500,
        )
    except Exception as e:
        logger.warning("Coherence judge failed for '%s': %s", topic["topic"], e)
        return {"topic": topic["topic"], "skipped": True, "reason": str(e)}

    parsed = _parse_judge_response(raw)
    if parsed is None:
        return {"topic": topic["topic"], "skipped": True, "reason": "parse failure"}

    return {
        "topic": topic["topic"],
        "coherence": parsed.get("coherence", 0),
        "reasoning": parsed.get("reasoning", ""),
    }


# ---------------------------------------------------------------------------
# Report + runner
# ---------------------------------------------------------------------------


@dataclass
class RadarEvalReport:
    cross_source: dict = field(default_factory=dict)
    temporal: dict = field(default_factory=dict)
    personalization: dict = field(default_factory=dict)
    coherence_results: list[dict] = field(default_factory=list)
    summary: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "cross_source": self.cross_source,
            "temporal": self.temporal,
            "personalization": self.personalization,
            "coherence_results": self.coherence_results,
            "summary": self.summary,
        }


def run_radar_eval(
    db_path: str | Path,
    profile_terms: ProfileTerms | None = None,
    judge_llm=None,
) -> RadarEvalReport:
    """Run trending radar quality checks."""
    report = RadarEvalReport()

    # Load latest snapshot
    conn = sqlite3.connect(str(db_path))
    try:
        row = conn.execute(
            "SELECT snapshot_json FROM trending_radar ORDER BY id DESC LIMIT 1"
        ).fetchone()
    except sqlite3.OperationalError:
        report.summary = {"passed": False, "reason": "no trending_radar table"}
        return report
    finally:
        conn.close()

    if not row:
        report.summary = {"passed": False, "reason": "no snapshots found"}
        return report

    try:
        snapshot = json.loads(row[0])
    except (json.JSONDecodeError, TypeError):
        report.summary = {"passed": False, "reason": "invalid snapshot JSON"}
        return report

    # Structural checks
    report.cross_source = _check_cross_source(snapshot)
    report.temporal = _check_temporal_validity(snapshot)

    if profile_terms:
        report.personalization = _check_personalization(snapshot, profile_terms)

    # Optional LLM coherence
    if judge_llm:
        for topic in snapshot.get("topics", []):
            result = _score_coherence(topic, judge_llm)
            report.coherence_results.append(result)

    # Summary
    structural_passed = report.cross_source.get("passed", False) and report.temporal.get(
        "passed", False
    )
    coherence_scores = [r["coherence"] for r in report.coherence_results if not r.get("skipped")]
    avg_coherence = (
        round(sum(coherence_scores) / len(coherence_scores), 2) if coherence_scores else None
    )

    report.summary = {
        "passed": structural_passed,
        "structural_passed": structural_passed,
        "avg_coherence": avg_coherence,
        "topics_evaluated": len(snapshot.get("topics", [])),
    }
    return report
