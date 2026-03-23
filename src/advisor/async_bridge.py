"""Async-to-sync bridge for running coroutines from sync contexts."""

from __future__ import annotations

import asyncio
import threading


def run_async(coro):
    """Run an async coroutine from synchronous code.

    If no event loop is running, uses asyncio.run().
    If an event loop is already running (e.g. inside FastAPI),
    spawns a new thread with its own loop.
    """
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    result = {}
    error = {}

    def runner():
        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)
            result["value"] = loop.run_until_complete(coro)
        except Exception as exc:
            error["value"] = exc
        finally:
            loop.close()

    thread = threading.Thread(target=runner)
    thread.start()
    thread.join(timeout=30)
    if thread.is_alive():
        raise TimeoutError("Async operation timed out")
    if "value" in error:
        raise error["value"]
    return result["value"]
