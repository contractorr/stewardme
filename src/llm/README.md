# LLM Package

Provider selection and provider-specific model adapters live here.

## Related Specs

- `specs/technical/llm.md`
- `specs/technical/llm-council.md`
- `specs/technical/usage-cost-estimation.md`

## Entry Points

- `factory.py`: provider selection, auto-detection, and cheap-tier helpers
- `base.py`: shared provider interfaces, tool definitions, and common errors
- `providers/claude.py`, `providers/openai.py`, `providers/openai_compatible.py`, `providers/gemini.py`: concrete provider implementations

## Working Rules

- Provider adapters should conform to the shared base interfaces so advisor, research, and onboarding code can swap providers safely.
- Auto-detection and API-key inference need to stay predictable because multiple surfaces rely on them.
- Model or usage-accounting changes tend to ripple into advisor, research, and web settings tests.

## Validation

- `uv run pytest tests/llm/ tests/advisor/test_agentic.py tests/research/test_synthesis.py -q`
