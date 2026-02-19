# AI Coach

Personal AI-powered professional advisor combining journal knowledge with external intelligence gathering for contextual career and life advice.

## Overview

AI Coach is a RAG-based system that:
- Stores personal journal entries with semantic search (ChromaDB)
- Scrapes external intelligence (HN, RSS, GitHub, arXiv, Reddit, Dev.to, Crunchbase, NewsAPI)
- Proactive recommendations for learning, career, entrepreneurial, and investment opportunities
- Deep research agent with web search and LLM synthesis
- Goal tracking with staleness detection, check-ins, and milestone progress
- Topic trend detection via embedding clustering (emerging/declining topics)
- Structured logging (structlog) with JSON mode for daemon, Rich console for CLI
- Retry + token-bucket rate limiting on all external API calls
- Uses Claude API to provide personalized advice based on all sources

## Quick Start

### Prerequisites
- Python 3.11+
- Anthropic API key

### Installation

```bash
# Clone and install
git clone <repo-url>
cd ai-coach
pip install -e .

# Initialize directories
coach init

# Set API key
export ANTHROPIC_API_KEY="your-key-here"
```

### Configuration

Copy and edit the config:
```bash
cp config.example.yaml ~/coach/config.yaml
```

Config locations (checked in order):
1. `./config.yaml` (project local)
2. `~/.coach/config.yaml`
3. `~/coach/config.yaml`

## Commands

### Journal Management

```bash
# Add entry (opens editor if no content)
coach journal add "Today I worked on..."
coach journal add -t project --title "API Redesign" "Started planning..."
coach journal add -t goal --tags "career,learning" "Learn Rust this quarter"

# Entry types: daily, project, goal, reflection

# List entries
coach journal list
coach journal list -t project -n 20

# Semantic search
coach journal search "career goals"
coach journal search "rust learning" -n 10

# View specific entry
coach journal view 2024-01-15_daily_standup.md

# Sync embeddings (after manual edits)
coach journal sync
```

### AI Advisor

```bash
# Ask questions (uses RAG context from journal + intel)
coach ask "What should I focus on this week?"
coach ask "How can I improve my Python skills?" --type career

# Weekly review (analyzes recent journal entries)
coach review

# Opportunity detection (combines your profile with trends)
coach opportunities
```

### Proactive Recommendations

```bash
# Generate recommendations by category
coach recommend learning          # Skills to learn
coach recommend career            # Career moves
coach recommend entrepreneurial   # Business opportunities
coach recommend investment        # Investment themes
coach recommend all               # All categories

# Action briefs and history
coach recommend brief             # Weekly action brief
coach recommend history           # View past recommendations
coach recommend view <id>         # View specific rec
coach recommend update <id> --status completed
coach recommend rate <id> 5       # Rate usefulness (1-5)
```

### Goal Tracking

```bash
# Manage goals with staleness detection
coach goals add "Learn Rust" --deadline 2024-06-01
coach goals list                  # Shows staleness indicators
coach goals check-in <id> "Made progress on chapters 1-3"
coach goals status <id> --status in_progress
coach goals analyze <id>          # AI analysis of goal progress

# Milestones
coach goals milestone add <goal> "Complete chapters 1-5"
coach goals milestone complete <goal> 0    # Complete milestone by index
coach goals progress <goal>                # Progress bar + milestone table
```

### Topic Trends

```bash
# Detect emerging/declining journal topics via embedding clustering
coach trends
coach trends --days 180 --window monthly
coach trends --clusters 12
```

### Deep Research

```bash
# AI-driven research on topics from your goals/journal
coach research run "distributed systems"
coach research topics             # Show suggested research topics
coach research list               # List all research reports
coach research view <id>          # View full report
```

### Intelligence Gathering

```bash
# Scrape all enabled sources now
coach scrape

# View recent intelligence
coach brief
coach brief -n 14 --limit 50

# Show configured sources
coach sources

# Export intel
coach intel-export --format json --output intel.json
coach intel-export --format csv --days 30
```

### Data Export

```bash
# Export journal entries
coach journal export --format json --output journal.json
coach journal export --format markdown --output journal/

# Export intelligence
coach intel-export --format csv --output intel.csv
```

### Background Daemon

```bash
# Run scheduler in background (daily scraping, weekly research)
coach daemon start
coach daemon run-once             # Single execution of all jobs
```

## Configuration Reference

```yaml
llm:
  provider: claude
  api_key: ${ANTHROPIC_API_KEY}  # env var expansion
  model: claude-sonnet-4-20250514

paths:
  journal_dir: ~/coach/journal   # markdown files
  chroma_dir: ~/coach/chroma     # vector embeddings
  intel_db: ~/coach/intel.db     # scraped intel

sources:
  rss_feeds:
    - https://news.ycombinator.com/rss
    - https://feeds.arstechnica.com/arstechnica/technology-lab
  custom_blogs:
    - https://paulgraham.com/articles.html
  github_trending:
    enabled: true
    languages: [python, rust, go]
    timeframe: daily
  enabled:
    - hn_top
    - rss_feeds
    - github_trending
    - custom_blogs
    - arxiv
    - reddit
    - devto

research:
  web_search_provider: tavily  # or serpapi
  web_search_api_key: ${TAVILY_API_KEY}
  max_sources: 5
  weekly_schedule: "sunday 8am"

recommendations:
  enabled_categories: [learning, career, entrepreneurial, investment]
  similarity_threshold: 0.85   # dedup similarity cutoff
  dedup_window_days: 30        # days before re-recommending
  weekly_brief: true
  schedule: "monday 7am"

rag:
  max_context_chars: 8000      # total context budget for RAG
  journal_weight: 0.7          # journal vs intel split (0.7 = 70% journal)

search:
  default_results: 5           # default number of search results
  intel_similarity_threshold: 0.7

rate_limits:
  default: {requests_per_second: 2, burst: 5}
  tavily: {requests_per_second: 1, burst: 1}
  hackernews: {requests_per_second: 5, burst: 10}
  reddit: {requests_per_second: 1, burst: 2}

schedule:
  weekly_review: "sunday 9am"
  intelligence_gather: "daily 6am"
  research: "sunday 8am"
  recommendations: "monday 7am"
```

## Data Storage

All data stored in `~/coach/`:
- `journal/` - Markdown files with YAML frontmatter
- `chroma/` - ChromaDB vector embeddings
- `intel.db` - SQLite database for scraped intelligence

## Web UI

Browser dashboard wrapping the same modules the CLI uses. FastAPI backend + Next.js 14 + NextAuth (GitHub/Google OAuth).

### Setup

```bash
# Backend
pip install -e ".[web]"
export SECRET_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
export NEXTAUTH_SECRET="generate-with-openssl-rand-base64-32"
uvicorn web.app:app --reload  # :8000

# Frontend
cd web && npm install && npm run dev  # :3000
```

### Docker Compose

```bash
docker compose up
# backend :8000, frontend :3000
```

### Pages

| Route | Description |
|-------|-------------|
| `/login` | GitHub / Google OAuth |
| `/` | Dashboard — recent journal, goals, intel |
| `/journal` | Create/read/delete entries |
| `/advisor` | Chat with AI advisor (RAG-powered) |
| `/goals` | Goals + milestones + check-ins |
| `/intel` | Intelligence feed + trigger scrape |
| `/settings` | API key management (Fernet-encrypted) |

### API Endpoints

All routes require JWT via `Authorization: Bearer <token>`.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check |
| GET/PUT | `/api/settings` | API keys (masked in GET) |
| GET/POST | `/api/journal` | List / create entries |
| GET/PUT/DELETE | `/api/journal/{path}` | Read / update / delete |
| POST | `/api/advisor/ask` | Ask advisor |
| GET/POST | `/api/goals` | List / create goals |
| POST | `/api/goals/{path}/check-in` | Check in |
| PUT | `/api/goals/{path}/status` | Update status |
| POST | `/api/goals/{path}/milestones` | Add milestone |
| GET | `/api/intel/recent` | Recent intel |
| GET | `/api/intel/search?q=` | Search intel |
| POST | `/api/intel/scrape` | Trigger scrape |
| GET | `/api/research/topics` | Suggested topics |
| POST | `/api/research/run` | Run research |

## Architecture

```
src/
├── journal/       # Storage, embeddings, search, export, trend detection
├── advisor/       # LLM orchestration, RAG, recommendations, goals + milestones
├── intelligence/  # Scrapers (8 sources), scheduler, export
├── research/      # Deep research agent, topic selection, synthesis
├── web/           # FastAPI backend — auth, crypto, routes
├── cli/           # Click commands, config (Pydantic), logging, retry, rate limiting
web/               # Next.js 14 frontend — OAuth, dashboard, settings
```

**Data Flow:**
1. Journal entries → Markdown + auto-embedded to ChromaDB
2. Scrapers → SQLite intel DB (8 sources, with retry + rate limiting)
3. Goals/journal → Topic selection → Deep research → Reports
4. All context → RAG retrieval → Claude generates advice/recommendations
5. Journal embeddings → KMeans clustering → Topic trend detection

**Cross-cutting:**
- Structured logging via `structlog` — JSON output in daemon mode, Rich console in CLI
- Automatic retries with exponential backoff on all HTTP and LLM calls (`tenacity`)
- Token-bucket rate limiting per source (configurable in `rate_limits` config)
- All magic numbers centralized in Pydantic config models with validation

## Dependencies

Core: `click`, `rich`, `anthropic`, `chromadb`, `httpx`, `pydantic`, `structlog`, `tenacity`, `scikit-learn`, `numpy`, `frontmatter`, `pyyaml`

Web: `fastapi`, `uvicorn`, `python-jose`, `cryptography`, `python-multipart`

Dev: `pytest`, `ruff`, `mypy`

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"
pip install -e ".[web]"  # web deps

# Run tests
pytest                    # all (373 tests)
pytest tests/web/ -v      # web API tests only

# Lint
ruff check src tests
ruff format src tests

# Type check
mypy src
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `RateLimitError` from Claude | Reduce `rate_limits` in config or wait; retries handle transient 429s automatically |
| ChromaDB version conflicts | Pin `chromadb>=0.4.0`; delete `~/coach/chroma/` and re-sync if schema changed |
| `ModuleNotFoundError: sklearn` | `pip install scikit-learn>=1.3.0` (needed for `coach trends`) |
| Stale embeddings after manual edits | Run `coach journal sync` to re-index |
| Daemon not logging | Check `~/coach/logs/`; daemon uses JSON-format structlog output |

## License

MIT
