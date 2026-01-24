# AI Coach

Personal AI-powered professional advisor combining journal knowledge with external intelligence gathering for contextual career and life advice.

## Overview

AI Coach is a RAG-based system that:
- Stores personal journal entries with semantic search (ChromaDB)
- Scrapes external intelligence (Hacker News, RSS feeds, GitHub trending)
- Uses Claude API to provide personalized advice based on both sources

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

# Advice types: general, career, goals, opportunities

# Weekly review (analyzes recent journal entries)
coach review

# Opportunity detection (combines your profile with trends)
coach opportunities
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
    timeframe: daily  # daily, weekly, monthly
  enabled:
    - hn_top
    - rss_feeds
    - github_trending
    - custom_blogs

schedule:
  weekly_review: "sunday 9am"
  intelligence_gather: "daily 6am"
```

## Data Storage

All data stored in `~/coach/`:
- `journal/` - Markdown files with YAML frontmatter
- `chroma/` - ChromaDB vector embeddings
- `intel.db` - SQLite database for scraped intelligence

## Architecture

```
src/
├── journal/       # Storage + embeddings + search
├── advisor/       # LLM orchestration + RAG
├── intelligence/  # Scrapers + scheduler
└── cli/           # Click commands
```

**Data Flow:**
1. Journal entries → Markdown + auto-embedded to ChromaDB
2. Scrapers → SQLite intel DB
3. Ask question → RAG retrieves context → Claude generates advice

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check src tests
ruff format src tests

# Type check
mypy src
```

## License

MIT
