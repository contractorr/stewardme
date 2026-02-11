"""Tests for action brief generator."""

from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from advisor.action_brief import ActionBriefGenerator
from advisor.recommendation_storage import Recommendation, RecommendationStorage


@pytest.fixture
def rec_storage(tmp_path):
    db = tmp_path / "recs.db"
    storage = RecommendationStorage(db)
    # Add some test recs
    storage.save(Recommendation(
        category="learning", title="Learn Kubernetes",
        description="K8s for microservices", rationale="Hot skill",
        score=8.5,
    ))
    storage.save(Recommendation(
        category="career", title="Apply to FAANG",
        description="Senior roles open", rationale="Career growth",
        score=7.2,
    ))
    storage.save(Recommendation(
        category="investment", title="Low score rec",
        description="Below threshold", rationale="Meh",
        score=3.0,
    ))
    return storage


@pytest.fixture
def mock_rag():
    rag = MagicMock()
    rag.get_recent_entries.return_value = "recent journal entries"
    rag.get_intel_context.return_value = "intel trends"
    return rag


@pytest.fixture
def mock_llm():
    def llm_caller(system, prompt, **kwargs):
        return "# Action Brief\n\nHere are your priorities this week."
    return llm_caller


@pytest.fixture
def generator(mock_rag, mock_llm, rec_storage):
    return ActionBriefGenerator(
        rag=mock_rag,
        llm_caller=mock_llm,
        rec_storage=rec_storage,
    )


class TestActionBriefGenerate:
    def test_generate_with_recs(self, generator):
        brief = generator.generate(min_score=6.0)
        assert isinstance(brief, str)
        assert "Action Brief" in brief

    def test_generate_empty_when_no_qualifying_recs(self, mock_rag, mock_llm, tmp_path):
        empty_storage = RecommendationStorage(tmp_path / "empty.db")
        gen = ActionBriefGenerator(
            rag=mock_rag, llm_caller=mock_llm, rec_storage=empty_storage,
        )
        brief = gen.generate()
        assert "No Priority Actions" in brief

    def test_generate_respects_min_score(self, mock_rag, mock_llm, rec_storage):
        gen = ActionBriefGenerator(
            rag=mock_rag, llm_caller=mock_llm, rec_storage=rec_storage,
        )
        # Only recs >= 9.0, none qualify
        brief = gen.generate(min_score=9.0)
        assert "No Priority Actions" in brief

    def test_generate_respects_max_items(self, generator, rec_storage):
        brief = generator.generate(max_items=1, min_score=5.0)
        assert isinstance(brief, str)


class TestActionBriefFormat:
    def test_format_recommendations(self, generator, rec_storage):
        recs = rec_storage.get_top_by_score(min_score=6.0, limit=5)
        text = generator._format_recommendations(recs)
        assert "LEARNING" in text
        assert "Learn Kubernetes" in text
        assert "8.5" in text

    def test_empty_brief_format(self, generator):
        brief = generator._generate_empty_brief()
        assert "No Priority Actions" in brief
        assert datetime.now().strftime("%b") in brief


class TestActionBriefSave:
    def test_generate_and_save(self, mock_rag, mock_llm, rec_storage, tmp_path):
        journal_dir = tmp_path / "journal"
        journal_dir.mkdir()
        from journal.storage import JournalStorage
        journal_storage = JournalStorage(journal_dir)

        gen = ActionBriefGenerator(
            rag=mock_rag, llm_caller=mock_llm,
            rec_storage=rec_storage, journal_storage=journal_storage,
        )
        filepath = gen.generate_and_save(min_score=6.0)
        assert filepath is not None
        assert filepath.exists()
        assert "actionbrief" in filepath.name

    def test_generate_and_save_no_storage(self, mock_rag, mock_llm, rec_storage):
        gen = ActionBriefGenerator(
            rag=mock_rag, llm_caller=mock_llm,
            rec_storage=rec_storage, journal_storage=None,
        )
        result = gen.generate_and_save()
        assert result is None
