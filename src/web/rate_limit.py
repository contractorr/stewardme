"""Per-user rate limiting for the web backend.

Two layers, both in-memory sliding windows (reset on deploy, acceptable for
single-worker):

1. Shared-key ("lite mode") limits — daily budget + burst interval for users
   on the shared API key.
2. Per-user route limits applied to ALL users: a strict bucket for routes
   that trigger paid LLM calls and a general bucket for the rest of the API,
   configurable via ``web.rate_limit`` in config.yaml.

Periodic pruning prevents unbounded memory growth from abandoned users.
"""

import hashlib
import time
from collections import defaultdict

from fastapi import Depends, HTTPException, Request

from web.auth import get_current_user

# 30 queries per rolling 24h window
DAILY_LIMIT = 30
WINDOW_SECONDS = 86400  # 24h

# Burst: 1 request per 10 seconds
BURST_INTERVAL = 10.0

# Onboarding gets a separate, more generous budget so users can finish
# the profile interview without exhausting their daily allowance.
ONBOARDING_BURST_INTERVAL = 3.0
ONBOARDING_LIMIT = 20  # max turns in one onboarding session

# Pruning: evict stale entries every N checks, cap total tracked users
_PRUNE_EVERY = 500  # calls between full prune sweeps
_MAX_TRACKED_USERS = 10_000  # hard cap on tracked user IDs

# user_id -> list of timestamps
_request_log: dict[str, list[float]] = defaultdict(list)
_onboarding_log: dict[str, list[float]] = defaultdict(list)
_call_counter = 0


def _prune(user_id: str, now: float) -> list[float]:
    """Remove timestamps older than the window for a single user."""
    cutoff = now - WINDOW_SECONDS
    log = [t for t in _request_log[user_id] if t > cutoff]
    _request_log[user_id] = log
    return log


def _periodic_prune(now: float) -> None:
    """Sweep all logs and evict users with no recent activity."""
    global _call_counter
    _call_counter += 1
    if _call_counter < _PRUNE_EVERY:
        return
    _call_counter = 0

    cutoff = now - WINDOW_SECONDS
    onboard_cutoff = now - 3600

    stale = [uid for uid, ts in _request_log.items() if not ts or ts[-1] <= cutoff]
    for uid in stale:
        del _request_log[uid]

    stale_ob = [uid for uid, ts in _onboarding_log.items() if not ts or ts[-1] <= onboard_cutoff]
    for uid in stale_ob:
        del _onboarding_log[uid]

    # Hard cap: if still over limit, drop oldest-activity users
    if len(_request_log) > _MAX_TRACKED_USERS:
        by_age = sorted(_request_log.items(), key=lambda kv: kv[1][-1] if kv[1] else 0)
        for uid, _ in by_age[: len(_request_log) - _MAX_TRACKED_USERS]:
            del _request_log[uid]


def check_shared_key_rate_limit(user_id: str, *, onboarding: bool = False) -> None:
    """Raise 429 if shared-key user exceeds limits.

    Onboarding calls use a separate budget so the profile interview
    never competes with regular usage.
    """
    now = time.time()
    _periodic_prune(now)

    if onboarding:
        _check_onboarding_limit(user_id, now)
        return

    log = _prune(user_id, now)

    # Burst check
    if log and (now - log[-1]) < BURST_INTERVAL:
        retry_after = int(BURST_INTERVAL - (now - log[-1])) + 1
        raise HTTPException(
            status_code=429,
            detail="Lite mode limit reached — add your own API key in Settings for unlimited access",
            headers={"Retry-After": str(retry_after)},
        )

    # Daily limit check
    if len(log) >= DAILY_LIMIT:
        oldest = log[0]
        retry_after = int(oldest + WINDOW_SECONDS - now) + 1
        raise HTTPException(
            status_code=429,
            detail="Lite mode limit reached — add your own API key in Settings for unlimited access",
            headers={"Retry-After": str(retry_after)},
        )

    # Record request
    _request_log[user_id].append(now)


def _check_onboarding_limit(user_id: str, now: float) -> None:
    """Separate rate limit for onboarding — generous burst, capped per session."""
    cutoff = now - 3600  # 1h window for onboarding
    log = [t for t in _onboarding_log[user_id] if t > cutoff]
    _onboarding_log[user_id] = log

    if log and (now - log[-1]) < ONBOARDING_BURST_INTERVAL:
        retry_after = int(ONBOARDING_BURST_INTERVAL - (now - log[-1])) + 1
        raise HTTPException(
            status_code=429,
            detail="Please wait a moment before sending the next message",
            headers={"Retry-After": str(retry_after)},
        )

    if len(log) >= ONBOARDING_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Onboarding session limit reached — please try again later or add your own API key in Settings",
            headers={"Retry-After": "60"},
        )

    _onboarding_log[user_id].append(now)


# --- Per-user route limits (all users, not just shared-key) ---------------

DEFAULT_LLM_PER_MINUTE = 20
DEFAULT_GENERAL_PER_MINUTE = 120
ROUTE_WINDOW_SECONDS = 60.0

# (key, bucket) -> list of timestamps
_route_log: dict[tuple[str, str], list[float]] = defaultdict(list)
# (enabled, llm_per_minute, general_per_minute), cached after first read
_route_limit_cache: tuple[bool, int, int] | None = None


def _route_limit_settings() -> tuple[bool, int, int]:
    """Read web.rate_limit config once; fall back to defaults on any error."""
    global _route_limit_cache
    if _route_limit_cache is None:
        try:
            from web.deps_base import get_config

            cfg = get_config().web.rate_limit
            _route_limit_cache = (cfg.enabled, cfg.llm_per_minute, cfg.general_per_minute)
        except Exception:
            _route_limit_cache = (True, DEFAULT_LLM_PER_MINUTE, DEFAULT_GENERAL_PER_MINUTE)
    return _route_limit_cache


def _check_window(key: tuple[str, str], limit: int, now: float) -> int | None:
    """Sliding-window check. Returns Retry-After seconds when limited."""
    cutoff = now - ROUTE_WINDOW_SECONDS
    log = [t for t in _route_log[key] if t > cutoff]
    if len(log) >= limit:
        _route_log[key] = log
        return int(log[0] + ROUTE_WINDOW_SECONDS - now) + 1
    log.append(now)
    _route_log[key] = log
    return None


def check_route_rate_limit(user_id: str, bucket: str = "llm") -> None:
    """Raise 429 when a user exceeds the per-route limit for a bucket.

    Applies to every user regardless of key source — LLM routes are metered
    spend even with a personal key, and unmetered routes are still abusable.
    """
    enabled, llm_limit, general_limit = _route_limit_settings()
    if not enabled:
        return
    limit = llm_limit if bucket == "llm" else general_limit
    retry_after = _check_window((user_id, bucket), limit, time.time())
    if retry_after is not None:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded — try again shortly",
            headers={"Retry-After": str(retry_after)},
        )


async def enforce_llm_rate_limit(user: dict = Depends(get_current_user)) -> None:
    """Dependency: strict per-user limit for routes that trigger LLM calls."""
    check_route_rate_limit(user["id"], "llm")


def general_request_retry_after(request: Request) -> int | None:
    """Middleware helper: general API limit keyed on auth header (or IP).

    Returns Retry-After seconds when the request should be rejected, None
    otherwise. Uses the raw Authorization header hash so limiting happens
    before (and independent of) JWT validation.
    """
    enabled, _llm_limit, general_limit = _route_limit_settings()
    if not enabled:
        return None
    auth = request.headers.get("authorization")
    if auth:
        key = hashlib.sha256(auth.encode()).hexdigest()[:32]
    else:
        key = request.client.host if request.client else "unknown"
    return _check_window((key, "general"), general_limit, time.time())


def reset_rate_limits() -> None:
    """Clear all rate limit state. Used in tests."""
    global _call_counter, _route_limit_cache
    _request_log.clear()
    _onboarding_log.clear()
    _route_log.clear()
    _route_limit_cache = None
    _call_counter = 0
