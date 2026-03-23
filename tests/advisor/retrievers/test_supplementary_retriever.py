"""Tests for SupplementaryRetriever."""

from unittest.mock import MagicMock

from advisor.retrievers.supplementary import SupplementaryRetriever


class TestGetDocumentContext:
    def test_no_library_index(self):
        sr = SupplementaryRetriever()
        assert sr.get_document_context("q") == ""

    def test_with_attachment_ids(self):
        lib = MagicMock()
        lib.get_item_text.return_value = {
            "report_id": "r1",
            "title": "Doc",
            "extracted_text": "content here",
            "file_name": "doc.pdf",
            "source_kind": "document",
        }
        sr = SupplementaryRetriever(library_index=lib)
        result = sr.get_document_context("q", attachment_ids=["r1"])
        assert "Doc" in result
        assert "content here" in result

    def test_no_results_returns_empty(self):
        lib = MagicMock()
        lib.get_item_text.return_value = None
        lib.hybrid_search.return_value = []
        sr = SupplementaryRetriever(library_index=lib)
        assert sr.get_document_context("q") == ""


class TestGetRepoContext:
    def test_no_user_id(self):
        sr = SupplementaryRetriever()
        assert sr.get_repo_context("q") == ""

    def test_no_intel_db(self):
        sr = SupplementaryRetriever(user_id="u1")
        assert sr.get_repo_context("q") == ""


class TestGetCurriculumContext:
    def test_no_user_id(self):
        sr = SupplementaryRetriever()
        assert sr.get_curriculum_context("q") == ""

    def test_no_intel_db(self):
        sr = SupplementaryRetriever(user_id="u1")
        assert sr.get_curriculum_context("q") == ""
