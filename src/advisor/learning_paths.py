"""Learning path generator — structured multi-week curricula stored as markdown."""

import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

import frontmatter
import structlog

from .prompts import PromptTemplates
from .rag import RAGRetriever

logger = structlog.get_logger()


def _slug(text: str) -> str:
    s = re.sub(r"[^\w\s-]", "", text.lower().strip())
    return re.sub(r"[\s_]+", "-", s)[:40]


class LearningPathStorage:
    """Markdown file storage for learning paths."""

    def __init__(self, path: str | Path = "~/coach/learning_paths"):
        self.dir = Path(path).expanduser()
        self.dir.mkdir(parents=True, exist_ok=True)

    def save(self, skill: str, content: str, metadata: Optional[dict] = None) -> Path:
        """Save a learning path as markdown with frontmatter."""
        path_id = uuid.uuid4().hex[:8]
        now = datetime.now()
        filename = f"{now.strftime('%Y-%m-%d')}_{_slug(skill)}_{path_id}.md"
        filepath = self.dir / filename

        post = frontmatter.Post(content)
        post.metadata = {
            "id": path_id,
            "skill": skill,
            "status": "active",
            "progress": 0,
            "total_modules": self._count_modules(content),
            "completed_modules": 0,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
        }
        if metadata:
            post.metadata.update(metadata)

        filepath.write_text(frontmatter.dumps(post))
        return filepath

    def list_paths(self, status: Optional[str] = None) -> list[dict]:
        """List all learning paths."""
        paths = []
        for f in sorted(self.dir.glob("*.md"), reverse=True):
            try:
                post = frontmatter.load(f)
                m = post.metadata
                if status and m.get("status") != status:
                    continue
                paths.append(
                    {
                        "id": m.get("id", ""),
                        "skill": m.get("skill", ""),
                        "status": m.get("status", "active"),
                        "progress": m.get("progress", 0),
                        "total_modules": m.get("total_modules", 0),
                        "completed_modules": m.get("completed_modules", 0),
                        "created_at": m.get("created_at", ""),
                        "updated_at": m.get("updated_at", m.get("created_at", "")),
                        "path": str(f),
                    }
                )
            except Exception:
                continue
        return paths

    def get(self, path_id: str) -> Optional[dict]:
        """Get a learning path by ID."""
        for f in self.dir.glob("*.md"):
            try:
                post = frontmatter.load(f)
                if str(post.metadata.get("id")) == path_id:
                    return {
                        **post.metadata,
                        "content": post.content,
                        "path": str(f),
                    }
            except Exception:
                continue
        return None

    def update_progress(self, path_id: str, completed_modules: int) -> bool:
        """Update progress on a learning path."""
        for f in self.dir.glob("*.md"):
            try:
                post = frontmatter.load(f)
                if str(post.metadata.get("id")) == path_id:
                    total = post.metadata.get("total_modules", 1) or 1
                    post.metadata["completed_modules"] = min(completed_modules, total)
                    post.metadata["progress"] = round(completed_modules / total * 100)
                    post.metadata["updated_at"] = datetime.now().isoformat()
                    if completed_modules >= total:
                        post.metadata["status"] = "completed"
                    f.write_text(frontmatter.dumps(post))
                    return True
            except Exception:
                continue
        return False

    def _count_modules(self, content: str) -> int:
        """Count modules in learning path content."""
        return max(1, len(re.findall(r"^###\s+Module\s+\d+", content, re.MULTILINE)))


class LearningPathGenerator:
    """Generate structured learning paths via LLM."""

    def __init__(self, rag: RAGRetriever, llm_caller, storage: LearningPathStorage):
        self.rag = rag
        self.llm_caller = llm_caller
        self.storage = storage

    def generate(self, skill_name: str, current_level: int = 1, target_level: int = 4) -> Path:
        """Generate a new learning path for a skill.

        Args:
            skill_name: Skill to learn
            current_level: Current proficiency 1-5
            target_level: Target proficiency 1-5

        Returns:
            Path to saved learning path file
        """
        profile_ctx = self.rag.get_profile_context()

        # Get learning style and hours from profile
        learning_style = "mixed"
        weekly_hours = 5
        try:
            from profile.storage import ProfileStorage

            ps = ProfileStorage()
            p = ps.load()
            if p:
                learning_style = p.learning_style
                weekly_hours = p.weekly_hours_available
        except Exception:
            pass

        prompt = PromptTemplates.LEARNING_PATH_GENERATION.format(
            profile_context=profile_ctx,
            skill_name=skill_name,
            current_level=current_level,
            target_level=target_level,
            learning_style=learning_style,
            weekly_hours=weekly_hours,
        )

        content = self.llm_caller(PromptTemplates.SYSTEM, prompt, max_tokens=3000)

        return self.storage.save(
            skill=skill_name,
            content=content,
            metadata={
                "current_level": current_level,
                "target_level": target_level,
                "learning_style": learning_style,
                "weekly_hours": weekly_hours,
            },
        )

    def get_next_action(self) -> Optional[str]:
        """Suggest what to study next based on active learning paths."""
        active = self.storage.list_paths(status="active")
        if not active:
            return None

        # Pick the path with most momentum (highest progress but not done)
        active.sort(key=lambda p: p["progress"], reverse=True)
        top = active[0]

        path_data = self.storage.get(top["id"])
        if not path_data:
            return None

        profile_ctx = self.rag.get_profile_context()
        prompt = f"""Based on this active learning path, suggest what to study next this week.

{profile_ctx}

LEARNING PATH: {path_data["skill"]}
Progress: {path_data["completed_modules"]}/{path_data["total_modules"]} modules complete

FULL PATH:
{path_data["content"][:3000]}

Give a concise, actionable suggestion for this week's study session."""

        return self.llm_caller(PromptTemplates.SYSTEM, prompt, max_tokens=500)
