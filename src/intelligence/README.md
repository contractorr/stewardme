# Intelligence Package

Radar ingestion, ranking, watchlists, entity extraction, and trend detection live here.

## Related Specs

- `specs/functional/intelligence-feed.md`
- `specs/functional/trending-radar.md`
- `specs/functional/company-movement-pipeline.md`
- `specs/functional/github-project-monitoring.md`
- `specs/technical/intelligence.md`
- `specs/technical/trending-radar.md`
- `specs/technical/company-movement-pipeline.md`
- `specs/technical/regulatory-change-pipeline.md`

## Entry Points

- `scheduler.py`, `runners.py`, `job_registry.py`: background source orchestration
- `scraper.py`, `scraper_factory.py`, `sources/`: shared scraper interfaces and source implementations
- `search.py`, `user_intel_view.py`, `watchlist.py`, `watchlist_pipeline.py`: retrieval, filtering, and user-specific radar views
- `trending_radar.py`, `goal_intel_match.py`, `hiring_signals.py`, `regulatory.py`: ranking and derived-signal pipelines
- `company_watch.py`, `github_repo_poller.py`, `github_repo_store.py`, `github_repos.py`: tracked company and repository workflows
- `entity_extractor.py`, `entity_store.py`, `embeddings.py`: enrichment and semantic lookup support

## Working Rules

- Scrapers should stay isolated behind shared base types and scheduler registration.
- New source or pipeline behavior should update the relevant functional and technical specs and add targeted tests in `tests/intelligence/`.
- Feed, ranking, and watchlist changes usually affect `src/web/routes/intel.py`, `src/web/routes/github_repos.py`, and `web/src/types/radar.ts`.

## Validation

- `just test-intelligence`
- `uv run pytest tests/intelligence/ -q`
- `uv run pytest tests/web/test_intel_routes.py tests/web/test_github_repos_routes.py -q`
