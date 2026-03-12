# Memory Graph Spreading Activation

**Status:** In Progress
**Author:** —
**Date:** 2026-03-12

## Problem

Memory recall is flat — `FactStore.search()` does semantic or keyword retrieval independently. If a user asks about "job interviews", facts about "Python" (their preferred language for technical screens) won't surface unless the query text matches. Related facts connected by shared entities remain invisible.

## Users

All users of the advisor pipeline. Memory recall happens automatically during RAG retrieval.

## Desired Behavior

1. When facts are stored, named entities (proper nouns, acronyms) are extracted and linked in a graph.
2. When searching, seed results expand through shared entity links to pull in topically related facts.
3. Single-hop expansion only — sufficient for 50-500 fact scale.
4. Graph expansion is a post-processing step after existing semantic/keyword search.
5. Results merged via Reciprocal Rank Fusion (RRF) with seeds weighted 0.8, graph neighbors 0.2.

## Acceptance Criteria

- [ ] `extract_entities(text)` returns multi-word proper nouns and acronyms from fact text
- [ ] Adding a fact indexes its entities into `fact_entities` and `fact_entity_links` tables
- [ ] `search()` with `use_graph=True` (default) expands seed results through shared entities
- [ ] `search()` with `use_graph=False` behaves identically to current behavior
- [ ] Superseded/deleted facts are excluded from graph neighbors
- [ ] Entity links are cleaned up on fact delete and update
- [ ] `backfill_entity_links()` indexes existing facts missing entity links
- [ ] Conflict resolver uses `use_graph=False` to avoid false NOOPs
- [ ] No new dependencies — regex-only entity extraction

## Edge Cases

- Facts with no extractable entities: no entity links created, search still works via base retrieval
- All-lowercase text: no entities extracted, graceful empty
- Entity shared by 50+ facts: `graph_limit` caps neighbor expansion
- Existing databases: `CREATE TABLE IF NOT EXISTS` is idempotent, `backfill_entity_links()` for migration
