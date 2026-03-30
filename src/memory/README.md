# Memory Package

Persistent user memory, observation extraction, and consolidation logic live here.

## Related Specs

- `specs/functional/memory-threads.md`
- `specs/technical/memory.md`
- `specs/technical/memory-observation-consolidation.md`
- `specs/technical/memory-graph-activation.md`

## Entry Points

- `store.py`: fact persistence, retrieval, and user-scoped views
- `pipeline.py`: observation extraction and write orchestration
- `extractor.py`, `entity_extractor.py`, `consolidator.py`: extraction and consolidation helpers
- `resolver.py`: conflict resolution
- `models.py`: memory data structures

## Working Rules

- Memory writes must remain user-scoped.
- Soft-delete and visibility semantics need to stay consistent across API, retrieval, and downstream ranking paths.
- `store.py` is a hotspot, so prefer helper extraction and targeted tests before adding more branching.

## Validation

- `just test-memory`
- `uv run pytest tests/memory/ tests/web/test_memory_routes.py -q`
