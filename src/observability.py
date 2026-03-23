"""Observability: metrics collection and run summary logging."""

import re
import threading
import time
from contextlib import contextmanager
from typing import Any

import structlog

logger = structlog.get_logger().bind(source="observability")


class Metrics:
    """Simple dict-based metrics collector for counters and timers."""

    _PRICING_PER_MILLION = (
        ("gpt-4o-mini", 0.15, 0.60),
        ("gpt-4o", 2.50, 10.00),
        ("haiku", 0.25, 1.25),
        ("sonnet", 3.00, 15.00),
        ("opus", 15.00, 75.00),
        ("gemini", 0.00, 0.00),
    )

    def __init__(self):
        self._lock = threading.Lock()
        self._counters: dict[str, int] = {}
        self._timers: dict[str, list[float]] = {}
        self._tokens: dict[str, dict[str, float]] = {}

    def counter(self, name: str, value: int = 1):
        """Increment a counter by the given value."""
        with self._lock:
            self._counters[name] = self._counters.get(name, 0) + value

    @contextmanager
    def timer(self, name: str):
        """Context manager to time an operation and store duration."""
        start = time.time()
        try:
            yield
        finally:
            duration = time.time() - start
            with self._lock:
                if name not in self._timers:
                    self._timers[name] = []
                self._timers[name].append(duration)

    def token_usage(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        *,
        cache_creation_input_tokens: int = 0,
        cache_read_input_tokens: int = 0,
        billed_input_tokens: float | None = None,
    ) -> None:
        """Track per-model token usage and billed-token adjustments."""
        normalized_model = (model or "unknown").strip() or "unknown"
        effective_billed_input = (
            float(billed_input_tokens)
            if billed_input_tokens is not None
            else float(input_tokens + cache_creation_input_tokens)
        )
        with self._lock:
            entry = self._tokens.setdefault(
                normalized_model,
                {
                    "input_tokens": 0.0,
                    "output_tokens": 0.0,
                    "cache_creation_input_tokens": 0.0,
                    "cache_read_input_tokens": 0.0,
                    "billed_input_tokens": 0.0,
                },
            )
            entry["input_tokens"] += input_tokens
            entry["output_tokens"] += output_tokens
            entry["cache_creation_input_tokens"] += cache_creation_input_tokens
            entry["cache_read_input_tokens"] += cache_read_input_tokens
            entry["billed_input_tokens"] += effective_billed_input

    def _get_pricing(self, model: str) -> tuple[float, float, bool]:
        lower_model = model.lower()
        for pattern, input_rate, output_rate in self._PRICING_PER_MILLION:
            if pattern in lower_model:
                return input_rate, output_rate, True
        return 0.0, 0.0, False

    def summary(self) -> dict[str, Any]:
        """Return a summary of all collected metrics."""
        with self._lock:
            counters = dict(self._counters)
            timers = {name: list(durations) for name, durations in self._timers.items()}
            tokens = {name: dict(values) for name, values in self._tokens.items()}

        timer_summary = {}
        for name, durations in timers.items():
            if durations:
                sorted_d = sorted(durations)
                timer_summary[name] = {
                    "count": len(sorted_d),
                    "total": sum(sorted_d),
                    "avg": sum(sorted_d) / len(sorted_d),
                    "min": sorted_d[0],
                    "max": sorted_d[-1],
                    "p50": sorted_d[int(len(sorted_d) * 0.5)],
                    "p95": sorted_d[min(int(len(sorted_d) * 0.95), len(sorted_d) - 1)],
                    "p99": sorted_d[min(int(len(sorted_d) * 0.99), len(sorted_d) - 1)],
                }
            else:
                timer_summary[name] = {"count": 0}

        token_summary = {}
        for model, usage in tokens.items():
            input_rate, output_rate, has_pricing = self._get_pricing(model)
            estimated_cost = (usage["billed_input_tokens"] / 1_000_000.0) * input_rate + (
                usage["output_tokens"] / 1_000_000.0
            ) * output_rate
            token_summary[model] = {
                "input_tokens": int(usage["input_tokens"]),
                "output_tokens": int(usage["output_tokens"]),
                "cache_creation_input_tokens": int(usage["cache_creation_input_tokens"]),
                "cache_read_input_tokens": int(usage["cache_read_input_tokens"]),
                "billed_input_tokens": round(usage["billed_input_tokens"], 2),
                "estimated_cost_usd": round(estimated_cost, 6),
                "has_pricing": has_pricing,
            }

        return {
            "counters": counters,
            "timers": timer_summary,
            "token_usage": token_summary,
        }

    def reset(self):
        """Clear all metrics."""
        with self._lock:
            self._counters.clear()
            self._timers.clear()
            self._tokens.clear()

    @staticmethod
    def _sanitize_name(name: str) -> str:
        """Sanitize a metric name for Prometheus (alphanum + underscores)."""
        return re.sub(r"[^a-zA-Z0-9_]", "_", name)

    def prometheus_text(self) -> str:
        """Return metrics in Prometheus exposition format."""
        s = self.summary()
        lines: list[str] = []

        for name, value in s["counters"].items():
            safe = self._sanitize_name(name)
            lines.append(f"# TYPE coach_{safe} counter")
            lines.append(f"coach_{safe} {value}")

        for name, data in s["timers"].items():
            safe = self._sanitize_name(name)
            if data.get("count", 0) == 0:
                continue
            lines.append(f"# TYPE coach_{safe} summary")
            for q in ("0.5", "0.95", "0.99"):
                pkey = {"0.5": "p50", "0.95": "p95", "0.99": "p99"}[q]
                lines.append(f'coach_{safe}{{quantile="{q}"}} {data[pkey]:.6f}')
            lines.append(f"coach_{safe}_count {data['count']}")
            lines.append(f"coach_{safe}_sum {data['total']:.6f}")

        for model, usage in s["token_usage"].items():
            safe_model = self._sanitize_name(model)
            lines.append(f"# TYPE coach_token_{safe_model}_input gauge")
            lines.append(f"coach_token_{safe_model}_input {usage['input_tokens']}")
            lines.append(f"# TYPE coach_token_{safe_model}_output gauge")
            lines.append(f"coach_token_{safe_model}_output {usage['output_tokens']}")

        return "\n".join(lines) + "\n" if lines else ""


# Module-level singleton
metrics = Metrics()


def compute_cost(model: str, billed_input: float, output_tokens: int) -> float:
    """Estimate USD cost for a single request given token counts."""
    input_rate, output_rate, _ = metrics._get_pricing(model)
    return round(
        (billed_input / 1_000_000) * input_rate + (output_tokens / 1_000_000) * output_rate, 8
    )


def log_run_summary():
    """Log the current metrics summary via structlog."""
    summary = metrics.summary()
    logger.info("run_summary", **summary)
