# Research

## Overview

The research module is a RAG-adjacent deep-research pipeline that automatically selects topics from goals, journal trends, and recurring themes, fetches web sources via Tavily or DuckDuckGo, synthesizes LLM-generated reports, and stores results as both journal entries (`entry_type="research"`) and intel DB items for hybrid retrieval. It exposes a sync `DeepResearchAgent`, an async `AsyncDeepResearchAgent`, two web search clients, an LLM synthesizer, and a topic selector. Public exports from `__init__.py`: `TopicSelector`, `WebSearchClient`, `ResearchSynthesizer`, `DeepResearchAgent`.

## Dependencies

**Depends on:** `llm` (ResearchSynthesizer uses create_llm_provider), `journal` (DeepResearchAgent stores entries + reads goals/tags for user context), `intelligence.scraper` (IntelItem, IntelStorage for storing research results), `cli.retry` (TokenBucketRateLimiter for WebSearchClient), `httpx` (sync + async HTTP), `beautifulsoup4` (DuckDuckGo scraping)

**Depended on by:** `intelligence.scheduler` (ResearchRunner wraps DeepResearchAgent), `coach_mcp` (research_topics + research_run tools)

---

## Components

### SearchResult

**File:** `src/research/web_search.py`

#### Behavior

Plain dataclass representing a single search result from any provider.

```python
@dataclass
class SearchResult:
    title: str
    url: str
    content: str
    score: float = 0.0
```

DuckDuckGo results always receive `score=0.5` (hardcoded). Tavily results receive the score returned by the API (`item.get("score", 0.0)`). Missing Tavily titles default to `"Untitled"`.

#### Invariants

- `score` from DuckDuckGo is always `0.5` (hardcoded) — not a real relevance score.
- `content` may be `""` (empty string) when scraping fails — callers must handle empty content.
- `url` is not validated — may be relative or malformed depending on source.

#### Error Handling

No exceptions raised; pure data holder.

---

### WebSearchClient

**File:** `src/research/web_search.py`

#### Behavior

Synchronous HTTP search client. Supports Tavily (paid, higher quality) with automatic fallback to DuckDuckGo HTML scraping when no API key is present. Enforces a token-bucket rate limit of 1 request/second.

```python
def __init__(
    self,
    api_key: Optional[str] = None,    # falls back to os.getenv("TAVILY_API_KEY")
    provider: str = "tavily",
    max_results: int = 8,
    max_content_chars: int = 3000,
)
```

HTTP client: `httpx.Client(timeout=30.0)`.
Rate limiter: `TokenBucketRateLimiter(requests_per_second=1.0, burst=1)` — called via `_rate_limit()` at the top of every `search()` call.

#### Inputs / Outputs

```python
def search(self, query: str, search_depth: str = "advanced") -> list[SearchResult]
def close(self) -> None
# also supports context manager (__enter__ / __exit__)
```

**Provider selection logic in `search()`:**

1. `provider == "tavily"` AND `api_key` is set → `_tavily_search(query, search_depth)`
2. `provider == "duckduckgo"` OR `api_key` is falsy → `_duckduckgo_search(query)`. When key is missing, logs `"No TAVILY_API_KEY, falling back to DuckDuckGo"` at INFO level.
3. Any other provider string → logs error `"Unknown search provider: %s"`, returns `[]`.

**`_tavily_search()` POST request:**

- Endpoint: `https://api.tavily.com/search`
- Body:
  ```json
  {
    "api_key": "<key>",
    "query": "<query>",
    "search_depth": "advanced",
    "include_answer": true,
    "include_raw_content": false,
    "max_results": 8
  }
  ```
- Content per result truncated to `max_content_chars` (default 3000) via slice `[: self.max_content_chars]`.

**`_duckduckgo_search()` scraping:**

- Endpoint: `https://html.duckduckgo.com/html/` with `?q=<query>`
- Header: `User-Agent: Mozilla/5.0 (compatible; stewardme/0.1)`
- HTML parser: `BeautifulSoup`. CSS selectors: `.result` (items), `.result__a` (title + href), `.result__snippet` (content).
- Items without a title element are skipped. Items without title text or href are skipped.
- Results capped at `max_results` via `soup.select(".result")[: self.max_results]`.
- All DuckDuckGo results get `score=0.5`.

#### Invariants

- Rate limiting (`_rate_limit()`) is called before every `search()` call regardless of provider.
- DuckDuckGo fallback is automatic when `api_key` is absent — callers cannot force DuckDuckGo with a key present.
- `max_results` and `max_content_chars` are applied per-provider and may truncate differently.
- `search()` always returns a `list` — never `None`; returns `[]` on error or unknown provider.

#### Error Handling

- `_tavily_search`: catches `httpx.HTTPStatusError` (logs status + body), `httpx.RequestError` (logs error), then a second redundant catch of `(httpx.HTTPStatusError, httpx.RequestError, ValueError)` — all return `[]`.
- `_duckduckgo_search`: bare `except Exception` → logs error, returns `[]`.

#### Configuration

| Parameter | Default | Source |
|-----------|---------|--------|
| `api_key` | `None` → `os.getenv("TAVILY_API_KEY")` | constructor or env |
| `provider` | `"tavily"` | constructor |
| `max_results` | `8` | constructor |
| `max_content_chars` | `3000` | constructor |
| HTTP timeout | `30.0` s | hardcoded |
| Rate limit | `1.0` req/s, burst `1` | hardcoded |

---

### AsyncWebSearchClient

**File:** `src/research/web_search.py`

#### Behavior

Async mirror of `WebSearchClient`. Uses `httpx.AsyncClient`. Does **not** implement rate limiting. Synthesis remains synchronous — only the HTTP I/O is async.

```python
def __init__(
    self,
    api_key: Optional[str] = None,
    provider: str = "tavily",
    max_results: int = 8,
    max_content_chars: int = 3000,
)
```

HTTP client: `httpx.AsyncClient(timeout=30.0)`.

#### Inputs / Outputs

```python
async def search(self, query: str, search_depth: str = "advanced") -> list[SearchResult]
async def close(self) -> None   # calls self.client.aclose()
# supports async context manager (__aenter__ / __aexit__)
```

Same provider selection logic as sync version. When provider is an unknown string that is not `"duckduckgo"` and `api_key` is set but provider is not `"tavily"`, returns `[]` (no explicit log, falls through the `if/elif` with no else clause that logs).

#### Invariants

- No rate limiting — unlike `WebSearchClient`, there is no `_rate_limit()` call.
- Returns `[]` on HTTP errors (status codes) or network exceptions.
- Not a drop-in replacement for `WebSearchClient` — differences: no rate limit, no recent tags in user context upstream.

#### Error Handling

- `_tavily_search`: catches `(httpx.HTTPStatusError, httpx.RequestError, ValueError)` → logs `"Async Tavily search failed: %s"`, returns `[]`.
- `_duckduckgo_search`: bare `except Exception` → logs `"Async DuckDuckGo search failed: %s"`, returns `[]`.

#### Configuration

Identical defaults to `WebSearchClient`. No rate limiter constructed.

---

### ResearchSynthesizer

**File:** `src/research/synthesis.py`

#### Behavior

Wraps an LLM provider to generate structured markdown research reports from a list of `SearchResult` objects. Reports follow a fixed five-section template. Retries on transient LLM errors; falls back to a source-list report on hard failure; returns a no-results stub when the results list is empty.

```python
def __init__(
    self,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    provider: Optional[str] = None,
    client=None,             # injectable test client
)
```

All args forwarded verbatim to `create_llm_provider()`.

**Class-level constants:**

`SYSTEM_PROMPT`:
```
You are a research assistant that synthesizes information from multiple sources into actionable research reports.

Your reports should be:
- Concise but comprehensive
- Focused on practical insights
- Well-structured with clear sections
- Honest about limitations or conflicting information
```

`SYNTHESIS_PROMPT` template (injects `{topic}`, `{sources}`, `{user_context}`):
```
Synthesize a research report on "{topic}" based on these sources:

{sources}

USER CONTEXT (their goals/interests):
{user_context}

Generate a research report with these sections:
## Summary
(2-3 sentence overview)

## Key Insights
(Bullet points of the most important findings)

## Relevance to Your Goals
(How this connects to the user's stated interests/goals)

## Sources
(List sources with brief descriptions)

## Next Steps
(2-3 actionable recommendations)

Be specific and practical. Cite sources when making claims.
```

#### Inputs / Outputs

```python
@llm_retry(exceptions=(LLMRateLimitError, LLMError))
def synthesize(
    self,
    topic: str,
    results: list[SearchResult],
    user_context: str = "",
    max_tokens: int = 2000,
) -> str
```

Returns a markdown-formatted string. One of three outputs:

1. **Normal path:** LLM response from `self.llm.generate(messages=[{"role": "user", "content": prompt}], system=SYSTEM_PROMPT, max_tokens=max_tokens)`.
2. **Empty results:** returns `_empty_report(topic)` immediately, no LLM call.
3. **LLM failure:** returns `_fallback_report(topic, results)`.

**`_format_sources()`** — one block per result:
```
[Source N] {title}
URL: {url}
Content: {content}

```
Blocks joined with `"\n"`.

**`_empty_report(topic)`** returns:
```markdown
## Summary
No sources found for "{topic}". This may be due to search API limitations or an overly specific query.

## Key Insights
- Unable to gather information at this time

## Next Steps
- Try a more general search term
- Check if TAVILY_API_KEY is configured correctly
- Research this topic manually
```

**`_fallback_report(topic, results)`** returns (source list limited to `results[:5]`):
```markdown
## Summary
Research gathered on "{topic}" but synthesis unavailable due to API error.

## Sources Found
- [title](url)
...

## Next Steps
- Review sources manually
- Retry research later
```

#### Invariants

- Empty `results` list triggers `_empty_report()` — no LLM call made.
- LLM failure after 3 retries triggers `_fallback_report()` — source list capped at 5 URLs.
- `synthesize()` always returns a non-empty `str` — never `None` or raises.
- Retry uses exponential backoff — caller should not add its own retry wrapper.
- Report always contains the 5-section structure (Summary, Key Insights, Relevance, Sources, Next Steps) when LLM succeeds.

#### Caveats

- `_fallback_report()` caps sources at 5 — may truncate a large result set silently.

#### Error Handling

- `@llm_retry(exceptions=(LLMRateLimitError, LLMError))`: tenacity decorator with `stop_after_attempt(3)`, `wait_exponential(multiplier=1, min=2.0, max=30.0)`. Reraises after exhaustion.
- Inner `try/except LLMError` inside `synthesize()`: catches any `LLMError` that survives retries, logs `"LLM synthesis failed: %s"`, returns `_fallback_report()` — does NOT re-raise.
- Empty `results` list: short-circuits before any LLM call, returns `_empty_report()`.
- `user_context=""` (empty string): substituted with `"No specific context provided."` before prompt formatting.

#### Configuration

| Parameter | Default | Notes |
|-----------|---------|-------|
| `max_tokens` | `2000` | per `synthesize()` call |
| retry attempts | `3` | `stop_after_attempt(3)` |
| retry wait min | `2.0` s | `wait_exponential(min=2.0)` |
| retry wait max | `30.0` s | `wait_exponential(max=30.0)` |
| fallback source cap | `5` | `results[:5]` |

---

### TopicSelector

**File:** `src/research/topics.py`

#### Behavior

Generates a ranked list of research topics by aggregating three sources: explicit goal entries, journal embedding trends, and frequency-weighted journal themes. Deduplicates across all three sources (case-insensitive). Filters out recently-researched topics. Returns at most `max_topics` results sorted by score descending.

```python
def __init__(
    self,
    storage: JournalStorage,
    journal_search=None,           # optional; enables trend extraction
    max_topics: int = 2,
    theme_window_days: int = 30,
    min_mentions: int = 3,
    skip_researched_days: int = 60,
)
```

#### Inputs / Outputs

```python
def get_topics(self, researched_topics: Optional[list[str]] = None) -> list[dict]
# Returns list of {topic, source, score, reason}, length <= max_topics

def get_recent_research_topics(self) -> list[str]
# Returns topic strings for research entries within skip_researched_days window

def get_suggested_topics(self) -> list[dict]
# Alias: calls get_recent_research_topics() then get_topics()
```

**Three topic sources (applied in order, deduplicated before merge):**

**1. Goals (`_extract_goal_topics()`)**

- Reads `entry_type="goal"`, limit 20.
- Lowercases content and applies 5 regex patterns (with `re.IGNORECASE`):
  - `r"research\s+(?:about\s+)?([^,.!\n]+)"`
  - `r"learn\s+(?:more\s+)?about\s+([^,.!\n]+)"`
  - `r"understand\s+([^,.!\n]+)"`
  - `r"explore\s+([^,.!\n]+)"`
  - `r"deep\s+dive\s+(?:into\s+)?([^,.!\n]+)"`
- Topic accepted only if `3 < len(topic) < 100` (after `.strip()`).
- Topic cased with `.title()`.
- `score = 10` (fixed, highest priority).
- `reason = f"Explicit goal: {entry['title'][:40]}"`.

**2. Trends (`_extract_trend_topics()`)**

- Requires `journal_search` to be set; returns `[]` otherwise.
- Instantiates `TrendDetector(journal_search)`, calls `.get_emerging_topics(threshold=0.2, days=60)`.
- Takes top 5 results.
- Score formula: `min(9, 5 + growth_rate * 10)`.
- Topic cased with `.title()`.
- `reason = f"Emerging trend (growth={growth_rate:+.0%})"`.
- Any exception → silently returns `[]`.

**3. Journal themes (`_cluster_journal_themes()`)**

- Reads last 100 entries (`list_entries(limit=100)`), filters to entries within `theme_window_days` (default 30) using ISO-format `created` field.
- Extracts words with `r"\b[a-zA-Z]{4,}\b"` (minimum 4 characters) after lowercasing.
- Tags from each entry are added with weight `+2` (i.e., `word_counter[tag.lower()] += 2`).
- Stopwords removed (63 words — see full list below).
- Considers only top 20 words by frequency (`most_common(20)`).
- Topic included only if `count >= min_mentions` (default 3).
- Score: `min(count, 10)` (capped at 10).
- Topic cased with `.title()`.
- `reason = f"Mentioned {count} times in last {theme_window_days} days"`.

**Stopwords list (63 words):**
`that, this, with, from, have, been, were, will, would, could, should, about, which, their, there, what, when, where, than, then, they, them, some, more, also, just, only, very, much, such, like, into, over, after, before, being, through, each, work, working, worked, want, need, think, know, make, made, take, took, come, came, going, doing, done, time, today, week, month, year, daily, journal, entry, note, notes, goal, goals, project`

**Final merge and sort:**
- Candidates from all three sources deduplicated (case-insensitive) in source order (goals → trends → themes).
- Sorted descending by `score`.
- Sliced to `max_topics`.

**`get_recent_research_topics()`:**
- Reads `entry_type="research"`, limit 50.
- Filters to entries where `created` is within the last `skip_researched_days` (default 60) days.
- Extracts topic from `post.get("topic")` or `entry["title"].replace("Research: ", "")`.

#### Invariants

- Returns at most `max_topics=2` topics — hardcoded default.
- Topics researched within 60 days are always skipped regardless of score.
- Dedup is case-insensitive — "Machine Learning" and "machine learning" are the same topic.
- Goal pattern extraction is done with regex, not LLM — no API call in topic selection.
- `get_topics()` always returns a list — never `None`; may be empty.

#### Error Handling

- `_extract_trend_topics`: bare `except Exception` — any error returns `[]`.
- `_cluster_journal_themes`: ISO date parse errors (`ValueError`, `TypeError`) caught per entry, entry skipped.
- `get_recent_research_topics`: ISO date parse errors caught per entry, entry skipped.

#### Configuration

| Parameter | Default | Notes |
|-----------|---------|-------|
| `max_topics` | `2` | output cap |
| `theme_window_days` | `30` | lookback for theme clustering |
| `min_mentions` | `3` | minimum word count for theme inclusion |
| `skip_researched_days` | `60` | recency window for dedup |
| trend threshold | `0.2` | `TrendDetector.get_emerging_topics(threshold=0.2)` |
| trend lookback | `60` days | `TrendDetector.get_emerging_topics(days=60)` |
| trend top-N | `5` | `emerging[:5]` |
| goal entry limit | `20` | `list_entries(entry_type="goal", limit=20)` |
| theme entry limit | `100` | `list_entries(limit=100)` |
| theme top-N words | `20` | `most_common(20)` |
| keyword min length | `4` chars | `r"\b[a-zA-Z]{4,}\b"` |
| tag weight | `2` | `word_counter[tag] += 2` |
| topic len min | `> 3` chars | goal pattern filter |
| topic len max | `< 100` chars | goal pattern filter |
| score cap (trends) | `9` | `min(9, ...)` |
| score cap (themes) | `10` | `min(count, 10)` |

---

### DeepResearchAgent

**File:** `src/research/agent.py`

#### Behavior

Synchronous orchestrator. Selects topics (or accepts a manual override), runs web search, synthesizes a report, stores it as a journal entry and an intel DB item, and embeds the content. Returns a result list describing success or failure per topic.

```python
def __init__(
    self,
    journal_storage: JournalStorage,
    intel_storage: IntelStorage,
    embeddings: EmbeddingManager,
    config: Optional[dict] = None,    # defaults to {}
)
```

#### Inputs / Outputs

```python
def run(self, specific_topic: Optional[str] = None) -> list[dict]
# Returns list of result dicts per topic

def get_suggested_topics(self) -> list[dict]
def close(self) -> None    # calls search_client.close()
```

Result dict on success: `{"topic": str, "filepath": Path, "success": True}`
Result dict on empty search: `{"topic": str, "filepath": None, "success": False}`
Result dict on caught exception: `{"topic": str, "filepath": None, "success": False, "error": str(e)}`

**Pipeline per topic (in `run()`):**

1. `search_client.search(topic)` — if empty list returned, appends failure result and continues to next topic.
2. `synthesizer.synthesize(topic, search_results, user_context)` — always called with user context string.
3. `_store_journal_entry(topic, report, topic_info)` — creates `entry_type="research"`, `title="Research: {topic}"`, tags `["research", "auto", topic_info["source"]]`, metadata `{"topic": topic, "research_source": topic_info["source"], "research_reason": topic_info["reason"]}`.
4. `_store_intel_item(topic, report, search_results)` — saves `IntelItem(source="deep_research", title="Research: {topic}", url="research://{slug}/{YYYYMMDD}", summary=report[:500], content=report, published=datetime.now(), tags=["research", "auto"])`.
5. `_add_embeddings(filepath, report)` — calls `embeddings.add_entry(str(filepath), content, {"type": "research"})`.

**Intel URL scheme:** `research://{topic.lower().replace(' ', '-')}/{datetime.now().strftime('%Y%m%d')}`

**Intel summary truncation:** `report[:500]` (only applied if `len(report) > 500`; otherwise full report).

**Manual topic override:** when `specific_topic` is passed, topics list is `[{"topic": specific_topic, "source": "manual", "score": 10, "reason": "User specified"}]`.

**`_get_user_context()`:**
- Goals: `list_entries(entry_type="goal", limit=5)` → formats as `"GOALS:\n- {title}\n..."`.
- Recent interests: `list_entries(limit=10)` → collects tags from all entries (up to 10 unique), formats as `"RECENT INTERESTS:\nTags: tag1, tag2, ..."`.
- Returns empty string if no data.

#### Invariants

- Empty search results for a topic produce `success=False` without calling the LLM synthesizer.
- Intel item URL scheme is always `research://{slug}/{date}` — distinguishable from HTTP URLs.
- `run()` processes all topics and catches per-topic errors — one failed topic does not abort others.
- Journal entry type is always `"research"` — never `"daily"` or other types.
- User context always includes goals + recent tags — not profile summary.

#### Caveats

- Per-topic `IOError/ValueError/KeyError` are caught and produce `success=False`; other exceptions propagate — callers must be aware of this asymmetry.

#### Error Handling

- Per-topic `except (IOError, ValueError, KeyError)`: logs `"Research failed for %s: %s"`, appends failure result with `"error"` key, continues.
- All other exceptions propagate out of `run()`.
- No search results: warning logged `"No search results for topic: %s"`, result appended with `success=False`, continues.

#### Configuration

Config consumed from `config["research"]`:

| Key | Default | Forwarded to |
|-----|---------|-------------|
| `max_topics_per_week` | `2` | `TopicSelector.max_topics` |
| `skip_if_researched_days` | `60` | `TopicSelector.skip_researched_days` |
| `api_key` | `None` | `WebSearchClient.api_key` |
| `api_provider` | `"tavily"` | `WebSearchClient.provider` |
| `sources_per_topic` | `8` | `WebSearchClient.max_results` |

Config consumed from `config["llm"]`:

| Key | Default | Forwarded to |
|-----|---------|-------------|
| `model` | `None` | `ResearchSynthesizer.model` |
| `provider` | `None` | `ResearchSynthesizer.provider` |
| `api_key` | `None` | `ResearchSynthesizer.api_key` |

---

### AsyncDeepResearchAgent

**File:** `src/research/agent.py`

#### Behavior

Async variant of `DeepResearchAgent`. Uses `AsyncWebSearchClient` for non-blocking HTTP. All other steps (synthesis, journal storage, intel storage, embeddings) remain synchronous. Constructor and config consumption are identical to the sync version.

```python
def __init__(
    self,
    journal_storage: JournalStorage,
    intel_storage: IntelStorage,
    embeddings: EmbeddingManager,
    config: Optional[dict] = None,
)
```

#### Inputs / Outputs

```python
async def run(self, specific_topic: Optional[str] = None) -> list[dict]
async def close(self) -> None    # calls await search_client.close()
```

#### Differences from sync `DeepResearchAgent`

| Aspect | Sync | Async |
|--------|------|-------|
| Search client | `WebSearchClient` | `AsyncWebSearchClient` |
| Rate limiting | Yes (token bucket) | No |
| `search()` call | blocking | `await self.search_client.search(topic)` |
| Synthesis call | sync `synthesizer.synthesize(...)` | same (still sync, comment: `"# Synthesis is sync (LLM call)"`) |
| `_get_user_context()` | goals + recent entry tags | goals only (no recent tags section) |
| Journal metadata | includes `"research_reason"` key | omits `"research_reason"` key |
| Failure result dict | includes `"error": str(e)` key | omits `"error"` key |
| `close()` | `self.search_client.close()` | `await self.search_client.close()` |
| No-topics log | logs `"No topics to research"` | does not log, silently returns `[]` |

#### Invariants

- Search is async; synthesis and storage remain sync — `asyncio.gather` is only used for parallel searches.
- Not a drop-in async replacement: missing `"error"` key in failure dicts, missing `research_reason` metadata key.
- No rate limiting (unlike sync `WebSearchClient`).
- User context omits recent tags (unlike `DeepResearchAgent`).

#### Error Handling

- Per-topic `except (IOError, ValueError, KeyError)`: logs `"Async research failed for %s: %s"`, appends `{"topic": topic, "filepath": None, "success": False}` (no `"error"` key), continues.

#### Configuration

Identical config keys and defaults to `DeepResearchAgent`.
---

## Test Expectations

- `WebSearchClient.search()`: verify Tavily POST request body format; verify DuckDuckGo HTML parsing with mock BeautifulSoup; verify fallback to DuckDuckGo when `api_key` absent; verify unknown provider returns `[]`.
- `WebSearchClient` rate limiting: verify `_rate_limit()` called before every `search()` call.
- `ResearchSynthesizer.synthesize()`: mock LLM; verify empty results → `_empty_report()` (no LLM call); verify LLM failure → `_fallback_report()` (source list capped at 5).
- `ResearchSynthesizer` retry: mock LLM to raise `LLMRateLimitError` twice then succeed; verify 3 attempts total.
- `TopicSelector.get_topics()`: mock journal storage; verify goal pattern extraction; verify 60-day dedup skips recently researched topics; verify case-insensitive dedup across sources; verify `max_topics=2` cap.
- `DeepResearchAgent.run()`: mock WebSearchClient + ResearchSynthesizer + storage; verify empty search results → `success=False` without LLM call; verify `research://` URL scheme in stored intel item; verify `IOError/ValueError/KeyError` caught per-topic; verify other exceptions propagate.
- `AsyncDeepResearchAgent`: verify differences from sync version (no rate limit, no recent tags in context, no `"error"` key in failure dicts).
- Mocks required: `httpx.Client`/`httpx.AsyncClient`, LLM provider, `JournalStorage`, `IntelStorage`, `EmbeddingManager`.
