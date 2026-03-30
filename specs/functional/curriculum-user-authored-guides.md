# User-Authored Curriculum Guides

**Status:** Implemented
**Date:** 2026-03-30

## Purpose

The assistant can add user-owned learning guides when the built-in catalog is not enough.

This capability exists to solve two different problems:

- the user explicitly asks for a guide on a topic that is missing or too narrow
- the assistant notices a clear learning gap and wants to propose a useful guide

This is an assistant capability first, not a new primary Learn-page workflow.

## Product Rules

- Built-in guides remain the default Learn catalog.
- User-authored guides are mixed into Learn only after they have been generated.
- The assistant must prefer extending or pointing to an existing guide when that already covers the need.
- The assistant must not silently create lots of content.

## Explicit Assistant Actions

When the user explicitly asks for a new guide, the assistant may generate one immediately.

Supported explicit actions:

- create a new standalone guide from a topic prompt
- extend an existing guide with supplemental material focused on a user request

Expected behavior:

- the assistant checks for overlapping existing guides first
- if a close existing guide already fits, the assistant should prefer that guide or offer an extension
- if generation succeeds, the guide is stored as user-owned curriculum content and appears in Learn

## Proactive Guide Proposals

The assistant may proactively suggest a new guide when confidence is high that the topic would help the user.

High-confidence cases include:

- the user repeatedly asks questions around a topic not covered by the catalog
- the user's goals or current work clearly require a missing body of knowledge
- an existing guide is relevant but materially too narrow for the user's stated need

Default rule:

- proactive behavior must be suggestion-first, not silent generation

That means the assistant should create a guide candidate or ask for approval before generating content unless the user has explicitly asked for generation in the current conversation.

## Approval Policy

- Explicit user request to create or add a guide: generation is allowed immediately.
- Explicit user request to extend a guide: extension is allowed immediately.
- Proactive assistant idea with no user approval yet: create a candidate suggestion only.
- Silent autonomous generation without user approval: not allowed by default.

## Dedupe And Overlap Rules

Before creating a guide or proposal, the system should check for overlap against active guides.

The assistant should avoid:

- creating a guide whose title or topic substantially matches an existing guide
- creating a proactive candidate for a topic that already exists
- creating repeated candidates for the same topic within a recent window

When overlap is found, preferred fallbacks are:

- recommend the existing guide
- extend the existing guide
- explain why no new guide was created

## Learn Product Placement

This feature should not turn Learn into a content-builder UI.

Allowed surfaces:

- assistant chat
- suggestion feed
- generated user-owned guides appearing in the normal Learn catalog after creation

Disallowed default UX changes:

- prominent create-guide controls on the Learn landing page
- separate default sections that dominate the core browse-and-study flow

## Acceptance Criteria

- [ ] The assistant can generate a standalone guide when the user explicitly asks.
- [ ] The assistant can extend an existing guide when the user explicitly asks for more depth or a missing angle.
- [ ] The assistant checks for overlapping guides before generating.
- [ ] Proactive guide creation requires approval by default.
- [ ] Proactive guide proposals can be surfaced as suggestion items.
- [ ] Newly generated guides appear in the Learn catalog after sync.
- [ ] Generated guides are stored as user-owned curriculum content.

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| User asks for a guide that already exists | Assistant points to the existing guide or offers an extension instead of duplicating it |
| User asks for a guide very similar to an existing one | Assistant may still generate only if the requested angle is materially different |
| Proactive candidate already exists for the same topic | Do not create another candidate |
| A guide candidate becomes obsolete because a guide was created later | Candidate should stop surfacing as active guidance |
| Generation fails because LLM credentials are unavailable | Assistant explains that generation is unavailable and does not create partial content |
