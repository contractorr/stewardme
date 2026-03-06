# Intelligence Feed

**Status:** Approved
**Author:** —
**Date:** 2026-03-02

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
2. System returns items newest-first with title, source, summary, URL, and publish date

### Searching intel

1. User searches intel by keyword (FTS) or semantic similarity
2. Results are ranked and returned with relevance indicators

### Trending topics

1. System detects cross-source topic convergence (topic appearing in 2+ source families with at least 4 items within a time window)
2. User can view trending topics with supporting items from each source

### Goal-intel matching

1. System matches intel items against user's active goals
2. Matched items surface in heartbeat notifications and daily briefs

### Manual refresh

1. User can trigger an immediate scrape of all or specific sources
2. System reports items found, deduplicated, and saved

## Acceptance Criteria

- [ ] Scheduled scrapes run automatically via `coach daemon`
- [ ] Items are deduplicated by both URL and content hash
- [ ] Semantic dedup prevents near-identical items across different sources (when enabled)
- [ ] User can browse and search intel via CLI, web, and MCP
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

## Out of Scope

- User-generated intel items (manual URL submission)
- Intel item annotations or bookmarking
- Push notifications for new intel (that's heartbeat/signals)
- Source-specific configuration beyond what's in `config.yaml`
