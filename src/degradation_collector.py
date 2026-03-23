"""Request-scoped degradation collector using ContextVar."""

from contextvars import ContextVar

_collector: ContextVar[list[dict] | None] = ContextVar("degradation_collector", default=None)

# Metric → user-friendly message mapping
_MESSAGES: dict[str, str] = {
    "graceful.advisor.cache_init": "Context cache unavailable",
    "graceful.advisor.rag_retrieval": "Some context retrieval failed",
    "graceful.advisor.memory_inject": "Memory context unavailable",
    "graceful.advisor.thread_inject": "Thread context unavailable",
    "graceful.advisor.entity_init": "Entity graph unavailable",
    "graceful.intel.scrape": "Some intelligence sources failed",
    "graceful.journal.embeddings": "Journal search partially degraded",
    "graceful.profile.load": "Profile data unavailable",
    "graceful.curriculum.store": "Curriculum data unavailable",
}


def init_collector() -> None:
    """Initialize a fresh collector for the current context."""
    _collector.set([])


def record_degradation(component: str, message: str | None = None) -> None:
    """Record a degradation event. No-op if collector not initialized."""
    items = _collector.get(None)
    if items is None:
        return
    msg = message or _MESSAGES.get(component, "Some data sources were unavailable")
    items.append({"component": component, "message": msg})


def get_degradations() -> list[dict]:
    """Return collected degradations for the current request."""
    return _collector.get(None) or []


def clear_collector() -> None:
    """Clear the collector for the current context."""
    _collector.set(None)
