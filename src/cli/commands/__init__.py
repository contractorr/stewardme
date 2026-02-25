"""CLI command modules."""

from .advisor import ask, goals, opportunities, review
from .capabilities import capabilities
from .daemon import daemon
from .database import db
from .export import export
from .init import init
from .intelligence import brief, intel_export, scrape, sources
from .journal import journal
from .learn import learn
from .profile import profile
from .projects import projects
from .recommend import recommend
from .reflect import reflect
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
    "db",
    "research",
    "recommend",
    "init",
    "trends",
    "reflect",
    "export",
    "profile",
    "learn",
    "projects",
    "capabilities",
]
