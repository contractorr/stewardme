"""Tests for token bucket rate limiter."""

import asyncio
import time

import pytest

from cli.rate_limit import TokenBucketRateLimiter


class TestTokenBucketRateLimiter:
    """Test token bucket behavior."""

    def test_initial_burst(self):
        """Burst tokens available immediately."""
        limiter = TokenBucketRateLimiter(requests_per_second=1.0, burst=3)
        # Should be able to acquire 3 immediately
        for _ in range(3):
            limiter.acquire_sync()
        assert limiter.available_tokens < 1.0

    def test_rate_enforcement(self):
        """Rate is enforced after burst exhausted."""
        limiter = TokenBucketRateLimiter(requests_per_second=10.0, burst=1)
        limiter.acquire_sync()  # Use burst
        start = time.monotonic()
        limiter.acquire_sync()  # Should wait ~0.1s
        elapsed = time.monotonic() - start
        assert elapsed >= 0.05  # At least some wait

    @pytest.mark.asyncio
    async def test_async_acquire(self):
        """Async acquire works."""
        limiter = TokenBucketRateLimiter(requests_per_second=10.0, burst=5)
        for _ in range(5):
            await limiter.acquire()
        assert limiter.available_tokens < 1.0

    @pytest.mark.asyncio
    async def test_concurrent_access(self):
        """Multiple coroutines can use limiter safely."""
        limiter = TokenBucketRateLimiter(requests_per_second=100.0, burst=10)
        results = []

        async def worker(i):
            await limiter.acquire()
            results.append(i)

        await asyncio.gather(*[worker(i) for i in range(10)])
        assert len(results) == 10

    def test_token_refill(self):
        """Tokens refill over time."""
        limiter = TokenBucketRateLimiter(requests_per_second=100.0, burst=5)
        # Exhaust tokens
        for _ in range(5):
            limiter.acquire_sync()
        # Wait for refill
        time.sleep(0.05)
        assert limiter.available_tokens >= 1.0

    def test_custom_config(self):
        """Custom rates work."""
        limiter = TokenBucketRateLimiter(requests_per_second=0.5, burst=2)
        assert limiter.rate == 0.5
        assert limiter.max_tokens == 2
