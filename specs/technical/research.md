---
id: research
category: tracked_module
status: experimental
implements:
- deep-research
code_paths:
- src/research
- src/web/routes/research.py
- web/src/app/(dashboard)/research/page.tsx
- tests/research
last_reviewed: '2026-03-30'
---

# Research

**Status:** Updated for the simplified product model

## Overview

Research orchestration powers deep dives, dossier refreshes, and durable report generation behind Radar and Research.

## Key Modules

- research runners and summarizers
- `src/web/routes/research.py`
- Research report surfaces and Radar dossier actions

## Interfaces

- research start and refresh endpoints
- report generation and retrieval paths
- dossier-linked research execution

## Outbound Query Hygiene + Audit Log

`src/research/outbound.py`:

- `sanitize_outbound_query(query, max_words=10)` — deliberately simple
  guardrail, not NLP. Drops queries containing feelings vocabulary; strips
  first-person pronouns; for sentence-like input (>10 words or first-person
  markers) reduces to the content-word core (function words removed); caps
  at 10 words. Returns `None` to drop.
- `OutboundLogger.record(query, provider)` — appends
  `{timestamp, query, provider}` JSONL to
  `$COACH_HOME/research/outbound_log.jsonl` (path injectable for tests) and
  returns the entry. IO errors propagate: an unloggable query must not be
  sent.

Both `WebSearchClient.search()` and `AsyncWebSearchClient.search()` run
sanitize → record → issue, in that order, using the resolved provider
(tavily vs duckduckgo fallback). Issued entries also accumulate on
`client.issued_queries`; `DeepResearchAgent` appends them to each report /
dossier update as an `## Outbound Queries` section and in the result dict
(`outbound_queries`). Agents with mocked/injected search clients bypass
hygiene by design — the guarantee attaches to the real clients.

## Simplified Product Notes

- Research is entered from concrete work such as a thread, escalation, or active dossier.
- Archived outputs belong in Research for later reuse.
