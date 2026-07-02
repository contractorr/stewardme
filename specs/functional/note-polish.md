---
id: note-polish
category: tracked_feature
status: experimental
technical_specs:
- specs/technical/note-polish.md
- specs/technical/web.md
foundations:
- specs/foundations/design-system.md
- specs/foundations/ux-guidelines.md
last_reviewed: '2026-07-02'
---

# Note Polish (Messy Notes → Reviewed HTML)

## Problem

Users accumulate messy markdown and plain-text notes — typos, broken grammar, half-sentences,
repeated points, and the occasional factual slip. They want the app to turn a raw note into a
polished document they can read in the app, but they do not want silent rewriting: every
correction must be visible and explicitly accepted before the polished version replaces the
original.

## Users

- Users who capture rough notes (meetings, reading notes, study notes) and want a clean,
  trustworthy reading copy inside the app.

## Desired Behavior

### Submit

1. User opens Notes and pastes (or types) messy markdown or plain text, with an optional title.
2. The system polishes the note with the configured LLM:
   - fixes spelling and grammar,
   - corrects clear factual errors,
   - rewords awkward sections for clarity,
   - removes repetitive or duplicative content,
   - preserves the author's meaning, structure, and voice; it does not add new claims.
3. The system produces a polished document plus a review bundle:
   - a line-level diff between the original and polished text, and
   - an itemized list of corrections, each labeled `spelling`, `grammar`, `factual`,
     `rewording`, or `removal`, with the original text, the replacement, and a short reason.

### Review the diff

1. The user sees the itemized corrections grouped by type and the full diff.
2. The user either accepts or discards the polish. Acceptance is all-or-nothing in this
   version (no per-correction cherry-picking).
3. Until a decision is made, the note is `pending` and keeps the original text so the user
   can still discard.

### Accept

1. On accept, the system stores the polished note as sanitized HTML for in-app viewing and
   permanently discards the original input text.
2. The note becomes `accepted` and appears in the user's notes list.
3. Opening an accepted note renders the stored HTML.

### Discard

1. On discard, the pending note and its polish are deleted entirely; nothing is stored.

## Acceptance Criteria

- [ ] Submitting a note returns a pending note with polished output, a diff, and an itemized
      corrections list with per-item type labels (spelling/grammar/factual/rewording/removal).
- [ ] The diff faithfully reflects original vs polished text (a user can reconstruct what
      changed from it).
- [ ] Accepting a pending note stores HTML, marks it accepted, and the original input text is
      no longer retrievable through any endpoint.
- [ ] Discarding a pending note deletes it; it no longer appears in any list.
- [ ] Accepted notes are listed with title and date and render as HTML in the app.
- [ ] Stored HTML is sanitized: script tags, event handlers, and non-http(s) URLs never
      survive to the stored document.
- [ ] Notes are per-user: another user cannot list, view, accept, or delete them.
- [ ] When no LLM key is configured, submission fails with a clear message and nothing is
      stored.
- [ ] Empty or whitespace-only input is rejected with a validation error.

## Edge Cases

| Scenario | Expected Behavior |
| --- | --- |
| Note already clean (nothing to fix) | Polish returns near-identical text, an empty or tiny corrections list, and the user can still accept to get the HTML version |
| Very long note beyond the processing limit | Rejected upfront with the limit stated; nothing is sent to the LLM |
| LLM returns malformed output | The system falls back to treating the whole response as the polished text with an empty corrections list; if the response is unusable, the user sees a retryable error and nothing is stored |
| Note contains code blocks | Code blocks are preserved verbatim (not spell-checked or reworded) and render as code in the HTML |
| Note contains raw HTML | Dangerous markup is stripped during sanitization; safe formatting may be kept |
| User closes the app with a pending note | The pending note (with original) remains available to review, accept, or discard later |
| Duplicate submission of the same text | Creates a separate pending note; no dedup in this version |

## Out of Scope

- Per-correction accept/reject (cherry-picking individual edits).
- File uploads (PDF/DOCX) — paste text only in this version.
- Editing the polished HTML in-app after acceptance.
- Automatic flashcard generation from polished notes (future work; see `anki-decks`).
- Multi-note merge or organization features (folders, tags).

## Validation Notes

- Smallest meaningful validation slice: submit → inspect diff/corrections → accept → verify
  original is gone and HTML is stored; discard path verifies deletion.
- Contract impact: new `/api/notes/*` endpoints; new frontend types and Notes page.
- Follow-up spec work: generate flashcards from an accepted note into an Anki-style deck.
