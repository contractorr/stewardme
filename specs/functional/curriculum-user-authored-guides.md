# User-Authored Curriculum Guides

**Status:** Draft
**Author:** Codex
**Date:** 2026-03-29

## Problem

Learn currently treats the curriculum as a built-in catalog scanned from `content/curriculum/`.
Users can enroll in guides and progress through them, but they cannot ask the app to generate a
new guide for a topic they care about, add user-owned supplemental material, or remove custom
guides they no longer want. This creates a gap between the app's existing study workflow and the
user's need for topic-specific learning paths on demand.

## Users

- Users who want to study a topic that is not covered by the built-in curriculum
- Users who want to deepen an existing guide with more specialized material
- Users who want custom learning content to behave like the rest of Learn without polluting the
  built-in catalog

## Desired Behavior

1. User opens `Learn` and sees a new `Your Guides` area that is visually separate from the built-in
   curriculum library and tree.
2. User can click `Create guide`, enter a topic, specify desired depth, target audience, and
   available time budget, and optionally add a short free-form instruction.
3. The app uses the user's configured LLM access to generate a structured learning guide for that
   topic, including a title, chapter list, summaries, learning objectives, and chapter content.
4. When generation succeeds, the new guide appears under `Your Guides` and behaves like a normal
   guide for:
   - chapter reading
   - progress tracking
   - quizzes
   - teach-back
   - review scheduling
5. Creating a guide does not auto-enroll the user. The user can review the generated guide first
   and then choose whether to enroll.
6. Built-in guides remain visible in the existing library and tree views, but user-authored guides
   are shown in a separate user-owned section and are not mixed into built-in programs or the
   built-in prerequisite tree in the MVP.
7. User can open any guide and choose `Extend guide`.
8. Extending a guide creates a separate user-owned supplemental guide linked to the source guide. The
   supplemental material is treated as custom content, not as a mutation of the built-in guide.
9. On a built-in guide detail page, the user can see any generated extensions associated with that
   guide and open them directly.
10. On a user-authored guide detail page, the user can generate additional extensions the same way.
11. User can delete any user-authored guide or user-authored extension from Learn.
12. Deleting a user-authored guide sends it to a recoverable archive rather than removing it
    permanently in the MVP.
13. User can view archived guides and restore them.
14. Built-in guides cannot be deleted.
15. If guide generation is unavailable because no LLM credentials are configured, the app explains
    that guide generation requires an available model rather than failing silently.

## Acceptance Criteria

- [ ] `Learn` shows a dedicated `Your Guides` section that is separate from the built-in guide grid
  and tree.
- [ ] User can create a guide by providing a topic, target depth, target audience, and time budget.
- [ ] A created guide is stored as user-owned curriculum content and appears only for that user.
- [ ] Creating a guide does not auto-enroll the user.
- [ ] A created guide can be opened in the existing guide detail and chapter reader flows.
- [ ] A created guide supports normal curriculum progress, quiz, teach-back, and review behavior.
- [ ] User can extend a built-in guide without changing or overwriting the built-in guide itself.
- [ ] User can extend a user-authored guide with additional user-owned material.
- [ ] Extensions are represented as separate linked guides rather than as in-place mutations of the
  source guide.
- [ ] Guide detail shows whether a guide is built-in or user-authored.
- [ ] Guide detail shows linked user-authored extensions for the current guide when they exist.
- [ ] User can delete a user-authored guide or extension from the UI.
- [ ] Deleting a user-authored guide archives it, removes it from active Learn views, and prevents
  it from reappearing in active views on the next curriculum sync.
- [ ] User can restore an archived user-authored guide and recover its learning state.
- [ ] Built-in guides remain unchanged after user guide creation, extension generation, sync, and
  deletion operations.
- [ ] If generation fails, the user sees a clear error state and no partial guide is surfaced as a
  completed guide.
- [ ] If LLM credentials are unavailable, create/extend actions are disabled or fail with a clear
  actionable message.

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| User creates a guide for a topic similar to a built-in guide | The generated guide is still stored as user-authored and shown in `Your Guides`, not merged into the built-in catalog |
| User extends a built-in guide multiple times | Each extension is kept as separate user-owned supplemental content linked to the source guide |
| User deletes a guide with in-progress chapters and review items | The guide disappears from active Learn views but its state is preserved so restore can recover it |
| User deletes a guide that is referenced by older journal entries | The journal entries remain; restoring the guide re-enables normal Learn navigation |
| User tries to delete a built-in guide | The UI does not offer the action and the API rejects it if called directly |
| Generation produces invalid or incomplete curriculum content | The app surfaces generation failure and does not publish the guide as ready |
| User has no LLM key configured | Create and extend actions explain that generation is unavailable until an LLM is configured |
| User opens `/learn` with no custom guides | `Your Guides` shows an empty state with a create-guide CTA |
| User-generated guide has no enrollment yet | It still appears in `Your Guides` and can be enrolled or opened directly |
| User restores an archived guide whose source guide still exists | The restored guide returns to `Your Guides` with its previous extension link and progress state intact |

## Out of Scope

- Blending user-authored guides into built-in learning programs or the built-in prerequisite tree
- Collaborative or shared guides across users
- Manual WYSIWYG chapter editing in the MVP
- Auto-publishing user-authored guides into the global `content/curriculum/` corpus
- Cross-user recommendation learning from user-authored guide topics
- Replacing built-in guides in place with user-generated rewrites
