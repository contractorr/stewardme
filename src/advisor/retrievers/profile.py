"""Profile context retriever."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import structlog

if TYPE_CHECKING:
    from profile.storage import UserProfile

logger = structlog.get_logger()


class ProfileRetriever:
    """Loads and caches user profile for LLM context injection."""

    def __init__(self, profile_path: str = "~/coach/profile.yaml"):
        self._profile_path = profile_path
        self._cached_profile: UserProfile | None = None
        self._cached_profile_mtime: float = 0.0

    def load(self) -> UserProfile | None:
        """Load profile with mtime-gated instance cache."""
        path = Path(self._profile_path).expanduser()
        try:
            mtime = path.stat().st_mtime
        except OSError:
            return None
        if self._cached_profile is not None and mtime == self._cached_profile_mtime:
            return self._cached_profile
        try:
            from profile.storage import ProfileStorage

            profile = ProfileStorage(self._profile_path).load()
        except Exception as e:
            logger.debug("profile_load_failed", error=str(e))
            return None
        self._cached_profile = profile
        self._cached_profile_mtime = mtime
        return profile

    def get_profile_context(self, structured: bool = False) -> str:
        """Return compact or multi-section XML profile summary."""
        try:
            profile = self.load()
            if profile:
                if structured:
                    return f"\n{profile.structured_summary()}\n"
                return f"\nUSER PROFILE: {profile.summary()}\n"
        except Exception as e:
            logger.debug("profile_load_skipped", error=str(e))
        return ""

    def get_profile_keywords(self) -> list[str]:
        """Extract key terms from profile for intel query augmentation."""
        try:
            profile = self.load()
            if not profile:
                return []

            keywords = []
            if profile.skills:
                keywords.extend(s.name for s in profile.skills[:8])
            keywords.extend(profile.languages_frameworks[:6])
            keywords.extend(profile.technologies_watching[:6])
            keywords.extend(profile.industries_watching[:4])
            keywords.extend(profile.interests[:4])
            for p in profile.active_projects[:3]:
                keywords.extend(p.lower().split()[:3])
            return [k.lower().strip() for k in keywords if k.strip()]
        except Exception:
            return []

    def load_profile_terms(self):
        """Load profile and build ProfileTerms for intel filtering."""
        from intelligence.search import build_profile_terms

        return build_profile_terms(self.load())
