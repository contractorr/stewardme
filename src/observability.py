"""Observability: metrics collection and run summary logging."""

import time
from contextlib import contextmanager
from typing import Any

import structlog

logger = structlog.get_logger().bind(source="observability")


class Metrics:
    """Simple dict-based metrics collector for counters and timers."""

    def __init__(self):
        self._counters: dict[str, int] = {}
        self._timers: dict[str, list[float]] = {}

    def counter(self, name: str, value: int = 1):
        """Increment a counter by the given value."""
        self._counters[name] = self._counters.get(name, 0) + value

    @contextmanager
    def timer(self, name: str):
        """Context manager to time an operation and store duration."""
        start = time.time()
        try:
            yield
        finally:
            duration = time.time() - start
            if name not in self._timers:
                self._timers[name] = []
            self._timers[name].append(duration)

    def summary(self) -> dict[str, Any]:
        """Return a summary of all collected metrics."""
        timer_summary = {}
        for name, durations in self._timers.items():
            if durations:
                timer_summary[name] = {
                    "count": len(durations),
                    "total": sum(durations),
                    "avg": sum(durations) / len(durations),
                    "min": min(durations),
                    "max": max(durations),
                }
            else:
                timer_summary[name] = {"count": 0}

        return {
            "counters": dict(self._counters),
            "timers": timer_summary,
        }

    def reset(self):
        """Clear all metrics."""
        self._counters.clear()
        self._timers.clear()


# Module-level singleton
metrics = Metrics()


def log_run_summary():
    """Log the current metrics summary via structlog."""
    summary = metrics.summary()
    logger.info("run_summary", **summary)
