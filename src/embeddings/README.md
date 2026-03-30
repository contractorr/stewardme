# Embeddings Package

Shared embedding-provider selection and versioning helpers live here.

## Related Specs

- `specs/functional/configurable-embeddings.md`
- `specs/technical/configurable-embeddings.md`

## Entry Points

- `factory.py`: provider selection and environment-based auto-detection
- `base.py`: common embedding protocol
- `openai.py`, `gemini.py`: provider-specific embedding adapters
- `versioning.py`: embedding-version helpers for rebuild and invalidation flows

## Working Rules

- Auto-detection should prefer real providers from configured credentials and fall back safely when none are available.
- Provider adapters should expose the same callable contract so journal, intelligence, curriculum, and library code can swap implementations cleanly.
- Versioning changes need to stay compatible with existing persisted vector stores.

## Validation

- `uv run pytest tests/embeddings/ tests/journal/test_embeddings.py tests/library/test_embeddings.py -q`
