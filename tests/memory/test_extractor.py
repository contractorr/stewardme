"""Tests for FactExtractor with mocked LLM."""

import json
from unittest.mock import MagicMock

import pytest

from memory.extractor import FactExtractor
from memory.models import FactCategory, FactSource


@pytest.fixture
def provider():
    return MagicMock()


@pytest.fixture
def extractor(provider):
    return FactExtractor(provider=provider, max_facts_per_entry=5)


class TestJournalExtraction:
    def test_happy_path(self, extractor, provider):
        provider.generate.return_value = json.dumps(
            [
                {
                    "text": "User prefers Axum over Actix",
                    "category": "preference",
                    "confidence": 0.85,
                },
                {"text": "User is building a Rust API", "category": "context", "confidence": 0.9},
            ]
        )
        facts = extractor.extract_from_journal(
            "entry-1", "Tried Axum today, way better than Actix."
        )
        assert len(facts) == 2
        assert facts[0].text == "User prefers Axum over Actix"
        assert facts[0].category == FactCategory.PREFERENCE
        assert facts[0].source_type == FactSource.JOURNAL
        assert facts[0].source_id == "entry-1"

    def test_skips_short_entries(self, extractor):
        facts = extractor.extract_from_journal("e1", "ok")
        assert facts == []

    def test_respects_max_facts(self, extractor, provider):
        provider.generate.return_value = json.dumps(
            [{"text": f"Fact {i}", "category": "context", "confidence": 0.8} for i in range(10)]
        )
        facts = extractor.extract_from_journal("e1", "A" * 100)
        assert len(facts) <= 5

    def test_filters_low_confidence(self, extractor, provider):
        provider.generate.return_value = json.dumps(
            [
                {"text": "Weak signal", "category": "context", "confidence": 0.3},
                {"text": "Strong signal", "category": "context", "confidence": 0.8},
            ]
        )
        facts = extractor.extract_from_journal("e1", "Some journal entry content here.")
        assert len(facts) == 1
        assert facts[0].text == "Strong signal"

    def test_filters_invalid_category(self, extractor, provider):
        provider.generate.return_value = json.dumps(
            [
                {"text": "Valid", "category": "skill", "confidence": 0.8},
                {"text": "Invalid cat", "category": "invalid_cat", "confidence": 0.8},
            ]
        )
        facts = extractor.extract_from_journal("e1", "Some content for extraction here.")
        assert len(facts) == 1

    def test_handles_llm_error(self, extractor, provider):
        provider.generate.side_effect = Exception("API error")
        facts = extractor.extract_from_journal("e1", "Some journal content for extraction.")
        assert facts == []

    def test_handles_malformed_json(self, extractor, provider):
        provider.generate.return_value = "not json at all"
        facts = extractor.extract_from_journal("e1", "Some content that we try to extract from.")
        assert facts == []

    def test_strips_markdown_fences(self, extractor, provider):
        provider.generate.return_value = (
            '```json\n[{"text": "Fact", "category": "skill", "confidence": 0.8}]\n```'
        )
        facts = extractor.extract_from_journal("e1", "Some content to extract facts from here.")
        assert len(facts) == 1


class TestFeedbackExtraction:
    def test_thumbs_down(self, extractor, provider):
        provider.generate.return_value = json.dumps(
            [
                {
                    "text": "User not interested in Java",
                    "category": "preference",
                    "confidence": 0.75,
                },
            ]
        )
        facts = extractor.extract_from_feedback(
            "rec-1",
            "thumbs_down",
            {"title": "Learn Java", "description": "Java tutorial recommendation"},
        )
        assert len(facts) == 1
        assert facts[0].source_type == FactSource.FEEDBACK
        assert facts[0].source_id == "rec-1"

    def test_thumbs_up(self, extractor, provider):
        provider.generate.return_value = json.dumps(
            [
                {"text": "User interested in Rust", "category": "preference", "confidence": 0.7},
            ]
        )
        facts = extractor.extract_from_feedback("rec-2", "useful", {"title": "Rust book"})
        assert len(facts) == 1


class TestGoalExtraction:
    def test_goal_created(self, extractor, provider):
        provider.generate.return_value = json.dumps(
            [
                {
                    "text": "User actively learning Rust",
                    "category": "goal_context",
                    "confidence": 0.95,
                },
            ]
        )
        facts = extractor.extract_from_goal(
            "goal-1", {"title": "Learn Rust", "event_type": "created", "tags": ["rust"]}
        )
        assert len(facts) == 1
        assert facts[0].source_type == FactSource.GOAL
        assert facts[0].category == FactCategory.GOAL_CONTEXT
