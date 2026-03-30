# Profile Package

User profile storage and interview-driven onboarding live here.

## Related Specs

- `specs/functional/profile-onboarding.md`
- `specs/functional/settings-account.md`
- `specs/technical/profile.md`

## Entry Points

- `storage.py`: profile persistence and normalization
- `interview.py`: LLM-guided profile interview and JSON extraction

## Working Rules

- Stored profile fields are reused across advisor, curriculum, and settings flows, so schema changes need coordinated updates.
- Interview finalization must always resolve into a storage-compatible profile object.
- Onboarding and settings changes usually require matching route-test updates.

## Validation

- `uv run pytest tests/profile/ tests/web/test_onboarding_routes.py tests/web/test_profile_routes.py tests/services/test_profile_service.py -q`
