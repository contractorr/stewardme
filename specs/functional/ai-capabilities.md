# AI Capabilities KB and Capability Horizon Model

**Status:** Implemented
**Author:** —
**Date:** 2026-03-11

## Problem

Users making career and strategic decisions need current context about AI capabilities — what works, what doesn't, and where things are heading. Without a structured knowledge base, the advisor gives generic answers about AI that may be outdated or inaccurate.

## Users

All users asking AI-related questions. Context injected into advisor prompts automatically.

## Desired Behavior

### Static KB

1. Curated knowledge across 6 domains: coding, research, reasoning, autonomy, creative, tool_use.
2. Each domain includes: what works, limitations, key benchmarks, trajectory.
3. `render_context()` produces formatted LLM prompt context for specified domains.
4. `render_summary()` produces a ~500 char high-level snapshot.
5. Staleness warning logged when data exceeds 90 days old.

### Capability Horizon Model

1. Aggregates AI capability scraper output into per-domain structured estimates via LLM synthesis.
2. 10 domains: software_engineering, data_analysis, creative_writing, scientific_research, legal_reasoning, medical_diagnosis, customer_service, physical_world_interaction, long_horizon_planning, multimodal_understanding.
3. Per domain: current_level (0–1), months_to_next_threshold (0–120), confidence (low/medium/high), key_signals.
4. Pydantic-validated; gaps filled from static fallback.
5. Persisted to SQLite, pruned to 10 rows.

### Scrapers (6 classes in `ai_capabilities.py`)

1. `AICapabilitiesScraper` — METR GitHub API + Chatbot Arena + HELM
2. `METRScraper` — METR evaluation results
3. `EpochAIScraper` — notable AI models
4. `AIIndexScraper` — Stanford AI Index metrics
5. `ARCEvalsScraper` — ARC evaluation results
6. `FrontierEvalsGitHubScraper` — LLM-filtered GitHub issues from frontier eval repos

## Acceptance Criteria

- [ ] KB covers 6 domains with structured what-works/limitations/benchmarks/trajectory.
- [ ] Staleness warning fires after 90 days.
- [ ] Horizon model produces validated per-domain estimates.
- [ ] Static fallback fills gaps when scraper data or LLM is unavailable.
- [ ] All 6 scrapers produce structured intel items.

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| KB data > 90 days old | Warning logged; stale data still served |
| LLM synthesis fails | Static fallback data used for horizon model |
| Scraper target site down | Scraper returns empty; other scrapers unaffected |
| Domain not in static fallback | Omitted from horizon model output |

## Out of Scope

- User-editable capability assessments
- Real-time benchmark tracking
