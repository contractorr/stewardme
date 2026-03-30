# Journal Package

Markdown journal storage, search, threads, exports, and derived analysis live here.

## Related Specs

- `specs/functional/journaling.md`
- `specs/functional/extraction-receipt.md`
- `specs/functional/ai-mind-map.md`
- `specs/functional/recurring-thread-inbox.md`
- `specs/technical/journal.md`
- `specs/technical/extraction-receipt.md`
- `specs/technical/recurring-thread-inbox.md`

## Entry Points

- `storage.py`: markdown CRUD and frontmatter persistence
- `fts.py`, `embeddings.py`, `search.py`: keyword, semantic, and hybrid retrieval
- `threads.py`, `thread_store.py`, `thread_inbox.py`: recurring-thread detection and inbox state
- `mind_map.py`, `trends.py`, `sentiment.py`: derived analysis and visualization support
- `titler.py`, `templates.py`, `extraction_receipts.py`, `export.py`: capture helpers and export flows

## Working Rules

- Journal writes should remain path-safe, markdown-backed, and compatible with existing frontmatter metadata.
- Search flows must degrade gracefully when embeddings are unavailable.
- Thread and research metadata written into journal entries should stay compatible with downstream web and research consumers.

## Validation

- `just test-journal`
- `uv run pytest tests/journal/ tests/web/test_journal_routes.py tests/web/test_journal_mind_map_routes.py tests/web/test_threads_routes.py -q`
