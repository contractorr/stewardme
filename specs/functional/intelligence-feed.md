# Intelligence Feed

**Status:** Approved
**Author:** —
**Date:** 2026-03-06

## Problem

Users need curated industry intelligence relevant to their interests without manually checking dozens of sources. The advisor also needs fresh external context to give timely advice.

## Users

All users. Power users configure custom RSS feeds and enable additional sources.

## Desired Behavior

### Automated scraping

1. System runs scrapers on a configurable schedule (cron-based)
2. Each scraper fetches items from its source, normalizes them into a common format (title, URL, summary, tags, publish date)
3. Items are deduplicated by URL and content hash before storage
4. Semantic dedup catches near-duplicate content across sources (opt-in via `config.sources.semantic_dedup`, off by default)

Available sources (14 source files, 19 scraper classes — `ai_capabilities.py` contains 6 sub-scrapers):
- **Default enabled:** Hacker News top stories, RSS feeds
- **Opt-in:** GitHub trending, arXiv papers, Reddit (configurable subreddits), Product Hunt, YC Jobs, Google Patents, AI capabilities tracker (METR, Epoch AI, AI Index, ARC Evals, Frontier Evals), tech events, GitHub Issues (user's repos), Crunchbase, Google Trends, Indeed Hiring Lab

### Browsing intel

1. User lists recent intel items, optionally filtered by source or tags
2. System returns items with title, source, summary, URL, publish date, and relevance indicators
3. When an item matches the user's watchlist, the item is visibly labeled and can be ranked ahead of generic items even if it is slightly older

### Watchlists

1. User can create persistent watchlist items for companies, people, roles, sectors, technologies, geographies, events, and free-form themes
2. Each watchlist item can store optional context: why it matters, priority, tags, goal linkage, time horizon, aliases, and preferred sources
3. Watchlist items are available via web, CLI, and MCP
4. Intel matching uses watchlist terms and aliases, then adds a plain-language "Why this matters to you" explanation to the item
5. Watchlist matches boost ranking in feed and search so bespoke items surface before generic browsing results

### Intel follow-up

1. User can save a matched intel item for later follow-up
2. User can add or update a short note on a matched intel item
3. Saved or annotated items persist across sessions for that user

### Searching intel

1. User searches intel by keyword (FTS) or semantic similarity
2. Results are ranked and returned with relevance indicators

### Trending topics

1. System detects cross-source topic convergence (topic appearing in 2+ source families with at least 4 items within a time window)
2. User can view trending topics with supporting items from each source

### Goal-intel matching

1. System matches intel items against user's active goals
2. Matched items surface in heartbeat notifications and daily briefs
3. Goal matching and watchlist matching coexist; they do not replace each other

### Manual refresh

1. User can trigger an immediate scrape of all or specific sources
2. System reports items found, deduplicated, and saved

## Acceptance Criteria

- [ ] Scheduled scrapes run automatically via `coach daemon`
- [ ] Items are deduplicated by both URL and content hash
- [ ] Semantic dedup prevents near-identical items across different sources (when enabled)
- [ ] User can browse and search intel via CLI, web, and MCP
- [ ] User can CRUD watchlist items via CLI, web, and MCP
- [ ] Intel items can be matched against watchlists and visibly labeled with a "Why this matters to you" explanation
- [ ] Matching watchlist items are ranked ahead of generic feed items when relevance is otherwise comparable
- [ ] User can save or annotate matched intel for later follow-up
- [ ] Trending radar detects topics appearing in 2+ source families with minimum 4 items
- [ ] User can manually trigger a scrape
- [ ] Failed scrapes for one source don't block other sources
- [ ] RSS feeds are configurable via `config.yaml`
- [ ] Rate limiting infrastructure exists (token bucket in `cli/rate_limit.py`) but is not yet wired into scrapers

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| Source is down or returns error | Log error, skip source, continue with others |
| RSS feed returns malformed XML | Skip feed, log warning |
| Duplicate item from different sources | Deduplicated; only one copy stored |
| No sources enabled | No scraping occurs; intel DB stays empty |
| Very large RSS feed (1000+ items) | Hard-capped at 20 entries per feed |
| No API key for paid source (Tavily, Crunchbase) | Source silently skipped or falls back |
| Watchlist item duplicates an existing one | Upsert or merge by normalized label instead of creating noisy duplicates |
| Intel item matches multiple watchlist items | Show top matches in priority order and use the strongest one for ranking |
| User saves an intel item without a note | Save succeeds with an empty note |
| User clears note and unsaves item | Follow-up entry is removed or treated as inactive |

## Out of Scope

- User-generated intel items (manual URL submission)
- Push notifications for new intel (that's heartbeat/signals)
- Source-specific configuration beyond what's in `config.yaml`
