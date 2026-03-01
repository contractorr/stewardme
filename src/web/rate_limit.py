"""Per-user rate limiting for shared-key (lite mode) users.

In-memory sliding window — resets on deploy. Acceptable for now.
"""

import time
from collections import defaultdict

from fastapi import HTTPException

# 30 queries per rolling 24h window
DAILY_LIMIT = 30
WINDOW_SECONDS = 86400  # 24h

# Burst: 1 request per 10 seconds
BURST_INTERVAL = 10.0

# user_id -> list of timestamps
_request_log: dict[str, list[float]] = defaultdict(list)


def _prune(user_id: str, now: float) -> list[float]:
    """Remove timestamps older than the window."""
    cutoff = now - WINDOW_SECONDS
    log = [t for t in _request_log[user_id] if t > cutoff]
    _request_log[user_id] = log
    return log


def check_shared_key_rate_limit(user_id: str) -> None:
    """Raise 429 if shared-key user exceeds limits."""
    now = time.time()
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


def reset_rate_limits() -> None:
    """Clear all rate limit state. Used in tests."""
    _request_log.clear()
