"""Structured graceful degradation: log + count instead of silent swallow."""

import functools
import sys
from contextlib import contextmanager

import structlog

from observability import metrics


def _log_and_count(metric: str, log_level: str, qualname: str | None = None) -> None:
    """Log the caught exception and increment the metric counter. Never raises."""
    try:
        kw: dict = {"metric": metric}
        if qualname:
            kw["qualname"] = qualname
        getattr(structlog.get_logger(), log_level)("graceful.caught", exc_info=True, **kw)
        metrics.counter(metric)
        # Record for request-scoped UI degradation reporting
        try:
            from degradation_collector import record_degradation

            record_degradation(metric)
        except Exception:
            pass
    except Exception:
        try:
            print(f"graceful: {metric} logging failed", file=sys.stderr)
        except Exception:
            pass


def graceful(
    metric: str, *, fallback=None, log_level: str = "warning", exc_types: tuple = (Exception,)
):
    """Decorator: catch *exc_types*, log, count, return *fallback*."""

    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except exc_types:
                _log_and_count(metric, log_level, qualname=fn.__qualname__)
                return fallback

        return wrapper

    return decorator


@contextmanager
def graceful_context(metric: str, *, log_level: str = "warning", exc_types: tuple = (Exception,)):
    """Context manager: catch *exc_types*, log, count, continue."""
    try:
        yield
    except exc_types:
        _log_and_count(metric, log_level)
