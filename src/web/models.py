"""Pydantic request/response schemas for the web API."""

from typing import Optional

from pydantic import BaseModel, Field

# --- Settings ---


class SettingsUpdate(BaseModel):
    """Update user settings / API keys."""

    llm_provider: Optional[str] = None
    llm_model: Optional[str] = None
    llm_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None
    github_token: Optional[str] = None
    eventbrite_token: Optional[str] = None
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_user: Optional[str] = None
    smtp_pass: Optional[str] = None
    smtp_to: Optional[str] = None


class SettingsResponse(BaseModel):
    """Settings with bool mask for secrets (never raw keys)."""

    llm_provider: Optional[str] = None
    llm_model: Optional[str] = None
    llm_api_key_set: bool = False
    llm_api_key_hint: Optional[str] = None
    tavily_api_key_set: bool = False
    tavily_api_key_hint: Optional[str] = None
    github_token_set: bool = False
    github_token_hint: Optional[str] = None
    eventbrite_token_set: bool = False
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_user: Optional[str] = None
    smtp_pass_set: bool = False
    smtp_to: Optional[str] = None


# --- Journal ---


class JournalCreate(BaseModel):
    content: str = Field(..., max_length=100_000)
    entry_type: str = "daily"
    title: Optional[str] = None
    tags: Optional[list[str]] = None


class JournalUpdate(BaseModel):
    content: Optional[str] = Field(None, max_length=100_000)
    metadata: Optional[dict] = None


class JournalEntry(BaseModel):
    path: str
    title: str
    type: str
    created: Optional[str] = None
    tags: list[str] = []
    preview: str = ""
    content: Optional[str] = None


# --- Advisor ---


class AdvisorAsk(BaseModel):
    question: str = Field(..., max_length=5000)
    advice_type: str = "general"
    conversation_id: str | None = None


class AdvisorResponse(BaseModel):
    answer: str
    advice_type: str
    conversation_id: str


class ConversationMessage(BaseModel):
    role: str
    content: str
    created_at: str


class ConversationListItem(BaseModel):
    id: str
    title: str
    updated_at: str
    message_count: int


class ConversationDetail(BaseModel):
    id: str
    title: str
    messages: list[ConversationMessage]


# --- Goals ---


class GoalCreate(BaseModel):
    title: str = Field(..., max_length=200)
    content: str = Field("", max_length=10_000)
    tags: Optional[list[str]] = None


class GoalCheckIn(BaseModel):
    notes: Optional[str] = Field(None, max_length=5000)


class GoalStatusUpdate(BaseModel):
    status: str  # active, paused, completed, abandoned


class MilestoneAdd(BaseModel):
    title: str = Field(..., max_length=200)


class MilestoneComplete(BaseModel):
    milestone_index: int


# --- Intel ---


class IntelItem(BaseModel):
    source: str
    title: str
    url: str
    summary: str
    published: Optional[str] = None
    tags: list[str] = []


# --- Research ---


class ResearchRun(BaseModel):
    topic: Optional[str] = None


class ResearchTopic(BaseModel):
    topic: str
    source: str
    score: float
    reason: str


# --- Onboarding ---


class OnboardingChat(BaseModel):
    message: str = Field(..., max_length=5000)


class OnboardingResponse(BaseModel):
    message: str
    done: bool = False
    goals_created: int = 0
