"""Scan content directories to discover guides and chapters."""

import hashlib
import re
from pathlib import Path

import structlog

from .models import Chapter, DifficultyLevel, Guide, GuideCategory

logger = structlog.get_logger()

# Regex for extracting order prefix from filenames like "01-introduction.md"
_ORDER_RE = re.compile(r"^(\d+)-")

# Box-drawing characters (U+2500–U+257F) and common ASCII art patterns
_BOX_DRAWING_RE = re.compile(r"[\u2500-\u257F]")
_ASCII_ART_RE = re.compile(r"[+|]\-{3,}[+|]|[+|]{2,}\-|─{3,}|═{3,}|╔|╗|╚|╝|├|┤|┌|┐|└|┘")
_TABLE_SEP_RE = re.compile(r"^\s*[-|:]+\s*$")
_FORMULA_RE = re.compile(r"\$[^$]+\$|\\frac|\\sum|\\int|\\sqrt|∑|∫|√|≈|≠|≤|≥|∈|∀|∃")

# Words per minute for reading time estimates
_WPM = 250

# Category inference from directory name keywords
_CATEGORY_KEYWORDS: dict[str, GuideCategory] = {
    "philosophy": GuideCategory.HUMANITIES,
    "epistemology": GuideCategory.HUMANITIES,
    "religion": GuideCategory.HUMANITIES,
    "theology": GuideCategory.HUMANITIES,
    "history": GuideCategory.HUMANITIES,
    "linguistics": GuideCategory.HUMANITIES,
    "world-history": GuideCategory.HUMANITIES,
    "mathematics": GuideCategory.SCIENCE,
    "statistics": GuideCategory.SCIENCE,
    "physics": GuideCategory.SCIENCE,
    "chemistry": GuideCategory.SCIENCE,
    "biology": GuideCategory.SCIENCE,
    "genetics": GuideCategory.SCIENCE,
    "ecology": GuideCategory.SCIENCE,
    "geology": GuideCategory.SCIENCE,
    "oceanography": GuideCategory.SCIENCE,
    "climate": GuideCategory.SCIENCE,
    "energy": GuideCategory.SCIENCE,
    "medicine": GuideCategory.SCIENCE,
    "neuroscience": GuideCategory.SCIENCE,
    "cognitive": GuideCategory.SCIENCE,
    "economics": GuideCategory.BUSINESS,
    "accounting": GuideCategory.BUSINESS,
    "finance": GuideCategory.BUSINESS,
    "mba": GuideCategory.BUSINESS,
    "private-markets": GuideCategory.BUSINESS,
    "game-theory": GuideCategory.SOCIAL_SCIENCE,
    "psychology": GuideCategory.SOCIAL_SCIENCE,
    "sociology": GuideCategory.SOCIAL_SCIENCE,
    "demography": GuideCategory.SOCIAL_SCIENCE,
    "government": GuideCategory.SOCIAL_SCIENCE,
    "politics": GuideCategory.SOCIAL_SCIENCE,
    "law": GuideCategory.SOCIAL_SCIENCE,
    "geopolitics": GuideCategory.SOCIAL_SCIENCE,
    "computer-science": GuideCategory.TECHNOLOGY,
    "ai-ml": GuideCategory.TECHNOLOGY,
    "cybersecurity": GuideCategory.TECHNOLOGY,
    "engineering": GuideCategory.TECHNOLOGY,
    "information-theory": GuideCategory.TECHNOLOGY,
    "agriculture": GuideCategory.SCIENCE,
    "complex-systems": GuideCategory.SCIENCE,
}

_INDUSTRY_CATEGORY = GuideCategory.INDUSTRY

# Difficulty heuristics based on guide order (lower = more introductory)
_ADVANCED_KEYWORDS = {"private-markets", "geopolitics", "cybersecurity", "ai-ml"}
_INTRO_KEYWORDS = {"introduction", "fundamentals", "crash-course"}


def _infer_category(dir_name: str, is_industry: bool = False) -> GuideCategory:
    if is_industry:
        return _INDUSTRY_CATEGORY
    lower = dir_name.lower()
    for keyword, cat in _CATEGORY_KEYWORDS.items():
        if keyword in lower:
            return cat
    return GuideCategory.PROFESSIONAL


def _infer_difficulty(dir_name: str, order: int) -> DifficultyLevel:
    lower = dir_name.lower()
    if any(kw in lower for kw in _ADVANCED_KEYWORDS):
        return DifficultyLevel.ADVANCED
    if any(kw in lower for kw in _INTRO_KEYWORDS) or order <= 5:
        return DifficultyLevel.INTRODUCTORY
    if order <= 20:
        return DifficultyLevel.INTERMEDIATE
    return DifficultyLevel.ADVANCED


def _extract_title(content: str, filename: str) -> str:
    """Extract title from first H1 heading or derive from filename."""
    for line in content.split("\n", 10):
        line = line.strip()
        if line.startswith("# ") and not line.startswith("## "):
            return line[2:].strip()
    # Fallback: derive from filename
    stem = Path(filename).stem
    m = _ORDER_RE.match(stem)
    if m:
        stem = stem[m.end() :]
    return stem.replace("-", " ").replace("_", " ").title()


def _detect_diagrams(content: str) -> bool:
    return bool(_BOX_DRAWING_RE.search(content) or _ASCII_ART_RE.search(content))


def _detect_tables(content: str) -> bool:
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if "|" in line and i + 1 < len(lines) and _TABLE_SEP_RE.match(lines[i + 1]):
            return True
    return False


def _detect_formulas(content: str) -> bool:
    return bool(_FORMULA_RE.search(content))


def _content_hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def _guide_title_from_dir(dir_name: str) -> str:
    """Derive guide title from directory name."""
    m = _ORDER_RE.match(dir_name)
    stem = dir_name[m.end() :] if m else dir_name
    # Remove trailing -guide, -curriculum, -crash-course
    for suffix in ["-guide", "-curriculum", "-crash-course"]:
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
    return stem.replace("-", " ").replace("_", " ").title()


def _guide_order(dir_name: str) -> int:
    m = _ORDER_RE.match(dir_name)
    return int(m.group(1)) if m else 99


class CurriculumScanner:
    """Walks content directories and discovers guides + chapters."""

    def __init__(self, content_dirs: list[Path]):
        self.content_dirs = [Path(d).expanduser().resolve() for d in content_dirs]

    def scan(self) -> tuple[list[Guide], list[Chapter]]:
        """Scan all content dirs and return (guides, chapters)."""
        guides: list[Guide] = []
        chapters: list[Chapter] = []
        seen_guide_ids: set[str] = set()

        for content_dir in self.content_dirs:
            if not content_dir.exists():
                logger.warning("curriculum.scan.dir_missing", path=str(content_dir))
                continue
            self._scan_dir(content_dir, guides, chapters, seen_guide_ids)

        guides.sort(key=lambda g: (_guide_order(g.id), g.title))
        return guides, chapters

    def _scan_dir(
        self,
        base: Path,
        guides: list[Guide],
        chapters: list[Chapter],
        seen: set[str],
    ) -> None:
        # Look for NN-*-guide/ directories and Industries/ subdirs
        for entry in sorted(base.iterdir()):
            if not entry.is_dir():
                continue
            name = entry.name

            if name == "Industries":
                self._scan_industries(entry, guides, chapters, seen)
                continue

            # Skip hidden dirs and non-guide dirs
            if name.startswith("."):
                continue

            # Any dir containing .md files is a guide
            md_files = sorted(entry.glob("*.md"))
            if not md_files:
                continue

            if name in seen:
                continue
            seen.add(name)

            guide, guide_chapters = self._build_guide(entry, name, md_files, is_industry=False)
            guides.append(guide)
            chapters.extend(guide_chapters)

    def _scan_industries(
        self,
        industries_dir: Path,
        guides: list[Guide],
        chapters: list[Chapter],
        seen: set[str],
    ) -> None:
        for entry in sorted(industries_dir.iterdir()):
            if not entry.is_dir() or entry.name.startswith("."):
                continue
            md_files = sorted(entry.glob("*.md"))
            if not md_files:
                continue

            guide_id = f"industry-{entry.name.lower()}"
            if guide_id in seen:
                continue
            seen.add(guide_id)

            guide, guide_chapters = self._build_guide(entry, guide_id, md_files, is_industry=True)
            guide.title = f"{entry.name} Industry"
            guides.append(guide)
            chapters.extend(guide_chapters)

    def _build_guide(
        self,
        guide_dir: Path,
        guide_id: str,
        md_files: list[Path],
        is_industry: bool,
    ) -> tuple[Guide, list[Chapter]]:
        order = _guide_order(guide_id)
        guide_chapters: list[Chapter] = []
        total_words = 0
        has_glossary = False

        for idx, md_file in enumerate(md_files):
            try:
                content = md_file.read_text(encoding="utf-8")
            except Exception:
                logger.warning("curriculum.scan.read_error", file=str(md_file))
                continue

            words = len(content.split())
            total_words += words
            title = _extract_title(content, md_file.name)
            is_glossary = "glossary" in md_file.stem.lower()
            if is_glossary:
                has_glossary = True

            chapter_id = f"{guide_id}/{md_file.stem}"
            chapter = Chapter(
                id=chapter_id,
                guide_id=guide_id,
                title=title,
                filename=md_file.name,
                order=idx,
                word_count=words,
                reading_time_minutes=max(1, words // _WPM),
                has_diagrams=_detect_diagrams(content),
                has_tables=_detect_tables(content),
                has_formulas=_detect_formulas(content),
                is_glossary=is_glossary,
                content_hash=_content_hash(content),
            )
            guide_chapters.append(chapter)

        reading_time = sum(c.reading_time_minutes for c in guide_chapters)

        # Infer prerequisites from ordering
        prereqs: list[str] = []
        if order > 1 and not is_industry:
            # Previous numbered guide is a soft prereq
            prev = f"{order - 1:02d}-"
            for d in (guide_dir.parent).iterdir():
                if d.is_dir() and d.name.startswith(prev):
                    prereqs.append(d.name)
                    break

        guide = Guide(
            id=guide_id,
            title=_guide_title_from_dir(guide_id),
            category=_infer_category(guide_id, is_industry),
            difficulty=_infer_difficulty(guide_id, order),
            source_dir=str(guide_dir),
            chapter_count=len(guide_chapters),
            total_word_count=total_words,
            total_reading_time_minutes=reading_time,
            has_glossary=has_glossary,
            prerequisites=prereqs,
        )
        return guide, guide_chapters
