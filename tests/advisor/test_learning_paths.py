"""Tests for learning path check-ins and deep-dive generation."""

from unittest.mock import MagicMock

import frontmatter

from advisor.learning_paths import LearningPathStorage, SubModuleGenerator
from advisor.prompts import PromptTemplates

SAMPLE_PATH_CONTENT = """# Learning Path: Python

## Overview
Learn Python from intermediate to advanced.

## Modules

### Module 1: Advanced Data Structures
**Focus**: Collections, heaps, deques
**Resources**:
- Python docs
**Project**: Build a priority queue
**Milestone**: Complete project

### Module 2: Concurrency
**Focus**: asyncio, threading
**Resources**:
- Real Python tutorials
**Project**: Build an async scraper
**Milestone**: Working scraper

### Module 3: Testing
**Focus**: pytest, mocking
**Resources**:
- pytest docs
**Project**: Test a REST API
**Milestone**: 90% coverage

## Final Project
Build a complete CLI tool.

## Success Criteria
Pass all modules.
"""


def _create_path(tmp_path, content=None, completed=0, total=3):
    """Helper: create a learning path file and return storage + path_id."""
    storage = LearningPathStorage(tmp_path / "lp")
    filepath = storage.save("Python", content or SAMPLE_PATH_CONTENT)
    post = frontmatter.load(filepath)
    path_id = post.metadata["id"]

    # Set initial progress
    if completed > 0:
        post.metadata["completed_modules"] = completed
        post.metadata["progress"] = round(completed / total * 100)
        filepath.write_text(frontmatter.dumps(post))

    return storage, path_id


class TestCheckIn:
    def test_check_in_continue_increments_progress(self, tmp_path):
        storage, path_id = _create_path(tmp_path)
        result = storage.check_in(path_id, 1, "continue")
        assert result is not None
        assert result["completed_modules"] == 1

    def test_check_in_skip_increments_progress(self, tmp_path):
        storage, path_id = _create_path(tmp_path)
        result = storage.check_in(path_id, 1, "skip")
        assert result is not None
        assert result["completed_modules"] == 1

    def test_check_in_deepen_no_progress_change(self, tmp_path):
        storage, path_id = _create_path(tmp_path)
        result = storage.check_in(path_id, 1, "deepen")
        assert result is not None
        assert result["completed_modules"] == 0

    def test_check_in_records_history(self, tmp_path):
        storage, path_id = _create_path(tmp_path)
        storage.check_in(path_id, 1, "continue")
        storage.check_in(path_id, 2, "deepen")

        path = storage.get(path_id)
        check_ins = path["check_ins"]
        assert len(check_ins) == 2
        assert check_ins[0]["action"] == "continue"
        assert check_ins[0]["module"] == 1
        assert check_ins[1]["action"] == "deepen"
        assert "timestamp" in check_ins[0]

    def test_check_in_invalid_action(self, tmp_path):
        storage, path_id = _create_path(tmp_path)
        result = storage.check_in(path_id, 1, "invalid")
        assert result is None

    def test_check_in_nonexistent_path(self, tmp_path):
        storage = LearningPathStorage(tmp_path / "lp")
        (tmp_path / "lp").mkdir(parents=True, exist_ok=True)
        result = storage.check_in("nonexistent", 1, "continue")
        assert result is None

    def test_check_in_auto_completes_path(self, tmp_path):
        storage, path_id = _create_path(tmp_path, completed=2, total=3)
        result = storage.check_in(path_id, 3, "continue")
        assert result is not None
        assert result["status"] == "completed"
        assert result["completed_modules"] == 3
        assert result["progress"] == 100


class TestSubModuleGenerator:
    def test_generate_deep_dive_injects_content(self, tmp_path):
        storage, path_id = _create_path(tmp_path)
        mock_llm = MagicMock(return_value="#### Deep Dive\n\nDeep content here.")
        gen = SubModuleGenerator(mock_llm, storage)

        result = gen.generate_deep_dive(path_id, 1)
        assert result is not None
        assert "#### Deep Dive" in result

        # Verify injected into file
        path = storage.get(path_id)
        assert "#### Deep Dive" in path["content"]
        assert "Deep content here." in path["content"]

    def test_deep_dive_placed_before_next_module(self, tmp_path):
        storage, path_id = _create_path(tmp_path)
        mock_llm = MagicMock(return_value="#### Deep Dive\n\nExtra detail.")
        gen = SubModuleGenerator(mock_llm, storage)

        gen.generate_deep_dive(path_id, 1)

        path = storage.get(path_id)
        content = path["content"]
        dive_pos = content.index("#### Deep Dive")
        mod2_pos = content.index("### Module 2")
        assert dive_pos < mod2_pos

    def test_deep_dive_nonexistent_path(self, tmp_path):
        storage = LearningPathStorage(tmp_path / "lp")
        (tmp_path / "lp").mkdir(parents=True, exist_ok=True)
        mock_llm = MagicMock()
        gen = SubModuleGenerator(mock_llm, storage)
        assert gen.generate_deep_dive("nonexistent", 1) is None

    def test_deep_dive_nonexistent_module(self, tmp_path):
        storage, path_id = _create_path(tmp_path)
        mock_llm = MagicMock()
        gen = SubModuleGenerator(mock_llm, storage)
        assert gen.generate_deep_dive(path_id, 99) is None


class TestCheckInAnalysis:
    def test_feedback_prompt_formatted(self):
        result = PromptTemplates.CHECK_IN_ANALYSIS.format(
            skill="Python",
            module_number=2,
            module_title="Concurrency",
            action="deepen",
            check_in_history="[{module: 1, action: continue}]",
            completed=1,
            total=3,
        )
        assert "Python" in result
        assert "Concurrency" in result
        assert "deepen" in result
        assert "1" in result and "3" in result
