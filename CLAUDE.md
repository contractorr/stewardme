# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Activate venv (do this first)
source .venv/bin/activate

# Install
pip install -e ".[dev]"          # dev deps
pip install -e ".[all-providers]" # all LLM providers

# Test
pytest                                          # all tests
pytest tests/advisor/test_engine.py::test_ask_advice -v  # single test
pytest --cov=src --cov-report=term-missing -v   # with coverage

# Lint & format
ruff check src tests
ruff format src tests

# Type check (advisory, not enforced in CI)
mypy src/ --ignore-missing-imports
```

Tests require `ANTHROPIC_API_KEY=test-key` in env. Async tests use `pytest-asyncio` with `asyncio_mode = "auto"`.

## Architecture

RAG-based personal AI advisor. User writes journal entries, system scrapes external intelligence, advisor combines both via retrieval-augmented generation.

### Core modules (all under `src/`)

- **journal/** — Markdown files with YAML frontmatter (`storage.py`), ChromaDB embeddings (`embeddings.py`), semantic+keyword search, KMeans trend detection (`trends.py`), sentiment analysis (`sentiment.py`), entry templates (`templates.py`)
- **intelligence/** — 5 async scrapers in `sources/` (HN, GitHub, arXiv, Reddit, RSS) inheriting `BaseScraper`, SQLite storage with URL+content-hash dedup, APScheduler for background jobs
- **advisor/** — `AdvisorEngine` orchestrates LLM+RAG. `RAGRetriever` blends journal (70%) + intel (30%) context. Unified `Recommender` with single 1-10 scoring. Recommendations stored as markdown with frontmatter. Goal tracking, weekly action briefs
- **research/** — Deep research agent: topic selection from journal/goals/trends → web search (Tavily or DuckDuckGo free fallback) → LLM synthesis → reports
- **llm/** — Provider factory with auto-detection from env vars. Unified `LLMProvider` interface with Claude/OpenAI/Gemini implementations
- **cli/** — Click CLI (`coach` command). Commands: ask, review, goals, journal, recommend, research, trends, reflect, export, daemon, init. Pydantic config validation. Structlog logging

### Data flow

1. Journal entries → markdown files in `~/coach/journal/` + ChromaDB embeddings + sentiment analysis
2. Scrapers → SQLite `~/coach/intel.db` with dedup
3. Recommendations → markdown files in `~/coach/recommendations/`
4. Query → RAG retrieval (journal+intel) → LLM → advice
5. Background: scheduler runs scrapes + weekly reviews + optional email digests via `coach daemon`

### Cross-cutting

- **Retries:** Tenacity exponential backoff on HTTP/LLM calls (`cli/retry.py`)
- **Rate limiting:** Token bucket per source (`cli/rate_limit.py`)
- **Security:** Path traversal protection in journal CRUD, URL scheme validation, API key redaction in logs, content length limits
- **Observability:** `observability.py` counters/timers, structlog correlation IDs

## Feature Freeze

Core loop stabilization in progress. Do NOT add new features.

Core (stable): journal, intelligence scrapers, RAG retrieval, advisor Q&A, recommendations
Experimental: goal tracking, deep research, trend clustering, learning paths
Removed: mood analysis, burnout detection, momentum detection

### Adding a new intelligence source

1. Create scraper in `src/intelligence/sources/` inheriting `BaseScraper`
2. Implement `source_name` property + `scrape()` async method
3. Register in `scheduler.py` → `_init_scrapers()`

## MCP Server

`src/coach_mcp/` exposes core modules as MCP tools (journal, goals, intel, recommendations, research, reflection). Claude Code does the reasoning; MCP server provides data + context retrieval only — no LLM calls in the MCP layer.

```bash
# Run standalone
python -m coach_mcp  # stdio transport

# Configured in .mcp.json for Claude Code auto-discovery
```

Tools: `journal_get_context`, `journal_create`, `journal_list`, `journal_read`, `journal_search`, `journal_delete`, `goals_list`, `goals_add`, `goals_check_in`, `goals_update_status`, `goals_add_milestone`, `goals_complete_milestone`, `intel_search`, `intel_get_recent`, `intel_scrape_now`, `recommendations_list`, `recommendations_update_status`, `recommendations_rate`, `research_topics`, `research_run`, `get_reflection_prompts`

## Config

App config: `~/coach/config.yaml` (see `config.example.yaml`). Pydantic-validated on load. Supports env var interpolation (`${ANTHROPIC_API_KEY}`).
