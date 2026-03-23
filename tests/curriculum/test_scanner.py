"""Tests for curriculum scanner."""

from pathlib import Path

import pytest

from curriculum.models import GuideCategory
from curriculum.scanner import CurriculumScanner, _detect_diagrams, _extract_title, _infer_category


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
