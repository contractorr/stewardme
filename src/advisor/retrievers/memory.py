"""Memory and recurring thoughts retriever."""

from __future__ import annotations

import structlog

from advisor.async_bridge import run_async
from graceful import graceful_context

logger = structlog.get_logger()


class MemoryRetriever:
    """Retrieves memory facts and recurring thought threads."""

    # Class-level default; facade can override via instance attribute
    _run_async = staticmethod(run_async)

    def __init__(self, fact_store=None, memory_config: dict | None = None, thread_store=None):
        self._fact_store = fact_store
        self._memory_config = memory_config or {}
        self._thread_store = thread_store

    def get_memory_context(self, query: str = "") -> str:
        """Get distilled memory block for system prompt injection."""
        if not self._fact_store:
            return ""

        try:
            max_facts = self._memory_config.get("max_context_facts", 25)
            high_conf = self._memory_config.get("high_confidence_threshold", 0.9)
            thread_boosts = self._get_thread_fact_boosts()

            relevant = []
            if query:
                relevant = self._fact_store.search(query, limit=max_facts)

            all_active = self._fact_store.get_all_active()
            high_conf_facts = [
                f
                for f in all_active
                if self._effective_fact_confidence(f, thread_boosts) >= high_conf
            ]

            seen = set()
            merged = []
            ranked_candidates = sorted(
                high_conf_facts + relevant,
                key=lambda fact: self._effective_fact_confidence(fact, thread_boosts),
                reverse=True,
            )
            for f in ranked_candidates:
                if f.id not in seen:
                    seen.add(f.id)
                    merged.append(f)
                if len(merged) >= max_facts:
                    break

            if not merged:
                return ""

            observations = []
            with graceful_context("graceful.retriever.observations"):
                observations = self._fact_store.get_all_active_observations()

            return self._format_memory_block(
                merged, thread_boosts=thread_boosts, observations=observations
            )
        except Exception as e:
            logger.debug("memory_context_failed", error=str(e))
            return ""

    def _format_memory_block(
        self,
        facts: list,
        thread_boosts: dict[str, float] | None = None,
        observations: list | None = None,
    ) -> str:
        """Format facts into grouped system prompt block."""
        from memory.models import FactCategory

        category_labels = {
            FactCategory.PREFERENCE: "Preferences",
            FactCategory.SKILL: "Skills",
            FactCategory.CONSTRAINT: "Constraints",
            FactCategory.PATTERN: "Patterns",
            FactCategory.CONTEXT: "Current Context",
            FactCategory.GOAL_CONTEXT: "Goal Context",
        }

        lines = ["<user_memory>"]

        if observations:
            lines.append("## Observations")
            for obs in sorted(observations, key=lambda x: x.confidence, reverse=True):
                lines.append(f"* {obs.text}")
            lines.append("")

        grouped: dict[str, list] = {}
        for f in facts:
            if f.category == FactCategory.OBSERVATION:
                continue
            label = category_labels.get(f.category, str(f.category))
            grouped.setdefault(label, []).append(f)

        display_order = [
            "Current Context",
            "Goal Context",
            "Preferences",
            "Skills",
            "Constraints",
            "Patterns",
        ]
        for section in display_order:
            if section not in grouped:
                continue
            lines.append(f"## {section}")
            for f in sorted(
                grouped[section],
                key=lambda x: self._effective_fact_confidence(x, thread_boosts or {}),
                reverse=True,
            ):
                lines.append(f"- {f.text}")
            lines.append("")

        lines.append("</user_memory>")
        return "\n".join(lines)

    def get_recurring_thoughts_context(self, max_threads: int = 3) -> str:
        """Get active recurring thought threads for system prompt injection."""
        if not self._thread_store:
            return ""

        try:
            from datetime import datetime, timedelta

            threads = self._run_async(self._thread_store.get_active_threads(min_entries=2))

            if not threads:
                return ""

            now = datetime.now()
            thirty_days_ago = now - timedelta(days=30)

            scored = []
            for t in threads:
                entries = self._run_async(self._thread_store.get_thread_entries(t.id))
                recent_count = sum(1 for e in entries if e.entry_date >= thirty_days_ago)
                first_date = min(e.entry_date for e in entries) if entries else t.created_at
                last_date = max(e.entry_date for e in entries) if entries else t.updated_at
                weeks_span = max(1, (last_date - first_date).days // 7)
                days_since_last = (now - last_date).days

                scored.append(
                    {
                        "thread": t,
                        "strength": getattr(t, "strength", 0.0),
                        "recent_count": recent_count,
                        "weeks_span": weeks_span,
                        "days_since_last": days_since_last,
                    }
                )

            scored.sort(
                key=lambda x: (x["strength"], x["recent_count"], -x["days_since_last"]),
                reverse=True,
            )
            top = scored[:max_threads]

            if not any(s["strength"] > 0.05 for s in top):
                return ""

            lines = ["<recurring_thoughts>", "The user has persistent recurring thoughts:"]
            for i, s in enumerate(top, 1):
                t = s["thread"]
                ago = s["days_since_last"]
                ago_str = "today" if ago == 0 else f"{ago} days ago"
                lines.append(
                    f'{i}. "{t.label}" — {t.entry_count} entries over '
                    f"{s['weeks_span']} weeks, last {ago_str}"
                )
            lines.append("</recurring_thoughts>")
            return "\n".join(lines)
        except Exception as e:
            logger.debug("recurring_thoughts_failed", error=str(e))
            return ""

    def _get_thread_fact_boosts(self) -> dict[str, float]:
        """Map source entry IDs to a small confidence bonus from strong threads."""
        if not self._thread_store:
            return {}

        boosts: dict[str, float] = {}
        try:
            threads = self._run_async(self._thread_store.get_active_threads(min_entries=2))
            for thread in threads:
                strength = float(getattr(thread, "strength", 0.0))
                if strength <= 0.5:
                    continue
                bonus = min(0.1, max(0.0, (strength - 0.5) * 0.2))
                if bonus <= 0:
                    continue
                entries = self._run_async(self._thread_store.get_thread_entries(thread.id))
                for entry in entries:
                    boosts[entry.entry_id] = max(boosts.get(entry.entry_id, 0.0), bonus)
        except Exception as exc:
            logger.debug("thread_fact_boosts_failed", error=str(exc))
        return boosts

    @staticmethod
    def _effective_fact_confidence(fact, thread_boosts: dict[str, float]) -> float:
        return min(1.0, fact.confidence + thread_boosts.get(fact.source_id, 0.0))
