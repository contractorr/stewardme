# Curriculum Package

Structured learning content, user-authored guides, progress tracking, reviews, and generated practice live here.

## Related Specs

- `specs/functional/curriculum.md`
- `specs/functional/curriculum-user-authored-guides.md`
- `specs/technical/curriculum.md`
- `specs/technical/curriculum-user-authored-guides.md`

## Entry Points

- `store.py`: canonical persistence and derived reads for guides, chapters, and progress
- `scanner.py`, `content_schema.py`: repository content ingestion and schema validation
- `user_content.py`, `guide_generator.py`: user-authored guide creation and storage
- `personalization.py`, `spaced_repetition.py`: adaptive review and scheduling logic
- `question_generator.py`: quiz, assessment, and teach-back generation
- `models.py`, `embeddings.py`: curriculum domain models and cross-guide similarity support

## Working Rules

- Built-in guides remain repository-backed; user-authored flows must preserve origin and provenance metadata.
- Contract changes usually touch `src/web/routes/curriculum.py`, `src/web/models.py`, and `web/src/types/curriculum.ts`.
- `store.py` is a hotspot, so prefer helper extraction and targeted tests over wide edits.

## Validation

- `just test-curriculum`
- `uv run pytest tests/curriculum/ tests/web/test_curriculum_routes.py -q`
