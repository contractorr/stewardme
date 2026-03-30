"""Pydantic request/response schemas for the web API."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# --- Settings ---


class CustomProviderCreate(BaseModel):
    display_name: str = Field(..., min_length=1, max_length=100)
    base_url: str = Field(..., min_length=1, max_length=500)
    api_key: str = Field(..., min_length=1)
    model: str = Field(..., min_length=1, max_length=200)


class CustomProviderUpdate(BaseModel):
    id: str = Field(..., min_length=1)
    display_name: str | None = Field(None, min_length=1, max_length=100)
    base_url: str | None = Field(None, min_length=1, max_length=500)
    api_key: str | None = Field(None, min_length=1)
    model: str | None = Field(None, min_length=1, max_length=200)


class SettingsUpdate(BaseModel):
    """Update user settings / API keys."""

    llm_provider: str | None = None
    llm_model: str | None = None
    llm_council_enabled: bool | None = None
    llm_api_key: str | None = None
    llm_api_key_claude: str | None = None
    llm_api_key_openai: str | None = None
    llm_api_key_gemini: str | None = None
    llm_remove_providers: list[str] = Field(default_factory=list)
    llm_custom_provider_add: CustomProviderCreate | None = None
    llm_custom_provider_update: CustomProviderUpdate | None = None
    llm_custom_providers_remove: list[str] = Field(default_factory=list)
    tavily_api_key: str | None = None
    github_token: str | None = None
    github_pat: str | None = None
    eventbrite_token: str | None = None
    # Feature toggles
    feature_extended_thinking: bool | None = None
    feature_memory_enabled: bool | None = None
    feature_threads_enabled: bool | None = None
    feature_recommendations_enabled: bool | None = None
    feature_research_enabled: bool | None = None
    feature_entity_extraction_enabled: bool | None = None
    feature_trending_radar_enabled: bool | None = None
    feature_heartbeat_enabled: bool | None = None
    feature_company_movement_enabled: bool | None = None
    feature_hiring_signals_enabled: bool | None = None
    feature_regulatory_signals_enabled: bool | None = None
    feature_github_monitoring: bool | None = None


class LLMProviderKeyStatus(BaseModel):
    provider: str
    configured: bool = False
    hint: str | None = None
    council_eligible: bool = False


class CustomProviderInfo(BaseModel):
    id: str
    display_name: str
    base_url: str
    model: str


class SettingsResponse(BaseModel):
    """Settings with bool mask for secrets (never raw keys)."""

    llm_provider: str | None = None
    llm_model: str | None = None
    llm_council_enabled: bool = True
    llm_council_ready: bool = False
    llm_provider_keys: list[LLMProviderKeyStatus] = Field(default_factory=list)
    llm_custom_providers: list[CustomProviderInfo] = Field(default_factory=list)
    llm_api_key_set: bool = False
    llm_api_key_hint: str | None = None
    has_profile: bool = False
    using_shared_key: bool = False
    has_own_key: bool = False
    tavily_api_key_set: bool = False
    tavily_api_key_hint: str | None = None
    github_token_set: bool = False
    github_token_hint: str | None = None
    github_pat_set: bool = False
    github_pat_hint: str | None = None
    eventbrite_token_set: bool = False
    # Feature toggles (default = global config fallback)
    feature_extended_thinking: bool = True
    feature_memory_enabled: bool = True
    feature_threads_enabled: bool = True
    feature_recommendations_enabled: bool = False
    feature_research_enabled: bool = False
    feature_entity_extraction_enabled: bool = True
    feature_trending_radar_enabled: bool = True
    feature_heartbeat_enabled: bool = False
    feature_company_movement_enabled: bool = False
    feature_hiring_signals_enabled: bool = False
    feature_regulatory_signals_enabled: bool = False
    feature_github_monitoring: bool = False


# --- Usage ---


class UsageModelStats(BaseModel):
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    query_count: int = 0
    estimated_cost_usd: float = 0.0


class UsageStatsResponse(BaseModel):
    days: int = 30
    total_queries: int = 0
    total_estimated_cost_usd: float = 0.0
    by_model: list[UsageModelStats] = Field(default_factory=list)


# --- Curriculum ---


class CurriculumCausalLensResponse(BaseModel):
    drivers: list[str] = Field(default_factory=list)
    mechanism: str = ""
    effects: list[str] = Field(default_factory=list)
    second_order_effects: list[str] = Field(default_factory=list)


class CurriculumMisconceptionCardResponse(BaseModel):
    misconception: str = ""
    why_it_seems_true: str = ""
    correction: str = ""
    counterexample: str = ""


class CurriculumGuideSynthesisResponse(BaseModel):
    what_this_explains: str = ""
    where_it_applies: list[str] = Field(default_factory=list)
    where_it_breaks: str = ""


class CurriculumChapterProgressResponse(BaseModel):
    user_id: str = ""
    chapter_id: str = ""
    guide_id: str = ""
    status: str = "not_started"
    reading_time_seconds: int = 0
    scroll_position: float = 0.0
    started_at: str | None = None
    completed_at: str | None = None
    updated_at: str | None = None


class CurriculumChapterResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    guide_id: str
    title: str
    filename: str
    order: int
    summary: str = ""
    objectives: list[str] = Field(default_factory=list)
    checkpoints: list[str] = Field(default_factory=list)
    content_references: list[str] = Field(default_factory=list)
    content_format: str = "markdown"
    schema_version: int = 0
    word_count: int = 0
    reading_time_minutes: int = 0
    has_diagrams: bool = False
    has_tables: bool = False
    has_formulas: bool = False
    is_glossary: bool = False
    content_hash: str = ""
    status: str | None = None
    reading_time_seconds: int | None = None
    causal_lens: CurriculumCausalLensResponse | None = None
    misconception_card: CurriculumMisconceptionCardResponse | None = None


class CurriculumGuideResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    title: str
    summary: str = ""
    category: str = ""
    difficulty: str = ""
    source_dir: str = ""
    origin: str = ""
    kind: str = ""
    owner_user_id: str = ""
    base_guide_id: str | None = None
    chapter_count: int = 0
    total_word_count: int = 0
    total_reading_time_minutes: int = 0
    has_glossary: bool = False
    prerequisites: list[str] = Field(default_factory=list)
    track: str = ""
    enrolled: bool = False
    enrollment_completed_at: str | None = None
    chapters_total: int = 0
    chapters_completed: int = 0
    progress_pct: float = 0.0
    mastery_score: float = 0.0
    guide_synthesis: CurriculumGuideSynthesisResponse | None = None


class CurriculumGuideDetailResponse(CurriculumGuideResponse):
    chapters: list[CurriculumChapterResponse] = Field(default_factory=list)


class CurriculumChapterDetailResponse(CurriculumChapterResponse):
    content: str = ""
    progress: CurriculumChapterProgressResponse | None = None
    prev_chapter: str | None = None
    next_chapter: str | None = None


class CurriculumReviewItemResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    user_id: str = ""
    chapter_id: str = ""
    guide_id: str = ""
    question: str = ""
    expected_answer: str = ""
    bloom_level: str = "remember"
    item_type: str = "quiz"
    easiness_factor: float = 2.5
    interval_days: int = 1
    repetitions: int = 0
    next_review: str | None = None
    last_reviewed: str | None = None
    content_hash: str = ""
    created_at: str | None = None


# --- Journal ---


class QuickCapture(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)


class JournalCreate(BaseModel):
    content: str = Field(..., max_length=100_000)
    entry_type: str = "daily"
    title: str | None = None
    tags: list[str] | None = None


class JournalUpdate(BaseModel):
    content: str | None = Field(None, max_length=100_000)
    metadata: dict | None = None


class JournalEntry(BaseModel):
    path: str
    title: str
    type: str
    created: str | None = None
    tags: list[str] = []
    preview: str = ""
    content: str | None = None
    metadata: dict = {}


class JournalMindMapNode(BaseModel):
    id: str
    label: str
    kind: str
    weight: float = 0.0
    confidence: float = 0.0
    is_root: bool = False
    source_type: str | None = None
    source_label: str = ""
    source_ref: str = ""


class JournalMindMapEdge(BaseModel):
    source: str
    target: str
    label: str = ""
    strength: float = 0.0


class JournalMindMapResponse(BaseModel):
    map_id: str
    entry_path: str
    entry_title: str
    summary: str = ""
    rationale: str = ""
    generator: str = ""
    nodes: list[JournalMindMapNode] = []
    edges: list[JournalMindMapEdge] = []
    created_at: str = ""
    updated_at: str = ""


class JournalMindMapEnvelope(BaseModel):
    status: Literal["ready", "not_available", "insufficient_signal"] = "not_available"
    mind_map: JournalMindMapResponse | None = None


# --- Advisor ---


class AdvisorAsk(BaseModel):
    question: str = Field(..., max_length=5000)
    advice_type: str = "general"
    conversation_id: str | None = None
    attachment_ids: list[str] = Field(default_factory=list)


class DegradationItem(BaseModel):
    component: str
    message: str


class AdvisorResponse(BaseModel):
    answer: str
    advice_type: str
    conversation_id: str
    council_used: bool = False
    council_member_count: int = 0
    council_providers: list[str] = Field(default_factory=list)
    council_failed_providers: list[str] = Field(default_factory=list)
    council_partial: bool = False
    degradations: list[DegradationItem] = Field(default_factory=list)


class TraceListItem(BaseModel):
    session_id: str
    size_bytes: int
    created_at: float


class TraceDetail(BaseModel):
    session_id: str
    entries: list[dict] = Field(default_factory=list)
    from_line: int = 0


class ConversationAttachment(BaseModel):
    library_item_id: str
    file_name: str | None = None
    mime_type: str | None = None


class ConversationMessage(BaseModel):
    id: str | None = None
    role: str
    content: str
    created_at: str
    attachments: list[ConversationAttachment] = Field(default_factory=list)


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
    tags: list[str] | None = None


class GoalCheckIn(BaseModel):
    notes: str | None = Field(None, max_length=5000)


class GoalStatusUpdate(BaseModel):
    status: str = Field(..., pattern=r"^(active|paused|completed|abandoned)$")


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
    published: str | None = None
    tags: list[str] = []


# --- Research ---


class ResearchRun(BaseModel):
    topic: str | None = None


class ResearchTopic(BaseModel):
    topic: str
    source: str
    score: float
    reason: str


# --- Onboarding ---


class ProfileStatus(BaseModel):
    has_profile: bool = False
    is_stale: bool = False
    has_api_key: bool = False
    has_own_key: bool = False
    using_shared_key: bool = False


class OnboardingChat(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)


class OnboardingResponse(BaseModel):
    message: str
    done: bool = False
    goals_created: int = 0
    turn: int = 0
    estimated_total: int = 8


class FeedCategoryItem(BaseModel):
    id: str
    label: str
    icon: str
    feed_count: int
    preselected: bool = False


class OnboardingFeedsRequest(BaseModel):
    selected_category_ids: list[str]


class OnboardingFeedsResponse(BaseModel):
    feeds_added: int
    categories: list[str]


# --- Greeting ---


class GreetingResponse(BaseModel):
    text: str
    cached: bool = False
    stale: bool = False
    return_brief: dict | None = None
    degradations: list["DegradationItem"] = Field(default_factory=list)


# --- Briefing ---


class InsightResponse(BaseModel):
    id: int = 0
    type: str = ""
    severity: int = 0
    title: str = ""
    detail: str = ""
    suggested_actions: list[str] = []
    evidence: list[str] = []
    source_url: str = ""
    created_at: str = ""
    expires_at: str | None = None
    insight_hash: str = ""
    watchlist_evidence: list[str] = []


class ReasoningTrace(BaseModel):
    source_signal: str = ""
    profile_match: str = ""
    confidence: float = 0.5
    caveats: str = ""


class CriticData(BaseModel):
    """Adversarial critic output for a recommendation."""

    confidence: str = "Medium"  # High / Medium / Low
    confidence_rationale: str = ""
    critic_challenge: str = ""
    missing_context: str = ""
    alternative: str | None = None
    intel_contradictions: str | None = None


class BriefingRecommendation(BaseModel):
    id: str = ""
    category: str = ""
    title: str = ""
    description: str = ""
    score: float = 0.0
    status: str = ""
    reasoning_trace: ReasoningTrace | None = None
    critic: CriticData | None = None
    watchlist_evidence: list[str] = []
    action_item: "RecommendationActionItem | None" = None
    user_rating: int | None = Field(None, ge=1, le=5)
    feedback_comment: str | None = None
    feedback_at: str | None = None
    why_now: list[dict] = []
    harvested_outcome: dict | None = None


class RecommendationActionItem(BaseModel):
    objective: str = ""
    next_step: str = ""
    effort: str = Field("medium", pattern=r"^(small|medium|large)$")
    due_window: str = Field("this_week", pattern=r"^(today|this_week|later)$")
    blockers: list[str] = Field(default_factory=list)
    success_criteria: str = ""
    status: str = Field("accepted", pattern=r"^(accepted|deferred|blocked|completed|abandoned)$")
    review_notes: str | None = None
    goal_path: str | None = None
    goal_title: str | None = None
    created_at: str = ""
    updated_at: str = ""


class RecommendationActionCreate(BaseModel):
    goal_path: str | None = None
    objective: str | None = Field(None, max_length=200)
    next_step: str | None = Field(None, max_length=500)
    effort: str | None = Field(None, pattern=r"^(small|medium|large)$")
    due_window: str | None = Field(None, pattern=r"^(today|this_week|later)$")
    blockers: list[str] | None = None
    success_criteria: str | None = Field(None, max_length=500)


class RecommendationActionUpdate(BaseModel):
    status: str | None = Field(None, pattern=r"^(accepted|deferred|blocked|completed|abandoned)$")
    effort: str | None = Field(None, pattern=r"^(small|medium|large)$")
    due_window: str | None = Field(None, pattern=r"^(today|this_week|later)$")
    blockers: list[str] | None = None
    review_notes: str | None = Field(None, max_length=5000)
    next_step: str | None = Field(None, max_length=500)
    success_criteria: str | None = Field(None, max_length=500)
    goal_path: str | None = None


class RecommendationFeedbackRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: str | None = Field(None, max_length=2000)


class TrackedRecommendationAction(BaseModel):
    recommendation_id: str = ""
    recommendation_title: str = ""
    category: str = ""
    score: float = 0.0
    recommendation_status: str = ""
    created_at: str = ""
    action_item: RecommendationActionItem


class WeeklyPlanResponse(BaseModel):
    items: list[TrackedRecommendationAction] = Field(default_factory=list)
    capacity_points: int = 0
    used_points: int = 0
    remaining_points: int = 0
    generated_at: str = ""


class WatchlistItem(BaseModel):
    id: str = ""
    label: str = ""
    kind: str = "theme"
    aliases: list[str] = []
    why: str = ""
    priority: str = "medium"
    tags: list[str] = []
    goal: str = ""
    time_horizon: str = "quarter"
    source_preferences: list[str] = []
    domain: str = ""
    github_org: str = ""
    ticker: str = ""
    topics: list[str] = []
    geographies: list[str] = []
    linked_dossier_ids: list[str] = []
    created_at: str = ""
    updated_at: str = ""


class IntelFollowUp(BaseModel):
    url: str = ""
    title: str = ""
    saved: bool = False
    note: str = ""
    watchlist_ids: list[str] = []
    created_at: str = ""
    updated_at: str = ""


class BriefingGoal(BaseModel):
    path: str = ""
    title: str = ""
    status: str = ""
    days_since_check: int = 0


class DailyBriefItem(BaseModel):
    kind: str = ""
    title: str = ""
    description: str = ""
    time_minutes: int = 0
    action: str = ""
    priority: int = 0


class DailyBrief(BaseModel):
    items: list[DailyBriefItem] = []
    budget_minutes: int = 0
    used_minutes: int = 0
    generated_at: str = ""


class SuggestionItem(BaseModel):
    """Unified suggestion — either from daily brief or recommendations."""

    source: str = ""  # "brief" | "recommendation" | "assumption_alert" | ...
    kind: str = ""  # "stale_goal" | "recommendation" | "nudge" | "intel_match" | ...
    title: str = ""
    description: str = ""
    action: str = ""
    priority: int = 0
    score: float = 0.0
    why_now: list[dict] | None = None
    payload: dict | None = None


class GoalIntelMatch(BaseModel):
    id: int = 0
    goal_path: str = ""
    goal_title: str = ""
    url: str = ""
    title: str = ""
    summary: str = ""
    score: float = 0.0
    urgency: str = ""
    match_reasons: list[str] = []
    created_at: str = ""
    llm_evaluated: bool = False


class BriefingResponse(BaseModel):
    recommendations: list[BriefingRecommendation] = []
    stale_goals: list[BriefingGoal] = []
    goals: list[BriefingGoal] = []
    has_data: bool = False
    adaptation_count: int = 0
    daily_brief: DailyBrief | None = None
    goal_intel_matches: list[GoalIntelMatch] = []
    dossier_escalations: list["DossierEscalationResponse"] = []
    company_movements: list["CompanyMovementResponse"] = []
    hiring_signals: list["HiringSignalResponse"] = []
    regulatory_alerts: list["RegulatoryAlertResponse"] = []
    assumptions: list["AssumptionAlertResponse"] = []
    degradations: list["DegradationItem"] = Field(default_factory=list)


# --- Trends ---


class TopicTrend(BaseModel):
    topic: str
    direction: str  # emerging/declining/stable
    growth_rate: float
    counts: list[int]
    windows: list[str]
    total_entries: int
    representative_titles: list[str]


# --- Projects ---


class MatchingIssue(BaseModel):
    title: str
    url: str
    summary: str
    tags: list[str]
    source: str
    match_score: int = 0


# --- Memory ---


class MemoryFact(BaseModel):
    id: str = ""
    text: str = ""
    category: str = ""
    source_type: str = ""
    source_id: str = ""
    confidence: float = 0.0
    created_at: str = ""
    updated_at: str = ""


class MemoryStats(BaseModel):
    total_active: int = 0
    total_superseded: int = 0
    by_category: dict = {}


# --- Threads ---


class ThreadSummary(BaseModel):
    id: str = ""
    label: str = ""
    entry_count: int = 0
    first_date: str = ""
    last_date: str = ""
    status: str = "active"


class ThreadInboxSummary(ThreadSummary):
    inbox_state: str = "active"
    linked_goal_path: str | None = None
    linked_dossier_id: str | None = None
    last_action: str = ""
    recent_snippets: list[str] = []


class ThreadEntryItem(BaseModel):
    entry_id: str = ""
    entry_date: str = ""
    similarity: float = 0.0


class ThreadDetail(BaseModel):
    id: str = ""
    label: str = ""
    entry_count: int = 0
    entries: list[ThreadEntryItem] = []


class ThreadInboxDetail(ThreadDetail):
    first_date: str = ""
    last_date: str = ""
    status: str = "active"
    inbox_state: str = "active"
    linked_goal_path: str | None = None
    linked_dossier_id: str | None = None
    last_action: str = ""
    recent_snippets: list[str] = []
    available_actions: dict = {}


class ThreadInboxStateUpdate(BaseModel):
    inbox_state: str = Field(
        ..., pattern=r"^(active|dismissed|goal_created|research_started|dossier_started|dormant)$"
    )
    linked_goal_path: str | None = None
    linked_dossier_id: str | None = None
    last_action: str = ""


# --- Engagement ---


class EngagementEvent(BaseModel):
    event_type: str = Field(
        ...,
        pattern=r"^(opened|saved|dismissed|acted_on|feedback_useful|feedback_irrelevant)$",
    )
    target_type: str = Field(..., max_length=50)
    target_id: str = Field(..., max_length=200)
    metadata: dict | None = None


class EngagementStats(BaseModel):
    by_target: dict = {}
    by_event: dict = {}
    total: int = 0


# --- User ---


class UserMe(BaseModel):
    name: str | None = None
    email: str | None = None


class UserMeUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)


# --- Profile ---


class ProfileResponse(BaseModel):
    current_role: str = ""
    career_stage: str = ""
    skills: list[dict] = []
    interests: list[str] = []
    aspirations: str = ""
    location: str = ""
    languages_frameworks: list[str] = []
    learning_style: str = "mixed"
    weekly_hours_available: int = 5
    goals_short_term: str = ""
    goals_long_term: str = ""
    industries_watching: list[str] = []
    technologies_watching: list[str] = []
    constraints: dict = {}
    fears_risks: list[str] = []
    active_projects: list[str] = []
    updated_at: str | None = None
    summary: str = ""
    is_stale: bool = False


class ProfileUpdate(BaseModel):
    current_role: str | None = None
    career_stage: str | None = None
    skills: list[dict] | None = None
    interests: list[str] | None = None
    aspirations: str | None = None
    location: str | None = None
    languages_frameworks: list[str] | None = None
    learning_style: str | None = None
    weekly_hours_available: int | None = None
    goals_short_term: str | None = None
    goals_long_term: str | None = None
    industries_watching: list[str] | None = None
    technologies_watching: list[str] | None = None
    constraints: dict | None = None
    fears_risks: list[str] | None = None
    active_projects: list[str] | None = None


# --- Library ---


class LibraryReportCreate(BaseModel):
    prompt: str = Field(..., min_length=10, max_length=10000)
    report_type: str = Field(
        "custom", pattern=r"^(crash_course|overview|memo|plan|custom|document)$"
    )
    title: str | None = Field(None, max_length=200)
    collection: str | None = Field(None, max_length=100)


class LibraryReportUpdate(BaseModel):
    title: str | None = Field(None, max_length=200)
    content: str | None = Field(None, max_length=100_000)
    collection: str | None = Field(None, max_length=100)


class LibraryReportListItem(BaseModel):
    id: str
    title: str
    report_type: str
    status: str
    collection: str | None = None
    prompt: str = ""
    source_kind: str = "generated"
    created: str = ""
    updated: str = ""
    last_generated_at: str = ""
    preview: str = ""
    file_name: str | None = None
    file_size: int | None = None
    mime_type: str | None = None
    has_attachment: bool = False
    extraction_status: str | None = None
    has_extracted_text: bool = False
    origin_surface: str = "library"
    visibility_state: str = "saved"
    index_status: str | None = None
    extracted_chars: int = 0


class LibraryReportResponse(LibraryReportListItem):
    content: str = ""


class ChatAttachmentResponse(BaseModel):
    attachment_id: str
    file_name: str | None = None
    mime_type: str | None = None
    index_status: str = "ready"
    visibility_state: str = "hidden"
    extracted_chars: int = 0
    warning: str | None = None


class ExtractionReceiptEnvelope(BaseModel):
    status: str = "pending"
    receipt: dict | None = None


class DossierEscalationResponse(BaseModel):
    escalation_id: str = ""
    topic_key: str = ""
    topic_label: str = ""
    score: float = 0.0
    state: str = "active"
    evidence: dict = {}
    payload: dict = {}
    created_at: str = ""
    updated_at: str = ""
    snoozed_until: str | None = None
    dismissed_at: str | None = None
    accepted_dossier_id: str | None = None


class DossierEscalationSnoozeRequest(BaseModel):
    until: str | None = None


class RecommendationOutcomeOverrideRequest(BaseModel):
    state: str = Field(..., pattern=r"^(positive|negative|unresolved|conflicted)$")
    note: str = Field("", max_length=2000)


class RecommendationOutcomeResponse(BaseModel):
    state: str = "unresolved"
    confidence: float = 0.0
    source_summary: str = ""
    user_overridden: bool = False
    evidence: list[dict] = []


class CompanyMovementResponse(BaseModel):
    id: int = 0
    company_key: str = ""
    company_label: str = ""
    movement_type: str = ""
    title: str = ""
    summary: str = ""
    significance: float = 0.0
    source_url: str = ""
    source_family: str = ""
    observed_at: str = ""
    metadata: dict = {}


class HiringSignalResponse(BaseModel):
    id: int = 0
    entity_key: str = ""
    entity_label: str = ""
    signal_type: str = ""
    title: str = ""
    summary: str = ""
    strength: float = 0.0
    source_url: str = ""
    observed_at: str = ""
    metadata: dict = {}


class RegulatoryAlertResponse(BaseModel):
    id: int = 0
    target_key: str = ""
    title: str = ""
    summary: str = ""
    source_family: str = ""
    change_type: str = ""
    urgency: str = ""
    relevance: float = 0.0
    effective_date: str | None = None
    source_url: str = ""
    observed_at: str = ""
    metadata: dict = {}


class AssumptionAlertResponse(BaseModel):
    id: str = ""
    title: str = ""
    detail: str = ""
    status: str = "active"
    updated_at: str | None = None


class AssumptionCreate(BaseModel):
    statement: str = Field(..., min_length=3, max_length=500)
    status: str = Field(
        "active", pattern=r"^(suggested|active|confirmed|invalidated|resolved|archived)$"
    )
    source_type: str = "manual"
    source_id: str = "manual"
    extraction_confidence: float | None = None
    linked_goal_path: str | None = None
    linked_dossier_id: str | None = None
    linked_entities: list[str] = []


class AssumptionUpdate(BaseModel):
    status: str | None = Field(
        None, pattern=r"^(suggested|active|confirmed|invalidated|resolved|archived)$"
    )
    latest_evidence_summary: str | None = Field(None, max_length=500)


class AssumptionResponse(BaseModel):
    id: str = ""
    statement: str = ""
    status: str = "active"
    source_type: str = "manual"
    source_id: str = ""
    extraction_confidence: float | None = None
    linked_goal_path: str | None = None
    linked_dossier_id: str | None = None
    linked_entities: list[str] = []
    latest_evidence_summary: str = ""
    last_evaluated_at: str | None = None
    created_at: str = ""
    updated_at: str = ""
    evidence: list[dict] = []


# --- GitHub Repo Monitoring ---


class MonitorRepoRequest(BaseModel):
    repo_full_name: str = Field(..., pattern=r"^[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+$")
    html_url: str = ""
    is_private: bool = False


class LinkGoalRequest(BaseModel):
    goal_path: str = Field(..., min_length=1)


class RepoSnapshotResponse(BaseModel):
    commits_30d: int = 0
    open_issues: int = 0
    open_prs: int = 0
    latest_release: str | None = None
    ci_status: str = "none"
    contributors_30d: int = 0
    pushed_at: str | None = None
    weekly_commits: list[int] = Field(default_factory=list)
    snapshot_at: str | None = None


class MonitoredRepoResponse(BaseModel):
    id: str = ""
    repo_full_name: str = ""
    html_url: str = ""
    is_private: bool = False
    linked_goal_path: str | None = None
    poll_tier: str = "moderate"
    last_polled_at: str | None = None
    added_at: str = ""
    latest_snapshot: RepoSnapshotResponse | None = None


class RepoSummaryResponse(BaseModel):
    name: str = ""
    full_name: str = ""
    private: bool = False
    html_url: str = ""
    language: str | None = None
    pushed_at: str | None = None
    open_issues_count: int = 0
