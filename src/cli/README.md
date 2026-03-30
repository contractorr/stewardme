# CLI Package

The `coach` command-line interface lives here.

## Related Specs

- `specs/technical/cli.md`
- `specs/technical/user-data-storage.md`

## Entry Points

- `main.py`: Click root command and process bootstrap
- `commands/`: user-facing command groups and standalone commands
- `config.py`, `config_models.py`: config loading and normalization
- `logging_config.py`: CLI logging setup
- `rate_limit.py`, `retry.py`, `utils.py`: shared command helpers

## Working Rules

- New commands should be added in `commands/` and registered through `commands/__init__.py`.
- Keep CLI handlers thin and delegate durable business logic to domain packages or `src/services/`.
- Setup and config flows should stay aligned with `docs/development.md` and `config.example.yaml`.

## Validation

- `uv run pytest tests/cli/ -q`
