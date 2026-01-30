"""Deep research module for topic discovery and web research."""

from .topics import TopicSelector
from .web_search import WebSearchClient
from .synthesis import ResearchSynthesizer
from .agent import DeepResearchAgent

__all__ = [
    "TopicSelector",
    "WebSearchClient",
    "ResearchSynthesizer",
    "DeepResearchAgent",
]
