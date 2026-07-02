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

## 2. Prompt-injection hardening on scraped content (F2)

### Desired Behavior

1. Any scraped/third-party content (intelligence items, web search results)
   that enters an advisor prompt is wrapped in
   `<untrusted_external_content source="...">…</untrusted_external_content>`
   so the model can tell data from instructions.
2. Literal wrapper tags inside scraped text are neutralized (escaped) so
   content cannot break out of, or spoof, the wrapper.
3. The advisor system prompt carries a standing rule: wrapped content is
   third-party data, never instructions; text directed at the assistant inside
   it is ignored, not acted on, and not repeated as advice.
4. In agentic mode, outbound tool calls (web search, feed fetch) are blocked
   at the code level when their arguments copy a span of ≥8 consecutive words
   verbatim from untrusted content seen earlier in the conversation. Blocked
   calls are logged and surfaced to the model as tool errors.

### Acceptance Criteria

- [ ] Assembled intel context is wrapped and a literal
      `</untrusted_external_content>` inside scraped text is escaped.
- [ ] The tool guard rejects an outbound call whose arguments echo ≥8
      consecutive words from an untrusted tool result, and allows a clean one.
- [ ] Placeholder strings ("No external intelligence available.") are not
      wrapped.

### Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| Scraped item contains the closing tag | Tag escaped; wrapper integrity preserved |
| Intel context truncated by token budget | Wrapper re-closed after truncation |
| Outbound call with paraphrased (not verbatim) injection | Not blocked — documented limitation of the blunt guard |
| Reranker / decomposed retrieval reorders intel lines | Tags stripped before reorder, re-applied after |

## 3. Web backend rate limiting (F4)

### Desired Behavior

1. Every authenticated user is rate-limited per user, regardless of whether
   they bring their own API key (the existing "lite mode" limit only covered
   shared-key users).
2. Routes that trigger paid LLM calls (advisor ask, research runs, curriculum
   question/guide generation and grading, onboarding chat) have a stricter
   limit than general API traffic.
3. Limits are configurable in `config.yaml` under `web.rate_limit`
   (`enabled`, `llm_per_minute` — default 20, `general_per_minute` — default
   120) and documented in `config.example.yaml`.
4. Exceeding a limit returns HTTP 429 with a `Retry-After` header.
5. One user hitting their limit never affects another user.

### Acceptance Criteria

- [ ] Hitting an LLM route past `llm_per_minute` returns 429 with
      `Retry-After`.
- [ ] A second user is unaffected while the first is limited.
- [ ] General API traffic past `general_per_minute` returns 429.
- [ ] `enabled: false` disables route limits (shared-key lite limits remain).

### Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| Unauthenticated request to general route | Keyed by client IP for the general limit; auth still returns 401 |
| Config file absent | Defaults apply (20/min LLM, 120/min general) |
| `/api/health` | Never rate-limited |

## Out of Scope

- Migration of directories for user IDs that previously contained path
  characters (none exist in the deployed OAuth `sub` formats).
- LLM-behavioral tests of the injection rule (layer 2 is prompt-level; only
  the mechanical layers are unit-tested).
