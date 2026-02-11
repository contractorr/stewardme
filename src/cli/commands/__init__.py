"""CLI command modules."""

from .advisor import ask, goals, opportunities, review
from .daemon import daemon
from .init import init
from .intelligence import brief, intel_export, scrape, sources
from .journal import journal
from .recommend import recommend
from .research import research
from .trends import trends

__all__ = [
    "journal",
    "ask",
    "review",
    "opportunities",
    "goals",
    "scrape",
    "brief",
    "sources",
    "intel_export",
    "daemon",
    "research",
    "recommend",
    "init",
    "trends",
]
