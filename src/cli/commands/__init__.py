"""CLI command modules."""

from .journal import journal
from .advisor import ask, review, opportunities, goals
from .intelligence import scrape, brief, sources, intel_export
from .daemon import daemon
from .research import research
from .recommend import recommend
from .init import init
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
