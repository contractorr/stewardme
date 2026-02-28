# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Activate venv (do this first)
source .venv/bin/activate

# Install
pip install -e ".[dev]"              # dev deps
pip install -e ".[all-providers]"    # all LLM providers
pip install -e ".[web]"             # FastAPI backend
pip install -e ".[dev,all-providers,web]"  # everything (matches CI)

# Test
pytest                                          # all tests
pytest tests/advisor/test_engine.py::test_ask_advice -v  # single test
pytest tests/web/ -v                            # web API only
pytest --cov=src --cov-report=term-missing -v   # with coverage (fail_under=50)

# Lint & format
ruff check src tests
ruff format src tests

# Type check (advisory, not enforced in CI)
mypy src/ --ignore-missing-imports

# Web app
uvicorn src.web.app:app --reload --port 8000  # backend
cd web && npm install && npm run dev            # frontend (port 3000)
```

Tests require `ANTHROPIC_API_KEY=test-key` in env. Async tests use `pytest-asyncio` with `asyncio_mode = "auto"` globally. Ruff ignores `E501`.

### Test patterns

Root `conftest.py` provides temp dirs, mock LLM provider, sample data, and httpx mocks. Web tests (`tests/web/conftest.py`) provide a `TestClient` with patched env + two JWT users for multi-user isolation. MCP tests auto-reset `bootstrap._components` singleton between runs. Check conftest files for available fixtures.

## Architecture

RAG-based personal AI advisor. Journal entries + external intelligence scrapers feed a retrieval-augmented generation pipeline. Runs as CLI (`coach`), FastAPI+Next.js web app, or MCP server.

### Core modules (all under `src/`)

- **advisor/** — `AdvisorEngine` with two modes and dual LLM instances (see below)
- **journal/** — Markdown files with YAML frontmatter, ChromaDB embeddings, semantic+keyword search, KMeans trend detection, sentiment analysis, entry templates
- **intelligence/** — 15 scrapers in `sources/` inheriting `BaseScraper` (HN, GitHub, arXiv, Reddit, RSS, Product Hunt, YC Jobs, Google Patents, AI capabilities, events, GitHub issues, Crunchbase, Google Trends, Indeed). Only HN+RSS enabled by default. SQLite storage with URL+content-hash dedup, APScheduler
- **research/** — Deep research: topic selection → web search (Tavily or DuckDuckGo fallback) → LLM synthesis → reports
- **llm/** — Provider factory with auto-detection from env vars. Unified `LLMProvider` interface: Claude/OpenAI/Gemini
- **profile/** — `UserProfile` Pydantic model (YAML-backed). `ProfileInterviewer` for LLM-driven onboarding (5-7 turns, force-extraction fallback). Two rendering modes: `summary()` (compact) and `structured_summary()` (multi-section XML)
- **cli/** — Click CLI (`coach` command). Pydantic config validation. Structlog logging
- **web/** — FastAPI backend: JWT auth (python-jose), Fernet-encrypted secret storage, per-user data isolation at `~/coach/users/{safe_user_id}/`. Global intel DB stays shared. 17 route modules. `get_or_create_user()` auto-registers on first request
- **coach_mcp/** — 54 MCP tools across 14 modules (journal, goals, intel, recommendations, research, reflect, profile, learning, projects, signals, brief, heartbeat, memory, threads)

### Advisor deep dive

Two modes in `AdvisorEngine.ask()`:
- **Agentic** (`use_tools=True`) — `AgenticOrchestrator` + `ToolRegistry`, LLM decides what to look up via tool calls
- **Classic RAG** — single-shot `RAGRetriever.get_combined_context()` + LLM

Dual LLM instances: `self.llm` (expensive) + `self.cheap_llm` (critic/scoring). Dynamic journal:intel weighting (default 70:30, adjusted from engagement data via `compute_dynamic_weight()`). SQLite-backed `ContextCache`. Memory (`<user_memory>` XML) and recurring thoughts (`<recurring_thoughts>` XML) injected into prompts.

### Web frontend (`web/`)

Next.js 16 + React 19 + TypeScript + Tailwind v4 + shadcn/ui. NextAuth v5 beta (GitHub/Google OAuth). JWT from NextAuth passed as `Authorization: Bearer` to FastAPI backend — `NEXTAUTH_SECRET` must match both sides. Middleware protects all routes except login/privacy/terms/api/auth.

### Data flow

1. Journal entries → markdown files in `~/coach/journal/` + ChromaDB embeddings + sentiment
2. Scrapers → SQLite `~/coach/intel.db` with dedup
3. Recommendations → markdown files in `~/coach/recommendations/`
4. Query → RAG retrieval (journal+intel, dynamic weighting) → profile + memory + threads context → LLM → advice
5. Background: scheduler runs scrapes + weekly reviews via `coach daemon`

### Cross-cutting

- **Retries:** Tenacity exponential backoff on HTTP/LLM calls (`cli/retry.py`)
- **Rate limiting:** Token bucket per source (`cli/rate_limit.py`)
- **Security:** Path traversal protection, URL scheme validation, API key redaction, content length limits, Fernet encryption for user secrets in web mode
- **Observability:** `observability.py` counters/timers, structlog correlation IDs

## Feature Freeze

Core loop stabilization in progress. Do NOT add new features.

Core (stable): journal, intelligence scrapers, RAG retrieval, advisor Q&A, recommendations
Experimental: goal tracking, deep research, trend clustering, learning paths, memory, threads, signals, heartbeat
Removed: mood analysis, burnout detection, momentum detection

## Adding a new intelligence source

(For when freeze lifts.)

1. Create scraper in `src/intelligence/sources/` inheriting `BaseScraper`
2. Implement `source_name` property + `scrape()` async method
3. Register in `scheduler.py` → `_init_scrapers()`

## MCP Server

`src/coach_mcp/` exposes 54 tools across 14 modules. Claude Code does the reasoning; MCP server provides data + context retrieval only — no LLM calls in the MCP layer. Tool convention: `TOOLS = [(name, schema_dict, handler_fn), ...]` per module, loaded lazily and cached in `server.py`.

```bash
python -m coach_mcp  # stdio transport, configured in .mcp.json for auto-discovery
```

## Config

`~/coach/config.yaml` (see `config.example.yaml`). Pydantic-validated. Supports env var interpolation (`${ANTHROPIC_API_KEY}`). Lookup order: `./config.yaml` → `~/.coach/config.yaml` → `~/coach/config.yaml`.

Notable config: `llm.extended_thinking`, `sources.deduplicate_rss_sources` (auto-disables dedicated scrapers when RSS equivalents exist), `agent.autonomous.*` for agentic features, `memory.*` and `threads.*` for context persistence.

## CI

- **test.yml** — Python 3.11 + 3.12 matrix, `pytest --cov-fail-under=50`, Codecov on 3.12
- **lint.yml** — `ruff check` + `ruff format --check` + `mypy` (continue-on-error). Separate job: `npm ci && npm run lint && npm run build` in `web/`
- **deploy.yml** — push to main triggers test then SSH docker compose deploy
