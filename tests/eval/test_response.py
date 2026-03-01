"""Tests for LLM-as-judge response scorer."""

import json
from unittest.mock import MagicMock

from eval.dataset import ResponseEvalCase
from eval.response import ResponseJudge, _parse_judge_response


class TestParseJudgeResponse:
    def test_valid_json(self):
        raw = json.dumps({"overall": 4, "trait_scores": {"a": 1}})
        assert _parse_judge_response(raw)["overall"] == 4

    def test_json_in_markdown_block(self):
        raw = 'Some text\n{"overall": 3, "reasoning": "ok"}\nmore text'
        parsed = _parse_judge_response(raw)
        assert parsed["overall"] == 3

    def test_invalid_json(self):
        assert _parse_judge_response("not json at all") is None

    def test_empty_string(self):
        assert _parse_judge_response("") is None


class TestResponseJudge:
    def test_score_with_mock_llm(self):
        llm = MagicMock()
        llm.generate.return_value = json.dumps(
            {
                "trait_scores": {"actionable": 1, "references context": 0},
                "forbidden_scores": {"hallucinated URL": 0},
                "overall": 4,
                "reasoning": "Good advice but missing context refs",
            }
        )
        judge = ResponseJudge(llm)
        case = ResponseEvalCase(
            query="test",
            expected_traits=["actionable", "references context"],
            forbidden_traits=["hallucinated URL"],
        )
        result = judge.score(case, "some response text")
        assert result["overall"] == 4
        assert result["trait_scores"]["actionable"] == 1
        assert result["forbidden_scores"]["hallucinated URL"] == 0
        assert "query" in result

    def test_no_llm_returns_skipped(self):
        judge = ResponseJudge(None)
        case = ResponseEvalCase(query="test")
        result = judge.score(case, "response")
        assert result["skipped"] is True

    def test_llm_exception_returns_skipped(self):
        llm = MagicMock()
        llm.generate.side_effect = RuntimeError("API down")
        judge = ResponseJudge(llm)
        case = ResponseEvalCase(query="test")
        result = judge.score(case, "response")
        assert result["skipped"] is True
        assert "API down" in result["reason"]

    def test_unparseable_llm_response(self):
        llm = MagicMock()
        llm.generate.return_value = "I refuse to output JSON"
        judge = ResponseJudge(llm)
        case = ResponseEvalCase(query="test")
        result = judge.score(case, "response")
        assert result["skipped"] is True
        assert "failed to parse" in result["reason"]

    def test_prompt_includes_traits(self):
        llm = MagicMock()
        llm.generate.return_value = json.dumps(
            {"overall": 3, "trait_scores": {}, "forbidden_scores": {}, "reasoning": ""}
        )
        judge = ResponseJudge(llm)
        case = ResponseEvalCase(
            query="q",
            expected_traits=["actionable"],
            forbidden_traits=["hallucinated"],
        )
        judge.score(case, "resp")
        call_args = llm.generate.call_args
        prompt = (
            call_args[1]["messages"][0]["content"]
            if "messages" in call_args[1]
            else call_args[0][0][0]["content"]
        )
        assert "actionable" in prompt
        assert "hallucinated" in prompt
