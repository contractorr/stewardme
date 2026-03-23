"""Engagement events, usage analytics, RSS feeds, and feedback."""

import json as _json

from user_crud import _get_conn

# --- Engagement events ---


def log_engagement(
    user_id: str,
    event_type: str,
    target_type: str,
    target_id: str,
    metadata: dict | None = None,
    db_path=None,
) -> None:
    """Record an engagement event."""
    conn = _get_conn(db_path)
    try:
        conn.execute(
            "INSERT INTO engagement_events (user_id, event_type, target_type, target_id, metadata_json) "
            "VALUES (?, ?, ?, ?, ?)",
            (user_id, event_type, target_type, target_id, _json.dumps(metadata or {})),
        )
        conn.commit()
    finally:
        conn.close()


def get_engagement_stats(user_id: str, days: int = 30, db_path=None) -> dict:
    """Return engagement counts by target_type and event_type for the last N days."""
    conn = _get_conn(db_path)
    try:
        rows = conn.execute(
            """
            SELECT target_type, event_type, COUNT(*) as cnt
            FROM engagement_events
            WHERE user_id = ? AND created_at >= datetime('now', ?)
            GROUP BY target_type, event_type
            """,
            (user_id, f"-{days} days"),
        ).fetchall()
        stats: dict = {"by_target": {}, "by_event": {}, "total": 0}
        for r in rows:
            tt, et, cnt = r["target_type"], r["event_type"], r["cnt"]
            stats["by_target"].setdefault(tt, {})[et] = cnt
            stats["by_event"].setdefault(et, {})[tt] = cnt
            stats["total"] += cnt
        return stats
    finally:
        conn.close()


# --- Usage events ---


def log_event(
    event: str, user_id: str | None = None, metadata: dict | None = None, db_path=None
) -> None:
    """Record a usage analytics event. Fail-silent — never bubbles up."""
    try:
        conn = _get_conn(db_path)
        conn.execute(
            "INSERT INTO usage_events (event, user_id, metadata) VALUES (?, ?, ?)",
            (event, user_id, _json.dumps(metadata) if metadata else None),
        )
        conn.commit()
        conn.close()
    except Exception:
        pass


def get_user_usage_stats(user_id: str, days: int = 30, db_path=None) -> dict:
    """Return per-user LLM cost/usage stats from usage_events metadata."""
    conn = _get_conn(db_path)
    window = f"-{days} days"
    try:
        rows = conn.execute(
            """
            SELECT
                COALESCE(json_extract(metadata, '$.model'), 'unknown') as model,
                COUNT(*) as query_count,
                COALESCE(SUM(json_extract(metadata, '$.input_tokens')), 0) as input_tokens,
                COALESCE(SUM(json_extract(metadata, '$.output_tokens')), 0) as output_tokens,
                COALESCE(SUM(json_extract(metadata, '$.estimated_cost_usd')), 0.0) as estimated_cost_usd
            FROM usage_events
            WHERE event = 'chat_query'
              AND user_id = ?
              AND created_at >= datetime('now', ?)
            GROUP BY model
            """,
            (user_id, window),
        ).fetchall()

        by_model = []
        total_queries = 0
        total_cost = 0.0
        for r in rows:
            by_model.append(
                {
                    "model": r["model"],
                    "query_count": r["query_count"],
                    "input_tokens": int(r["input_tokens"]),
                    "output_tokens": int(r["output_tokens"]),
                    "estimated_cost_usd": round(float(r["estimated_cost_usd"]), 6),
                }
            )
            total_queries += r["query_count"]
            total_cost += float(r["estimated_cost_usd"])

        return {
            "days": days,
            "total_queries": total_queries,
            "total_estimated_cost_usd": round(total_cost, 6),
            "by_model": by_model,
        }
    finally:
        conn.close()


def get_usage_stats(days: int = 30, db_path=None) -> dict:
    """Return aggregate usage stats for the last N days."""
    conn = _get_conn(db_path)
    window = f"-{days} days"
    try:
        row = conn.execute(
            "SELECT COUNT(*) as cnt FROM usage_events WHERE event='chat_query' AND created_at >= datetime('now', ?)",
            (window,),
        ).fetchone()
        chat_queries = row["cnt"] if row else 0

        row = conn.execute(
            "SELECT AVG(json_extract(metadata, '$.latency_ms')) as avg_ms FROM usage_events "
            "WHERE event='chat_query' AND created_at >= datetime('now', ?)",
            (window,),
        ).fetchone()
        avg_latency_ms = round(row["avg_ms"]) if row and row["avg_ms"] else None

        row = conn.execute(
            "SELECT COUNT(DISTINCT user_id) as cnt FROM usage_events "
            "WHERE created_at >= datetime('now', '-7 days') AND user_id IS NOT NULL"
        ).fetchone()
        active_users_7d = row["cnt"] if row else 0

        event_counts = {}
        for ev in ("onboarding_complete", "journal_entry_created", "goal_created"):
            row = conn.execute(
                "SELECT COUNT(*) as cnt FROM usage_events WHERE event=? AND created_at >= datetime('now', ?)",
                (ev, window),
            ).fetchone()
            event_counts[ev] = row["cnt"] if row else 0

        feedback_rows = conn.execute(
            "SELECT json_extract(metadata, '$.category') as cat, "
            "json_extract(metadata, '$.score') as score, COUNT(*) as cnt "
            "FROM usage_events WHERE event='recommendation_feedback' AND created_at >= datetime('now', ?) "
            "GROUP BY cat, score",
            (window,),
        ).fetchall()
        feedback: dict = {}
        for r in feedback_rows:
            cat = r["cat"] or "unknown"
            feedback.setdefault(cat, {"positive": 0, "negative": 0})
            if r["score"] and int(r["score"]) >= 1:
                feedback[cat]["positive"] += r["cnt"]
            else:
                feedback[cat]["negative"] += r["cnt"]

        scraper_rows = conn.execute(
            "SELECT json_extract(metadata, '$.source') as src, "
            "MAX(created_at) as last_run, "
            "AVG(json_extract(metadata, '$.items_added')) as avg_items, "
            "COUNT(*) as runs "
            "FROM usage_events WHERE event='scraper_run' AND created_at >= datetime('now', ?) "
            "GROUP BY src",
            (window,),
        ).fetchall()
        scraper_health = [
            {
                "source": r["src"],
                "last_run": r["last_run"],
                "avg_items": round(r["avg_items"], 1) if r["avg_items"] else 0,
                "runs": r["runs"],
            }
            for r in scraper_rows
        ]

        pv_rows = conn.execute(
            "SELECT json_extract(metadata, '$.path') as path, COUNT(*) as cnt "
            "FROM usage_events WHERE event='page_view' AND created_at >= datetime('now', ?) "
            "GROUP BY path ORDER BY cnt DESC",
            (window,),
        ).fetchall()
        page_views = [{"path": r["path"], "count": r["cnt"]} for r in pv_rows]

        return {
            "days": days,
            "chat_queries": chat_queries,
            "avg_latency_ms": avg_latency_ms,
            "active_users_7d": active_users_7d,
            "event_counts": event_counts,
            "recommendation_feedback": feedback,
            "scraper_health": scraper_health,
            "page_views": page_views,
        }
    finally:
        conn.close()


# --- User RSS feeds ---


def get_user_rss_feeds(user_id: str, db_path=None) -> list[dict]:
    """Get all RSS feeds for a user."""
    conn = _get_conn(db_path)
    try:
        rows = conn.execute(
            "SELECT id, user_id, url, name, added_by, created_at FROM user_rss_feeds "
            "WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def add_user_rss_feed(
    user_id: str, url: str, name: str | None = None, added_by: str = "user", db_path=None
) -> dict:
    """Upsert an RSS feed for a user. Returns the row."""
    conn = _get_conn(db_path)
    try:
        conn.execute(
            "INSERT INTO user_rss_feeds (user_id, url, name, added_by) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(user_id, url) DO UPDATE SET name = COALESCE(excluded.name, name)",
            (user_id, url, name, added_by),
        )
        conn.commit()
        row = conn.execute(
            "SELECT id, user_id, url, name, added_by, created_at FROM user_rss_feeds "
            "WHERE user_id = ? AND url = ?",
            (user_id, url),
        ).fetchone()
        return dict(row)
    finally:
        conn.close()


def remove_user_rss_feed(user_id: str, url: str, db_path=None) -> bool:
    """Remove an RSS feed for a user. Returns True if deleted."""
    conn = _get_conn(db_path)
    try:
        cur = conn.execute(
            "DELETE FROM user_rss_feeds WHERE user_id = ? AND url = ?",
            (user_id, url),
        )
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()


def get_all_user_rss_feeds(db_path=None) -> list[dict]:
    """Get all user RSS feeds across all users (for scheduler merge)."""
    conn = _get_conn(db_path)
    try:
        rows = conn.execute(
            "SELECT id, user_id, url, name, added_by, created_at FROM user_rss_feeds "
            "ORDER BY created_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_feedback_count(user_id: str, days: int = 30, db_path=None) -> int:
    """Count binary and numeric feedback events in the last N days."""
    conn = _get_conn(db_path)
    try:
        engagement_row = conn.execute(
            """
            SELECT COUNT(*) as cnt FROM engagement_events
            WHERE user_id = ?
              AND event_type IN ('feedback_useful', 'feedback_irrelevant')
              AND created_at >= datetime('now', ?)
            """,
            (user_id, f"-{days} days"),
        ).fetchone()
        recommendation_row = conn.execute(
            """
            SELECT COUNT(*) as cnt FROM usage_events
            WHERE user_id = ?
              AND event = 'recommendation_feedback'
              AND created_at >= datetime('now', ?)
            """,
            (user_id, f"-{days} days"),
        ).fetchone()
        engagement_count = engagement_row["cnt"] if engagement_row else 0
        recommendation_count = recommendation_row["cnt"] if recommendation_row else 0
        return engagement_count + recommendation_count
    finally:
        conn.close()
