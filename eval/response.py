"""LLM-as-judge response quality scorer."""

from __future__ import annotations

import json
import logging
import re

from eval.dataset import ResponseEvalCase

logger = logging.getLogger(__name__)

JUDGE_PROMPT = """You are an evaluation judge. Score the following AI advisor response against the rubric.

**User query:** {query}
**Advice type:** {advice_type}

**Response to evaluate:**
{response}

**Rubric:**
Expected traits (each should be present):
{expected_traits}

Forbidden traits (each should be absent):
{forbidden_traits}

Score each expected trait as 1 (present) or 0 (absent).
Score each forbidden trait as 1 (violation found) or 0 (clean).
Give an overall quality score from 1-5.

Respond in JSON only:
{{"trait_scores": {{"<trait>": 0or1, ...}}, "forbidden_scores": {{"<trait>": 0or1, ...}}, "overall": <1-5>, "reasoning": "<brief explanation>"}}"""


def _parse_judge_response(text: str) -> dict | None:
    """Parse JSON from LLM response, with regex fallback."""
    # Try direct JSON parse
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        pass

    # Try extracting JSON block
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group())
        except (json.JSONDecodeError, TypeError):
            pass

    return None


class ResponseJudge:
    def __init__(self, llm_provider):
        self.llm = llm_provider

    def score(self, case: ResponseEvalCase, response: str) -> dict:
        """Score a response against eval case rubric. Returns skipped if no LLM."""
        if self.llm is None:
            return {"skipped": True, "reason": "no LLM available"}

        prompt = JUDGE_PROMPT.format(
            query=case.query,
            advice_type=case.advice_type,
            response=response,
            expected_traits="\n".join(f"- {t}" for t in case.expected_traits)
            or "- (none specified)",
            forbidden_traits="\n".join(f"- {t}" for t in case.forbidden_traits)
            or "- (none specified)",
        )

        try:
            raw = self.llm.generate(
                messages=[{"role": "user", "content": prompt}],
                system="You are an evaluation judge. Respond only in valid JSON.",
                max_tokens=1000,
            )
        except Exception as e:
            logger.warning("LLM judge call failed: %s", e)
            return {"skipped": True, "reason": str(e)}

        parsed = _parse_judge_response(raw)
        if parsed is None:
            return {"skipped": True, "reason": "failed to parse judge response", "raw": raw}

        return {
            "query": case.query,
            "trait_scores": parsed.get("trait_scores", {}),
            "forbidden_scores": parsed.get("forbidden_scores", {}),
            "overall": parsed.get("overall", 0),
            "reasoning": parsed.get("reasoning", ""),
        }
