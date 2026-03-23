"""Prometheus metrics endpoint — unauthenticated for scraping."""

from starlette.responses import Response

from observability import metrics


def _scraper_health_lines() -> list[str]:
    """Best-effort scraper health as Prometheus gauges."""
    try:
        from intelligence.health import ScraperHealthTracker
        from web.deps import get_coach_paths

        paths = get_coach_paths()
        tracker = ScraperHealthTracker(paths["intel_db"])
        lines: list[str] = []
        for row in tracker.get_health_summary():
            source = metrics._sanitize_name(row.get("source", "unknown"))
            status = row.get("status", "unknown")
            status_val = {"healthy": 1, "degraded": 0.5, "failing": 0, "backoff": -1}.get(status, 0)
            lines.append(f'coach_scraper_health{{source="{source}"}} {status_val}')
        return lines
    except Exception:
        return []


async def get_metrics():
    text = metrics.prometheus_text()
    health_lines = _scraper_health_lines()
    if health_lines:
        text += "# TYPE coach_scraper_health gauge\n"
        text += "\n".join(health_lines) + "\n"
    return Response(
        content=text,
        media_type="text/plain; version=0.0.4; charset=utf-8",
    )
