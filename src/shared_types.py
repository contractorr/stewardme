"""Shared enums and types for ai-coach."""

from enum import StrEnum


class GoalStatus(StrEnum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class RecommendationStatus(StrEnum):
    SUGGESTED = "suggested"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DISMISSED = "dismissed"


class IntelSource(StrEnum):
    HACKERNEWS = "hackernews"
    REDDIT = "reddit"
    RSS = "rss"
    GITHUB_TRENDING = "github_trending"
    ARXIV = "arxiv"
    DEVTO = "devto"
    CRUNCHBASE = "crunchbase"
    NEWSAPI = "newsapi"


class EntryType(StrEnum):
    DAILY = "daily"
    PROJECT = "project"
    GOAL = "goal"
    REFLECTION = "reflection"
    INSIGHT = "insight"
    NOTE = "note"
    RESEARCH = "research"
    ACTION_BRIEF = "action_brief"
