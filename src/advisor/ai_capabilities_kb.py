"""Static knowledge base of current AI system capabilities.

Curated data on what AI can/can't do, organized by domain.
Updated periodically; logs warning when stale.
"""

from datetime import datetime, timedelta

import structlog

logger = structlog.get_logger()

LAST_UPDATED = datetime(2026, 2, 1)
STALENESS_DAYS = 90

AI_CAPABILITY_DOMAINS: dict[str, dict] = {
    "coding": {
        "what_works": [
            "Code completion and generation (single functions, boilerplate)",
            "Bug detection and fix suggestions",
            "Code review and refactoring assistance",
            "Test generation for existing code",
            "Multi-file edits with agentic coding tools (Claude Code, Cursor, Copilot)",
        ],
        "limitations": [
            "Large-scale architecture design still needs human judgment",
            "Novel algorithm invention remains rare",
            "Long-horizon multi-repo refactors unreliable without oversight",
            "Security-critical code needs human review",
        ],
        "key_benchmarks": [
            "SWE-bench Verified: top agents solve ~70% of real GitHub issues",
            "HumanEval: frontier models >95% pass@1",
            "METR autonomy evals: agents can complete multi-step coding tasks with tool use",
        ],
        "trajectory": "Rapidly improving; agentic coding approaching junior-dev level on scoped tasks",
    },
    "research": {
        "what_works": [
            "Literature review and summarization",
            "Hypothesis generation from existing data",
            "Experiment design suggestions",
            "Paper writing assistance and editing",
        ],
        "limitations": [
            "Cannot run physical experiments",
            "Hallucination risk in factual claims — needs verification",
            "Novelty of generated ideas often incremental",
        ],
        "key_benchmarks": [
            "GPQA Diamond: frontier models ~70% on PhD-level science questions",
            "FrontierMath: <5% on novel research-level math problems",
        ],
        "trajectory": "Strong at synthesis and ideation; weak at truly novel discoveries",
    },
    "reasoning": {
        "what_works": [
            "Multi-step logical reasoning (with chain-of-thought)",
            "Mathematical problem solving up to competition level",
            "Legal and contract analysis",
            "Strategic planning and scenario analysis",
        ],
        "limitations": [
            "Inconsistent on adversarial/trick problems",
            "Long chains of reasoning can drift",
            "Spatial and physical reasoning still weak",
        ],
        "key_benchmarks": [
            "MATH: frontier models >90% on competition math",
            "ARC-AGI: ~50% with scaffolding, well below human performance",
            "MMLU-Pro: top models ~85%",
        ],
        "trajectory": "Chain-of-thought and extended thinking yield large gains; still brittle on edge cases",
    },
    "autonomy": {
        "what_works": [
            "Web browsing and information gathering",
            "Tool use (APIs, file systems, terminals)",
            "Multi-step task execution with self-correction",
            "Computer use (GUI interaction) at basic level",
        ],
        "limitations": [
            "Long-horizon tasks (>1hr) still unreliable",
            "Error recovery in novel situations poor",
            "Safety and alignment concerns with fully autonomous operation",
            "Cost scales linearly with agent runtime",
        ],
        "key_benchmarks": [
            "METR autonomy evals: agents can handle ~4hr equivalent tasks with scaffolding",
            "WebArena: ~35% success on realistic web tasks",
            "OSWorld: ~15-25% on full desktop computer tasks",
        ],
        "trajectory": "Fastest-improving domain; viable for constrained automation today",
    },
    "creative": {
        "what_works": [
            "Image generation (photorealistic, artistic styles)",
            "Music composition and audio generation",
            "Video generation (short clips, improving rapidly)",
            "Writing (marketing copy, drafts, brainstorming)",
        ],
        "limitations": [
            "Long-form narrative coherence still limited",
            "Precise control over output details difficult",
            "Copyright and attribution concerns unresolved",
        ],
        "key_benchmarks": [
            "Chatbot Arena (style): frontier models competitive with human writers on short-form",
            "Creative writing evals show strong fluency, weaker on novelty",
        ],
        "trajectory": "Image/video gen near commercial quality; text creativity improving but not replacing top-tier writers",
    },
    "tool_use": {
        "what_works": [
            "API integration and function calling",
            "Database queries and data analysis",
            "File manipulation and code execution",
            "Multi-tool orchestration (MCP, function calling)",
        ],
        "limitations": [
            "Tool selection errors in large tool catalogs",
            "Complex multi-tool workflows need careful prompting",
            "Irreversible actions (delete, send) need human confirmation",
        ],
        "key_benchmarks": [
            "Berkeley Function Calling Leaderboard: top models >90% accuracy",
            "ToolBench: frontier models handle multi-step tool chains",
        ],
        "trajectory": "Mature capability; MCP ecosystem expanding tool access rapidly",
    },
}


def _check_staleness() -> None:
    """Log warning if KB data is stale."""
    age = datetime.now() - LAST_UPDATED
    if age > timedelta(days=STALENESS_DAYS):
        logger.warning(
            "ai_capabilities_kb_stale",
            last_updated=LAST_UPDATED.isoformat(),
            days_old=age.days,
        )


def render_context(domains: list[str] | None = None) -> str:
    """Render capability data for specified domains as LLM context.

    Args:
        domains: List of domain keys to include. None = all domains.

    Returns:
        Formatted string suitable for injection into LLM prompts.
    """
    _check_staleness()

    target = domains or list(AI_CAPABILITY_DOMAINS.keys())
    parts = [f"(Last updated: {LAST_UPDATED.strftime('%Y-%m')})"]

    for domain in target:
        data = AI_CAPABILITY_DOMAINS.get(domain)
        if not data:
            continue

        parts.append(f"\n## {domain.replace('_', ' ').title()}")
        parts.append(f"Trajectory: {data['trajectory']}")

        parts.append("Works well:")
        for item in data["what_works"][:3]:
            parts.append(f"  - {item}")

        parts.append("Limitations:")
        for item in data["limitations"][:2]:
            parts.append(f"  - {item}")

        parts.append("Benchmarks:")
        for item in data["key_benchmarks"][:2]:
            parts.append(f"  - {item}")

    return "\n".join(parts)


def render_summary() -> str:
    """High-level summary (~500 chars) of current AI capabilities."""
    _check_staleness()

    return (
        f"AI Capabilities Snapshot ({LAST_UPDATED.strftime('%Y-%m')}): "
        "Coding agents solve ~70% of real GitHub issues (SWE-bench). "
        "Reasoning models >90% on competition math but <5% on research-level problems. "
        "Autonomous agents handle ~4hr tasks with scaffolding; web tasks ~35% success. "
        "Tool use mature (>90% function calling accuracy). "
        "Creative gen near commercial quality for images; video improving fast. "
        "Key gaps: long-horizon autonomy, novel research, adversarial reasoning."
    )
