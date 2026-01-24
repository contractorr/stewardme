"""Prompt templates for different advice types."""


class PromptTemplates:
    """Specialized prompts for the advisor engine."""

    SYSTEM_BASE = """You are a professional AI coach and advisor. You have access to the user's personal journal entries and external intelligence about their industry/interests.

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

USER QUESTION: {question}

Provide a helpful, specific response:"""

    @classmethod
    def get_prompt(cls, prompt_type: str) -> str:
        """Get prompt template by type."""
        prompts = {
            "career": cls.CAREER_ADVICE,
            "weekly_review": cls.WEEKLY_REVIEW,
            "goals": cls.GOAL_ANALYSIS,
            "opportunities": cls.OPPORTUNITY_DETECTION,
            "general": cls.GENERAL_ASK,
        }
        return prompts.get(prompt_type, cls.GENERAL_ASK)
