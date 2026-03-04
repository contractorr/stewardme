"""Intel scraping quality evaluation — pure SQLite analytics, no LLM."""

from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path

from intelligence.trending_radar import _SOURCE_FAMILIES


def _source_family(source: str) -> str:
    if source in _SOURCE_FAMILIES:
        return _SOURCE_FAMILIES[source]
    if source.startswith("rss:"):
        return "rss"
    return source


# ---------------------------------------------------------------------------
# Measurement functions
# ---------------------------------------------------------------------------


def _measure_freshness(conn: sqlite3.Connection, days: int = 7) -> dict:
    """Age distribution of intel_items.published."""
    now = datetime.utcnow()
    cutoff = (now - timedelta(days=days)).isoformat()

    total = conn.execute("SELECT COUNT(*) FROM intel_items").fetchone()[0]
    if total == 0:
        return {"total_items": 0, "pct_fresh": 0.0, "staleness_p50_days": None, "buckets": {}}

    fresh = conn.execute(
        "SELECT COUNT(*) FROM intel_items WHERE scraped_at >= ?", (cutoff,)
    ).fetchone()[0]

    # Staleness distribution
    rows = conn.execute(
        "SELECT julianday('now') - julianday(scraped_at) AS age_days FROM intel_items ORDER BY age_days"
    ).fetchall()
    ages = [r[0] for r in rows if r[0] is not None]
    p50 = ages[len(ages) // 2] if ages else None

    # Bucketed counts
    buckets = {"0-1d": 0, "1-3d": 0, "3-7d": 0, "7-14d": 0, "14-30d": 0, "30d+": 0}
    for age in ages:
        if age <= 1:
            buckets["0-1d"] += 1
        elif age <= 3:
            buckets["1-3d"] += 1
        elif age <= 7:
            buckets["3-7d"] += 1
        elif age <= 14:
            buckets["7-14d"] += 1
        elif age <= 30:
            buckets["14-30d"] += 1
        else:
            buckets["30d+"] += 1

    return {
        "total_items": total,
        "pct_fresh": round(fresh / total, 4) if total else 0.0,
        "staleness_p50_days": round(p50, 2) if p50 is not None else None,
        "buckets": buckets,
    }


def _measure_source_diversity(conn: sqlite3.Connection) -> dict:
    """Items per source + Gini coefficient of distribution."""
    rows = conn.execute(
        "SELECT source, COUNT(*) as cnt FROM intel_items GROUP BY source ORDER BY cnt DESC"
    ).fetchall()
    if not rows:
        return {"unique_sources": 0, "unique_families": 0, "gini": 0.0, "per_source": {}}

    per_source = {r[0]: r[1] for r in rows}
    families = {_source_family(s) for s in per_source}

    # Gini coefficient
    counts = sorted(per_source.values())
    n = len(counts)
    total = sum(counts)
    if total == 0 or n <= 1:
        gini = 0.0
    else:
        cumulative = sum((i + 1) * c for i, c in enumerate(counts))
        gini = (2 * cumulative) / (n * total) - (n + 1) / n

    return {
        "unique_sources": len(per_source),
        "unique_families": len(families),
        "gini": round(gini, 4),
        "per_source": per_source,
    }


def _measure_dedup(conn: sqlite3.Connection) -> dict:
    """Dedup effectiveness from scraper_health + duplicate_of counts."""
    # Per-source dedup from scraper_health
    per_source = {}
    try:
        rows = conn.execute(
            "SELECT source, last_items_scraped, last_items_deduped FROM scraper_health"
        ).fetchall()
        for source, scraped, deduped in rows:
            scraped = scraped or 0
            deduped = deduped or 0
            per_source[source] = {
                "last_scraped": scraped,
                "last_deduped": deduped,
                "dedup_ratio": round(deduped / scraped, 4) if scraped else 0.0,
            }
    except sqlite3.OperationalError:
        pass  # scraper_health table may not exist

    # Global duplicate_of count
    try:
        dup_count = conn.execute(
            "SELECT COUNT(*) FROM intel_items WHERE duplicate_of IS NOT NULL"
        ).fetchone()[0]
        total = conn.execute("SELECT COUNT(*) FROM intel_items").fetchone()[0]
    except sqlite3.OperationalError:
        dup_count = 0
        total = 0

    return {
        "duplicate_of_count": dup_count,
        "total_items": total,
        "overall_dedup_ratio": round(dup_count / total, 4) if total else 0.0,
        "per_source": per_source,
    }


def _measure_reliability(conn: sqlite3.Connection) -> dict:
    """Scraper health summary — reuses ScraperHealthTracker logic inline."""
    now = datetime.utcnow().isoformat()
    try:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM scraper_health ORDER BY source").fetchall()
        conn.row_factory = None
    except sqlite3.OperationalError:
        return {"sources": [], "status_counts": {}, "avg_error_rate": 0.0}

    sources = []
    status_counts: dict[str, int] = {"healthy": 0, "degraded": 0, "failing": 0, "backoff": 0}
    error_rates = []

    for r in rows:
        r = dict(r)
        errs = r.get("consecutive_errors", 0) or 0
        if r.get("backoff_until") and r["backoff_until"] > now:
            status = "backoff"
        elif errs >= 3:
            status = "failing"
        elif errs >= 1:
            status = "degraded"
        else:
            status = "healthy"

        total_runs = r.get("total_runs", 0) or 0
        total_errs = r.get("total_errors", 0) or 0
        err_rate = round(total_errs / total_runs * 100, 1) if total_runs else 0.0

        status_counts[status] += 1
        error_rates.append(err_rate)
        sources.append({"source": r["source"], "status": status, "error_rate": err_rate})

    avg_err = round(sum(error_rates) / len(error_rates), 1) if error_rates else 0.0
    total_sources = len(sources)
    healthy_pct = round(status_counts["healthy"] / total_sources, 4) if total_sources else 0.0

    return {
        "sources": sources,
        "status_counts": status_counts,
        "avg_error_rate": avg_err,
        "healthy_scraper_pct": healthy_pct,
    }


def _measure_content_quality(conn: sqlite3.Connection) -> dict:
    """Average summary length, % with tags, % with valid URLs."""
    total = conn.execute("SELECT COUNT(*) FROM intel_items").fetchone()[0]
    if total == 0:
        return {
            "avg_summary_len": 0,
            "pct_has_tags": 0.0,
            "pct_valid_url": 0.0,
            "total_items": 0,
        }

    avg_len = (
        conn.execute(
            "SELECT AVG(LENGTH(summary)) FROM intel_items WHERE summary IS NOT NULL"
        ).fetchone()[0]
        or 0
    )

    has_tags = conn.execute(
        "SELECT COUNT(*) FROM intel_items WHERE tags IS NOT NULL AND tags != ''"
    ).fetchone()[0]

    # Valid URL = starts with http:// or https://
    urls = conn.execute("SELECT url FROM intel_items").fetchall()
    valid_urls = sum(1 for (u,) in urls if re.match(r"https?://", u or ""))

    return {
        "avg_summary_len": round(avg_len, 1),
        "pct_has_tags": round(has_tags / total, 4),
        "pct_valid_url": round(valid_urls / total, 4),
        "total_items": total,
    }


# ---------------------------------------------------------------------------
# Report + runner
# ---------------------------------------------------------------------------

_DEFAULT_THRESHOLDS = {
    "pct_fresh_min": 0.2,
    "healthy_scraper_pct_min": 0.3,
    "pct_valid_url_min": 0.8,
}


@dataclass
class IntelEvalReport:
    freshness: dict = field(default_factory=dict)
    diversity: dict = field(default_factory=dict)
    dedup: dict = field(default_factory=dict)
    reliability: dict = field(default_factory=dict)
    content_quality: dict = field(default_factory=dict)
    summary: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "freshness": self.freshness,
            "diversity": self.diversity,
            "dedup": self.dedup,
            "reliability": self.reliability,
            "content_quality": self.content_quality,
            "summary": self.summary,
        }


def run_intel_eval(
    db_path: str | Path,
    freshness_days: int = 7,
    thresholds: dict | None = None,
) -> IntelEvalReport:
    """Run all intel quality measurements against an intel.db."""
    t = {**_DEFAULT_THRESHOLDS, **(thresholds or {})}
    report = IntelEvalReport()

    conn = sqlite3.connect(str(db_path))
    try:
        report.freshness = _measure_freshness(conn, days=freshness_days)
        report.diversity = _measure_source_diversity(conn)
        report.dedup = _measure_dedup(conn)
        report.reliability = _measure_reliability(conn)
        report.content_quality = _measure_content_quality(conn)
    finally:
        conn.close()

    # Threshold checks
    failures = []
    pct_fresh = report.freshness.get("pct_fresh", 0)
    if pct_fresh < t["pct_fresh_min"]:
        failures.append(f"pct_fresh={pct_fresh:.2%} < {t['pct_fresh_min']:.0%}")

    healthy_pct = report.reliability.get("healthy_scraper_pct", 0)
    if healthy_pct < t["healthy_scraper_pct_min"]:
        failures.append(
            f"healthy_scraper_pct={healthy_pct:.2%} < {t['healthy_scraper_pct_min']:.0%}"
        )

    pct_valid = report.content_quality.get("pct_valid_url", 0)
    if pct_valid < t["pct_valid_url_min"]:
        failures.append(f"pct_valid_url={pct_valid:.2%} < {t['pct_valid_url_min']:.0%}")

    report.summary = {
        "passed": len(failures) == 0,
        "failures": failures,
        "thresholds": t,
    }
    return report
