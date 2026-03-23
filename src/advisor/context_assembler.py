"""Context assembler — orchestrates per-source retrievers into unified context."""

from __future__ import annotations

import asyncio
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import structlog

from advisor.async_bridge import run_async
from advisor.context_budget import truncate_to_token_budget
from advisor.query_analyzer import QueryAnalysis, RetrievalMode
from advisor.retrievers.intel import IntelRetriever
from advisor.retrievers.journal import JournalRetriever
from advisor.retrievers.memory import MemoryRetriever
from advisor.retrievers.profile import ProfileRetriever
from advisor.retrievers.supplementary import SupplementaryRetriever
from db import wal_connect

if TYPE_CHECKING:
    from advisor.entity_retriever import EntityRetriever
    from advisor.query_analyzer import QueryAnalyzer
    from advisor.query_decomposer import QueryDecomposer
    from services.reranker import CrossEncoderReranker

logger = structlog.get_logger()


@dataclass
class AskContext:
    """Consolidated context for ask() calls."""

    journal: str
    intel: str
    profile: str
    memory: str = ""
    thoughts: str = ""
    documents: str = ""
    entity_context: str = ""
    repo_context: str = ""
    curriculum_context: str = ""


class ContextAssembler:
    """Orchestrates multiple retrievers into unified context for LLM prompts."""

    def __init__(
        self,
        journal: JournalRetriever,
        intel: IntelRetriever,
        profile: ProfileRetriever,
        memory: MemoryRetriever | None = None,
        supplementary: SupplementaryRetriever | None = None,
        *,
        max_context_chars: int = 8000,
        max_context_tokens: int | None = None,
        journal_weight: float = 0.7,
        users_db_path: Path | None = None,
        user_id: str | None = None,
        query_analyzer: QueryAnalyzer | None = None,
        query_decomposer: QueryDecomposer | None = None,
        entity_retriever: EntityRetriever | None = None,
        reranker: CrossEncoderReranker | None = None,
        cache=None,
    ):
        self._journal = journal
        self._intel = intel
        self._profile = profile
        self._memory = memory
        self._supplementary = supplementary
        self.max_context_chars = max_context_chars
        self.max_context_tokens = (
            max_context_tokens if max_context_tokens is not None else max_context_chars // 4
        )
        self.journal_weight = journal_weight
        self._users_db_path = users_db_path
        self._user_id = user_id
        self.query_analyzer = query_analyzer
        self.query_decomposer = query_decomposer
        self.entity_retriever = entity_retriever
        self.reranker = reranker
        self.cache = cache

    # ── High-level assembly ──────────────────────────────────────────

    def build_context_for_ask(
        self,
        query: str,
        rag_config: dict | None = None,
        attachment_ids: list[str] | None = None,
    ) -> AskContext:
        """Build consolidated context for ask() calls."""
        cfg = rag_config or {}

        enhanced = self.get_enhanced_context(query)
        profile_ctx = self._profile.get_profile_context(
            structured=cfg.get("structured_profile", False)
        )

        memory_ctx = ""
        if cfg.get("inject_memory", False) and self._memory:
            memory_ctx = self._memory.get_memory_context(query)

        thoughts_ctx = ""
        if cfg.get("inject_recurring_thoughts", False) and self._memory:
            thoughts_ctx = self._memory.get_recurring_thoughts_context()

        documents_ctx = ""
        if (cfg.get("inject_documents", False) or attachment_ids) and self._supplementary:
            documents_ctx = self._supplementary.get_document_context(
                query, attachment_ids=attachment_ids
            )

        repo_ctx = ""
        if cfg.get("inject_repo_context", True) and self._supplementary:
            repo_ctx = self._supplementary.get_repo_context(query)

        curriculum_ctx = ""
        if cfg.get("inject_curriculum", True) and self._supplementary:
            curriculum_ctx = self._supplementary.get_curriculum_context(query)

        return AskContext(
            journal=enhanced.journal,
            intel=enhanced.intel,
            profile=profile_ctx,
            memory=memory_ctx,
            thoughts=thoughts_ctx,
            documents=documents_ctx,
            entity_context=enhanced.entity_context,
            repo_context=repo_ctx,
            curriculum_context=curriculum_ctx,
        )

    def get_enhanced_context(self, query: str) -> AskContext:
        """Get text and optional entity context for advisor prompts."""
        if not self.query_analyzer:
            journal_ctx, intel_ctx = self.get_combined_context(query)
            return AskContext(journal=journal_ctx, intel=intel_ctx, profile="")

        try:
            analysis: QueryAnalysis = self.query_analyzer.analyze(query)
        except Exception as exc:
            logger.warning("enhanced_context_analysis_failed", error=str(exc))
            journal_ctx, intel_ctx = self.get_combined_context(query)
            return AskContext(journal=journal_ctx, intel=intel_ctx, profile="")

        entity_budget = 0
        entity_context = ""
        if (
            analysis.mode in {RetrievalMode.ENTITY, RetrievalMode.COMBINED}
            and self.entity_retriever
        ):
            entity_budget = int(self.max_context_chars * 0.2)
            try:
                entity_context = self.entity_retriever.retrieve(
                    analysis.matched_entities, query, max_chars=entity_budget
                )
            except Exception as exc:
                logger.warning("entity_context_failed", error=str(exc))
                entity_context = ""
        if entity_context:
            text_budget = self.max_context_chars - len(entity_context)
        else:
            text_budget = self.max_context_chars

        if analysis.temporal_filter:
            journal_ctx, intel_ctx = self._get_temporal_context(query, analysis, text_budget)
        elif (
            analysis.mode in {RetrievalMode.DECOMPOSED, RetrievalMode.COMBINED}
            and self.query_decomposer
        ):
            journal_ctx, intel_ctx = run_async(
                self._decomposed_retrieval(query, total_chars=text_budget)
            )
        else:
            journal_ctx, intel_ctx = self._get_text_context_for_budget(query, text_budget)

        if self.reranker and getattr(self.reranker, "available", False):
            journal_ctx, intel_ctx = self._apply_reranker(query, journal_ctx, intel_ctx)

        return AskContext(
            journal=journal_ctx,
            intel=intel_ctx,
            profile="",
            entity_context=entity_context,
        )

    def get_combined_context(
        self,
        query: str,
        journal_weight: float | None = None,
    ) -> tuple[str, str]:
        """Get both journal and intel context."""
        weight = self._resolve_journal_weight(query, journal_weight)
        total_chars = self.max_context_chars

        if self.cache:
            key = self.cache.make_key("combined", query, weight=weight, total_chars=total_chars)
            cached = self.cache.get(key)
            if cached is not None:
                import json

                parts = json.loads(cached)
                return parts["journal"], parts["intel"]

        journal_ctx, intel_ctx = self._get_text_context_for_budget(query, total_chars, weight)

        if self.cache:
            import json

            self.cache.set(key, json.dumps({"journal": journal_ctx, "intel": intel_ctx}))

        return journal_ctx, intel_ctx

    def get_full_context(
        self,
        query: str,
        include_research: bool = True,
    ) -> tuple[str, str, str]:
        """Get journal, intel, and research context."""
        journal_ctx, intel_ctx = self.get_combined_context(query)
        research_ctx = self._journal.get_research_context(query) if include_research else ""
        return journal_ctx, intel_ctx, research_ctx

    # ── Internals ────────────────────────────────────────────────────

    def _resolve_journal_weight(
        self,
        query: str = "",
        journal_weight: float | None = None,
    ) -> float:
        if journal_weight is not None:
            return journal_weight
        if self._users_db_path and self._user_id:
            return self.compute_dynamic_weight(query=query)
        return self.journal_weight

    def _get_text_context_for_budget(
        self,
        query: str,
        total_chars: int,
        journal_weight: float | None = None,
    ) -> tuple[str, str]:
        weight = self._resolve_journal_weight(query, journal_weight)
        journal_chars = int(total_chars * weight)
        intel_chars = total_chars - journal_chars
        journal_ctx = self._journal.get_journal_context(query, max_chars=journal_chars)
        intel_ctx = self._intel.get_intel_context(query, max_chars=intel_chars)
        return truncate_to_token_budget(journal_ctx, intel_ctx, weight, self.max_context_tokens)

    def _get_temporal_context(
        self,
        query: str,
        analysis: QueryAnalysis,
        total_chars: int,
    ) -> tuple[str, str]:
        """Retrieve context using temporal filtering on both journal and intel."""
        tf = analysis.temporal_filter
        search_query = analysis.cleaned_query or query
        weight = self._resolve_journal_weight(search_query)
        journal_chars = int(total_chars * weight)
        intel_chars = total_chars - journal_chars

        journal_results = self._journal.search.temporal_search(
            search_query, start=tf.start, end=tf.end, n_results=5
        )
        if journal_results:
            parts = []
            total = 0
            for r in journal_results:
                entry_text = (
                    f"\n--- Entry: {r['title']} ({r['type']}) ---\n"
                    f"Date: {r['created']}\n"
                    f"Tags: {', '.join(r['tags']) if r['tags'] else 'none'}\n\n"
                    f"{r['content']}\n"
                )
                if total + len(entry_text) > journal_chars:
                    remaining = journal_chars - total
                    if remaining > 200:
                        parts.append(entry_text[:remaining] + "...[truncated]")
                    break
                parts.append(entry_text)
                total += len(entry_text)
            journal_ctx = "\n".join(parts) if parts else "No relevant journal entries found."
        else:
            journal_ctx = "No relevant journal entries found."

        if self._intel.intel_search:
            intel_results = self._intel.intel_search.temporal_search(
                search_query, start=tf.start, end=tf.end, n_results=5
            )
            if intel_results:
                parts = []
                total = 0
                for item in intel_results:
                    source = item.get("source", "unknown")
                    title = item.get("title", "Untitled")
                    summary = item.get("summary", "")[:200]
                    url = item.get("url", "")
                    entry = f"- [{source}] {title}"
                    if summary:
                        entry += f": {summary}"
                    if url:
                        entry += f" ({url})"
                    if total + len(entry) > intel_chars:
                        break
                    parts.append(entry)
                    total += len(entry)
                intel_ctx = "\n".join(parts) if parts else "No relevant intelligence found."
            else:
                intel_ctx = "No relevant intelligence found."
        else:
            intel_ctx = self._intel.get_intel_context(search_query, max_chars=intel_chars)

        return truncate_to_token_budget(journal_ctx, intel_ctx, weight, self.max_context_tokens)

    async def _decomposed_retrieval(
        self,
        query: str,
        total_chars: int,
    ) -> tuple[str, str]:
        sub_questions = await self.query_decomposer.decompose(query)
        if len(sub_questions) == 1:
            return self._get_text_context_for_budget(sub_questions[0], total_chars)

        sub_budget = total_chars // max(len(sub_questions), 1)
        results = await asyncio.gather(
            *[
                asyncio.to_thread(self._get_text_context_for_budget, sub_query, sub_budget)
                for sub_query in sub_questions
            ],
            return_exceptions=True,
        )
        journal_parts = []
        intel_parts = []
        for result in results:
            if isinstance(result, Exception):
                continue
            journal_parts.append(result[0])
            intel_parts.append(result[1])
        if not journal_parts and not intel_parts:
            return self._get_text_context_for_budget(query, total_chars)

        weight = self._resolve_journal_weight(query)
        journal_budget = int(total_chars * weight)
        intel_budget = total_chars - journal_budget
        return (
            self._merge_context_lines(journal_parts, journal_budget),
            self._merge_context_lines(intel_parts, intel_budget),
        )

    def _merge_context_lines(self, contexts: list[str], max_chars: int) -> str:
        scores: dict[str, int] = {}
        lines_by_key: dict[str, str] = {}
        order: list[str] = []
        for context in contexts:
            for raw_line in context.splitlines():
                line = raw_line.strip()
                if not line:
                    continue
                key = self._line_key(line)
                if key not in lines_by_key:
                    lines_by_key[key] = line
                    order.append(key)
                scores[key] = scores.get(key, 0) + 1
        merged = []
        total = 0
        for key in sorted(order, key=lambda value: (-scores[value], order.index(value))):
            line = lines_by_key[key]
            if total + len(line) + 1 > max_chars:
                break
            merged.append(line)
            total += len(line) + 1
        return "\n".join(merged)

    @staticmethod
    def _line_key(line: str) -> str:
        match = re.search(r"\((https?://[^)]+)\)", line)
        return match.group(1) if match else line.lower()

    def _apply_reranker(self, query: str, journal_ctx: str, intel_ctx: str) -> tuple[str, str]:
        """Rerank context passages using cross-encoder."""
        try:
            intel_lines = [line for line in intel_ctx.split("\n") if line.strip()]
            if len(intel_lines) > 1:
                indices = self.reranker.rerank(query, intel_lines, top_k=len(intel_lines))
                intel_ctx = "\n".join(intel_lines[i] for i in indices)
        except Exception as exc:
            logger.debug("reranker_apply_failed", error=str(exc))
        return journal_ctx, intel_ctx

    # ── Dynamic weighting ────────────────────────────────────────────

    def compute_dynamic_weight(self, user_id: str | None = None, query: str = "") -> float:
        """Compute journal_weight from engagement data."""
        uid = user_id or self._user_id
        if not uid or not self._users_db_path:
            return self.journal_weight

        try:
            with wal_connect(self._users_db_path) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(
                    """
                    SELECT target_type, event_type, COUNT(*) as cnt
                    FROM engagement_events
                    WHERE user_id = ? AND created_at >= datetime('now', '-30 days')
                    GROUP BY target_type, event_type
                    """,
                    (uid,),
                ).fetchall()

            total = sum(r["cnt"] for r in rows)
            if total < 10:
                return self.journal_weight

            positive_events = {"opened", "saved", "acted_on", "feedback_useful"}
            journal_score = sum(
                r["cnt"]
                for r in rows
                if r["target_type"] == "journal" and r["event_type"] in positive_events
            )
            intel_score = sum(
                r["cnt"]
                for r in rows
                if r["target_type"] == "intel" and r["event_type"] in positive_events
            )
            denom = journal_score + intel_score
            if denom == 0:
                return self.journal_weight

            journal_ratio = journal_score / denom
            weight = 0.7 + 0.15 * (journal_ratio - 0.5)
            weight += self._recommendation_weight_adjustment(uid, query)
            return max(0.5, min(0.85, weight))
        except Exception as e:
            logger.debug("dynamic_weight_fallback", error=str(e))
            return self.journal_weight

    def _recommendation_weight_adjustment(self, user_id: str, query: str) -> float:
        """Tilt journal vs intel weight when the query aligns with engaged categories."""
        if not query.strip():
            return 0.0

        try:
            from advisor.recommendations import CATEGORY_QUERIES
        except Exception:
            return 0.0

        query_terms = {token for token in query.lower().split() if token}
        if not query_terms:
            return 0.0

        category_direction = {
            "learning": 0.05,
            "career": 0.04,
            "entrepreneurial": 0.03,
            "projects": 0.03,
            "investment": -0.05,
        }

        try:
            with wal_connect(self._users_db_path) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(
                    """
                    SELECT json_extract(metadata_json, '$.category') as category,
                           event_type,
                           COUNT(*) as cnt
                    FROM engagement_events
                    WHERE user_id = ?
                      AND target_type = 'recommendation'
                      AND event_type IN ('feedback_useful', 'feedback_irrelevant')
                      AND created_at >= datetime('now', '-30 days')
                    GROUP BY category, event_type
                    """,
                    (user_id,),
                ).fetchall()
        except Exception as exc:
            logger.debug("recommendation_weight_adjustment_failed", error=str(exc))
            return 0.0

        counts: dict[str, dict[str, int]] = {}
        for row in rows:
            category = row["category"] or "unknown"
            counts.setdefault(category, {"feedback_useful": 0, "feedback_irrelevant": 0})
            counts[category][row["event_type"]] += row["cnt"]

        adjustment = 0.0
        for category, query_text in CATEGORY_QUERIES.items():
            if category not in counts or category not in category_direction:
                continue
            category_terms = {token for token in query_text.lower().split() if token}
            if not (query_terms & category_terms):
                continue
            useful = counts[category]["feedback_useful"]
            irrelevant = counts[category]["feedback_irrelevant"]
            total = useful + irrelevant
            if total < 4:
                continue
            sentiment = (useful - irrelevant) / total
            adjustment += category_direction[category] * sentiment

        return max(-0.05, min(0.05, adjustment))
