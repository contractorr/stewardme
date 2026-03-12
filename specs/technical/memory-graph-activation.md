# Memory Graph Spreading Activation — Technical Spec

**Status:** In Progress
**Date:** 2026-03-12

## Schema (v2)

Two new tables in `memory.db`, created via `CREATE TABLE IF NOT EXISTS` in `_init_db`:

```sql
CREATE TABLE IF NOT EXISTS fact_entities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    normalized TEXT NOT NULL UNIQUE
);
CREATE INDEX IF NOT EXISTS idx_fact_entities_normalized ON fact_entities(normalized);

CREATE TABLE IF NOT EXISTS fact_entity_links (
    entity_id INTEGER NOT NULL REFERENCES fact_entities(id),
    fact_id TEXT NOT NULL REFERENCES steward_facts(id),
    PRIMARY KEY (entity_id, fact_id)
);
CREATE INDEX IF NOT EXISTS idx_fact_entity_links_fact ON fact_entity_links(fact_id);
CREATE INDEX IF NOT EXISTS idx_fact_entity_links_entity ON fact_entity_links(entity_id);
```

`SCHEMA_VERSION` bumped from 1 to 2.

## Components

### `src/memory/entity_extractor.py`

```python
def extract_entities(text: str) -> list[str]
```

Regex NER — no LLM, no spaCy:
- Multi-word proper nouns: consecutive Title-Case words (2+ word runs), e.g. "Machine Learning", "Fast API"
- Standalone acronyms: ALLCAPS 2+ chars, e.g. "AWS", "ML"
- Single Title-Case words adjacent to known tech patterns also captured
- Filters: skip common sentence starters ("User", "The", "They"), dedupe via lowercase normalization
- O(n) on ~15-word fact text

### `src/memory/store.py` modifications

**New private methods:**

- `_index_entities(fact: StewardFact)` — extract entities from fact.text, upsert into fact_entities (INSERT OR IGNORE on normalized), link in fact_entity_links
- `_get_entity_neighbors(seed_ids: set[str], exclude_ids: set[str]) -> list[tuple[str, int]]` — SQL join: seed facts → their entities → other active facts sharing those entities, grouped by fact_id, ordered by shared_count DESC

**Modified methods:**

- `add()` — call `_index_entities(fact)` after `_upsert_embedding`
- `update()` — delete old entity links before superseding, new fact indexed via `add()`
- `delete()` — delete entity links for deleted fact
- `reset()` — truncate fact_entities and fact_entity_links
- `search()` — new params: `use_graph: bool = True`, `graph_limit: int = 5`. After base retrieval, if use_graph and seeds exist, call `_get_entity_neighbors`, RRF merge, cap at limit

**New public method:**

- `backfill_entity_links() -> int` — LEFT JOIN to find active facts without links, index each

### `src/memory/resolver.py`

Line 51: `self.store.search(candidate.text, limit=3, use_graph=False)`

## RRF Merge Algorithm

```python
k = 60  # standard smoothing constant
seed_weight, graph_weight = 0.8, 0.2

for i, fact in enumerate(seeds):
    scores[fact.id] += seed_weight / (k + i + 1)

for rank, (fact_id, shared_count) in enumerate(neighbors):
    boost = min(1.0, shared_count * 0.5)
    scores[fact_id] += graph_weight * (1 + boost) / (k + rank + 1)

# Sort by score DESC, return top `limit` facts
```

## Invariants

- Entity extraction is regex-only, O(n), <0.1ms per fact
- Graph expansion is single-hop only
- Superseded facts never appear as graph neighbors
- `use_graph=False` produces identical behavior to pre-change search
- Schema migration is idempotent (`CREATE TABLE IF NOT EXISTS`)
