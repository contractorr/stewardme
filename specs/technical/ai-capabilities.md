# AI Capabilities KB and Capability Horizon Model

**Status:** Implemented

## Overview

Two-layer AI capability awareness: static curated KB for prompt injection + dynamic horizon model from scraper synthesis.

## Key Modules

- `src/advisor/ai_capabilities_kb.py` — static KB
- `src/intelligence/capability_model.py` — horizon model
- `src/intelligence/sources/ai_capabilities.py` — 6 scraper classes

## Static KB (`ai_capabilities_kb.py`)

- `AI_CAPABILITY_DOMAINS` dict — 6 domains (coding, research, reasoning, autonomy, creative, tool_use)
- Each domain: `what_works` list, `limitations` list, `key_benchmarks` list, `trajectory` string
- `LAST_UPDATED` datetime, `STALENESS_DAYS = 90`
- `render_context(domains?) -> str` — formatted for LLM prompt injection (top 3 items per section)
- `render_summary() -> str` — ~500 char overview
- `_check_staleness()` — logs warning if data age > STALENESS_DAYS

## Capability Horizon Model (`capability_model.py`)

- `CapabilityHorizonModel(db_path, llm?)` — constructor
- `CAPABILITY_DOMAINS` — 10 domain names
- `CapabilityDomain` (Pydantic): current_level (0–1), months_to_next_threshold (0–120), confidence (low/medium/high), key_signals list
- `_STATIC_FALLBACK` — default values when LLM/scraper data unavailable
- `get_horizon_context() -> str` — ~2000 char summary for LLM injection
- `get_domain_trajectory(domain) -> CapabilityDomain`
- SQLite table `capability_model`, pruned to 10 rows

## Scrapers (`sources/ai_capabilities.py`)

6 classes inheriting `BaseScraper`:
1. `AICapabilitiesScraper` — METR GitHub API, Chatbot Arena, HELM
2. `METRScraper` — METR evaluation results
3. `EpochAIScraper` — notable AI models from Epoch AI
4. `AIIndexScraper` — Stanford AI Index
5. `ARCEvalsScraper` — ARC evaluation results
6. `FrontierEvalsGitHubScraper` — GitHub issues from frontier eval repos, LLM-filtered

Helper functions: `_llm_extract_json()`, `_llm_extract_single()` for parsing unstructured HTML.

## Dependencies

- `intelligence.scraper.BaseScraper`
- `llm.factory.create_cheap_provider`
- `httpx`, `bs4.BeautifulSoup`
- `shared_types.IntelSource`
