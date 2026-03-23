"""Tests for curriculum scanner."""

from pathlib import Path

import pytest

from curriculum.models import GuideCategory
from curriculum.scanner import (
    CurriculumScanner,
    _detect_diagrams,
    _extract_title,
    _infer_category,
    build_tree_layout,
    load_skill_tree,
)


@pytest.fixture
def content_dir(tmp_path):
    """Create a minimal content directory structure."""
    # Guide 1
    guide1 = tmp_path / "01-philosophy-guide"
    guide1.mkdir()
    (guide1 / "01-introduction.md").write_text(
        "# Introduction to Philosophy\n\nOverview of philosophy.\n"
    )
    (guide1 / "02-logic.md").write_text("# Logic and Reasoning\n\nFormal logic basics.\n")
    (guide1 / "03-glossary.md").write_text("# Glossary\n\nTerms and definitions.\n")

    # Guide 2
    guide2 = tmp_path / "02-economics-guide"
    guide2.mkdir()
    (guide2 / "01-introduction.md").write_text(
        "# Introduction to Economics\n\nSupply and demand.\n"
    )

    # Industry guide
    industries = tmp_path / "Industries" / "Healthcare"
    industries.mkdir(parents=True)
    (industries / "healthcare-crash-course.md").write_text(
        "# Healthcare Industry Overview\n\nHealthcare sector analysis.\n"
    )

    return tmp_path


def test_scan_discovers_guides(content_dir):
    scanner = CurriculumScanner([content_dir])
    guides, chapters = scanner.scan()

    assert len(guides) >= 3  # 2 regular + 1 industry
    guide_ids = {g.id for g in guides}
    assert "01-philosophy-guide" in guide_ids
    assert "02-economics-guide" in guide_ids
    assert "industry-healthcare" in guide_ids


def test_scan_discovers_chapters(content_dir):
    scanner = CurriculumScanner([content_dir])
    guides, chapters = scanner.scan()

    # Philosophy guide has 3 chapters
    phil_chapters = [c for c in chapters if c.guide_id == "01-philosophy-guide"]
    assert len(phil_chapters) == 3


def test_chapter_properties(content_dir):
    scanner = CurriculumScanner([content_dir])
    _, chapters = scanner.scan()

    intro = next(c for c in chapters if c.id == "01-philosophy-guide/01-introduction")
    assert intro.title == "Introduction to Philosophy"
    assert intro.word_count > 0
    assert intro.reading_time_minutes >= 1
    assert not intro.is_glossary

    glossary = next(c for c in chapters if c.id == "01-philosophy-guide/03-glossary")
    assert glossary.is_glossary


def test_guide_has_glossary_flag(content_dir):
    scanner = CurriculumScanner([content_dir])
    guides, _ = scanner.scan()

    phil = next(g for g in guides if g.id == "01-philosophy-guide")
    assert phil.has_glossary

    econ = next(g for g in guides if g.id == "02-economics-guide")
    assert not econ.has_glossary


def test_prerequisites_inferred(content_dir):
    scanner = CurriculumScanner([content_dir])
    guides, _ = scanner.scan()

    econ = next(g for g in guides if g.id == "02-economics-guide")
    assert "01-philosophy-guide" in econ.prerequisites


def test_industry_guide_category(content_dir):
    scanner = CurriculumScanner([content_dir])
    guides, _ = scanner.scan()

    hc = next(g for g in guides if g.id == "industry-healthcare")
    assert hc.category == GuideCategory.INDUSTRY


def test_extract_title_from_h1():
    assert _extract_title("# My Title\n\nContent", "file.md") == "My Title"


def test_extract_title_fallback():
    assert _extract_title("No heading here\nJust text", "03-my-topic.md") == "My Topic"


def test_detect_diagrams():
    assert _detect_diagrams("┌──────┐\n│ box  │\n└──────┘")
    assert _detect_diagrams("+----+\n| hi |\n+----+")
    assert not _detect_diagrams("Just regular text here")


def test_infer_category():
    assert _infer_category("economics-guide") == GuideCategory.BUSINESS
    assert _infer_category("physics-fundamentals") == GuideCategory.SCIENCE
    assert _infer_category("computer-science-algorithms") == GuideCategory.TECHNOLOGY
    assert _infer_category("unknown-topic") == GuideCategory.PROFESSIONAL


def test_missing_dir_handled():
    scanner = CurriculumScanner([Path("/nonexistent/path")])
    guides, chapters = scanner.scan()
    assert guides == []
    assert chapters == []


def test_content_hash_deterministic(content_dir):
    scanner = CurriculumScanner([content_dir])
    _, chapters1 = scanner.scan()
    _, chapters2 = scanner.scan()

    for c1, c2 in zip(chapters1, chapters2):
        assert c1.content_hash == c2.content_hash


# --- Skill tree tests ---


@pytest.fixture
def content_dir_with_manifest(content_dir):
    """Add a skill_tree.yaml to content_dir."""
    manifest = content_dir / "skill_tree.yaml"
    manifest.write_text(
        """version: 1
tracks:
  foundations:
    title: "Foundations"
    description: "Core frameworks"
    color: "#6366f1"
    guides:
      - id: "01-philosophy-guide"
        prerequisites: []
      - id: "02-economics-guide"
        prerequisites: ["01-philosophy-guide"]
  industry:
    title: "Industry"
    description: "Sector deep dives"
    color: "#ef4444"
    guides:
      - id: "industry-healthcare"
        prerequisites: ["01-philosophy-guide"]
"""
    )
    return content_dir


def test_skill_tree_loaded(content_dir_with_manifest):
    """Manifest overrides auto-inferred prereqs."""
    scanner = CurriculumScanner([content_dir_with_manifest])
    guides, _ = scanner.scan()

    econ = next(g for g in guides if g.id == "02-economics-guide")
    assert econ.prerequisites == ["01-philosophy-guide"]

    phil = next(g for g in guides if g.id == "01-philosophy-guide")
    assert phil.prerequisites == []


def test_skill_tree_sets_track(content_dir_with_manifest):
    scanner = CurriculumScanner([content_dir_with_manifest])
    guides, _ = scanner.scan()

    phil = next(g for g in guides if g.id == "01-philosophy-guide")
    assert phil.track == "foundations"

    hc = next(g for g in guides if g.id == "industry-healthcare")
    assert hc.track == "industry"


def test_skill_tree_missing_fallback(content_dir):
    """No manifest = auto-inferred prereqs, empty track."""
    scanner = CurriculumScanner([content_dir])
    guides, _ = scanner.scan()

    econ = next(g for g in guides if g.id == "02-economics-guide")
    assert "01-philosophy-guide" in econ.prerequisites
    assert econ.track == ""


def test_skill_tree_guide_not_in_manifest(content_dir_with_manifest):
    """Guide not listed in manifest gets empty track/prereqs."""
    # Add a guide not in the manifest
    extra = content_dir_with_manifest / "99-unknown-guide"
    extra.mkdir()
    (extra / "01-intro.md").write_text("# Unknown\n\nContent.\n")

    scanner = CurriculumScanner([content_dir_with_manifest])
    guides, _ = scanner.scan()

    unknown = next(g for g in guides if g.id == "99-unknown-guide")
    assert unknown.track == ""
    assert unknown.prerequisites == []


def test_load_skill_tree_invalid_yaml(tmp_path):
    manifest = tmp_path / "skill_tree.yaml"
    manifest.write_text("{{invalid yaml content")
    result = load_skill_tree(tmp_path)
    assert result is None


def test_get_track_metadata(content_dir_with_manifest):
    scanner = CurriculumScanner([content_dir_with_manifest])
    meta = scanner.get_track_metadata()

    assert "foundations" in meta
    assert meta["foundations"]["title"] == "Foundations"
    assert meta["foundations"]["color"] == "#6366f1"
    assert "industry" in meta


# --- build_tree_layout tests ---


def test_build_tree_layout_basic():
    """Entry points at depth 0, dependents at depth 1."""
    skill_tree = (
        {
            "A": [],
            "B": ["A"],
            "C": ["A"],
        },
        {"A": "t1", "B": "t1", "C": "t1"},
        {"t1": {"title": "Track 1", "description": "", "color": "#000"}},
    )
    positions = build_tree_layout(skill_tree)
    assert positions["A"]["depth"] == 0
    assert positions["B"]["depth"] == 1
    assert positions["C"]["depth"] == 1


def test_build_tree_layout_diamond():
    """A→B, A→C, B→D, C→D — D should be at depth 2."""
    skill_tree = (
        {
            "A": [],
            "B": ["A"],
            "C": ["A"],
            "D": ["B", "C"],
        },
        {"A": "t1", "B": "t1", "C": "t1", "D": "t1"},
        {"t1": {"title": "Track 1", "description": "", "color": "#000"}},
    )
    positions = build_tree_layout(skill_tree)
    assert positions["A"]["depth"] == 0
    assert positions["B"]["depth"] == 1
    assert positions["C"]["depth"] == 1
    assert positions["D"]["depth"] == 2


def test_build_tree_layout_no_manifest():
    """None skill_tree returns empty dict."""
    assert build_tree_layout(None) == {}
