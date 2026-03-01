"""Tests for retrieval metrics."""

import pytest

from eval.dataset import RetrievalEvalCase
from eval.retrieval import mrr, precision_at_k, recall_at_k, score_retrieval_case


class TestPrecisionAtK:
    def test_perfect(self):
        assert precision_at_k(["a", "b", "c"], ["a", "b", "c"], 3) == 1.0

    def test_none_relevant(self):
        assert precision_at_k(["x", "y", "z"], ["a"], 3) == 0.0

    def test_partial(self):
        # 1 relevant in top 3
        assert precision_at_k(["a", "x", "y"], ["a"], 3) == pytest.approx(1 / 3)

    def test_k_larger_than_results(self):
        # Only 2 results, k=5: 1 hit / 5
        assert precision_at_k(["a", "x"], ["a"], 5) == pytest.approx(1 / 5)

    def test_k_zero(self):
        assert precision_at_k(["a"], ["a"], 0) == 0.0

    def test_substring_match(self):
        # "rust" should match "learn-rust-2024"
        assert precision_at_k(["learn-rust-2024", "other"], ["rust"], 2) == pytest.approx(0.5)

    def test_case_insensitive(self):
        assert precision_at_k(["Learn-Rust"], ["learn-rust"], 1) == 1.0


class TestRecallAtK:
    def test_perfect(self):
        assert recall_at_k(["a", "b"], ["a", "b"], 5) == 1.0

    def test_none_found(self):
        assert recall_at_k(["x", "y"], ["a", "b"], 5) == 0.0

    def test_partial(self):
        # 1 of 2 expected found
        assert recall_at_k(["a", "x"], ["a", "b"], 5) == pytest.approx(0.5)

    def test_empty_expected(self):
        assert recall_at_k(["a"], [], 5) == 1.0

    def test_substring_match(self):
        assert recall_at_k(["path/to/learn-rust.md"], ["learn-rust"], 5) == 1.0


class TestMRR:
    def test_first_position(self):
        assert mrr(["a", "b", "c"], ["a"]) == 1.0

    def test_second_position(self):
        assert mrr(["x", "a", "c"], ["a"]) == pytest.approx(0.5)

    def test_not_found(self):
        assert mrr(["x", "y", "z"], ["a"]) == 0.0

    def test_multiple_expected_first_match(self):
        # MRR uses first relevant hit
        assert mrr(["x", "a", "b"], ["a", "b"]) == pytest.approx(0.5)

    def test_empty_results(self):
        assert mrr([], ["a"]) == 0.0


class TestScoreRetrievalCase:
    def test_full_scoring(self):
        case = RetrievalEvalCase(query="test", expected_doc_ids=["doc-a"], description="test")
        results = ["doc-a", "x", "y", "z", "w"]
        scores = score_retrieval_case(case, results)
        assert scores["query"] == "test"
        assert scores["precision@3"] == pytest.approx(1 / 3)
        assert scores["recall@3"] == 1.0
        assert scores["mrr"] == 1.0

    def test_no_hits(self):
        case = RetrievalEvalCase(query="q", expected_doc_ids=["missing"])
        scores = score_retrieval_case(case, ["a", "b", "c"])
        assert scores["precision@5"] == 0.0
        assert scores["recall@5"] == 0.0
        assert scores["mrr"] == 0.0
