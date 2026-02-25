"""Tests for CapabilityHorizonModel — persistence, validation, fallback, row cap."""

import json
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

from intelligence.capability_model import (
    _STATIC_FALLBACK,
    CAPABILITY_DOMAINS,
    CapabilityDomain,
    CapabilityHorizonModel,
)
from intelligence.scraper import IntelItem

# ---------------------------------------------------------------------------
# Pydantic validation tests
# ---------------------------------------------------------------------------


class TestCapabilityDomainValidation:
    def test_valid_domain(self):
        d = CapabilityDomain(
            name="software_engineering",
            current_level=0.7,
            months_to_next_threshold=6,
            confidence="high",
            key_signals=["SWE-bench ~70%"],
            last_updated=datetime.now(),
        )
        assert d.current_level == 0.7

    def test_current_level_too_high(self):
        with pytest.raises(ValidationError):
            CapabilityDomain(
                name="test",
                current_level=1.5,
                months_to_next_threshold=6,
                confidence="high",
                key_signals=["signal"],
                last_updated=datetime.now(),
            )

    def test_confidence_invalid(self):
        with pytest.raises(ValidationError):
            CapabilityDomain(
                name="test",
                current_level=0.5,
                months_to_next_threshold=6,
                confidence="very high",
                key_signals=["signal"],
                last_updated=datetime.now(),
            )

    def test_months_negative(self):
        with pytest.raises(ValidationError):
            CapabilityDomain(
                name="test",
                current_level=0.5,
                months_to_next_threshold=-1,
                confidence="medium",
                key_signals=["signal"],
                last_updated=datetime.now(),
            )

    def test_months_too_large(self):
        with pytest.raises(ValidationError):
            CapabilityDomain(
                name="test",
                current_level=0.5,
                months_to_next_threshold=121,
                confidence="medium",
                key_signals=["signal"],
                last_updated=datetime.now(),
            )

    def test_key_signals_empty(self):
        with pytest.raises(ValidationError):
            CapabilityDomain(
                name="test",
                current_level=0.5,
                months_to_next_threshold=6,
                confidence="medium",
                key_signals=[],
                last_updated=datetime.now(),
            )

    def test_key_signals_too_many(self):
        with pytest.raises(ValidationError):
            CapabilityDomain(
                name="test",
                current_level=0.5,
                months_to_next_threshold=6,
                confidence="medium",
                key_signals=["a", "b", "c", "d", "e", "f", "g"],
                last_updated=datetime.now(),
            )

    def test_current_level_boundary_zero(self):
        d = CapabilityDomain(
            name="test",
            current_level=0.0,
            months_to_next_threshold=0,
            confidence="low",
            key_signals=["signal"],
            last_updated=datetime.now(),
        )
        assert d.current_level == 0.0

    def test_current_level_boundary_one(self):
        d = CapabilityDomain(
            name="test",
            current_level=1.0,
            months_to_next_threshold=120,
            confidence="high",
            key_signals=["signal"],
            last_updated=datetime.now(),
        )
        assert d.current_level == 1.0


# ---------------------------------------------------------------------------
# CapabilityHorizonModel tests
# ---------------------------------------------------------------------------


def _make_mock_llm_response(domains=None):
    """Build a JSON response that mimics what the cheap LLM would return."""
    if domains is None:
        domains = []
        for name in CAPABILITY_DOMAINS:
            fb = _STATIC_FALLBACK.get(name, {})
            domains.append(
                {
                    "name": name,
                    "current_level": fb.get("current_level", 0.5),
                    "months_to_next_threshold": fb.get("months_to_next_threshold", 12),
                    "confidence": fb.get("confidence", "medium"),
                    "key_signals": fb.get("key_signals", ["test signal"]),
                }
            )
    return json.dumps(domains)


class TestCapabilityHorizonModel:
    @pytest.fixture
    def db_path(self, tmp_path):
        return tmp_path / "test_intel.db"

    @pytest.fixture
    def model(self, db_path):
        return CapabilityHorizonModel(db_path)

    def test_get_horizon_context_always_under_2000_chars(self, model, db_path):
        """get_horizon_context() must be <=2000 chars regardless of data."""
        # Manually populate with long signals
        now = datetime.now()
        model._domains = []
        for name in CAPABILITY_DOMAINS:
            model._domains.append(
                CapabilityDomain(
                    name=name,
                    current_level=0.5,
                    months_to_next_threshold=12,
                    confidence="medium",
                    key_signals=["A" * 200, "B" * 200, "C" * 200],
                    last_updated=now,
                )
            )
        model._persist()

        ctx = model.get_horizon_context()
        assert len(ctx) <= 2000

    @patch("intelligence.capability_model.create_cheap_provider")
    def test_persistence_roundtrip(self, mock_factory, model, db_path):
        """Refresh with mock data, reload, verify exact values."""
        mock_provider = MagicMock()
        mock_provider.generate.return_value = _make_mock_llm_response()
        mock_factory.return_value = mock_provider

        items = [
            IntelItem(
                source="test",
                title="Test item",
                url="https://example.com/1",
                summary="Test summary",
            )
        ]
        model.refresh(items)

        # Reload from DB
        model2 = CapabilityHorizonModel(db_path)
        assert model2.load() is True
        assert len(model2.domains) == len(CAPABILITY_DOMAINS)

        # Verify field values match
        for d1, d2 in zip(
            sorted(model.domains, key=lambda d: d.name),
            sorted(model2.domains, key=lambda d: d.name),
        ):
            assert d1.name == d2.name
            assert d1.current_level == d2.current_level
            assert d1.months_to_next_threshold == d2.months_to_next_threshold
            assert d1.confidence == d2.confidence

    @patch("intelligence.capability_model.create_cheap_provider")
    def test_fallback_all_scrapers_empty_db_empty(self, mock_factory, model):
        """All scrapers empty + no DB → populates from static KB without raising."""
        mock_provider = MagicMock()
        # LLM returns no useful data
        mock_provider.generate.return_value = "[]"
        mock_factory.return_value = mock_provider

        model.refresh([])

        assert len(model.domains) == len(CAPABILITY_DOMAINS)
        # Verify domains come from static fallback
        for d in model.domains:
            assert d.name in _STATIC_FALLBACK

    @patch("intelligence.capability_model.create_cheap_provider")
    def test_row_cap_at_10(self, mock_factory, model, db_path):
        """After 11 refreshes, only 10 rows remain."""
        mock_provider = MagicMock()
        mock_provider.generate.return_value = _make_mock_llm_response()
        mock_factory.return_value = mock_provider

        for _ in range(11):
            model.refresh(
                [
                    IntelItem(
                        source="test",
                        title="Test",
                        url="https://example.com/x",
                        summary="x",
                    )
                ]
            )

        from db import wal_connect

        with wal_connect(db_path) as conn:
            count = conn.execute("SELECT COUNT(*) FROM capability_model").fetchone()[0]
        assert count == 10

    @patch("intelligence.capability_model.create_cheap_provider")
    def test_invalid_domain_skipped_valid_stored(self, mock_factory, model):
        """When LLM returns a dict that fails validation, skip it, store the rest."""
        # Build response with one invalid domain (current_level=1.5) and one valid
        domains = [
            {
                "name": "software_engineering",
                "current_level": 1.5,  # invalid
                "months_to_next_threshold": 6,
                "confidence": "high",
                "key_signals": ["signal"],
            },
            {
                "name": "data_analysis",
                "current_level": 0.65,
                "months_to_next_threshold": 8,
                "confidence": "medium",
                "key_signals": ["signal"],
            },
        ]
        mock_provider = MagicMock()
        mock_provider.generate.return_value = json.dumps(domains)
        mock_factory.return_value = mock_provider

        model.refresh(
            [IntelItem(source="test", title="T", url="https://example.com/1", summary="s")]
        )

        # data_analysis should be stored, software_engineering should fallback to static
        names = {d.name for d in model.domains}
        assert "data_analysis" in names
        assert "software_engineering" in names  # from static fallback
        # software_engineering should have static fallback value (0.7), not 1.5
        se = next(d for d in model.domains if d.name == "software_engineering")
        assert se.current_level == 0.7

    def test_get_domain_trajectory(self, model):
        """Verify trajectory narrative is properly formatted."""
        now = datetime.now()
        model._domains = [
            CapabilityDomain(
                name="legal_reasoning",
                current_level=0.6,
                months_to_next_threshold=12,
                confidence="medium",
                key_signals=["bar exam pass rates", "contract review accuracy"],
                last_updated=now,
            )
        ]
        traj = model.get_domain_trajectory("legal_reasoning")
        assert "Legal Reasoning" in traj
        assert "0.6" in traj
        assert "12 months" in traj
        assert "bar exam pass rates" in traj

    def test_get_domain_trajectory_missing(self, model):
        """Non-existent domain returns informative message."""
        model._domains = []
        traj = model.get_domain_trajectory("nonexistent")
        assert "No data" in traj

    def test_empty_model_load_returns_false(self, model):
        """Loading from empty DB returns False."""
        assert model.load() is False

    @patch("intelligence.capability_model.create_cheap_provider")
    def test_llm_failure_uses_static(self, mock_factory, model):
        """If LLM call fails entirely, all domains come from static KB."""
        mock_provider = MagicMock()
        mock_provider.generate.side_effect = Exception("LLM unavailable")
        mock_factory.return_value = mock_provider

        model.refresh([])
        assert len(model.domains) == len(CAPABILITY_DOMAINS)
