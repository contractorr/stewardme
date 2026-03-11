"""Helpers for running coroutine-based internals from sync MCP tool handlers."""

from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import TypeVar

T = TypeVar("T")


def run_coro_sync(awaitable) -> T:
    """Run a coroutine from sync code even when the current thread already has a running loop."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(awaitable)

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(asyncio.run, awaitable)
        return future.result()
