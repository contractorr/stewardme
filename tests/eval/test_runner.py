"""Tests for eval runner."""

import json
from unittest.mock import MagicMock

import pytest

from eval.runner import EvalReport, EvalRunner


@pytest.fixture
def retrieval_dataset(tmp_path):
    p = tmp_path / "retrieval.yaml"
    p.write_text(
        """cases:
  - query: "Rust learning"
    expected_doc_ids: ["learn-rust"]
    description: "find rust goal"
  - query: "AI tools"
    expected_doc_ids: ["ai-reviewer"]
    description: "find AI item"
"""
    )
    return p


@pytest.fixture
def response_dataset(tmp_path):
    p = tmp_path / "response.yaml"
    p.write_text(
        """cases:
  - query: "What should I do?"
    expected_traits: ["actionable"]
    forbidden_traits: ["hallucinated URL"]
"""
    )
    return p


@pytest.fixture
def mock_journal_search():
    search = MagicMock()
    search.hybrid_search.return_value = [
        {"path": MagicMock(stem="learn-rust"), "title": "Learn Rust", "content": "..."},
        {"path": MagicMock(stem="weekly-review"), "title": "Weekly Review", "content": "..."},
    ]
    return search


@pytest.fixture
def mock_intel_search():
    search = MagicMock()
    search.hybrid_search.return_value = [
        {"url": "https://example.com/ai-reviewer", "title": "AI Reviewer", "content": "..."},
    ]
    return search


class TestEvalReport:
    def test_compute_summary_retrieval(self):
        report = EvalReport(
            retrieval_results=[
                {
                    "precision@3": 0.33,
                    "precision@5": 0.2,
                    "recall@5": 1.0,
                    "recall@10": 1.0,
                    "mrr": 1.0,
                },
                {
                    "precision@3": 0.0,
                    "precision@5": 0.0,
                    "recall@5": 0.0,
                    "recall@10": 0.0,
                    "mrr": 0.0,
                },
            ]
        )
        report.compute_summary()
        assert report.summary["avg_mrr"] == pytest.approx(0.5)
        assert report.summary["avg_recall@5"] == pytest.approx(0.5)

    def test_compute_summary_response(self):
        report = EvalReport(
            response_results=[
                {"overall": 4, "query": "a"},
                {"overall": 2, "query": "b"},
                {"skipped": True, "query": "c"},
            ]
        )
        report.compute_summary()
        assert report.summary["avg_response_score"] == pytest.approx(3.0)
        assert report.summary["response_cases_scored"] == 2
        assert report.summary["response_cases_skipped"] == 1

    def test_compute_summary_empty(self):
        report = EvalReport()
        report.compute_summary()
        assert report.summary["response_cases_skipped"] == 0


class TestEvalRunner:
    def test_run_retrieval(self, mock_journal_search, mock_intel_search, retrieval_dataset):
        runner = EvalRunner(
            journal_search=mock_journal_search,
            intel_search=mock_intel_search,
        )
        report = runner.run_retrieval(retrieval_dataset)
        assert len(report.retrieval_results) == 2
        # First case expects "learn-rust" — journal returns it
        assert report.retrieval_results[0]["mrr"] > 0
        assert "avg_mrr" in report.summary

    def test_run_retrieval_no_search(self, retrieval_dataset):
        runner = EvalRunner()
        report = runner.run_retrieval(retrieval_dataset)
        assert len(report.retrieval_results) == 2
        # No search = no results = zero metrics
        assert report.retrieval_results[0]["mrr"] == 0.0

    def test_run_response_no_advisor(self, response_dataset):
        runner = EvalRunner()
        report = runner.run_response(response_dataset)
        assert len(report.response_results) == 1
        assert report.response_results[0]["skipped"] is True

    def test_run_response_with_mocks(self, response_dataset, mock_llm_provider):
        advisor = MagicMock()
        advisor.ask.return_value = "You should focus on X and Y."

        mock_llm_provider.generate.return_value = json.dumps(
            {
                "trait_scores": {"actionable": 1},
                "forbidden_scores": {"hallucinated URL": 0},
                "overall": 4,
                "reasoning": "good",
            }
        )
        from eval.response import ResponseJudge

        judge = ResponseJudge(mock_llm_provider)
        runner = EvalRunner(advisor_engine=advisor, judge=judge)
        report = runner.run_response(response_dataset)
        assert len(report.response_results) == 1
        assert report.response_results[0]["overall"] == 4

    def test_run_all(
        self, mock_journal_search, mock_intel_search, retrieval_dataset, response_dataset
    ):
        runner = EvalRunner(
            journal_search=mock_journal_search,
            intel_search=mock_intel_search,
        )
        report = runner.run_all(retrieval_path=retrieval_dataset, response_path=response_dataset)
        assert len(report.retrieval_results) == 2
        assert len(report.response_results) == 1  # skipped (no advisor)
        assert "avg_mrr" in report.summary

    def test_advisor_exception_handled(self, response_dataset):
        advisor = MagicMock()
        advisor.ask.side_effect = RuntimeError("boom")
        judge = MagicMock()
        runner = EvalRunner(advisor_engine=advisor, judge=judge)
        report = runner.run_response(response_dataset)
        assert report.response_results[0]["skipped"] is True
