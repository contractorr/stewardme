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

    # === Recommendation Prompt ===

    UNIFIED_RECOMMENDATIONS = """Generate {category} recommendations based on the user's profile and market conditions.

USER PROFILE (from journal):
{journal_context}

INTELLIGENCE:
{intel_context}

Generate {max_items} actionable {category} recommendations. For each:

### [Title]
**Description**: What this is and why it matters
**Why**: Why this is relevant to them specifically (cite journal entries)
SCORE: [0-10 single score weighing relevance, feasibility, and impact]
**Next Steps**: Concrete actions to take

**REASONING**
SOURCE: [specific journal entry or intel item that triggered this]
PROFILE_MATCH: [how this aligns with user goals/skills/interests]
CONFIDENCE: [0.0-1.0]
CAVEATS: [risks, time commitment, limitations]

Be specific and actionable. Prioritize practical value over theoretical interest."""

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

    EVENT_RECOMMENDATIONS = """Based on the user's profile and upcoming events, recommend events to attend.

USER PROFILE:
{journal_context}

UPCOMING EVENTS:
{intel_context}

For each recommended event:

### [Event Name]
**Date**: When it happens
**Location**: Where (or Online)
**Why Attend**: Why this is relevant to them specifically (cite profile/journal)
**What to Get Out of It**: Networking, skills, speaking opportunity, etc.
**Deadlines**: CFP deadline, early-bird registration, etc.
SCORE: [0-10]
**Action**: Specific next step (register, submit CFP, etc.)

Prioritize time-sensitive items first (CFP deadlines closing soon, early-bird pricing ending)."""

    SKILL_GAP_ANALYSIS = """Analyze the gap between the user's current skills and their career aspirations.

USER PROFILE:
{profile_context}

JOURNAL CONTEXT (goals, reflections):
{journal_context}

Provide:
1. **Current Strengths** — What they're already good at
2. **Critical Gaps** — Skills they need for their aspirations but lack or are weak in
3. **Recommended Priority** — Which gaps to close first and why
4. **Industry Context** — How these gaps relate to market demand

For each gap:
- Skill name
- Current level (from profile, 1-5)
- Target level needed
- Importance (high/medium/low)
- Why it matters for their aspirations"""

    LEARNING_PATH_GENERATION = """Generate a structured learning path for the specified skill.

USER PROFILE:
{profile_context}

TARGET SKILL: {skill_name}
CURRENT LEVEL: {current_level}
TARGET LEVEL: {target_level}
LEARNING STYLE: {learning_style}
WEEKLY HOURS AVAILABLE: {weekly_hours}

Create a multi-week curriculum:

# Learning Path: {skill_name}

## Overview
Brief description of the path and expected outcomes.

## Modules

For each module (~1 week):
### Module N: [Title]
**Focus**: What you'll learn
**Resources**:
- Specific courses, docs, tutorials (include URLs where possible)
- Match to learning style ({learning_style})
**Project**: Small hands-on exercise
**Milestone**: How to know you've completed this module

## Final Project
A capstone project that demonstrates mastery.

## Success Criteria
How to know the learning path is complete.

Keep resources practical and specific. Prefer free resources when available."""

    PROJECT_RECOMMENDATIONS = """Based on the user's skills and interests, recommend open-source projects to contribute to.

USER PROFILE:
{journal_context}

AVAILABLE ISSUES/PROJECTS:
{intel_context}

For each recommendation:

### [Project/Issue Title]
**Repository**: Name and URL
**Why**: Why this matches their skills and interests
**Difficulty**: Easy/Medium/Hard
**Learning Potential**: What they'll learn from contributing
**First Step**: How to get started
SCORE: [0-10]"""

    SIDE_PROJECT_IDEAS = """Based on the user's journal entries (pain points, interests, ideas), suggest side-project ideas.

USER PROFILE:
{profile_context}

JOURNAL CONTEXT (frustrations, ideas, interests):
{journal_context}

Generate 3-5 side-project ideas. For each:

### [Project Idea Name]
**Problem**: What pain point this solves (cite journal entries)
**Description**: What the project does
**Tech Stack**: Suggested technologies (aligned with user's skills)
**Scope**: Weekend project / 1-month / 3-month
**Learning Value**: What new skills they'd develop
**Market Potential**: Could this become a product? (honest assessment)
SCORE: [0-10]"""

    AGENTIC_SYSTEM = """You are a professional AI coach with access to the user's journal, goals, intelligence feed, and profile.

Use tools to look up information before answering. Don't guess — search first.
You can also take actions when the user asks (create goals, check in, write journal entries).

Guidelines:
- Search journal/intel for relevant context before giving advice
- Check goal status when discussing progress
- Be concise and actionable
- Call multiple tools if needed for complete context
- Don't over-fetch — be strategic about which tools to call"""

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
