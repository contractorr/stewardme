# Memory & Threads

**Status:** Partially Implemented
**Author:** -
**Date:** 2026-03-07

## Problem

The advisor forgets user preferences, patterns, and ongoing themes between sessions. Without persistent memory, users repeat themselves and the advisor gives inconsistent advice.

## Users

All users. Memory value compounds over time and is most useful for regular users with enough history.

## Desired Behavior

### Memory (persistent facts)

1. When a journal entry is created, system automatically extracts structured facts about the user.
2. Facts are categorized as `preference`, `skill`, `constraint`, `pattern`, `context`, or `goal_context`.
3. Each fact has a confidence score.
4. The memory pipeline supports journal entries, recommendation feedback, and goal events as source types.
5. Current product wiring automatically runs memory extraction on journal-entry writes; recommendation-feedback and goal-event ingestion are implemented in the pipeline but are not yet fully wired into all product surfaces.
6. Duplicate or conflicting facts are resolved through similarity checks and, when needed, LLM arbitration.
7. Active facts are injected into advisor prompts as memory context.

### Viewing and managing memory

1. User can list all active facts, optionally filtered by category.
2. User can inspect a single fact.
3. User can delete incorrect facts.
4. User can view memory statistics.

Current interface scope:
- CLI and MCP expose memory search flows.
- Web currently exposes list, get, delete, and stats routes.
- Web does not yet expose a semantic fact-search endpoint.

### Threads (recurring topics)

1. System detects recurring topics across journal entries using similarity-based grouping.
2. A thread is formed when multiple entries discuss a similar topic.
3. Threads are stored with constituent entry references.
4. Active threads are injected into advisor prompts as recurring-thought context.
5. User can view detected threads and their entries.

Current interface scope:
- CLI and MCP expose thread browsing and reindex operations.
- Web currently exposes working list/detail API routes for threads.
- Web does not yet provide a dedicated dashboard page or reindex UX for threads.

### Reindexing

1. User can trigger a reindex of threads if detection seems stale.
2. Reindex re-processes entries against current thresholds.

Current interface scope:
- Reindex is exposed in CLI and MCP.
- Reindex is not yet exposed in web.

## Acceptance Criteria

- [ ] Facts are automatically extracted from new journal entries.
- [ ] Facts are deduplicated before entering active context.
- [ ] Conflicting facts can be resolved through an arbitration step.
- [ ] A bounded set of facts is injected into advisor context.
- [ ] User can list and delete facts across the supported interfaces.
- [ ] Semantic fact search is available in CLI and MCP.
- [ ] Threads are detected from repeated themes across entries.
- [ ] Threads are injected into advisor prompts when enabled.
- [ ] Memory management is available via CLI, web, and MCP, with web currently limited to browse/delete/stats rather than semantic search.
- [ ] Thread browsing is available via CLI, MCP, and basic web API routes.
- [ ] Soft-deleted facts never appear in queries or prompt context.

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| First journal entry | Facts may be extracted but threads are not yet possible |
| Contradictory facts from different entries | Resolver favors the stronger or more recent interpretation |
| Large fact set accumulates | Only a bounded subset is injected into context |
| Very short entry | May extract zero facts without error |
| Thread falls below usefulness after data changes | Reindex can rebuild the thread set |

## Out of Scope

- User manually adding facts
- Cross-user memory or shared facts
- Automatic memory decay over time
- Explicit fact editing beyond deletion
