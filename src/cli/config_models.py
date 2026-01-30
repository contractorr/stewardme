"""Pydantic configuration models for AI Coach."""

import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class LLMConfig(BaseModel):
    """LLM provider configuration."""
    provider: str = "claude"
    model: str = "claude-sonnet-4-20250514"
    api_key: Optional[str] = None


class PathsConfig(BaseModel):
    """File paths configuration."""
    journal_dir: Path = Path("~/coach/journal")
    chroma_dir: Path = Path("~/coach/chroma")
    intel_db: Path = Path("~/coach/intel.db")
    log_file: Path = Path("~/coach/coach.log")

    @model_validator(mode="after")
    def expand_paths(self):
        """Expand ~ in all paths."""
        self.journal_dir = self.journal_dir.expanduser()
        self.chroma_dir = self.chroma_dir.expanduser()
        self.intel_db = self.intel_db.expanduser()
        self.log_file = self.log_file.expanduser()
        return self


class SourcesConfig(BaseModel):
    """Intelligence sources configuration."""
    custom_blogs: list[str] = Field(default_factory=list)
    rss_feeds: list[str] = Field(default_factory=lambda: ["https://news.ycombinator.com/rss"])
    enabled: list[str] = Field(default_factory=lambda: ["hn_top", "rss_feeds"])
    github_trending: dict = Field(default_factory=dict)


class ResearchConfig(BaseModel):
    """Deep research configuration."""
    enabled: bool = False
    max_topics: int = 3
    tavily_api_key: Optional[str] = None
    schedule: str = "0 21 * * 0"


class ScoringConfig(BaseModel):
    """Recommendation scoring configuration."""
    min_threshold: float = 6.0
    max_per_category: int = 3
    weights: dict = Field(default_factory=lambda: {
        "relevance": 0.3,
        "urgency": 0.25,
        "feasibility": 0.25,
        "impact": 0.2,
    })


class DeliveryConfig(BaseModel):
    """Recommendation delivery configuration."""
    methods: list[str] = Field(default_factory=lambda: ["journal"])
    schedule: str = "0 8 * * 0"


class RecommendationsConfig(BaseModel):
    """Recommendations system configuration."""
    enabled: bool = False
    scoring: ScoringConfig = Field(default_factory=ScoringConfig)
    delivery: DeliveryConfig = Field(default_factory=DeliveryConfig)


class RetryConfig(BaseModel):
    """Retry/backoff configuration."""
    max_attempts: int = 3
    min_wait: float = 2.0
    max_wait: float = 10.0
    llm_max_wait: float = 30.0


class LimitsConfig(BaseModel):
    """Resource limits configuration."""
    hn_max_stories: int = 30
    rss_max_entries: int = 20
    github_max_repos: int = 25
    journal_max_entries: int = 5
    journal_max_chars: int = 6000
    intel_max_items: int = 5
    intel_max_chars: int = 3000
    total_context_chars: int = 8000
    summary_truncate: int = 500
    preview_truncate: int = 200
    llm_max_tokens: int = 2000


class LoggingConfig(BaseModel):
    """Logging configuration."""
    level: str = "INFO"
    file_level: str = "DEBUG"


class CoachConfig(BaseModel):
    """Main configuration model."""
    llm: LLMConfig = Field(default_factory=LLMConfig)
    paths: PathsConfig = Field(default_factory=PathsConfig)
    sources: SourcesConfig = Field(default_factory=SourcesConfig)
    research: ResearchConfig = Field(default_factory=ResearchConfig)
    recommendations: RecommendationsConfig = Field(default_factory=RecommendationsConfig)
    retry: RetryConfig = Field(default_factory=RetryConfig)
    limits: LimitsConfig = Field(default_factory=LimitsConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)

    @model_validator(mode="after")
    def expand_env_vars(self):
        """Expand ${VAR} patterns in API keys."""
        if self.llm.api_key:
            key = self.llm.api_key
            if key.startswith("${") and key.endswith("}"):
                env_var = key[2:-1]
                self.llm.api_key = os.getenv(env_var, "")
        if self.research.tavily_api_key:
            key = self.research.tavily_api_key
            if key.startswith("${") and key.endswith("}"):
                env_var = key[2:-1]
                self.research.tavily_api_key = os.getenv(env_var, "")
        return self

    @classmethod
    def from_dict(cls, data: dict) -> "CoachConfig":
        """Create config from dict, migrating old format if needed."""
        # Handle old paths format (strings instead of Path objects)
        if "paths" in data:
            for key in ["journal_dir", "chroma_dir", "intel_db", "log_file"]:
                if key in data["paths"] and isinstance(data["paths"][key], str):
                    data["paths"][key] = Path(data["paths"][key])

        # Handle old limits format (flat dict at root)
        if "limits" in data and isinstance(data["limits"], dict):
            # Merge with defaults
            pass

        return cls.model_validate(data)

    def to_dict(self) -> dict:
        """Convert to dict for backwards compatibility."""
        return self.model_dump(mode="python")
