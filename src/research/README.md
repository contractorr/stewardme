# Research Package

Topic selection, web search, report synthesis, dossiers, and escalation logic live here.

## Related Specs

- `specs/functional/deep-research.md`
- `specs/functional/research-dossiers.md`
- `specs/functional/dossier-escalation-engine.md`
- `specs/technical/research.md`
- `specs/technical/research-dossiers.md`
- `specs/technical/dossier-escalation-engine.md`

## Entry Points

- `agent.py`: deep-research orchestration for reports and dossier updates
- `topics.py`: topic suggestion and selection
- `web_search.py`: web-search clients and result normalization
- `synthesis.py`: report and update synthesis
- `dossiers.py`: journal-backed dossier storage
- `escalation.py`: dossier escalation and action logic

## Working Rules

- Research artifacts stay journal-backed, so report and dossier metadata must remain compatible with journal consumers.
- Search, synthesis, and escalation flows should degrade cleanly when providers or sources are unavailable.
- Contract changes typically affect both `src/web/routes/research.py` and frontend library or radar types.

## Validation

- `uv run pytest tests/research/ tests/web/test_research_routes.py tests/web/test_dossier_escalations_routes.py -q`
