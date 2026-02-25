"""Adversarial pipeline integration tests with prompt-aware mock LLM."""

from unittest.mock import Mock

import pytest

from advisor.recommendation_storage import Recommendation, RecommendationStorage
from advisor.recommendations import Recommender
from advisor.scoring import RecommendationScorer

# -- Structured mock responses --

INTEL_CHECK_SUPPORTED = """\
CONTRADICTIONS: None found
NUANCE: None
VERDICT: SUPPORTED"""

INTEL_CHECK_CONTRADICTED = """\
CONTRADICTIONS: Recent HN discussion suggests Rust adoption is slowing in web backends
NUANCE: Only applies to web use cases, systems programming demand still strong
VERDICT: CONTRADICTED"""

INTEL_CHECK_COMPLICATED = """\
CONTRADICTIONS: Mixed signals — some companies adopting, others reverting to Go
NUANCE: The landscape is shifting quickly; timing matters
VERDICT: COMPLICATED"""

CRITIC_RESPONSE_HIGH = """\
CHALLENGE: The recommendation assumes continued growth but ignores recent consolidation in the space.
MISSING_CONTEXT: No data on the user's available time commitment or existing skill level.
ALTERNATIVE: Consider focusing on Go instead given broader industry adoption.
CONFIDENCE: High
CONFIDENCE_RATIONALE: Strong evidence from multiple intel sources supports the core thesis."""

CRITIC_RESPONSE_MEDIUM = """\
CHALLENGE: Market signals are mixed and the recommendation may be premature.
MISSING_CONTEXT: User's financial situation and risk tolerance are unknown.
ALTERNATIVE: A phased approach starting with a smaller commitment would reduce risk.
CONFIDENCE: Medium
CONFIDENCE_RATIONALE: Reasonable recommendation but material uncertainty exists."""

CRITIC_RESPONSE_LOW = """\
CHALLENGE: This recommendation contradicts multiple recent data points.
MISSING_CONTEXT: The underlying technology may be deprecated within 12 months.
ALTERNATIVE: Pivot to the successor technology instead.
CONFIDENCE: Low
CONFIDENCE_RATIONALE: Significant chance this advice is outdated given recent shifts."""

CRITIC_RESPONSE_VERBOSE_CONFIDENCE = """\
CHALLENGE: Overly optimistic about adoption timeline.
MISSING_CONTEXT: Competitor landscape not considered.
ALTERNATIVE: null
CONFIDENCE: High — strong evidence from multiple sources
CONFIDENCE_RATIONALE: Well-supported by recent trends despite the challenge."""

CRITIC_RESPONSE_NULL_ALTERNATIVE = """\
CHALLENGE: Minor concerns about implementation complexity.
MISSING_CONTEXT: Team size and existing infrastructure unknown.
ALTERNATIVE: null
CONFIDENCE: Medium
CONFIDENCE_RATIONALE: Broadly correct but execution risk is real."""


def _make_mock_llm(intel_response=INTEL_CHECK_SUPPORTED, critic_response=CRITIC_RESPONSE_HIGH):
    """Build prompt-aware mock LLM that routes by prompt content."""

    def _mock_llm_by_prompt(system, prompt, **kwargs):
        # Check "contrarian" first — unique to critic prompt.
        # "contradict" appears in both intel check AND critic (via {intel_contradictions}).
        if "contrarian" in prompt.lower():
            return critic_response
        if "contradict" in prompt.lower():
            return intel_response
        # Default: standard recommendation text
        return """\
### Test Recommendation
**Description**: A test recommendation
SCORE: 8.0
SOURCE: test source
CONFIDENCE: 0.8
"""

    return _mock_llm_by_prompt


@pytest.fixture
def storage(tmp_path):
    return RecommendationStorage(tmp_path / "recs")


@pytest.fixture
def mock_rag():
    rag = Mock()
    rag.get_journal_context.return_value = "User wants to learn Rust"
    rag.get_intel_context.return_value = "Rust demand growing 40%"
    rag.get_filtered_intel_context.return_value = "Rust demand growing 40%"
    rag.get_profile_context.return_value = "Software engineer interested in systems programming"
    rag.get_profile_keywords.return_value = ["rust", "systems"]
    return rag


def _make_recommender(mock_rag, storage, cheap_llm):
    """Helper to build a Recommender with zero threshold."""
    scorer = RecommendationScorer(min_threshold=0.0)
    return Recommender(mock_rag, cheap_llm, scorer, storage, cheap_llm_caller=cheap_llm)


def _make_rec(**overrides):
    defaults = dict(
        category="learning",
        title="Learn Rust Async",
        description="Master async programming in Rust",
        rationale="Strong demand in systems programming",
        score=8.0,
        metadata={},
    )
    defaults.update(overrides)
    return Recommendation(**defaults)


# ===== Intel Contradiction Check =====


class TestIntelContradictionCheck:
    def test_intel_check_supported(self, mock_rag, storage):
        """VERDICT: SUPPORTED → returns None."""
        llm = _make_mock_llm(intel_response=INTEL_CHECK_SUPPORTED)
        recommender = _make_recommender(mock_rag, storage, llm)
        rec = _make_rec()
        result = recommender._run_intel_contradiction_check(rec)
        assert result is None

    def test_intel_check_contradicted(self, mock_rag, storage):
        """VERDICT: CONTRADICTED → returns full response string."""
        llm = _make_mock_llm(intel_response=INTEL_CHECK_CONTRADICTED)
        recommender = _make_recommender(mock_rag, storage, llm)
        rec = _make_rec()
        result = recommender._run_intel_contradiction_check(rec)
        assert result is not None
        assert "CONTRADICTED" in result
        assert "Rust adoption is slowing" in result

    def test_intel_check_complicated(self, mock_rag, storage):
        """VERDICT: COMPLICATED → returns full response string."""
        llm = _make_mock_llm(intel_response=INTEL_CHECK_COMPLICATED)
        recommender = _make_recommender(mock_rag, storage, llm)
        rec = _make_rec()
        result = recommender._run_intel_contradiction_check(rec)
        assert result is not None
        assert "COMPLICATED" in result

    def test_intel_check_no_intel(self, mock_rag, storage):
        """Empty/no intel context → returns None (early exit)."""
        mock_rag_empty = Mock()
        mock_rag_empty.get_intel_context.return_value = "No relevant intel found"
        llm = _make_mock_llm()
        recommender = _make_recommender(mock_rag_empty, storage, llm)
        rec = _make_rec()
        result = recommender._run_intel_contradiction_check(rec)
        assert result is None


# ===== Adversarial Critic Parsing =====


class TestAdversarialCritic:
    def test_critic_parses_all_fields(self, mock_rag, storage):
        """All 5 fields parsed correctly from realistic response."""
        llm = _make_mock_llm(critic_response=CRITIC_RESPONSE_HIGH)
        recommender = _make_recommender(mock_rag, storage, llm)
        rec = _make_rec()
        result = recommender._run_adversarial_critic(
            rec, "profile ctx", "intel ctx", "None provided", None
        )
        assert result is not None
        assert "challenge" in result
        assert "missing_context" in result
        assert "alternative" in result
        assert "confidence" in result
        assert "confidence_rationale" in result
        assert "assumes continued growth" in result["challenge"]
        assert "Consider focusing on Go" in result["alternative"]

    def test_critic_confidence_high(self, mock_rag, storage):
        """'High' extracted, maps to 0.85 in reasoning_trace."""
        llm = _make_mock_llm(critic_response=CRITIC_RESPONSE_HIGH)
        recommender = _make_recommender(mock_rag, storage, llm)
        rec = _make_rec()
        result = recommender._run_adversarial_critic(
            rec, "profile ctx", "intel ctx", "None provided", None
        )
        assert result["confidence"] == "High"

    def test_critic_confidence_medium(self, mock_rag, storage):
        """'Medium' extracted, maps to 0.55."""
        llm = _make_mock_llm(critic_response=CRITIC_RESPONSE_MEDIUM)
        recommender = _make_recommender(mock_rag, storage, llm)
        rec = _make_rec()
        result = recommender._run_adversarial_critic(
            rec, "profile ctx", "intel ctx", "None provided", None
        )
        assert result["confidence"] == "Medium"

    def test_critic_confidence_low(self, mock_rag, storage):
        """'Low' extracted, maps to 0.25."""
        llm = _make_mock_llm(critic_response=CRITIC_RESPONSE_LOW)
        recommender = _make_recommender(mock_rag, storage, llm)
        rec = _make_rec()
        result = recommender._run_adversarial_critic(
            rec, "profile ctx", "intel ctx", "None provided", None
        )
        assert result["confidence"] == "Low"

    def test_critic_confidence_verbose(self, mock_rag, storage):
        """'High — strong evidence' still extracts 'High'."""
        llm = _make_mock_llm(critic_response=CRITIC_RESPONSE_VERBOSE_CONFIDENCE)
        recommender = _make_recommender(mock_rag, storage, llm)
        rec = _make_rec()
        result = recommender._run_adversarial_critic(
            rec, "profile ctx", "intel ctx", "None provided", None
        )
        assert result["confidence"] == "High"

    def test_critic_alternative_null(self, mock_rag, storage):
        """ALTERNATIVE: null → raw value is 'null' string."""
        llm = _make_mock_llm(critic_response=CRITIC_RESPONSE_NULL_ALTERNATIVE)
        recommender = _make_recommender(mock_rag, storage, llm)
        rec = _make_rec()
        result = recommender._run_adversarial_critic(
            rec, "profile ctx", "intel ctx", "None provided", None
        )
        assert result["alternative"] == "null"


# ===== Full Pipeline Integration =====


class TestAdversarialPipeline:
    def test_pipeline_sets_all_metadata(self, mock_rag, storage):
        """After full pipeline, rec.metadata has all critic fields."""
        llm = _make_mock_llm(
            intel_response=INTEL_CHECK_SUPPORTED,
            critic_response=CRITIC_RESPONSE_HIGH,
        )
        recommender = _make_recommender(mock_rag, storage, llm)
        rec = _make_rec()
        recommender._run_adversarial_pipeline(rec, "profile ctx", "intel ctx")

        meta = rec.metadata
        assert meta["confidence"] == "High"
        assert "assumes continued growth" in meta["critic_challenge"]
        assert "available time" in meta["missing_context"]
        assert "Go" in meta["alternative"]
        assert "Strong evidence" in meta["confidence_rationale"]
        # reasoning_trace confidence mapped from High
        assert meta["reasoning_trace"]["confidence"] == 0.85

    def test_pipeline_with_contradictions(self, mock_rag, storage):
        """Intel contradictions passed through to metadata and critic."""
        llm = _make_mock_llm(
            intel_response=INTEL_CHECK_CONTRADICTED,
            critic_response=CRITIC_RESPONSE_MEDIUM,
        )
        recommender = _make_recommender(mock_rag, storage, llm)
        rec = _make_rec()
        recommender._run_adversarial_pipeline(rec, "profile ctx", "intel ctx")

        meta = rec.metadata
        assert "intel_contradictions" in meta
        assert "CONTRADICTED" in meta["intel_contradictions"]
        assert meta["confidence"] == "Medium"
        assert meta["reasoning_trace"]["confidence"] == 0.55

    def test_pipeline_null_alternative_becomes_none(self, mock_rag, storage):
        """ALTERNATIVE: null in critic → metadata['alternative'] is None."""
        llm = _make_mock_llm(
            intel_response=INTEL_CHECK_SUPPORTED,
            critic_response=CRITIC_RESPONSE_NULL_ALTERNATIVE,
        )
        recommender = _make_recommender(mock_rag, storage, llm)
        rec = _make_rec()
        recommender._run_adversarial_pipeline(rec, "profile ctx", "intel ctx")

        assert rec.metadata["alternative"] is None

    def test_pipeline_low_confidence_maps_correctly(self, mock_rag, storage):
        """Low confidence → 0.25 in reasoning_trace."""
        llm = _make_mock_llm(
            intel_response=INTEL_CHECK_COMPLICATED,
            critic_response=CRITIC_RESPONSE_LOW,
        )
        recommender = _make_recommender(mock_rag, storage, llm)
        rec = _make_rec()
        recommender._run_adversarial_pipeline(rec, "profile ctx", "intel ctx")

        assert rec.metadata["confidence"] == "Low"
        assert rec.metadata["reasoning_trace"]["confidence"] == 0.25
        assert "intel_contradictions" in rec.metadata
