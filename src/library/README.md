# Library Package

Library report storage, PDF extraction, indexing, and semantic lookup live here.

## Related Specs

- `specs/functional/library-reports.md`
- `specs/functional/attach-to-ask-bridge.md`
- `specs/technical/library.md`
- `specs/technical/attach-to-ask-bridge.md`

## Entry Points

- `reports.py`: markdown-backed report and uploaded-document storage
- `index.py`: SQLite FTS index and optional semantic search support
- `embeddings.py`: vector lookup helpers for library records
- `pdf_text.py`: PDF text extraction for uploads and chat attachments

## Working Rules

- Library records and attachments must stay contained within the library directory and keep extracted-text metadata in sync.
- Upload and indexing changes usually affect both the Library workspace and chat-attachment flows.
- Search behavior should stay useful even when embeddings are unavailable or extraction is partial.

## Validation

- `uv run pytest tests/library/ tests/web/test_library_routes.py tests/web/test_advisor_routes.py -q`
