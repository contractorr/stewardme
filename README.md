# StewardMe

[![CI](https://github.com/contractorr/stewardme/actions/workflows/test.yml/badge.svg)](https://github.com/contractorr/stewardme/actions/workflows/test.yml)
[![Lint](https://github.com/contractorr/stewardme/actions/workflows/lint.yml/badge.svg)](https://github.com/contractorr/stewardme/actions/workflows/lint.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: AGPL-3.0](https://img.shields.io/badge/license-AGPL--3.0-green.svg)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

**An e-bike for the mind** — AI that guides you through new topics, professional growth and personal reflection, grounded in live data, personalised to you.

**Try the live demo at [StewardMe.ai](https://stewardme.ai)**

- **Master new topics** — 50+ structured guides with spaced repetition, Bloom's taxonomy quizzes, and teach-back prompts. Add your own material. 
- **Stay ahead** — 19 scrapers (HN, GitHub, arXiv, Reddit, Product Hunt, YC Jobs, Google Patents, RSS, and more) filtered to what matters to you
- **Reflect and grow** — journal your thinking, set goals, get advice grounded in your own context
- **Runs anywhere** — CLI, web app, MCP server (52 tools for Claude Code), or Docker one-liner

## Why StewardMe?

**The world moves fast** - 
There is a lot of signal online that is underutilised. Every day, you miss important events and updates that you might have found useful or interesting. The problem is they are buried across hundreds of sources, and everybody is time-poor.

**Foundation models are complementary** - 
Humans are limited in bandwidth, recall, and hours in the day. LLMs aren't. Right now our strengths are complementary. StewardMe is allows users to delegate the scanning, pattern-matching and synthesis to a model.

**Journaling closes the loop.** - 
Journaling forces reflection. Writing things down also creates a signal that can be leveraged to guide AI. It creates a feedback loop that allows models to do more targeted research and surface more relevant information to you over time. Your journal is what makes the AI personal. 

### How it compares

| | ChatGPT / Copilot | Notion AI | StewardMe |
|---|---|---|---|
| **Your data stays local** | No | No | Yes — SQLite + markdown files |
| **Scans live sources for you** | No | No | Yes — 19 scrapers (HN, arXiv, GitHub, Reddit, RSS, ...) |
| **Learns from your feedback** | No | No | Yes — per-category scoring adjusts over time |
| **Self-hosted** | No | No | Yes — Docker one-liner or bare metal |
| **Multi-provider LLM** | GPT only | GPT only | Claude, OpenAI, Gemini (auto-detect) |
| **Open source** | No | No | AGPL-3.0 |

## What it does

- **Curriculum & learn** — 50+ guides (327 chapters), SM-2 spaced repetition, Bloom's taxonomy quizzes, teach-back prompts, cross-guide connections via ChromaDB
- **Journal + semantic search** — markdown entries with YAML frontmatter, ChromaDB embeddings, sentiment analysis, trend detection
- **Intelligence radar** — 19 scrapers across 14 source files, SQLite storage with URL + content-hash dedup
- **AI advisor** — RAG retrieval (dynamic journal/intel blend from engagement data) fed to Claude, OpenAI, or Gemini. Agentic + classic modes
- **Goal tracking** — milestones, check-ins, staleness detection, nudges
- **Deep research** — topic selection from your context, web search (Tavily or DuckDuckGo), LLM synthesis → reports
- **Memory & threads** — persistent user memory (facts, context), thread inbox with state machine
- **Behavioural learning** — feedback on every recommendation, per-category scoring adjusts over time
- **Rich onboarding** — first-run wizard with LLM connectivity test, conversational profile interview

Works as a CLI (`coach`), web app (FastAPI + Next.js), or MCP server (52 tools) for Claude Code.

## Quick start

### Prerequisites

- Python 3.11+
- Node.js 18+ (for web UI)
- An LLM API key (Claude, OpenAI, or Gemini)

### Install

```bash
git clone https://github.com/contractorr/stewardme.git
cd stewardme
python -m venv .venv && source .venv/bin/activate
pip install -e ".[all-providers]"
coach init
```

### Configure

```bash
cp config.example.yaml ~/coach/config.yaml
# Edit with your preferences — API key can be set via env var or in-app
export ANTHROPIC_API_KEY="your-key"
```

### Run the CLI

```bash
coach journal add "Starting my Rust learning journey"
coach ask "What should I focus on this week?"
coach goals add "Learn Rust" --deadline 2025-06-01
coach scrape        # gather intel from all sources
coach trends        # detect emerging topics
coach research run "distributed systems"
```

### Run the web app

```bash
# Backend
pip install -e ".[web]"
cp .env.example .env  # fill in SECRET_KEY, NEXTAUTH_SECRET, OAuth creds
uvicorn src.web.app:app --reload --port 8000

# Frontend (separate terminal)
cd web && npm install && npm run dev
```

Open http://localhost:3000 — sign in with GitHub or Google.

### Docker (fastest)

```bash
cp .env.example .env  # fill in SECRET_KEY, NEXTAUTH_SECRET, OAuth creds
docker compose up --build
```

See [SETUP.md](SETUP.md) for full instructions including secret generation and production deployment.

## Architecture

```
src/
├── advisor/        # LLM orchestration, RAG retrieval, recommendations, agentic + classic modes
├── journal/        # Markdown storage, ChromaDB embeddings, semantic search, sentiment, trends
├── intelligence/   # 19 scrapers (14 source files), SQLite storage, APScheduler
├── curriculum/     # 50+ guides, SM-2 spaced repetition, Bloom's quizzes, teach-back
├── research/       # Deep research — topic selection, web search, LLM synthesis
├── memory/         # Persistent user memory (facts, context)
├── llm/            # Provider factory — Claude, OpenAI, Gemini (auto-detect from env)
├── profile/        # User profile, LLM-driven onboarding interview
├── library/        # Content library management (reports, PDF uploads)
├── services/       # Shared service layer
├── coach_mcp/      # MCP server — 52 tools across 13 modules
├── web/            # FastAPI backend — JWT auth, Fernet encryption, 24 route modules
├── cli/            # Click CLI, Pydantic config, structlog, retry, rate limiting
web/                # Next.js 16 + React 19 + Tailwind v4 + shadcn/ui
```

**Data flow:**

1. Journal entries → markdown files + ChromaDB embeddings + sentiment analysis
2. Scrapers → SQLite with URL + content-hash dedup
3. Query → RAG retrieval (journal + intel, dynamic weighting) + profile + memory → LLM → advice
4. Curriculum → SM-2 scheduling → quiz generation → Bloom's grading → progress tracking
5. Goals + journal → topic selection → deep research → reports
6. Embeddings → KMeans clustering → trend detection

## Configuration

See [`config.example.yaml`](config.example.yaml) for all options. Key sections:

| Section | What it controls |
|---------|-----------------|
| `llm` | Provider, API key, model override |
| `paths` | Journal dir, ChromaDB dir, intel DB |
| `sources` | RSS feeds, GitHub languages, Reddit subs, arXiv categories |
| `rag` | Context budget, journal/intel weight split |
| `recommendations` | Categories, dedup threshold, schedule |
| `research` | Web search provider (Tavily or DuckDuckGo free), schedule |
| `rate_limits` | Per-source token bucket config |
| `schedule` | Cron for intel gathering, reviews, research |

Config locations (checked in order): `./config.yaml` → `~/.coach/config.yaml` → `~/coach/config.yaml`

## CLI commands

| Command | Description |
|---------|-------------|
| `coach journal add/list/search/view/sync` | Journal CRUD + semantic search |
| `coach ask "question"` | Ask advisor with RAG context |
| `coach review` | Weekly review of recent entries |
| `coach goals add/list/check-in/status/analyze` | Goal tracking + milestones |
| `coach recommend [category]` | Generate recommendations |
| `coach research run/topics/list/view` | Deep research |
| `coach scrape` | Run all intel scrapers |
| `coach trends` | Detect emerging/declining topics |
| `coach mood` | Mood timeline from journal sentiment |
| `coach reflect` | Get reflection prompts |
| `coach daemon start` | Background scheduler |

## Web UI routes

| Route | Description |
|-------|-------------|
| `/home` | Dashboard with daily briefing, goals, suggestions |
| `/focus` | Advisor chat with RAG context |
| `/radar` | Intelligence feed from all scrapers |
| `/library` | Reports, PDF uploads, saved research |
| `/learn` | Curriculum hub — guides, quizzes, progress |
| `/journal` | Create, read, search entries |
| `/settings` | API key management (Fernet-encrypted), profile |

## MCP server

StewardMe exposes 52 tools across 13 modules via MCP for Claude Code integration. No LLM calls in the MCP layer — Claude Code does the reasoning, MCP provides data.

```bash
python -m coach_mcp  # stdio transport
```

Configured in `.mcp.json` for auto-discovery.

## Development

```bash
pip install -e ".[dev]"

# Tests
ANTHROPIC_API_KEY=test-key pytest                                  # fast local default
pytest -m "not slow and not web and not integration"              # fast core suite
pytest -m "web or integration or slow"                            # extended suites
pytest tests/web/ -q                                               # web API only
pytest --cov=src --cov-report=term-missing -m "not slow and not web and not integration"

# Lint + format
ruff check src tests
ruff format src tests

# Type check
mypy src/ --ignore-missing-imports
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Adding a new intelligence source

1. Create scraper in `src/intelligence/sources/` inheriting `BaseScraper`
2. Implement `source_name` property + `scrape()` async method
3. Register in `scheduler.py` → `_init_scrapers()`

## Deployment

Production setup uses Caddy as reverse proxy with auto HTTPS:

```bash
./deploy.sh  # validates .env, builds, starts docker compose prod
```

See `docker-compose.prod.yml` and `Caddyfile` for details.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `RateLimitError` from LLM | Reduce `rate_limits` in config; retries handle transient 429s |
| ChromaDB schema errors | Delete `~/coach/chroma/` and run `coach journal sync` |
| Stale embeddings | Run `coach journal sync` after manual file edits |
| Daemon not logging | Check `~/coach/logs/`; daemon uses JSON structlog |

## License

[AGPL-3.0](LICENSE) — free to use and self-host. If you run a modified version as a service, you must open-source your changes.
