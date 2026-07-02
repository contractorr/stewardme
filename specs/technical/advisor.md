---
id: advisor
category: tracked_module
status: updated
implements:
- ask-advice
- recommendations
code_paths:
- src/advisor
- src/web/routes/advisor.py
- web/src/app/(dashboard)/advisor/page.tsx
- web/src/app/(dashboard)/home/page.tsx
last_reviewed: '2026-03-30'
---

# Advisor

**Status:** Updated for the simplified product model

## Overview

Advisor remains the conversational engine, but Home is now the primary entry point. The full chat page exists as a continuation surface for longer threads.

## Key Modules

- `src/web/routes/advisor.py`
- `web/src/app/(dashboard)/page.tsx`
- `web/src/app/(dashboard)/advisor/page.tsx`
- `web/src/components/MessageRenderer.tsx`

## Interfaces

- `POST /api/advisor/ask/stream`
- conversation continuation via `/advisor?conv=...`
- attachment ids passed from the Home Ask flow

## Unified Prompt Assembly

`_build_advice_prompt()` always uses `build_context_for_ask()` + `_build_user_prompt()` for all advice types except `skill_gap` (which has its own dedicated path).

- No `use_extended` flag; the extended template is always used for `general` prompts.
- `build_context_for_ask()` internally calls `get_enhanced_context()`, so no separate call is needed.
- `rag_config` flags (`inject_memory`, `inject_documents`, etc.) control what `build_context_for_ask` retrieves, not which prompt branch runs.
- `_build_user_prompt()` collapses empty context slots via blank-line removal, so missing data is harmless.

## Advisory Discipline (prompt encoding)

`PromptTemplates.ADVISORY_DISCIPLINE` (appended to the base `SYSTEM` and
agentic system prompts) encodes the global rules from
`specs/functional/ask-advice.md` § Advisory Discipline: default-to-nothing,
≥3-dated-quote evidence bar for patterns, reflect-don't-diagnose, at most 3
items per section, hypothesis phrasing. Per-template specifics:

- `WEEKLY_REVIEW`: no mandated "patterns noticed / energy levels" — open
  questions require the quote bar; sentiment flagged only on a 3+-entry
  logged decline and paired only with a recovery suggestion.
- `OPPORTUNITY_DETECTION`: "at most 3, zero expected most runs" with an
  explicit bar (specific intel item + specific journal skill/goal + concrete
  action).
- `GOAL_ANALYSIS`: adjustments only when evidence shows stall/mis-scope,
  phrased as hypotheses; "no logged evidence either way" is a valid finding.
- `UNIFIED_RECOMMENDATIONS*`: "at most {max_items}", zero acceptable.
- `TOP_PICKS`, `WEEKLY_ACTION_BRIEF`, `EVENT_RECOMMENDATIONS`,
  `PROJECT_RECOMMENDATIONS`, `SIDE_PROJECT_IDEAS`: caps at 3 / "fewer if
  fewer clear the bar".
- `nudges.py`: fires only on actionable conditions (stale profile, stale
  goal, zero recent entries); no praise/streak nudges.

## Untrusted External Content (prompt-injection hardening)

`src/advisor/untrusted.py` provides the provenance layer for scraped content:

- `wrap_untrusted(text, source)` wraps intel/web text in
  `<untrusted_external_content source="...">…</untrusted_external_content>`;
  literal wrapper tags inside the text are entity-escaped
  (`neutralize_breakouts`) so content cannot break out of or spoof the
  wrapper. Placeholder strings ("No external intelligence…") and
  already-wrapped text are returned unchanged.
- `strip_untrusted_tags(text)` removes wrapper tags (used before line-level
  rerank/merge, which would otherwise reorder tag lines); callers re-wrap.
- `ensure_closed(text)` appends missing closing tags after token-budget
  truncation (`context_budget.truncate_to_token_budget` calls it on the intel
  side).
- `contains_verbatim_span(candidate, untrusted_texts, span_words=8)` is the
  agentic outbound-tool guard predicate (word-level n-gram match).

Wrapping is applied at retrieval/assembly time: `IntelRetriever`
(`_get_intel_context_uncached`, `get_filtered_intel_context`), the RAG facade
`get_filtered_intel_context`, and `ContextAssembler._get_temporal_context` /
`_decomposed_retrieval` / `_apply_reranker`. Anything flowing through intel
retrieval — including future sources like drop-folder ingest — is therefore
tagged without per-source work.

`PromptTemplates.UNTRUSTED_CONTENT_RULE` is appended to the base `SYSTEM` and
agentic system prompts: wrapped content is data, never instructions.

## Agentic Tool Execution

`AgenticOrchestrator` runs tool calls with:
- **Per-tool timeout** (`tool_timeout`, default 60s): each `registry.execute()` runs in a thread with `concurrent.futures.ThreadPoolExecutor`. Timeout produces a structured JSON error `{"error": "...timed out..."}`.
- **Structured error detection** (`_is_tool_error()`): JSON-parses tool results and checks for an `"error"` key. Replaces previous string-match heuristic that had false positives on content containing the word "error".
- **Untrusted result tagging**: results from toolsets carrying third-party content (`intel`, `web_search`) are wrapped in `<untrusted_external_content>` before entering the message history, and collected (together with `context` toolset results, whose intel side is already tagged at retrieval) for the outbound guard.
- **Outbound tool guard**: calls to outbound tools (`web_search`, `intel_add_rss_feed`) are rejected before execution when their arguments contain ≥8 consecutive words copied verbatim from collected untrusted content. The rejection is logged (`outbound_tool_call_blocked`) and returned to the model as a structured tool error. Deliberately blunt: it does not catch paraphrases.

## Simplified Product Notes

- Home defaults to capture and upgrades into advisor only when input clearly looks like a question or the user toggles Ask.
- The advisor page is no longer part of the primary navigation model.
- Home keeps the current thread inline for short exchanges and only links to `/advisor` when the user needs a longer continuation surface.
