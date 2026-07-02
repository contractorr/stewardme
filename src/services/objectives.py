"""User-maintained objectives file — gate pulse for weekly reviews.

``~/coach/objectives.yaml`` is written by the user only; the advisor reads
it and renders a deterministic GATE PULSE block (numbers, no commentary)
that leads the weekly review output. See
specs/functional/objectives-gate-pulse.md.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import structlog
import yaml
from pydantic import BaseModel, Field

logger = structlog.get_logger()

STALE_AFTER_DAYS = 42


class Gate(BaseModel):
    """A committed, measurable target."""

    name: str
    target: float
    current: float = 0


class Clock(BaseModel):
    """Hard dates the gates are measured against."""

    runway_ends: str | None = None  # coarse, e.g. "2028-06"
    go_no_go: date | None = None


class Objectives(BaseModel):
    """Schema of ~/coach/objectives.yaml."""

    last_reviewed: date | None = None
    gates: list[Gate] = Field(default_factory=list)
    clock: Clock = Field(default_factory=Clock)


def load_objectives(path: Path | None = None) -> Objectives | None:
    """Load the user's objectives file, or None when absent/empty/invalid.

    Invalid content logs a warning and returns None — the weekly review must
    never crash on this file. The advisor never writes it.
    """
    if path is None:
        from storage_paths import get_coach_home

        path = get_coach_home() / "objectives.yaml"
    path = Path(path)
    if not path.exists():
        return None
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not data:
            return None
        return Objectives.model_validate(data)
    except Exception as exc:
        logger.warning("objectives_load_failed", path=str(path), error=str(exc))
        return None


def _format_number(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else str(value)


def render_gate_pulse(objectives: Objectives | None, today: date | None = None) -> str:
    """Render the GATE PULSE block. Numbers only — no generated commentary."""
    if objectives is None:
        return ""
    today = today or date.today()

    lines: list[str] = []
    if objectives.last_reviewed and (today - objectives.last_reviewed).days > STALE_AFTER_DAYS:
        lines.append(
            f"objectives.yaml last reviewed {objectives.last_reviewed.isoformat()} "
            "— stale measuring stick."
        )

    lines.append("GATE PULSE")
    for gate in objectives.gates:
        lines.append(
            f"- {gate.name}: {_format_number(gate.current)} / {_format_number(gate.target)}"
        )
    if objectives.clock.go_no_go:
        days = (objectives.clock.go_no_go - today).days
        lines.append(f"- go/no-go: {objectives.clock.go_no_go.isoformat()} ({days} days)")
    if objectives.clock.runway_ends:
        lines.append(f"- runway ends: {objectives.clock.runway_ends}")

    return "\n".join(lines)
