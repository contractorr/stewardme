"""LLM note polishing — spelling/grammar/factual corrections with an audit trail."""

import difflib
import json
import re
from dataclasses import dataclass, field

import structlog

from notes.models import CORRECTION_TYPES

logger = structlog.get_logger()

MAX_NOTE_CHARS = 40_000

SYSTEM_PROMPT = """You are a careful copy editor. The user gives you a messy note \
(markdown or plain text). Produce a polished version that:
- fixes all spelling and grammar mistakes
- corrects clear factual errors (only when you are confident; note the correction)
- rewords awkward or unclear sections for clarity
- removes repetitive or duplicative content
- preserves the author's meaning, overall structure, and voice
- keeps code blocks verbatim (never edit content inside ``` fences)
- never adds new claims, facts, or sections that were not in the original
- uses clean markdown: headings, lists, emphasis, tables where the original implied them

Respond with ONLY a JSON object (no prose, no code fence) of this shape:
{
  "polished_markdown": "<the full polished note as markdown>",
  "corrections": [
    {"type": "spelling|grammar|factual|rewording|removal",
     "original": "<short excerpt from the original>",
     "corrected": "<the replacement text, empty for removals>",
     "reason": "<one short sentence>"}
  ]
}
List every meaningful change in "corrections". Use "removal" for deleted duplicate \
content with "corrected" as an empty string."""

_FENCE_RE = re.compile(r"^```(?:json)?\s*\n?(.*?)\n?```\s*$", re.DOTALL)


class NotePolishError(RuntimeError):
    """Raised when the LLM output is unusable."""


@dataclass
class PolishResult:
    polished_markdown: str
    corrections: list[dict] = field(default_factory=list)
    diff: str = ""


def _strip_fence(text: str) -> str:
    match = _FENCE_RE.match(text.strip())
    return match.group(1) if match else text.strip()


def _extract_json(text: str) -> dict | None:
    candidate = _strip_fence(text)
    try:
        parsed = json.loads(candidate)
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        pass
    # Try the largest {...} span (models sometimes wrap JSON in prose).
    start, end = candidate.find("{"), candidate.rfind("}")
    if start != -1 and end > start:
        try:
            parsed = json.loads(candidate[start : end + 1])
            return parsed if isinstance(parsed, dict) else None
        except json.JSONDecodeError:
            return None
    return None


def _normalize_corrections(raw: object) -> list[dict]:
    corrections: list[dict] = []
    if not isinstance(raw, list):
        return corrections
    for item in raw:
        if not isinstance(item, dict):
            continue
        ctype = str(item.get("type", "rewording")).strip().lower()
        if ctype not in CORRECTION_TYPES:
            ctype = "rewording"
        corrections.append(
            {
                "type": ctype,
                "original": str(item.get("original", ""))[:2000],
                "corrected": str(item.get("corrected", ""))[:2000],
                "reason": str(item.get("reason", ""))[:500],
            }
        )
    return corrections


def compute_diff(original: str, polished: str) -> str:
    return "\n".join(
        difflib.unified_diff(
            original.splitlines(),
            polished.splitlines(),
            fromfile="original",
            tofile="polished",
            lineterm="",
        )
    )


class NotePolisher:
    """Wraps an LLMProvider to polish a note and report every change."""

    def __init__(self, llm_provider):
        self.llm = llm_provider

    def polish(self, text: str) -> PolishResult:
        text = text.strip()
        if not text:
            raise NotePolishError("Note text is empty")
        if len(text) > MAX_NOTE_CHARS:
            raise NotePolishError(f"Note exceeds the {MAX_NOTE_CHARS} character limit")

        response = self.llm.generate(
            messages=[{"role": "user", "content": text}],
            system=SYSTEM_PROMPT,
            max_tokens=8000,
        )
        if not response or not response.strip():
            raise NotePolishError("The language model returned an empty response")

        parsed = _extract_json(response)
        if parsed and str(parsed.get("polished_markdown", "")).strip():
            polished = str(parsed["polished_markdown"]).strip()
            corrections = _normalize_corrections(parsed.get("corrections"))
        else:
            # Fallback: treat the whole response as the polished note.
            logger.warning("notes.polish.json_parse_failed")
            polished = _strip_fence(response)
            corrections = []

        if not polished.strip():
            raise NotePolishError("The language model returned an unusable response")

        return PolishResult(
            polished_markdown=polished,
            corrections=corrections,
            diff=compute_diff(text, polished),
        )
