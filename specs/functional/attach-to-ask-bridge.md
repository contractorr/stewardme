# Attach-to-Ask Bridge

**Status:** Draft
**Author:** -
**Date:** 2026-03-08

## Problem

The advisor is meant to answer questions using the user's documents, but the current web chat flow does not yet support in-thread document attachments. Users have to think in terms of the Library first, which breaks the immediacy of asking "here is my document; tell me what matters right now."

## Overview

Attach-to-Ask Bridge lets a user attach a document directly within chat, wait for it to become queryable, and receive the same-turn answer grounded in that document. The experience should feel chat-first and contextual, while reusing the same private per-user document storage and indexing path as uploaded Library documents.

## Users

Users asking advisor questions that depend on resumes, project briefs, strategy decks exported as PDFs, research papers, or other reference material already represented as PDFs.

## User Stories

- As a user, I want to attach a document while asking a question so I can get a grounded answer immediately.
- As a user, I want to see when the document is ready to use in the current conversation.
- As a user, I want to keep a useful chat attachment for later by saving it into my Library.
- As a user, I want large or weakly extractable documents to fail clearly rather than silently not influencing the answer.

## Dependencies

- Depends on advisor document-grounded retrieval in `specs/functional/ask-advice.md`.
- Depends on PDF upload, extracted-text indexing, and file download behaviors in `specs/functional/library-reports.md`.
- Reuses the private document storage and indexing model described in the technical library and web specs.
- May optionally feed memory extraction from uploaded documents as described in `specs/functional/memory-threads.md`.
- Not yet built: in-thread upload UX, attachment-aware chat request payloads in web, conversation attachment persistence, and chat-first visibility rules for uploaded documents.

## Detailed Behavior

### Supported file types

1. V1 supports PDF attachments only.
2. Non-PDF office documents, images, audio, and video are rejected in chat with a clear validation message.
3. Future support for other document types depends on new extraction and indexing capabilities and is not part of this feature.

### Chat-first attachment flow

1. User opens a first-party web chat surface and selects one or more PDF files while composing a message.
2. Each attachment appears as a pending attachment card in the composer.
3. System uploads the file, extracts text, indexes it, and attaches it to the current conversation turn.
4. The user sees a clear readiness state for each attachment:
   - `Uploading`
   - `Extracting`
   - `Ready to use`
   - `Limited text extracted` when extraction succeeded poorly
5. Once at least one attachment is ready, the user can submit or continue the current question with confidence that the document will influence the same response.

### Relationship to Library documents

1. Chat remains the primary UX entry point for this flow.
2. Under the hood, chat attachments reuse the same private per-user document storage and indexing path as uploaded Library PDFs.
3. A chat attachment should not require the user to leave chat or open the Library workspace first.
4. User can choose `Save to Library` from the chat attachment UI so the document becomes a visible durable Library item.
5. If the product introduces chat-only visibility before save, that hidden-origins behavior is a dependency of this feature rather than an already-shipped capability.

### Ready-to-query moment

1. The attachment UI should make it obvious when the document is available for the current turn.
2. The advisor request should include the ready attachment ids with the same user message.
3. The assistant answer should be allowed to reference the document in plain language.
4. If the user submits before extraction finishes, the product should either hold the request briefly for ordinary uploads or explain that the attachment may affect a later reply if indexing is still incomplete.

### Large-document handling

1. The existing raw upload limit for PDFs still applies.
2. If extracted text is large, the system should use document retrieval over indexed chunks rather than trying to stuff the entire document into one prompt.
3. The user does not need to manage chunking manually.
4. If the document is very large or weakly extractable, the system can fall back to top relevant snippets and a bounded summary for same-turn use.
5. If extraction yields almost no usable text, the upload can still succeed, but the user is warned that the document may have limited effect on the answer.

### Saving and reuse

1. Chat attachments remain visible in the conversation transcript so the user can tell what was included.
2. User can save an attachment to the Library from the attachment card or a post-answer action.
3. Saved attachments are reusable for later advisor turns through normal document retrieval.
4. If document-derived memory extraction is enabled, durable user-relevant facts can be extracted after upload, but that should not delay the same-turn chat answer.

Current interface scope:
- V1 focuses on PDF upload, readiness states, same-turn advisor grounding, and optional save-to-Library.
- V1 does not require drag-and-drop across every chat surface on day one.
- V1 does not require document editing inside chat.

## Acceptance Criteria

- [ ] A user can attach one or more PDFs directly within a web chat interaction.
- [ ] The chat UI shows per-attachment readiness states before or during answer generation.
- [ ] Ready attachments can influence the same advisor response.
- [ ] Attachment references persist in the conversation transcript.
- [ ] Users can save a useful chat attachment into the Library from chat.
- [ ] Large documents are handled through retrieval over extracted text rather than full-document prompt injection.
- [ ] Weakly extractable or scanned PDFs produce a warning rather than silent failure.
- [ ] Non-PDF files are rejected with a clear validation message.

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| User uploads a scanned PDF with little extractable text | Upload can succeed, but the UI warns that the document may have limited effect |
| User submits the chat message before indexing finishes | UI explains that the attachment is still processing and may affect the next turn if not ready in time |
| PDF exceeds upload limit | Upload is rejected before advisor submission |
| User attaches multiple PDFs | Each attachment shows its own readiness state and can be included in the same turn |
| User decides the attachment is not needed | They can remove it from the pending composer state before sending |
| User is in shared/lite mode | The request still works within normal model and rate-limit constraints |

## Success Metrics

- Increase in advisor turns that include attached documents
- Increase in successful same-turn document-grounded answers
- Increase in chat-to-Library saves for reusable documents
- Decrease in user drop-off between wanting to ask about a document and actually asking

## Out of Scope

- Non-PDF document support in V1
- Image, spreadsheet, audio, or video attachments
- Rich document annotation or highlighting inside chat
- OCR-specific improvements beyond the baseline PDF extraction path

## Open Questions

- Should chat attachments be visible in the main Library list immediately, or only after explicit save?
- Should the product permit sending a message while attachments are still indexing, or require at least one attachment to reach `Ready to use` first?
