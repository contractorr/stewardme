# Settings & Account

**Status:** Implemented
**Author:** -
**Date:** 2026-03-07

## Problem

Users need a safe place to manage API keys, understand whether they are on shared/lite mode, update account-facing identity details, and delete their account data when needed.

## Users

All authenticated web users.

## Desired Behavior

### Managing AI settings

1. User can view whether provider settings and secret keys are configured.
2. Secrets are never returned in raw form; the product shows masked state only.
3. User can save or update LLM and research-related credentials.
4. User can test LLM connectivity after saving a key.

### Lite mode

1. If the user has no personal LLM key, the product can fall back to shared/lite mode.
2. Lite mode is clearly explained in the UI.
3. Lite mode still supports the core product, but certain higher-cost capabilities remain limited.

### Account identity

1. User can view and edit their display name.
2. The product prefers the app-level display name over the raw OAuth name when available.

### Account deletion

1. User can delete their account.
2. Account deletion removes stored user metadata and attempts best-effort cleanup of per-user filesystem data.

## Acceptance Criteria

- [ ] Settings endpoints return masked state rather than raw secrets.
- [ ] User can update settings and test LLM connectivity from the web product.
- [ ] Lite/shared mode is surfaced in the UI when the user lacks a personal key.
- [ ] User can edit their display name.
- [ ] User can delete their account from the product.

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| User saves an invalid LLM key | Connectivity test fails with a clear error |
| User has no personal key | Product can continue in lite/shared mode |
| Name update fails | Settings UI remains usable; user can retry |
| File cleanup during delete partially fails | Account deletion succeeds and cleanup is logged as best effort |

## Out of Scope

- Billing and subscription management
- Multi-account switching in one session
- Secret export or key escrow features
