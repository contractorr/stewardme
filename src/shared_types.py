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


class CareerStage(StrEnum):
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    EXEC = "exec"


class IntelSource(StrEnum):
    HACKERNEWS = "hackernews"
    REDDIT = "reddit"
    RSS = "rss"
    GITHUB_TRENDING = "github_trending"
    ARXIV = "arxiv"
    EVENTS = "events"
    CONFS_TECH = "confs_tech"
    GITHUB_ISSUES = "github_issues"


class EntryType(StrEnum):
    DAILY = "daily"
    PROJECT = "project"
    GOAL = "goal"
    REFLECTION = "reflection"
    INSIGHT = "insight"
    NOTE = "note"
    QUICK = "quick"
    RESEARCH = "research"
    ACTION_BRIEF = "action_brief"
