"""Tests for eval dataset loading."""

import pytest  # noqa: F401 (used by fixtures)

from eval.dataset import (
    ResponseEvalCase,
    RetrievalEvalCase,
    load_response_dataset,
    load_retrieval_dataset,
)


@pytest.fixture
def retrieval_yaml(tmp_path):
    p = tmp_path / "retrieval.yaml"
    p.write_text(
        """cases:
  - query: "test query"
    expected_doc_ids: ["doc-1", "doc-2"]
    description: "test case"
  - query: "another query"
    expected_doc_ids: ["doc-3"]
    entry_type: "goal"
"""
    )
    return p


@pytest.fixture
def response_yaml(tmp_path):
    p = tmp_path / "response.yaml"
    p.write_text(
        """cases:
  - query: "career advice"
    advice_type: "career"
    expected_traits: ["actionable", "references profile"]
    forbidden_traits: ["hallucinated URL"]
    description: "career test"
  - query: "minimal case"
"""
    )
    return p


def test_load_retrieval_dataset(retrieval_yaml):
    cases = load_retrieval_dataset(retrieval_yaml)
    assert len(cases) == 2
    assert isinstance(cases[0], RetrievalEvalCase)
    assert cases[0].query == "test query"
    assert cases[0].expected_doc_ids == ["doc-1", "doc-2"]
    assert cases[0].description == "test case"
    assert cases[1].entry_type == "goal"


def test_load_response_dataset(response_yaml):
    cases = load_response_dataset(response_yaml)
    assert len(cases) == 2
    assert isinstance(cases[0], ResponseEvalCase)
    assert cases[0].advice_type == "career"
    assert cases[0].expected_traits == ["actionable", "references profile"]
    assert cases[0].forbidden_traits == ["hallucinated URL"]


def test_response_defaults(response_yaml):
    cases = load_response_dataset(response_yaml)
    minimal = cases[1]
    assert minimal.advice_type == "general"
    assert minimal.expected_traits == []
    assert minimal.forbidden_traits == []
    assert minimal.description == ""


def test_empty_dataset(tmp_path):
    p = tmp_path / "empty.yaml"
    p.write_text("cases: []\n")
    assert load_retrieval_dataset(p) == []
    assert load_response_dataset(p) == []


def test_missing_cases_key(tmp_path):
    p = tmp_path / "bad.yaml"
    p.write_text("other_key: true\n")
    assert load_retrieval_dataset(p) == []
    assert load_response_dataset(p) == []
