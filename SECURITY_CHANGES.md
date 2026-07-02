# Security Changes — hardening/compass-port

Plain-language summary of the security fixes on this branch (external code
review findings F1–F4), for updating the live deployment deliberately.
Detailed specs: `specs/functional/security-hardening.md`.

## 1. User ID path-traversal fix (F1) — `src/storage_paths.py`

**What was vulnerable:** user IDs (OAuth `sub` claims) flow into filesystem
paths (`~/coach/users/{id}/`) and ChromaDB collection names, but were only
sanitized by replacing `:` with `_`. A crafted `sub` containing `/` or `..`
could escape the per-user directory and read or write another user's data.

**What changed:** sanitization is now allowlist-based — every character
outside `[A-Za-z0-9_-]` becomes `_`; IDs that sanitize to nothing usable
(empty, or only `_`/`.`) are rejected with an error.

**Deployment impact:** none for existing users. The deployed OAuth `sub`
formats (alphanumerics plus `:`) map to exactly the same directory names as
before; a regression test pins that equivalence.

## 2. Prompt-injection hardening (F2) — scraper → advisor pipeline

**What was vulnerable:** scraped third-party content (HN, Reddit, arbitrary
RSS, web search) entered advisor prompts with no provenance marking and no
rule telling the model it is data. In agentic mode that content sits next to
tools that read the journal and trigger web searches — a path for a
malicious article to steer tool use or exfiltrate journal text.

**What changed (three layers):**
1. All scraped/intel content is wrapped in
   `<untrusted_external_content source="...">` at retrieval/assembly time;
   literal wrapper tags inside content are escaped so it can't break out.
2. The advisor system prompts carry a standing rule: wrapped content is
   data, never instructions; instruction-like text inside it is ignored.
3. The agentic orchestrator blocks outbound tool calls (`web_search`,
   `intel_add_rss_feed`) whose arguments copy ≥8 consecutive words verbatim
   from untrusted content in the conversation, logging
   `outbound_tool_call_blocked`. This is deliberately blunt — paraphrased
   injections are not caught by the code layer.

**Deployment impact:** none to configure. The RAG context cache will serve
pre-existing unwrapped entries until entries expire or the cache
(`~/coach/context_cache.db`) is cleared — clearing it on deploy is
recommended so wrapping applies immediately.

## 3. Web backend rate limiting (F4) — `src/web/rate_limit.py`

**What was vulnerable:** only shared-key ("lite mode") users had limits.
Users with personal keys — and any holder of a valid JWT, which
auto-registers on first request — could hammer LLM-invoking routes without
bound.

**What changed:** per-user sliding-window limits for **all** users:
- LLM routes (advisor ask/stream, research run + dossier create, curriculum
  question/guide generation and grading, onboarding chat): default
  **20/min per user**.
- All other `/api/*` routes: default **120/min**, keyed per auth token
  (client IP when unauthenticated). `/api/health` is exempt.
- Responses are `429` with a `Retry-After` header.

**Operator config (optional — defaults apply without it):**
```yaml
web:
  rate_limit:
    enabled: true
    llm_per_minute: 20
    general_per_minute: 120
```
Limits are in-memory (reset on deploy) and sized for a single worker; if you
scale to multiple uvicorn workers, each worker enforces its own window.

## 4. Research outbound query hygiene + audit log (F3) — `src/research/`

**What was vulnerable:** research topics are derived from journal themes and
goals; queries built from them were sent to Tavily/DuckDuckGo verbatim and
unlogged — private journal-derived text could leave the machine silently.

**What changed:**
- Every query passes `sanitize_outbound_query()` before sending: queries
  containing feelings vocabulary are dropped; first-person pronouns are
  stripped; sentence-like queries are reduced to a ≤10-word topic core.
- Every query actually sent is appended (timestamp, verbatim query,
  provider) to `~/coach/research/outbound_log.jsonl` **before** it is
  issued — if the log can't be written, the query is not sent — and is
  included in the research report under "## Outbound Queries".

**Deployment impact:** none to configure. Expect the new JSONL file under
`$COACH_HOME/research/` after the first research run.

## Rollout checklist

1. Deploy the branch (standard `docker compose ... up -d --build`).
2. Optionally clear `~/coach/context_cache.db` so untrusted-content
   wrapping applies to cached RAG contexts immediately.
3. Optionally set `web.rate_limit.*` in `config.yaml` if the defaults
   (20/min LLM, 120/min general) don't fit your usage.
4. Verify: `POST /api/advisor/ask` past the limit returns 429 with
   `Retry-After`; `~/coach/research/outbound_log.jsonl` appears after a
   research run.
