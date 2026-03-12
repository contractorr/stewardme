"""Tests for regex-based entity extraction."""

from memory.entity_extractor import extract_entities


def _normalized_set(results: list[tuple[str, str]]) -> set[str]:
    """Helper: extract the normalized keys from extract_entities output."""
    return {norm for _orig, norm in results}


def _originals_map(results: list[tuple[str, str]]) -> dict[str, str]:
    """Helper: normalized -> original mapping."""
    return {norm: orig for orig, norm in results}


class TestExtractEntities:
    def test_multi_word_proper_nouns(self):
        entities = _normalized_set(
            extract_entities("User works with Machine Learning and Deep Learning")
        )
        assert "machine learning" in entities
        assert "deep learning" in entities

    def test_acronyms(self):
        entities = _normalized_set(extract_entities("User uses AWS and GCP for ML deployments"))
        assert "aws" in entities
        assert "gcp" in entities
        assert "ml" in entities

    def test_sentence_start_filtering(self):
        entities = _normalized_set(extract_entities("User prefers Python. The team uses Java."))
        assert "user" not in entities
        assert "the" not in entities

    def test_empty_text(self):
        assert extract_entities("") == []
        assert extract_entities("   ") == []

    def test_all_lowercase(self):
        assert extract_entities("user prefers python for backend development") == []

    def test_dedup_normalization(self):
        entities = _normalized_set(extract_entities("AWS powers AWS services via AWS Lambda"))
        assert "aws" in entities
        assert len([n for n in entities if n == "aws"]) == 1

    def test_mixed_entities(self):
        entities = _normalized_set(
            extract_entities("User uses Fast API with AWS for Real Time systems")
        )
        assert "fast api" in entities or "real time" in entities
        assert "aws" in entities

    def test_single_proper_noun_mid_sentence(self):
        entities = _normalized_set(extract_entities("They use Python for Django projects"))
        assert "python" in entities
        assert "django" in entities

    def test_sentence_start_proper_noun(self):
        entities = _normalized_set(extract_entities("Python is their main language"))
        assert "python" in entities

    def test_preserves_original_casing(self):
        results = _originals_map(extract_entities("User uses AWS and Machine Learning"))
        assert results["aws"] == "AWS"
        assert results["machine learning"] == "Machine Learning"

    def test_returns_sorted(self):
        entities = extract_entities("ZZZ Corp uses AWS and BBB Framework")
        normalized = [norm for _orig, norm in entities]
        assert normalized == sorted(normalized)
