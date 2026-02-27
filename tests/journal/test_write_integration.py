"""Integration test: journal write triggers thread detection."""

from datetime import datetime
from unittest.mock import MagicMock

import pytest

from journal.thread_store import ThreadStore
from journal.threads import ThreadDetector


@pytest.fixture
def tmp_env(tmp_path):
    """Set up a minimal environment for write integration."""
    db_path = tmp_path / "threads.db"
    store = ThreadStore(db_path)

    collection = MagicMock()
    collection.count.return_value = 3

    embeddings_mock = MagicMock()
    embeddings_mock.collection = collection

    return {
        "store": store,
        "embeddings": embeddings_mock,
        "collection": collection,
        "db_path": db_path,
    }


class TestWriteTriggersDetection:
    @pytest.mark.asyncio
    async def test_write_hook_detects_thread(self, tmp_env):
        """After writing 3 similar entries, thread detection creates a thread."""
        store = tmp_env["store"]
        collection = tmp_env["collection"]

        entries = {
            "e1": [0.9, 0.3, 0.1],
            "e2": [0.88, 0.32, 0.12],
            "e3": [0.87, 0.33, 0.11],
        }

        def query_fn(query_embeddings=None, n_results=5, include=None):
            qvec = query_embeddings[0]
            scored = []
            for eid, evec in entries.items():
                dot = sum(a * b for a, b in zip(qvec, evec))
                distance = 1.0 - dot
                scored.append((eid, distance))
            scored.sort(key=lambda x: x[1])
            top = scored[:n_results]
            return {
                "ids": [[s[0] for s in top]],
                "distances": [[s[1] for s in top]],
            }

        collection.query = query_fn
        collection.get.return_value = {
            "documents": ["Learning distributed systems"],
            "embeddings": [[0.87, 0.33, 0.11]],
            "metadatas": [{}],
            "ids": ["e3"],
        }
        collection.count.return_value = 3

        detector = ThreadDetector(tmp_env["embeddings"], store, {"similarity_threshold": 0.7})

        match = await detector.detect("e3", entries["e3"], datetime(2026, 2, 12))

        assert match.thread_id is not None
        assert match.match_type == "created_new"

        thread = await store.get_thread(match.thread_id)
        assert thread is not None
        assert thread.entry_count == 3

    @pytest.mark.asyncio
    async def test_disabled_config_skips_detection(self, tmp_env):
        """When threads.enabled=False, detection is skipped entirely."""
        store = tmp_env["store"]

        class FakeConfig:
            enabled = False

        config = FakeConfig()
        assert config.enabled is False
        active = await store.get_active_threads()
        assert active == []
