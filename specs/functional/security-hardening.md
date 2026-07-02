# Security Hardening (External Review Port)

**Status:** Draft
**Author:** Raj
**Date:** 2026-07-02

Findings from an external code review of the publicly deployed multi-user web
app. Each numbered section corresponds to one review finding and lands as an
independent change.

## Problem

The web app is deployed publicly and multi-user. The review found: user IDs
flow into filesystem paths with blocklist-only sanitization (F1); scraped
third-party content enters advisor prompts without provenance marking (F2);
research queries derived from private journal text leave the machine unlogged
(F3); and the web backend has no rate limiting (F4).

## Users

Operators of the deployed web app, and all end users whose data isolation,
privacy, and API spend depend on these controls.

## 1. User ID sanitization (F1)

### Desired Behavior

1. Any user ID (OAuth `sub` claim) is mapped to a filesystem-safe directory
   name before being used in `~/coach/users/{safe_user_id}/` paths or ChromaDB
   collection names.
2. Sanitization is allowlist-based: every character outside `[A-Za-z0-9_-]`
   becomes `_`.
3. IDs that sanitize to nothing meaningful (empty, or only `_`/`.` characters)
   are rejected with an error instead of producing a directory.
4. Backward compatibility: IDs valid under the previous mapping (`:` → `_`,
   i.e. alphanumerics plus `:` such as `github:12345`) map to the **same**
   directory name as before, so existing user data directories keep working.

### Acceptance Criteria

- [ ] `../`, `..\`, `/etc/passwd`, `a/../../b`, and null bytes cannot escape
      the users root — the resolved per-user path stays under
      `$COACH_HOME/users/`.
- [ ] Empty or all-punctuation IDs raise `ValueError`.
- [ ] `"12345"`, `"github:12345"`, `"google-oauth2:987"` map to identical
      directory names under old and new sanitization.

### Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| `sub` containing `/` or `..` | Replaced with `_`; path stays under users root |
| `sub` of only dots/underscores after sanitization | `ValueError`, no directory created |
| Empty `sub` | `ValueError` |
| Existing user with `google:123` | Same directory `google_123` as before the change |

## Out of Scope

- Migration of directories for user IDs that previously contained path
  characters (none exist in the deployed OAuth `sub` formats).
