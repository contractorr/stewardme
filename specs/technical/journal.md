# Journal

## Overview

The journal module provides a full-stack personal journaling system backed by markdown files with YAML frontmatter. It handles CRUD operations with validation and path-traversal protection (`JournalStorage`), vector embeddings via ChromaDB for semantic search (`EmbeddingManager`), SQLite FTS5 full-text search with porter stemming (`JournalFTSIndex`), a unified hybrid search layer using Reciprocal Rank Fusion (`JournalSearch`), lexicon-based sentiment analysis (`analyze_sentiment`), LLM-generated titles (`generate_title`), five built-in entry templates (`templates.py`), recurring-topic detection through cosine-similarity clustering (`ThreadDetector` + `ThreadStore`), KMeans-based trend detection over time windows (`TrendDetector`), and JSON/markdown export (`JournalExporter`).

## Dependencies

**Depends on:** `db` (WAL connect for FTS + ThreadStore), `llm` (generate_title, TrendDetector.summarize_trends), `shared_types` (EntryType, CareerStage), `numpy`/`sklearn` (TrendDetector KMeans), `chromadb` (EmbeddingManager), `python-frontmatter`, `yaml`

**Depended on by:** `advisor` (JournalSearch for RAG retrieval), `memory` (MemoryPipeline reads journal entries), `research` (TopicSelector, DeepResearchAgent stores entries), `intelligence` (GoalIntelMatcher reads goal files), `web` (journal routes), `cli` (journal commands), `coach_mcp` (journal tools)

---

## Components

### JournalStorage

**File:** `src/journal/storage.py`

#### Behavior

Manages markdown files with YAML frontmatter under a single directory. On instantiation the directory (including parents) is created if absent. `create()` validates inputs, generates a filename from date + type + title slug, avoids collisions by appending `_1`, `_2`, etc., writes frontmatter via `python-frontmatter`, and returns the resolved `Path`. `list_entries()` globs `*.md` sorted in reverse filename order (newest first) and silently skips unreadable files. `get_all_content()` returns all entries without limit for use by embedding sync. `update()` always stamps `post["updated"]` with the current ISO timestamp. `delete()` returns `True` if the file existed and was removed, `False` otherwise.

#### Inputs / Outputs

`create(content, entry_type="daily", title=None, tags=None, metadata=None) -> Path`
- `content`: raw body text
- `entry_type`: must be in `ALLOWED_ENTRY_TYPES` (see constants below)
- `title`: defaults to `datetime.now().strftime("%B %d, %Y")` (e.g. `"March 02, 2026"`)
- `tags`: list of strings; only first `MAX_TAGS` kept; each sanitized; empty-after-strip tags dropped
- `metadata`: extra frontmatter keys merged in

`read(filepath) -> frontmatter.Post`

`update(filepath, content=None, metadata=None) -> Path`

`delete(filepath) -> bool`

`list_entries(entry_type=None, tags=None, limit=50) -> list[dict]`
- Each dict: `{path, title, type, created, tags, preview}` where `preview = post.content[:200]`
- Tag filter: entry passes if **any** tag in the filter list is present (OR logic)

`get_all_content() -> list[dict]`
- Each dict: `{"id": str(path), "content": post.content, "metadata": dict(post.metadata)}`
- No limit; no filter

#### Invariants

- `create()` always returns a unique `Path` — collision loop appends `_1`, `_2`, etc. indefinitely.
- Path traversal protection is only applied in `create()`; `read()`, `update()`, `delete()` do NOT call `_validate_path()`.
- `list_entries()` sort order (reverse filename) equals newest-first only because filenames start with `YYYY-MM-DD_`.
- Tags are silently truncated to `MAX_TAGS=20`; no error raised for excess tags.
- `get_all_content()` has no limit — callers must handle large journals.

#### Error Handling

- `create()` raises `ValueError` if `entry_type` not in `ALLOWED_ENTRY_TYPES`
- `create()` raises `ValueError` if `len(content) > 100_000`
- `create()` raises `ValueError("Path escapes journal directory: ...")` via `_validate_path()` if generated path resolves outside `journal_dir`
- `read()` raises `OSError` or `ValueError` on missing/malformed files (no internal catch)
- `update()` raises `OSError` or `ValueError` on missing/malformed files (no internal catch)
- `list_entries()` silently skips files raising `OSError` or `ValueError`
- `get_all_content()` silently skips files raising `OSError` or `ValueError`

#### Configuration

Constants:
```python
MAX_CONTENT_LENGTH = 100_000   # hard cap on entry body (100 KB)
MAX_TAG_LENGTH     = 50        # chars per tag after sanitization
MAX_TAGS           = 20        # max tags per entry; extras silently dropped
```

`EntryType` values (from `shared_types.EntryType`, a `StrEnum`):
```
"daily", "project", "goal", "reflection", "insight",
"note", "quick", "research", "action_brief"
```

Filename helpers:
- `_sanitize_slug(text)`: lowercase, spaces → `-`, strip `[^a-z0-9-]`, truncate to 50 chars
- `_sanitize_tag(tag)`: strip `[^\w\s-]`, `.strip()`, truncate to `MAX_TAG_LENGTH`

Filename pattern: `{YYYY-MM-DD}_{safe_type}_{slug}.md`

Path traversal protection (`_validate_path`): calls `filepath.resolve()`, raises if not relative to `self.journal_dir`. Called only in `create()`; `read()`, `update()`, `delete()` do not call it.

---

### EmbeddingManager

**File:** `src/journal/embeddings.py`

#### Behavior

Wraps a ChromaDB persistent collection for upsert-based vector storage of journal entries. On init, creates the `chroma_dir` (including parents), opens a `PersistentClient` with telemetry disabled, and creates/opens the named collection with cosine space metadata. `add_entry()` sanitizes metadata to ChromaDB-acceptable types before calling `collection.upsert()`. `sync_from_storage()` adds all provided entries and removes any IDs no longer present. `remove_entry()` swallows all exceptions. `delete_collection()` deletes and immediately re-creates the collection with the same name and metadata (effectively a reset).

#### Inputs / Outputs

`__init__(chroma_dir, collection_name="journal")`
- Collection metadata: `{"hnsw:space": "cosine", "embedding_model": "all-MiniLM-L6-v2"}`

`add_entry(entry_id, content, metadata=None) -> None`
- Calls `collection.upsert(ids=[entry_id], documents=[content], metadatas=...)`

`remove_entry(entry_id) -> None`

`query(query_text, n_results=5, where=None) -> list[dict]`
- Includes `["documents", "metadatas", "distances"]`
- Returns: `[{"id", "content", "metadata", "distance"}, ...]`
- Returns `[]` on empty collection

`sync_from_storage(entries) -> tuple[int, int]`
- Returns `(added, removed)` where `added` = entries not previously in the collection

`count() -> int`

`health_check() -> dict`
- Returns `{"status": "ok"|"error", "count": int, "collection_name": str, "model": str}` (plus `"error": str` on failure)

`delete_collection() -> None`

#### Invariants

- `add_entry()` is idempotent — calling it with the same `entry_id` upserts in place.
- `sync_from_storage()`: `added` count reflects only IDs not previously in the collection; every provided entry is upserted regardless.
- `delete_collection()` leaves the collection in a valid (empty) state, not absent.
- `remove_entry()` never raises — safe to call on non-existent IDs.
- ChromaDB collection is always initialized on construction; health check can determine if it's functional.

#### Error Handling

- `remove_entry()`: catches all exceptions, logs `WARNING embedding_remove_failed`, never re-raises
- `sync_from_storage()`: on failure to retrieve existing IDs, logs `WARNING chroma_get_existing_failed`, continues with empty `existing` set (all entries counted as "added")
- `health_check()`: catches all exceptions, returns `{"status": "error", ...}`

#### Configuration

```python
DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"
```

Metadata sanitization rules for ChromaDB (only `str | int | float | bool | None` accepted):
- `list` → join with `","` (empty list → `""`)
- other non-primitive types → `str(v)`
- if `clean_meta` is empty after sanitization → pass `metadatas=None` to upsert

---

### JournalSearch

**File:** `src/journal/search.py`

#### Behavior

Unified search interface composing `JournalStorage`, `EmbeddingManager`, and optionally `JournalFTSIndex`. Provides semantic search (ChromaDB cosine similarity), keyword search (FTS5 BM25 or in-memory fallback), and hybrid search (Reciprocal Rank Fusion). `get_context_for_query()` formats results as an LLM-ready context string with per-entry truncation.

`semantic_search()` falls back to `keyword_search()` when `self.embeddings is None`. It enriches ChromaDB results with full frontmatter by re-reading each file, silently skipping missing or unreadable paths.

`keyword_search()` routes to `_keyword_search_fts` when FTS index is present, else `_keyword_search_fallback`. The fallback scans `list_entries(limit=limit*2)` in memory; counts raw term occurrences in lowercased content (not unique).

#### Inputs / Outputs

`__init__(storage, embeddings, fts_index=None)`

`semantic_search(query, n_results=5, entry_type=None) -> list[dict]`
- `relevance = 1 - distance` (cosine distance to similarity conversion)

`keyword_search(keyword, entry_type=None, limit=20) -> list[dict]`
- FTS relevance: `-row["rank"]` (negates BM25 negative value)
- Fallback relevance: raw term occurrence count

`hybrid_search(query, n_results=5, semantic_weight=0.7, entry_type=None) -> list[dict]`
- Each sub-search retrieves `n_results * 2` candidates before fusion
- RRF formula: `score[path] += (1.0 / (rank_i + 1)) * weight`
  - semantic weight = `semantic_weight` (default `0.7`)
  - keyword weight = `1 - semantic_weight` (default `0.3`)
- Final result: top `n_results` by fused score

`get_context_for_query(query, max_entries=5, max_chars=8000) -> str`
- Returns `"No relevant journal entries found."` on empty results
- Entry format:
  ```
  --- Entry: {title} ({type}) ---
  Date: {created}
  Tags: {tag1, tag2} or "none"

  {content}
  ```
- Truncation: if next entry would exceed `max_chars` and `remaining > 200`, appends truncated slice with `"...[truncated]"`; otherwise breaks without appending

`sync_embeddings() -> tuple[int, int]`
- Syncs FTS index (if present) then embedding store from all storage entries

#### Invariants

- `hybrid_search()` always fetches `n_results * 2` candidates from each sub-search before fusion; final count may be < `n_results` if entries were skipped.
- `semantic_search()` falls back to `keyword_search()` when `self.embeddings is None` — not an error.
- `get_context_for_query()` always returns a non-empty string (returns `"No relevant journal entries found."` when results are empty).
- RRF rank starts at 1 (not 0) — formula is `1 / (rank + 1)`, so rank 0 → weight 1.0.

#### Error Handling

- `semantic_search()`: silently skips entries where path no longer exists or raises `OSError`/`ValueError`
- `_keyword_search_fts()` and `_keyword_search_fallback()`: silently skip entries raising `OSError`/`ValueError`

#### Configuration

Default weights: `semantic_weight=0.7`, keyword weight=`0.3`. Both sub-searches use `n_results * 2` candidates.

---

### JournalFTSIndex

**File:** `src/journal/fts.py`

#### Behavior

SQLite FTS5 full-text index stored at `<journal_dir>/../journal.db` (sibling of the `journal/` directory, not inside it). Uses porter stemming and unicode61 normalization. FTS5 has no native UPDATE, so `upsert()` always DELETEs then INSERTs. `sync_from_storage()` is incremental: re-indexes only entries whose `st_mtime` changed; skips entries whose file path no longer exists on disk; deletes stale rows for paths absent from the storage list. `search()` converts user input to a FTS5 MATCH expression via `_to_fts5_query()` and returns BM25-ranked results.

#### Inputs / Outputs

`__init__(journal_dir)`
- DB path: `<journal_dir>/../journal.db`

`upsert(path, title, entry_type, content, tags, mtime) -> None`

`delete(path) -> None`

`search(query, limit=20, entry_type=None) -> list[dict]`
- Returns: `[{path, title, entry_type, tags, rank}, ...]`
- `rank` is the raw BM25 value (negative in SQLite FTS5)
- Returns `[]` on empty/symbol-only query or `sqlite3.OperationalError`

`sync_from_storage(entries) -> tuple[int, int]`
- Returns `(added_or_updated, deleted)`

#### Invariants

- DB path is `<journal_dir>/../journal.db` — a sibling of the journal directory, never inside it.
- `upsert()` always DELETEs then INSERTs (FTS5 has no native UPDATE) — row count always changes.
- `sync_from_storage()` only re-indexes entries whose `st_mtime` changed; no-op for unchanged files.
- Empty or symbol-only query returns `[]` without touching the DB (`_to_fts5_query` returns `""`).
- `rank` values in results are negative BM25 scores — higher absolute value = better match.

#### Error Handling

- `search()`: on `sqlite3.OperationalError`, logs `WARNING journal_fts_search_error`, returns `[]`
- `_to_fts5_query()`: returns `""` for blank or symbol-only input, triggering early `[]` return in `search()`

#### Configuration

Schema:
```sql
CREATE VIRTUAL TABLE journal_fts USING fts5(
    path UNINDEXED,
    title,
    entry_type UNINDEXED,
    content,
    tags,
    tokenize='porter unicode61'
)

CREATE TABLE journal_fts_meta (
    path TEXT PRIMARY KEY,
    mtime REAL NOT NULL
)
```

Query transformation (`_to_fts5_query`):
- Extracts `[\w]+` tokens, lowercases, appends `*` for prefix matching
- Tokens implicitly ANDed (FTS5 default)

All connections use WAL mode via `db.wal_connect`. `row_factory = sqlite3.Row` set inline on the connection after `wal_connect`.

---

### analyze_sentiment

**File:** `src/journal/sentiment.py`

#### Behavior

Lexicon-based sentiment analysis with no external dependencies. Tokenizes text into a set of unique lowercase words using `re.findall(r"\b[a-z]+\b", text.lower())` — each word counted at most once regardless of frequency. Computes positive and negative hit counts against two fixed word sets. Returns a score, label, and raw counts.

#### Inputs / Outputs

`analyze_sentiment(text: str) -> dict`

Returns:
```python
{
    "score": float,           # rounded to 2 decimal places, range -1.0 to 1.0
    "label": str,             # "positive" | "negative" | "mixed" | "neutral"
    "positive_count": int,
    "negative_count": int,
}
```

Score formula:
```python
words = set(re.findall(r"\b[a-z]+\b", text.lower()))
pos   = len(words & _POSITIVE)
neg   = len(words & _NEGATIVE)
total = pos + neg
score = (pos - neg) / total   # or 0.0 if total == 0
```

Label thresholds:
```
total == 0            →  "neutral"
score >  0.2          →  "positive"
score < -0.2          →  "negative"
-0.2 <= score <= 0.2  →  "mixed"
```

#### Invariants

- Each word counted at most once regardless of frequency (set-based intersection).
- Score is always in `[-1.0, 1.0]` and rounded to 2 decimal places.
- `total == 0` (no recognized words) always produces `"neutral"` with `score=0.0`.
- Not thread-safe for concurrent modification of the lexicon sets (but lexicons are module-level constants — effectively immutable).

#### Error Handling

No exceptions raised. Returns `{"score": 0.0, "label": "neutral", ...}` when text contains no recognized words.

#### Configuration

Positive lexicon (32 words):
`great, good, excellent, happy, excited, proud, accomplished, progress, success, win, awesome, fantastic, love, enjoy, productive, motivated, inspired, grateful, thankful, confident, breakthrough, solved, achieved, improved, optimistic, energized, satisfied, fun, rewarding, thriving, focused, clear`

Negative lexicon (30 words):
`bad, terrible, frustrated, stuck, blocked, stressed, anxious, overwhelmed, exhausted, burned, burnout, failed, struggling, confused, worried, disappointed, tired, difficult, hard, impossible, lost, behind, procrastinating, unmotivated, drained, angry, annoyed, boring, painful, hopeless, doubt`

---

### Templates

**File:** `src/journal/templates.py`

#### Behavior

Provides five built-in structured templates and a lookup/list interface. Custom templates override builtins by key when passed to `get_template()` or `list_templates()`. `get_template()` returns `None` (not an exception) for unknown names.

#### Inputs / Outputs

`get_template(name, custom_templates=None) -> dict | None`
- Merge strategy: `{**BUILTIN_TEMPLATES, **custom_templates}`
- Returns `None` for unknown name

`list_templates(custom_templates=None) -> dict`
- Same merge strategy; returns full dict of all templates

#### Invariants

- Custom templates override builtins by key — they cannot be appended; they replace.
- `get_template()` returns `None` (not raises) on unknown name — callers must null-check.
- `list_templates()` always returns at least the 5 builtins.

#### Error Handling

`get_template()` returns `None` on unknown name; never raises.

#### Configuration

`BUILTIN_TEMPLATES` — 5 entries:

| Key | `name` | `type` | Sections |
|---|---|---|---|
| `"daily"` | Daily Reflection | `"daily"` | What went well today?, What challenged me?, Key learnings, Tomorrow's priorities |
| `"weekly"` | Weekly Review | `"reflection"` | Accomplishments this week, What didn't go as planned?, Patterns I noticed, Goals progress, Focus for next week |
| `"goal"` | Goal Setting | `"goal"` | Goal, Why this matters, Success criteria, First steps, Potential obstacles |
| `"project"` | Project Update | `"project"` | Status, Progress since last update, Blockers, Next milestones, Questions/decisions needed |
| `"learning"` | Learning Log | `"insight"` | What I learned, Key concepts, How this connects to my work, Next: apply this by |

---

### ThreadDetector

**File:** `src/journal/threads.py`

#### Behavior

Detects recurring topics by clustering journal entries via ChromaDB cosine similarity. On `detect()`, queries the collection for the top `candidate_count + 1` neighbors by embedding vector, excludes self, and filters to entries with `similarity >= similarity_threshold` (where `similarity = 1.0 - cosine_distance`). Then checks thread assignments of similar entries via `ThreadStore` and follows the decision tree below. `reindex_all()` wipes all threads via `ThreadStore.clear_all()`, then replays all entries chronologically (entries without a parseable `created` date sort to `datetime.min`).

Decision tree in `detect()`:
1. No similar entries above threshold → `match_type="unthreaded"`
2. Similar entries exist and any belong to an existing thread → join thread with highest average similarity across its matched entries → `match_type="joined_existing"`
3. Similar entries exist, none are threaded, and `len(unthreaded_similar) >= min_entries_for_thread - 1` (i.e. at least 1 other similar unthreaded entry) → create new thread, add all unthreaded similar entries plus current entry (current assigned `similarity=1.0`) → `match_type="created_new"`
4. Otherwise → `match_type="unthreaded"`

`_make_label()` fetches the entry document from ChromaDB, strips markdown `#` headers, takes the first line with `len > 10` truncated to 80 chars, falls back to `text[:80]`, or returns `"Recurring topic"` on any error. No LLM call.

#### Inputs / Outputs

`__init__(journal_embeddings, thread_store, config=None)`

`detect(entry_id, entry_embedding, entry_date) -> ThreadMatch` (async)

`reindex_all() -> dict` (async)
- Returns `{"threads_created": int, "entries_processed": int, "entries_threaded": int}`

`ThreadMatch` dataclass:
```python
@dataclass
class ThreadMatch:
    entry_id: str
    thread_id: str | None       # None when unthreaded
    match_type: str             # "joined_existing" | "created_new" | "unthreaded"
    similar_entries: list[str]  # IDs of similar entries found
    is_new_thread: bool         # True only for "created_new"
```

#### Invariants

- `detect()` requires the ChromaDB collection to have > 1 entry; single-entry collections always return `"unthreaded"`.
- Thread label is generated from content only (no LLM call) — `_make_label()` never makes an API call.
- `reindex_all()` is destructive: wipes all existing threads before rebuilding.
- Entries without a parseable `created` date sort to `datetime.min` in `reindex_all()`.
- `match_type="joined_existing"` uses the thread with highest average similarity, not highest single similarity.

#### Caveats

- `reindex_all()` calls `ThreadStore.clear_all()` — any manually-assigned thread labels are lost.
- Thread labels are heuristic (first meaningful line of content, ≤ 80 chars) and may be cryptic.

#### Error Handling

- `_query_similar()`: catches all exceptions, logs `WARNING thread_query_failed`, returns `[]`
- `_make_label()`: catches all exceptions, returns `"Recurring topic"`
- `reindex_all()`: returns zero-counts dict if collection is empty

#### Configuration

Config dict keys (with defaults):
```python
similarity_threshold   = 0.78   # cosine similarity cutoff
candidate_count        = 10     # top-N ChromaDB results queried per call
min_entries_for_thread = 2      # minimum entries to form a new thread
```

Missing config keys fall back to the defaults above. Collection must have more than 1 entry for a query to proceed.

---

### ThreadStore

**File:** `src/journal/thread_store.py`

#### Behavior

Async SQLite persistence for thread groupings, using WAL mode on every connection. `create_thread()` generates a 16-hex-character ID via `uuid4().hex[:16]` and always sets `status = "active"`. `add_entry()` uses `INSERT OR REPLACE` and also updates `journal_threads.updated_at`. `get_active_threads()` filters to `status='active'`, `HAVING COUNT >= min_entries`, ordered by `updated_at DESC`. `get_thread_entries()` orders by `entry_date ASC`. `clear_all()` deletes all rows from both tables; used exclusively by `reindex_all`.

#### Inputs / Outputs

`create_thread(label) -> Thread` (async)

`add_entry(thread_id, entry_id, similarity, entry_date) -> None` (async)

`get_thread(thread_id) -> Thread | None` (async)

`get_threads_for_entry(entry_id) -> list[Thread]` (async)

`get_active_threads(min_entries=2) -> list[Thread]` (async)

`get_thread_entries(thread_id) -> list[ThreadEntry]` (async)

`update_label(thread_id, label) -> None` (async)

`clear_all() -> None` (async)

`Thread` dataclass:
```python
@dataclass
class Thread:
    id: str             # uuid4().hex[:16]
    label: str
    created_at: datetime
    updated_at: datetime
    entry_count: int = 0
    status: str = "active"
```

`ThreadEntry` dataclass:
```python
@dataclass
class ThreadEntry:
    entry_id: str
    thread_id: str
    added_at: datetime
    similarity: float
    entry_date: datetime
```

#### Invariants

- All IDs are `uuid4().hex[:16]` (16 hex chars) — not sequential integers.
- `create_thread()` always sets `status = "active"`.
- `add_entry()` uses `INSERT OR REPLACE` — re-adding the same `(thread_id, entry_id)` pair updates `similarity` and `entry_date` in place.
- `get_active_threads()` filters by `status='active'` AND `COUNT >= min_entries` — threads with fewer entries are hidden, not deleted.
- `clear_all()` is the only bulk-delete path; all other operations are targeted.

#### Error Handling

No internal exception swallowing; SQLite errors propagate to callers.

#### Configuration

Schema:
```sql
CREATE TABLE journal_threads (
    id TEXT PRIMARY KEY,
    label TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'active'
)

CREATE TABLE thread_entries (
    thread_id TEXT NOT NULL,
    entry_id  TEXT NOT NULL,
    added_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    similarity REAL NOT NULL,
    entry_date TIMESTAMP NOT NULL,
    PRIMARY KEY (thread_id, entry_id),
    FOREIGN KEY (thread_id) REFERENCES journal_threads(id)
)

CREATE INDEX idx_thread_entries_entry ON thread_entries(entry_id)
CREATE INDEX idx_threads_status ON journal_threads(status)
```

All connections via `db.wal_connect`.

---

### generate_title

**File:** `src/journal/titler.py`

#### Behavior

Generates a short title for a journal entry using an LLM. Returns `None` immediately if no provider is passed, if content is fewer than 20 stripped characters, or if the LLM call raises any exception. Truncates content to the first 1,000 characters before sending. Post-processes the LLM response by stripping whitespace, double quotes, single quotes, and trailing periods. Accepts the result only if non-empty and fewer than 100 characters.

#### Inputs / Outputs

`generate_title(content: str, llm_provider=None) -> str | None`

Prompts:
```python
_SYSTEM = "You generate concise journal entry titles. Output ONLY the title, nothing else."
_PROMPT = "Generate a brief title (3-8 words) for this journal entry. No quotes, no punctuation at the end.\n\n{content}"
```

LLM call parameters: `max_tokens=30`

Guards:
- Returns `None` if `llm_provider is None`
- Returns `None` if `len(content.strip()) < 20`
- Truncates content to `content[:1000]` before sending
- Returns `None` if `not title` or `len(title) >= 100`

#### Invariants

- Returns `None` in four cases: `llm_provider is None`, `len(content.strip()) < 20`, LLM exception, or result ≥ 100 chars.
- Content is always truncated to first 1000 chars before sending — LLM never sees the full entry.
- Post-processing strips quotes and trailing periods — returned title is clean for use as filename slug.
- Not called during `JournalStorage.create()` directly; callers (journal MCP tool) invoke it separately.

#### Error Handling

Any exception from the LLM call: logs `DEBUG title_generation_failed`, returns `None`. Never re-raises.

#### Configuration

No external config; all constants are module-level literals.

---

### TrendDetector

**File:** `src/journal/trends.py`

#### Behavior

Detects emerging and declining topics by clustering journal entry embeddings with KMeans over time windows. `detect_trends()` fetches up to 500 entries via `list_entries(limit=500)`, retrieves their embeddings from ChromaDB, buckets them by ISO week or calendar month, clusters with KMeans, and computes per-cluster growth rates. Clusters with fewer than 2 windows of data are skipped. Results are sorted by `abs(growth_rate)` descending. `summarize_trends()` falls back to plain-text format if `llm_caller` is `None` or raises.

`_label_cluster()` labels a cluster using the most common tag among representative entries; falls back to the first title (truncated to 50 chars); falls back to `"Topic cluster"`.

#### Inputs / Outputs

`__init__(journal_search, llm_caller=None)`
- `llm_caller`: optional `callable(system, prompt, max_tokens) -> str`

`detect_trends(days=90, window="weekly", n_clusters=8) -> list[dict]`
- `window`: `"weekly"` (ISO week key `"YYYY-Www"`) or `"monthly"` (key `"YYYY-MM"`)
- Each result dict: `{topic, cluster_id, direction, growth_rate, counts, windows, total_entries, representative_titles}`
- Returns `[]` if `len(entries) < n_clusters` or `len(buckets) < 2`
- `n_clusters` capped at `len(entries)`

`get_emerging_topics(threshold=0.2, **kwargs) -> list[dict]`
- Filters `detect_trends` output to `growth_rate > threshold`

`get_declining_topics(threshold=0.2, **kwargs) -> list[dict]`
- Filters `detect_trends` output to `growth_rate < -threshold`

`summarize_trends(days=90) -> str`
- LLM call: `max_tokens=1000`
- Falls back to `_format_trends_text()` if `llm_caller` is `None` or raises

#### Invariants

- Returns `[]` when `len(entries) < n_clusters` or `len(buckets) < 2` — minimum data requirements.
- `n_clusters` is capped at `len(entries)` to prevent KMeans from failing on small datasets.
- Clusters with fewer than 2 time windows of data are skipped — single-window topics have no growth rate.
- `summarize_trends()` always returns a non-empty string (falls back to plain text format).
- Growth rate of `0.0` returned when all counts are zero or mean is zero (not `NaN`).

#### Caveats

- KMeans uses `random_state=42` for reproducibility, but cluster labels may shift if entry set changes significantly.
- `detect_trends()` fetches up to 500 entries — O(n) scan; slow on very large journals.

#### Error Handling

- `_get_entries_with_timestamps()`: silently skips entries raising `ValueError` or `OSError`
- `_get_embedding()`: catches all exceptions, returns `None`
- `summarize_trends()`: catches all LLM exceptions, falls back to plain text

#### Configuration

```python
# KMeans parameters
n_init=10, random_state=42

# Direction thresholds
growth_rate >  0.2  →  "emerging"
growth_rate < -0.2  →  "declining"
otherwise           →  "stable"

# Entry scan limit
list_entries(limit=500)
```

Growth rate formula (`_calc_growth_rate`):
```python
slope = np.polyfit(x, y, 1)[0]   # x = [0, 1, ..., n-1], y = counts per window
growth_rate = slope / mean(y)
# Returns 0.0 if all counts are zero or mean is zero
```

---

### JournalExporter

**File:** `src/journal/export.py`

#### Behavior

Exports journal entries to JSON or markdown. Both methods delegate filtering and content loading to `_get_entries()`. The output directory is created (including parents) if absent. JSON output wraps entries in `{"exported_at", "count", "entries"}`. Markdown output writes a header block followed by `## {title}` sections separated by `---`. When `days` is specified, entries with unparseable `created` fields are included (not dropped). When `limit` is not specified, defaults to 1,000. Both methods return the count of entries exported as `int`.

#### Inputs / Outputs

`export_json(output_path, entry_type=None, days=None, limit=None) -> int`
- JSON structure: `{"exported_at": ISO str, "count": int, "entries": [...]}`
- `json.dump` uses `indent=2, default=str`

`export_markdown(output_path, entry_type=None, days=None, limit=None) -> int`
- Header: `# Journal Export`, exported timestamp, entry count, `---`
- Per entry: `## {title}`, `**Type:** ... | **Date:** ...`, optional `**Tags:** ...`, content body, `---`

`_get_entries(entry_type, days, limit) -> list[dict]`
- Default limit: `limit or 1000`
- Date filter: parses `created` field as ISO datetime; entries with unparseable `created` or no `created` field are included when `days` is set
- Loads full content via `storage.read()`; silently skips files raising `OSError`/`ValueError`

#### Invariants

- Default `limit=1000` when not specified — not unbounded.
- Both `export_json()` and `export_markdown()` return the count of exported entries as `int`.
- Entries with unparseable `created` fields are INCLUDED (not dropped) when `days` filter is active.
- Output directory is created if absent — `mkdir(parents=True, exist_ok=True)`.

#### Error Handling

- File-level errors in `_get_entries()`: silently skips entries raising `OSError` or `ValueError`
- No exception raised if `output_path` parent creation fails (would propagate from `Path.mkdir`)

#### Configuration

Default export limit: `1000` entries when `limit` is not specified.
---

## Test Expectations

- `JournalStorage.create()`: verify collision avoidance loop generates `_1`, `_2` suffixes; verify `ValueError` on invalid `entry_type`; verify `MAX_CONTENT_LENGTH` and `MAX_TAGS` limits; verify path traversal rejection.
- `JournalStorage.list_entries()`: verify skipped unreadable files don't raise; verify OR-logic tag filter.
- `EmbeddingManager.sync_from_storage()`: mock ChromaDB; verify `added` count reflects only genuinely new IDs; verify removal of stale IDs.
- `JournalFTSIndex.sync_from_storage()`: verify mtime-based incremental update; verify stale row deletion.
- `JournalSearch.hybrid_search()`: mock both sub-searches; verify RRF fusion formula; verify fallback to keyword when embeddings absent.
- `analyze_sentiment()`: test all four label paths (positive/negative/mixed/neutral); test empty string; test text with no recognized words.
- `ThreadDetector.detect()`: mock ChromaDB query; verify all four decision-tree branches (unthreaded, joined_existing, created_new, unthreaded when min_entries not met).
- `TrendDetector.detect_trends()`: mock EmbeddingManager; verify `[]` when `len(entries) < n_clusters`; verify growth rate formula on synthetic data.
- `generate_title()`: verify `None` on short content; verify `None` on LLM exception; verify title length guard.
- Mocks required: `httpx`, ChromaDB client, LLM provider, filesystem (for storage tests).
