"""Daily brief builder — zero-LLM, time-budgeted action plan."""

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class DailyBriefItem:
    kind: str  # "stale_goal" | "recommendation" | "learning" | "nudge" | "intel_match"
    title: str
    description: str
    time_minutes: int
    action: str  # chat pre-fill
    priority: int  # 1-based, assigned during fill


@dataclass
class DailyBrief:
    items: list[DailyBriefItem] = field(default_factory=list)
    budget_minutes: int = 0
    used_minutes: int = 0
    generated_at: str = ""


# Fixed time estimates per kind
_TIME = {"stale_goal": 10, "recommendation": 15, "learning": 45, "nudge": 5, "intel_match": 5}


def _max_items(budget: int) -> int:
    if budget < 30:
        return 2
    if budget <= 60:
        return 3
    return 5


class DailyBriefBuilder:
    """Build a time-budgeted daily brief from pre-gathered data (no I/O)."""

    def build(
        self,
        *,
        stale_goals: list[dict],
        recommendations: list,
        learning_paths: list[dict],
        all_goals: list[dict],
        weekly_hours: int = 5,
        intel_matches: list[dict] | None = None,
    ) -> DailyBrief:
        budget = round(weekly_hours * 60 / 7)
        cap = _max_items(budget)

        _matches = intel_matches or []
        high_matches = [m for m in _matches if m.get("urgency") == "high"][:2]
        medium_matches = [m for m in _matches if m.get("urgency") == "medium"][:1]

        # Build candidate list in fixed priority order:
        # 1. Stale goals  2. Critical intel  3. Recommendations  4. Learning  5. Notable intel
        candidates: list[DailyBriefItem] = []

        for g in stale_goals:
            t = _TIME["stale_goal"]
            candidates.append(
                DailyBriefItem(
                    kind="stale_goal",
                    title=g.get("title", ""),
                    description=f"Last check-in {g.get('days_since_check', '?')} days ago",
                    time_minutes=t,
                    action=f"Help me check in on my goal: {g.get('title', '')}",
                    priority=0,
                )
            )

        for m in high_matches:
            t = _TIME["intel_match"]
            candidates.append(
                DailyBriefItem(
                    kind="intel_match",
                    title=m.get("title", ""),
                    description=m.get("summary", "")[:200],
                    time_minutes=t,
                    action=f"Tell me about this and how it relates to my goal: {m.get('title', '')}",
                    priority=0,
                )
            )

        for r in recommendations:
            t = _TIME["recommendation"]
            title = r.title if hasattr(r, "title") else r.get("title", "")
            desc = r.description if hasattr(r, "description") else r.get("description", "")
            candidates.append(
                DailyBriefItem(
                    kind="recommendation",
                    title=title,
                    description=desc[:200] if desc else "",
                    time_minutes=t,
                    action=f"Tell me more about: {title}",
                    priority=0,
                )
            )

        for lp in learning_paths:
            if lp.get("status", "active") != "active":
                continue
            t = _TIME["learning"]
            skill = lp.get("skill", "")
            candidates.append(
                DailyBriefItem(
                    kind="learning",
                    title=f"Learn: {skill}",
                    description=f"{lp.get('completed_modules', 0)}/{lp.get('total_modules', 0)} modules done",
                    time_minutes=t,
                    action=f"Help me make progress on learning {skill}",
                    priority=0,
                )
            )

        for m in medium_matches:
            t = _TIME["intel_match"]
            candidates.append(
                DailyBriefItem(
                    kind="intel_match",
                    title=m.get("title", ""),
                    description=m.get("summary", "")[:200],
                    time_minutes=t,
                    action=f"Tell me about this and how it relates to my goal: {m.get('title', '')}",
                    priority=0,
                )
            )

        # Fill within budget
        items: list[DailyBriefItem] = []
        used = 0
        for c in candidates:
            if len(items) >= cap:
                break
            if used + c.time_minutes > budget and items:
                break
            # Always include first item even if over budget
            used += c.time_minutes
            c.priority = len(items) + 1
            items.append(c)

        # Ambient fallback when no candidates
        if not items:
            if all_goals:
                g = all_goals[0]
                title = g.get("title", "")
                items.append(
                    DailyBriefItem(
                        kind="nudge",
                        title=title,
                        description="Quick check-in to keep momentum",
                        time_minutes=_TIME["nudge"],
                        action=f"Help me check in on my goal: {title}",
                        priority=1,
                    )
                )
                used = _TIME["nudge"]
            else:
                items.append(
                    DailyBriefItem(
                        kind="nudge",
                        title="Reflect",
                        description="Take a moment to journal or set a goal",
                        time_minutes=_TIME["nudge"],
                        action="Help me reflect on what I should focus on",
                        priority=1,
                    )
                )
                used = _TIME["nudge"]

        return DailyBrief(
            items=items,
            budget_minutes=budget,
            used_minutes=used,
            generated_at=datetime.now(timezone.utc).isoformat(),
        )
