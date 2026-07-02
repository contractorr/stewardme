# Local Drop-Folder Ingest

**Status:** Draft
**Author:** Raj
**Date:** 2026-07-02

## Problem

External pipelines (e.g. a scheduled task that reads Gmail via a connector)
should be able to feed items into StewardMe's intelligence feed without
StewardMe holding any mail or API credentials.

## Users

Operators wiring external automations into their own instance.

## Desired Behavior

1. A `local_drop` intelligence source reads files from a configurable
   directory (default `~/coach/intel_dropbox/`). Disabled by default; enable
   via `sources.local_drop.enabled` / `sources.local_drop.directory`.
2. Accepted formats:
   - `.md` — title from the first `#` heading (else filename); optional YAML
     frontmatter keys `title`, `url`, `source`, `published` (or `date`);
     body becomes content.
   - `.json` — minimal schema `{title, url?, source, published_at?,
     content}`; `title`, `source`, `content` required.
3. On successful ingest the file is moved to a `processed/` subfolder —
   never deleted. Name collisions get a numeric suffix.
4. Malformed or unreadable files are skipped with a logged warning (no
   crash) and left in place so the producer can fix them.
5. Existing URL + content-hash dedup applies. Items with no URL get an
   internal `localdrop://{content_hash}` URL, so they dedup on content hash
   alone; re-dropping the same content does not create a duplicate.
6. Drop-folder content is external, untrusted input: it flows through the
   `<untrusted_external_content>` tagging automatically because tagging
   happens at context assembly time (see security-hardening §2).

## Acceptance Criteria

- [ ] Both formats ingest with correct title/url/source/date mapping.
- [ ] Processed files are moved, not deleted; originals never remain in the
      drop root after successful ingest.
- [ ] Re-dropping the same content is deduplicated (0 new items).
- [ ] A malformed file logs a warning, is skipped, and remains in place.
- [ ] Intel context assembled from drop-folder items is wrapped in
      `<untrusted_external_content>`.

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| Drop directory absent | Scrape returns no items, no error |
| Unsupported extension (e.g. `.txt`) | Ignored, left in place |
| `processed/` name collision | Numeric suffix (`name-1.md`) |
| JSON missing `content` | Warning, skipped, left in place |
| Item without URL re-dropped | Deduped on content hash |

## Out of Scope

- Watching the directory (ingest happens on scheduler runs).
- Any fetching of remote resources referenced by dropped files.
