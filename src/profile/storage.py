"""Profile storage — Pydantic model + YAML CRUD at ~/coach/profile.yaml."""

from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field

from shared_types import CareerStage


class Skill(BaseModel):
    name: str
    proficiency: int = Field(ge=1, le=5, description="1=beginner, 5=expert")


class UserProfile(BaseModel):
    skills: list[Skill] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)
    career_stage: CareerStage = CareerStage.MID
    current_role: str = ""
    aspirations: str = ""
    location: str = ""
    languages_frameworks: list[str] = Field(default_factory=list)
    learning_style: str = "mixed"  # visual/reading/hands-on/mixed
    weekly_hours_available: int = 5
    updated_at: Optional[str] = None

    def is_stale(self, days: int = 90) -> bool:
        if not self.updated_at:
            return True
        updated = datetime.fromisoformat(self.updated_at)
        return (datetime.now() - updated).days > days

    def summary(self) -> str:
        """One-paragraph profile summary for LLM context."""
        parts = []
        if self.current_role:
            parts.append(f"Role: {self.current_role} ({self.career_stage})")
        if self.skills:
            top = sorted(self.skills, key=lambda s: s.proficiency, reverse=True)[:5]
            parts.append("Skills: " + ", ".join(f"{s.name}({s.proficiency})" for s in top))
        if self.languages_frameworks:
            parts.append("Tech: " + ", ".join(self.languages_frameworks[:8]))
        if self.interests:
            parts.append("Interests: " + ", ".join(self.interests[:6]))
        if self.aspirations:
            parts.append(f"Aspirations: {self.aspirations[:200]}")
        if self.location:
            parts.append(f"Location: {self.location}")
        if self.weekly_hours_available:
            parts.append(f"Available: {self.weekly_hours_available}h/week")
        parts.append(f"Learning style: {self.learning_style}")
        return " | ".join(parts)


class ProfileStorage:
    """YAML-backed profile storage."""

    def __init__(self, path: str | Path = "~/coach/profile.yaml"):
        self.path = Path(path).expanduser()

    def exists(self) -> bool:
        return self.path.exists()

    def load(self) -> Optional[UserProfile]:
        if not self.path.exists():
            return None
        with open(self.path) as f:
            data = yaml.safe_load(f)
        if not data:
            return None
        return UserProfile(**data)

    def save(self, profile: UserProfile) -> Path:
        profile.updated_at = datetime.now().isoformat()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Convert to plain dict with string values (avoid YAML Python-object tags)
        data = profile.model_dump()
        data["career_stage"] = str(data["career_stage"])
        data["skills"] = [
            {"name": s["name"], "proficiency": int(s["proficiency"])} for s in data["skills"]
        ]
        with open(self.path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        return self.path

    def update_field(self, field: str, value) -> UserProfile:
        """Update a single field on the profile."""
        profile = self.load() or UserProfile()
        if not hasattr(profile, field):
            raise ValueError(f"Unknown profile field: {field}")
        setattr(profile, field, value)
        self.save(profile)
        return profile

    def get_or_empty(self) -> UserProfile:
        return self.load() or UserProfile()
