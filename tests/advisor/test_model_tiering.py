"""Tests for model tiering — cheap provider routing."""

from unittest.mock import MagicMock

import pytest

from advisor.recommendation_storage import RecommendationStorage
from advisor.recommendations import RecommendationEngine


class TestCheapProviderFactory:
    def test_create_cheap_provider_claude(self):
        from llm.factory import create_cheap_provider

        client = MagicMock()
        resp = MagicMock()
        resp.content = [MagicMock(text="ok")]
        client.messages.create.return_value = resp

        provider = create_cheap_provider(provider="claude", client=client)
        assert provider.model == "claude-haiku-4-5"

    def test_create_cheap_provider_respects_override(self):
        from llm.factory import create_cheap_provider

        client = MagicMock()
        resp = MagicMock()
        resp.content = [MagicMock(text="ok")]
        client.messages.create.return_value = resp

        provider = create_cheap_provider(provider="claude", model="custom-model", client=client)
        assert provider.model == "custom-model"


class TestCheapCallerRouting:
    """Verify cheap caller is used for adversarial/critic calls, not main caller."""

    @pytest.fixture
    def mock_rag(self):
        rag = MagicMock()
        rag.get_journal_context.return_value = "journal"
        rag.get_intel_context.return_value = "intel"
        rag.get_filtered_intel_context.return_value = "intel"
        rag.get_profile_context.return_value = ""
        rag.get_profile_keywords.return_value = []
        rag.get_ai_capabilities_context.return_value = "ai ctx"
        # Enough entries to pass sparse data check
        rag.search = MagicMock()
        rag.search.storage.list_entries.return_value = [{}] * 10
        return rag

    @pytest.fixture
    def storage(self, tmp_path):
        return RecommendationStorage(tmp_path / "recs")

    def test_adversarial_uses_cheap_caller(self, mock_rag, storage):
        main_calls = []
        cheap_calls = []

        def main_caller(system, prompt, **kw):
            main_calls.append(prompt[:50])
            return "### Test Rec\n**Description**: test\nSCORE: 8.0\n"

        def cheap_caller(system, prompt, **kw):
            cheap_calls.append(prompt[:50])
            return "VERDICT: SUPPORTED\nCHALLENGE: none\nCONFIDENCE: High\n"

        engine = RecommendationEngine(
            mock_rag,
            main_caller,
            storage,
            config={"scoring": {"min_threshold": 0.0}},
            cheap_llm_caller=cheap_caller,
        )
        engine.generate_category("learning", save=False, with_action_plans=False)

        # Main caller used for generation prompt
        assert len(main_calls) >= 1
        # Cheap caller used for adversarial pipeline (contradiction + critic)
        assert len(cheap_calls) >= 1
