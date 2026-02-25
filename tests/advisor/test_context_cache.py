"""Tests for context cache."""

import time

import pytest

from advisor.context_cache import ContextCache


class TestContextCache:
    @pytest.fixture
    def cache(self, tmp_path):
        return ContextCache(tmp_path / "cache.db", default_ttl=10)

    def test_set_and_get(self, cache):
        cache.set("k1", "value1")
        assert cache.get("k1") == "value1"

    def test_get_missing_returns_none(self, cache):
        assert cache.get("nonexistent") is None

    def test_expired_entry_returns_none(self, tmp_path):
        cache = ContextCache(tmp_path / "cache.db", default_ttl=0)
        cache.set("k1", "value1")
        time.sleep(0.01)
        assert cache.get("k1") is None

    def test_upsert_overwrites(self, cache):
        cache.set("k1", "v1")
        cache.set("k1", "v2")
        assert cache.get("k1") == "v2"

    def test_make_key_deterministic(self, cache):
        k1 = cache.make_key("journal", "test query", max_entries=5)
        k2 = cache.make_key("journal", "test query", max_entries=5)
        assert k1 == k2

    def test_make_key_varies_by_params(self, cache):
        k1 = cache.make_key("journal", "test", max_entries=5)
        k2 = cache.make_key("journal", "test", max_entries=10)
        assert k1 != k2

    def test_clear_expired(self, tmp_path):
        cache = ContextCache(tmp_path / "cache.db", default_ttl=0)
        cache.set("k1", "v1")
        cache.set("k2", "v2")
        time.sleep(0.01)
        cache.clear_expired()
        # Both should be gone
        assert cache.get("k1") is None
        assert cache.get("k2") is None
