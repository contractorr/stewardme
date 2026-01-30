"""Prompt templates for different advice types."""


class PromptTemplates:
    """Specialized prompts for the advisor engine."""

    SYSTEM = """You are a professional AI coach and advisor. You have access to the user's personal journal entries and external intelligence about their industry/interests.

Your role is to provide:
- Actionable, specific advice
- Insights connecting their goals to opportunities
- Honest feedback without unnecessary flattery
- Strategic thinking about career and projects

Be concise. Prioritize practical next steps over general encouragement."""

    CAREER_ADVICE = """Based on the user's journal context below, provide career guidance.

Focus on:
- Skills to develop based on their current trajectory
- Potential opportunities aligned with their interests
- Concrete next steps they can take this week

JOURNAL CONTEXT:
{journal_context}

EXTERNAL INTELLIGENCE (recent industry trends):
{intel_context}

USER QUESTION: {question}

Provide specific, actionable advice:"""

    WEEKLY_REVIEW = """Generate a weekly review summary based on the user's recent journal entries.

Structure:
1. KEY ACCOMPLISHMENTS - What they achieved
2. PATTERNS NOTICED - Recurring themes, energy levels, blockers
3. OPPORTUNITIES - Based on their work and external trends
4. FOCUS FOR NEXT WEEK - 2-3 specific priorities

RECENT JOURNAL ENTRIES:
{journal_context}

RELEVANT INDUSTRY NEWS:
{intel_context}

Generate a concise but insightful weekly review:"""

    GOAL_ANALYSIS = """Analyze the user's goals and progress.

JOURNAL CONTEXT (including stated goals):
{journal_context}

USER QUESTION: {question}

Provide:
1. Goal clarity assessment - are their goals specific enough?
2. Progress analysis - what's working, what's not
3. Recommended adjustments
4. Next milestone to aim for"""

    OPPORTUNITY_DETECTION = """Based on the user's skills, interests, and recent industry developments, identify potential opportunities.

USER PROFILE (from journal):
{journal_context}

RECENT INDUSTRY INTELLIGENCE:
{intel_context}

Identify and explain 2-3 specific opportunities with:
- Why it's relevant to them specifically
- What they'd need to do to pursue it
- Potential risks or considerations"""

    GENERAL_ASK = """You are the user's personal AI coach. Answer their question using context from their journal and relevant external information.

JOURNAL CONTEXT:
{journal_context}

EXTERNAL INTELLIGENCE:
{intel_context}

{research_context}

USER QUESTION: {question}

Provide a helpful, specific response:"""

    GENERAL_ASK_WITH_RESEARCH = """You are the user's personal AI coach. Answer their question using context from their journal, external intelligence, and any relevant deep research.

JOURNAL CONTEXT:
{journal_context}

EXTERNAL INTELLIGENCE:
{intel_context}

DEEP RESEARCH (auto-generated reports on topics you've shown interest in):
{research_context}

USER QUESTION: {question}

Use the research context when relevant to provide more informed, thorough answers. Cite specific insights from research when applicable:"""

    # === Recommendation Prompts ===

    LEARNING_RECOMMENDATIONS = """Based on the user's goals, interests, and industry trends, recommend skills or courses to learn.

USER PROFILE (from journal):
{journal_context}

INDUSTRY INTELLIGENCE:
{intel_context}

Generate {max_items} learning recommendations. For each:

### [Skill/Course Name]
**Description**: What to learn and why it matters
**Why**: Why this is relevant to them specifically (cite journal entries)
RELEVANCE: [0-10 score]
URGENCY: [0-10 score based on market demand]
FEASIBILITY: [0-10 score based on their current skills]
IMPACT: [0-10 score for career/project impact]
**Next Steps**: Specific resources or actions to start learning

Focus on actionable, specific skills with clear ROI. Prioritize skills that bridge their current abilities with emerging opportunities."""

    CAREER_CHANGE_ANALYSIS = """Analyze potential career moves based on the user's trajectory and market conditions.

USER PROFILE (from journal):
{journal_context}

MARKET INTELLIGENCE:
{intel_context}

Generate {max_items} career recommendations. For each:

### [Role/Direction]
**Description**: What this career move entails
**Why**: Why this fits their profile and goals
RELEVANCE: [0-10 score]
URGENCY: [0-10 score based on market timing]
FEASIBILITY: [0-10 score based on skill gaps]
IMPACT: [0-10 score for income/satisfaction]
**Risk/Reward**: Honest assessment of tradeoffs
**Bridge Actions**: Steps to make this transition

Consider adjacent roles, industry pivots, and leadership paths. Be realistic about timelines and prerequisites."""

    ENTREPRENEURIAL_OPPORTUNITIES = """Identify business opportunities based on problems mentioned in journal and market gaps.

USER PROFILE (from journal):
{journal_context}

MARKET INTELLIGENCE:
{intel_context}

Generate {max_items} entrepreneurial recommendations. For each:

### [Business Idea/Project]
**Description**: What the opportunity is
**Why**: Why this matches their skills and observed problems
RELEVANCE: [0-10 score]
URGENCY: [0-10 score based on market timing]
FEASIBILITY: [0-10 score based on resources needed]
IMPACT: [0-10 score for potential outcome]
**Validation Steps**: How to test this idea quickly
**First Week Actions**: Concrete steps to start

Focus on problems they've complained about, skills they have, and market gaps from intel. Prefer ideas with low initial investment."""

    INVESTMENT_OPPORTUNITIES = """Identify investment-relevant trends based on the user's expertise and market conditions.

USER PROFILE (from journal):
{journal_context}

MARKET INTELLIGENCE:
{intel_context}

Generate {max_items} investment-related recommendations. For each:

### [Investment Theme/Area]
**Description**: What the opportunity is
**Why**: Why their expertise gives them an edge here
RELEVANCE: [0-10 score]
URGENCY: [0-10 score based on market timing]
FEASIBILITY: [0-10 score based on capital/access]
IMPACT: [0-10 score for potential returns]
**Options**: Different ways to participate (invest, build, consult, angel)
**Due Diligence**: What to research before acting

Focus on areas where their domain knowledge provides insight advantage. Not financial advice - highlight information edges from their expertise."""

    WEEKLY_ACTION_BRIEF = """Generate a weekly action brief with the top prioritized recommendations.

USER PROFILE (from journal):
{journal_context}

RECENT INTELLIGENCE:
{intel_context}

TOP RECOMMENDATIONS:
{recommendations}

Create a focused action brief with 3-5 priority items for this week.

# Weekly Action Brief - {date}

## Priority Actions This Week

For each item:
### [Priority Number]. [Category]: [Title] [Score: X.X]
**Why Now**: Time-sensitive rationale
**Context**: Brief background from journal/intel
**This Week**: Specific actions for the next 7 days
**Success Metric**: How to know progress was made

End with:
## Quick Wins (optional low-effort items)
## Items to Revisit Next Week

Be specific and actionable. Each item should have clear first steps."""

    ACTION_PLAN = """Generate a concrete action plan for this recommendation.

RECOMMENDATION:
Title: {title}
Category: {category}
Description: {description}
Rationale: {rationale}

USER CONTEXT:
{journal_context}

Create a step-by-step action plan with:

## Week 1: Getting Started
- 2-3 specific, actionable tasks
- Required resources or tools

## Week 2-3: Building Momentum
- 2-3 intermediate milestones
- Potential blockers and solutions

## Week 4+: Completion
- Final deliverables
- How to measure success

## Resources
- Specific links, courses, or tools (if applicable)

## Success Criteria
- 2-3 measurable outcomes

Be specific and practical. Each step should be completable in 1-2 hours."""

    @classmethod
    def get_prompt(cls, prompt_type: str, with_research: bool = False) -> str:
        """Get prompt template by type.

        Args:
            prompt_type: Type of prompt
            with_research: If True and general, use research-aware template
        """
        prompts = {
            "career": cls.CAREER_ADVICE,
            "weekly_review": cls.WEEKLY_REVIEW,
            "goals": cls.GOAL_ANALYSIS,
            "opportunities": cls.OPPORTUNITY_DETECTION,
            "general": cls.GENERAL_ASK,
            "general_with_research": cls.GENERAL_ASK_WITH_RESEARCH,
            "action_plan": cls.ACTION_PLAN,
        }
        if prompt_type == "general" and with_research:
            return prompts["general_with_research"]
        return prompts.get(prompt_type, cls.GENERAL_ASK)
