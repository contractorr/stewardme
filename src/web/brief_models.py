"""Pydantic models for the configurable brief feature."""

from pydantic import BaseModel, Field


class BriefCustomSection(BaseModel):
    """A user-authored standing instruction the brief always honors."""

    id: str = ""
    title: str = ""
    instructions: str = ""
    use_research: bool = False


class BriefConfig(BaseModel):
    """Per-user brief configuration."""

    enabled: bool = True
    min_interval_hours: int = Field(12, ge=1, le=168)
    include_signals: bool = True
    include_journal: bool = True
    include_calendar: bool = True
    include_email: bool = True
    max_items_per_section: int = Field(8, ge=3, le=20)
    custom_sections: list[BriefCustomSection] = []


class BriefResponse(BaseModel):
    id: str
    status: str
    summary: str = ""
    period_start: str
    period_end: str
    created_at: str
    sections: list[dict] = []


class BriefLatestResponse(BaseModel):
    brief: BriefResponse | None = None
    should_generate: bool = False
