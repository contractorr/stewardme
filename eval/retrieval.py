"""Retrieval quality metrics: precision@k, recall@k, MRR."""

from __future__ import annotations

from eval.dataset import RetrievalEvalCase


def _matches(doc_id: str, expected: list[str]) -> bool:
    """Check if doc_id substring-matches any expected ID (case-insensitive)."""
    doc_lower = doc_id.lower()
    return any(exp.lower() in doc_lower for exp in expected)


def precision_at_k(results: list[str], expected: list[str], k: int) -> float:
    """Fraction of top-k results that are relevant."""
    if k <= 0:
        return 0.0
    top_k = results[:k]
    hits = sum(1 for r in top_k if _matches(r, expected))
    return hits / k


def recall_at_k(results: list[str], expected: list[str], k: int) -> float:
    """Fraction of expected docs found in top-k results."""
    if not expected:
        return 1.0
    top_k = results[:k]
    found = sum(1 for exp in expected if any(exp.lower() in r.lower() for r in top_k))
    return found / len(expected)


def mrr(results: list[str], expected: list[str]) -> float:
    """Mean reciprocal rank: 1/rank of first relevant result."""
    for i, r in enumerate(results):
        if _matches(r, expected):
            return 1.0 / (i + 1)
    return 0.0


def score_retrieval_case(case: RetrievalEvalCase, results: list[str]) -> dict:
    """Score a single retrieval case at k=3,5,10."""
    return {
        "query": case.query,
        "description": case.description,
        "num_results": len(results),
        "precision@3": precision_at_k(results, case.expected_doc_ids, 3),
        "precision@5": precision_at_k(results, case.expected_doc_ids, 5),
        "precision@10": precision_at_k(results, case.expected_doc_ids, 10),
        "recall@3": recall_at_k(results, case.expected_doc_ids, 3),
        "recall@5": recall_at_k(results, case.expected_doc_ids, 5),
        "recall@10": recall_at_k(results, case.expected_doc_ids, 10),
        "mrr": mrr(results, case.expected_doc_ids),
    }
