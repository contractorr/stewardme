"""YAML dataset loader and eval case dataclasses."""

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class RetrievalEvalCase:
    query: str
    expected_doc_ids: list[str]
    entry_type: str | None = None
    description: str = ""


@dataclass
class ResponseEvalCase:
    query: str
    advice_type: str = "general"
    expected_traits: list[str] = field(default_factory=list)
    forbidden_traits: list[str] = field(default_factory=list)
    description: str = ""


def load_retrieval_dataset(path: Path) -> list[RetrievalEvalCase]:
    """Load retrieval eval cases from YAML file."""
    data = yaml.safe_load(path.read_text())
    cases = data.get("cases", [])
    return [
        RetrievalEvalCase(
            query=c["query"],
            expected_doc_ids=c.get("expected_doc_ids", []),
            entry_type=c.get("entry_type"),
            description=c.get("description", ""),
        )
        for c in cases
    ]


def load_response_dataset(path: Path) -> list[ResponseEvalCase]:
    """Load response eval cases from YAML file."""
    data = yaml.safe_load(path.read_text())
    cases = data.get("cases", [])
    return [
        ResponseEvalCase(
            query=c["query"],
            advice_type=c.get("advice_type", "general"),
            expected_traits=c.get("expected_traits", []),
            forbidden_traits=c.get("forbidden_traits", []),
            description=c.get("description", ""),
        )
        for c in cases
    ]
