"""Tests for embedding model versioning and collection naming."""

from pathlib import Path
from unittest.mock import patch

from chroma_utils import SimpleHashEmbeddingFunction
from embeddings.versioning import (
    EMBEDDING_SCHEMA_VERSION,
    _sanitize,
    auto_migrate_collection,
    model_tag,
    versioned_name,
)


class TestModelTag:
    """Test model_tag derivation from embedding functions."""

    def test_hash_fallback(self):
        fn = SimpleHashEmbeddingFunction()
        assert model_tag(fn) == "hash"

    def test_gemini_alias(self):
        """Gemini embedding function uses _model attr."""

        class FakeGemini:
            _model = "gemini-embedding-2-preview"

        assert model_tag(FakeGemini()) == "gemini2"

    def test_openai_alias(self):
        class FakeOpenAI:
            _model = "text-embedding-3-small"

        assert model_tag(FakeOpenAI()) == "oai3s"

    def test_openai_large_alias(self):
        class FakeOpenAI:
            _model = "text-embedding-3-large"

        assert model_tag(FakeOpenAI()) == "oai3l"

    def test_minilm_alias(self):
        class FakeMinilm:
            _model = "all-MiniLM-L6-v2"

        assert model_tag(FakeMinilm()) == "minilm6"

    def test_unknown_model_sanitized(self):
        class FakeUnknown:
            _model = "My-Custom Model/v3.1"

        tag = model_tag(FakeUnknown())
        assert tag == "my_custom_model"

    def test_name_method_fallback(self):
        """Falls back to name() when no _model attr."""

        class FakeProvider:
            def name(self):
                return "simple-hash-fallback"

        assert model_tag(FakeProvider()) == "hash"

    def test_no_attrs_returns_unknown(self):
        class Bare:
            pass

        tag = model_tag(Bare())
        assert tag == "unknown"


class TestSanitize:
    def test_basic(self):
        assert _sanitize("text-embedding-3-small") == "text_embedding_3"

    def test_truncation(self):
        result = _sanitize("a" * 50)
        assert len(result) <= 16

    def test_special_chars(self):
        assert _sanitize("Model/v3.1!") == "model_v3_1"

    def test_strips_trailing_underscores(self):
        result = _sanitize("abc___")
        assert not result.endswith("_")


class TestVersionedName:
    def test_basic_journal(self):
        fn = SimpleHashEmbeddingFunction()
        name = versioned_name("journal", fn)
        assert name == f"journal_v{EMBEDDING_SCHEMA_VERSION}_hash"

    def test_with_user_id(self):
        fn = SimpleHashEmbeddingFunction()
        name = versioned_name("journal", fn, user_id="user:123")
        assert name == f"journal_v{EMBEDDING_SCHEMA_VERSION}_hash_user_123"

    def test_different_models_different_names(self):
        hash_fn = SimpleHashEmbeddingFunction()

        class FakeGemini:
            _model = "gemini-embedding-2-preview"

        gemini_fn = FakeGemini()

        hash_name = versioned_name("journal", hash_fn)
        gemini_name = versioned_name("journal", gemini_fn)
        assert hash_name != gemini_name

    def test_intel_base(self):
        fn = SimpleHashEmbeddingFunction()
        name = versioned_name("intel", fn)
        assert name.startswith("intel_v")

    def test_profile_base(self):
        fn = SimpleHashEmbeddingFunction()
        name = versioned_name("profile", fn)
        assert name.startswith("profile_v")


class TestAutoMigrateCollection:
    def test_renames_old_to_new(self, tmp_path):
        old = tmp_path / "journal.json"
        old.write_text('{"test": 1}')

        result = auto_migrate_collection(tmp_path, "journal", "journal_v1_hash")

        assert result is True
        assert not old.exists()
        assert (tmp_path / "journal_v1_hash.json").exists()

    def test_skips_if_new_exists(self, tmp_path):
        old = tmp_path / "journal.json"
        old.write_text('{"old": 1}')
        new = tmp_path / "journal_v1_hash.json"
        new.write_text('{"new": 1}')

        result = auto_migrate_collection(tmp_path, "journal", "journal_v1_hash")

        assert result is False
        assert old.exists()  # old untouched

    def test_skips_if_old_missing(self, tmp_path):
        result = auto_migrate_collection(tmp_path, "journal", "journal_v1_hash")
        assert result is False

    def test_returns_false_on_error(self, tmp_path):
        old = tmp_path / "journal.json"
        old.write_text('{"test": 1}')

        with patch("pathlib.Path.rename", side_effect=OSError("perm denied")):
            result = auto_migrate_collection(tmp_path, "journal", "journal_v1_hash")
            assert result is False


class TestEmbeddingManagerVersioned:
    """Test that managers use versioned collection names."""

    def test_journal_default_versioned(self, temp_dirs):
        from journal.embeddings import EmbeddingManager

        m = EmbeddingManager(temp_dirs["chroma_dir"])
        assert "_v1_" in m.collection_name
        assert m.collection_name.startswith("journal_v")

    def test_journal_explicit_name_unchanged(self, temp_dirs):
        from journal.embeddings import EmbeddingManager

        m = EmbeddingManager(temp_dirs["chroma_dir"], collection_name="my_custom")
        assert m.collection_name == "my_custom"

    def test_journal_with_user_id(self, temp_dirs):
        from journal.embeddings import EmbeddingManager

        m = EmbeddingManager(temp_dirs["chroma_dir"], user_id="alice")
        assert "alice" in m.collection_name
        assert "_v1_" in m.collection_name

    def test_journal_base_name_override(self, temp_dirs):
        from journal.embeddings import EmbeddingManager

        m = EmbeddingManager(temp_dirs["chroma_dir"], base_name="profile")
        assert m.collection_name.startswith("profile_v")

    def test_intel_versioned(self, temp_dirs):
        from intelligence.embeddings import IntelEmbeddingManager

        m = IntelEmbeddingManager(temp_dirs["chroma_dir"])
        assert "_v1_" in m.collection_name
        assert m.collection_name.startswith("intel_v")

    def test_library_versioned(self, temp_dirs):
        from library.embeddings import LibraryEmbeddingManager

        m = LibraryEmbeddingManager(temp_dirs["chroma_dir"])
        assert "_v1_" in m.collection_name
        assert m.collection_name.startswith("library_v")

    def test_library_explicit_name(self, temp_dirs):
        from library.embeddings import LibraryEmbeddingManager

        m = LibraryEmbeddingManager(temp_dirs["chroma_dir"], collection_name="custom_lib")
        assert m.collection_name == "custom_lib"

    def test_curriculum_versioned(self, temp_dirs):
        from curriculum.embeddings import ChapterEmbeddingManager

        m = ChapterEmbeddingManager(temp_dirs["chroma_dir"])
        assert "_v1_" in m._emb.collection_name
        assert m._emb.collection_name.startswith("curriculum_chapters_v")

    def test_auto_migrate_on_init(self, temp_dirs):
        """Old unversioned file is renamed on first init."""
        chroma_dir = temp_dirs["chroma_dir"]
        old_file = Path(chroma_dir) / "journal.json"
        old_file.write_text('{"entry1": {"document": "test", "metadata": {}, "vector": [0.1]}}')

        from journal.embeddings import EmbeddingManager

        m = EmbeddingManager(chroma_dir)

        # Old file should be gone, new versioned file should exist
        assert not old_file.exists()
        new_file = Path(chroma_dir) / f"{m.collection_name}.json"
        assert new_file.exists()
