"""Tests for eval/grounding.py — advisor grounding evaluation."""

import json
from unittest.mock import MagicMock

import pytest

from eval.dataset import GroundingEvalCase, load_grounding_dataset
from eval.grounding import GroundingJudge
from eval.runner import EvalReport, EvalRunner


@pytest.fixture
def grounding_dataset(tmp_path):
    p = tmp_path / "grounding.yaml"
    p.write_text(
        """cases:
  - query: "What should I focus on?"
    description: "should reference journal"
  - query: "What tools are trending?"
    description: "should reference intel"
"""
    )
    return p


class TestGroundingEvalCase:
    def test_load(self, grounding_dataset):
        cases = load_grounding_dataset(grounding_dataset)
        assert len(cases) == 2
        assert isinstance(cases[0], GroundingEvalCase)
        assert cases[0].query == "What should I focus on?"
        assert cases[0].description == "should reference journal"

    def test_defaults(self, tmp_path):
        p = tmp_path / "minimal.yaml"
        p.write_text('cases:\n  - query: "hello"\n')
        cases = load_grounding_dataset(p)
        assert cases[0].description == ""


class TestGroundingJudge:
    def test_score_success(self, mock_llm_provider):
        mock_llm_provider.generate.return_value = json.dumps(
            {
                "grounding": 4,
                "hallucination_risk": 5,
                "context_coverage": 3,
                "reasoning": "well grounded",
            }
        )
        judge = GroundingJudge(mock_llm_provider)
        case = GroundingEvalCase(query="test query", description="test")
        result = judge.score(case, "response text", "journal ctx", "intel ctx")
        assert result["grounding"] == 4
        assert result["hallucination_risk"] == 5
        assert result["context_coverage"] == 3
        assert result["query"] == "test query"

    def test_no_llm(self):
        judge = GroundingJudge(None)
        case = GroundingEvalCase(query="test")
        result = judge.score(case, "resp", "j", "i")
        assert result["skipped"] is True

    def test_llm_exception(self, mock_llm_provider):
        mock_llm_provider.generate.side_effect = RuntimeError("boom")
        judge = GroundingJudge(mock_llm_provider)
        case = GroundingEvalCase(query="test")
        result = judge.score(case, "resp", "j", "i")
        assert result["skipped"] is True

    def test_parse_failure(self, mock_llm_provider):
        mock_llm_provider.generate.return_value = "not json at all"
        judge = GroundingJudge(mock_llm_provider)
        case = GroundingEvalCase(query="test")
        result = judge.score(case, "resp", "j", "i")
        assert result["skipped"] is True


class TestEvalRunnerGrounding:
    def test_run_grounding_no_deps(self, grounding_dataset):
        runner = EvalRunner()
        report = runner.run_grounding(grounding_dataset)
        assert len(report.grounding_results) == 2
        assert all(r["skipped"] for r in report.grounding_results)

    def test_run_grounding_with_mocks(self, grounding_dataset, mock_llm_provider):
        mock_llm_provider.generate.return_value = json.dumps(
            {"grounding": 4, "hallucination_risk": 5, "context_coverage": 3, "reasoning": "ok"}
        )
        advisor = MagicMock()
        advisor.ask.return_value = "Focus on your goals."
        rag = MagicMock()
        rag.get_combined_context.return_value = ("journal entries here", "intel items here")
        judge = GroundingJudge(mock_llm_provider)

        runner = EvalRunner(advisor_engine=advisor, rag=rag, grounding_judge=judge)
        report = runner.run_grounding(grounding_dataset)
        assert len(report.grounding_results) == 2
        assert report.grounding_results[0]["grounding"] == 4
        assert report.summary.get("avg_grounding") == 4.0

    def test_rag_failure_handled(self, grounding_dataset, mock_llm_provider):
        advisor = MagicMock()
        rag = MagicMock()
        rag.get_combined_context.side_effect = RuntimeError("db error")
        judge = GroundingJudge(mock_llm_provider)

        runner = EvalRunner(advisor_engine=advisor, rag=rag, grounding_judge=judge)
        report = runner.run_grounding(grounding_dataset)
        assert all(r["skipped"] for r in report.grounding_results)

    def test_advisor_failure_handled(self, grounding_dataset, mock_llm_provider):
        advisor = MagicMock()
        advisor.ask.side_effect = RuntimeError("llm error")
        rag = MagicMock()
        rag.get_combined_context.return_value = ("j", "i")
        judge = GroundingJudge(mock_llm_provider)

        runner = EvalRunner(advisor_engine=advisor, rag=rag, grounding_judge=judge)
        report = runner.run_grounding(grounding_dataset)
        assert all(r["skipped"] for r in report.grounding_results)


class TestEvalReportGrounding:
    def test_grounding_summary(self):
        report = EvalReport(
            grounding_results=[
                {"grounding": 4, "hallucination_risk": 5, "context_coverage": 3, "query": "a"},
                {"grounding": 2, "hallucination_risk": 3, "context_coverage": 4, "query": "b"},
                {"skipped": True, "query": "c"},
            ]
        )
        report.compute_summary()
        assert report.summary["avg_grounding"] == 3.0
        assert report.summary["avg_hallucination_risk"] == 4.0
        assert report.summary["avg_context_coverage"] == 3.5
        assert report.summary["grounding_cases_scored"] == 2
        assert report.summary["grounding_cases_skipped"] == 1
