"""Pydantic models for the notes package."""

from datetime import datetime

from pydantic import BaseModel, Field

CORRECTION_TYPES = {"spelling", "grammar", "factual", "rewording", "removal"}


class Note(BaseModel):
    id: str = ""
    user_id: str = ""
    title: str = ""
    status: str = "pending"  # 'pending' | 'accepted'
    original_text: str | None = None
    polished_markdown: str = ""
    polished_html: str = ""
    diff: str = ""
    corrections: list[dict] = Field(default_factory=list)
    created_at: datetime | None = None
    accepted_at: datetime | None = None
