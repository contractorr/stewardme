"""LLM-as-judge grounding evaluation — measures whether advisor uses retrieved context."""

from __future__ import annotations

import logging

from eval.dataset import GroundingEvalCase
from eval.response import _parse_judge_response

logger = logging.getLogger(__name__)

GROUNDING_PROMPT = """You are an evaluation judge. Score whether the advisor response is grounded in the provided context.

Context provided to the advisor:
<journal_context>{journal_context}</journal_context>
<intel_context>{intel_context}</intel_context>

Advisor response:
{response}

Score 1-5 on each axis:
- grounding: uses specific facts from context, not generic advice
- hallucination_risk: 5=clean, 1=fabricated specifics not in context
- context_coverage: references both journal AND intel when available

Respond in JSON only:
{{"grounding": <1-5>, "hallucination_risk": <1-5>, "context_coverage": <1-5>, "reasoning": "<brief explanation>"}}"""


class GroundingJudge:
    """Score advisor responses for grounding quality."""

    def __init__(self, llm_provider):
        self.llm = llm_provider

    def score(
        self,
        case: GroundingEvalCase,
        response: str,
        journal_context: str,
        intel_context: str,
    ) -> dict:
        """Score grounding of a response against retrieved context."""
        if self.llm is None:
            return {"skipped": True, "reason": "no LLM available", "query": case.query}

        prompt = GROUNDING_PROMPT.format(
            journal_context=journal_context or "(none)",
            intel_context=intel_context or "(none)",
            response=response,
        )

        try:
            raw = self.llm.generate(
                messages=[{"role": "user", "content": prompt}],
                system="You are an evaluation judge. Respond only in valid JSON.",
                max_tokens=1000,
            )
        except Exception as e:
            logger.warning("Grounding judge failed for '%s': %s", case.query, e)
            return {"skipped": True, "reason": str(e), "query": case.query}

        parsed = _parse_judge_response(raw)
        if parsed is None:
            return {"skipped": True, "reason": "parse failure", "query": case.query, "raw": raw}

        return {
            "query": case.query,
            "description": case.description,
            "grounding": parsed.get("grounding", 0),
            "hallucination_risk": parsed.get("hallucination_risk", 0),
            "context_coverage": parsed.get("context_coverage", 0),
            "reasoning": parsed.get("reasoning", ""),
        }
