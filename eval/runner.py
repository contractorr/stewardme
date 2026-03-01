"""Eval runner: orchestrates retrieval and response evaluations."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

from eval.dataset import load_response_dataset, load_retrieval_dataset
from eval.response import ResponseJudge
from eval.retrieval import score_retrieval_case

logger = logging.getLogger(__name__)

DATASETS_DIR = Path(__file__).parent / "datasets"


@dataclass
class EvalReport:
    retrieval_results: list[dict] = field(default_factory=list)
    response_results: list[dict] = field(default_factory=list)
    summary: dict = field(default_factory=dict)

    def compute_summary(self):
        """Aggregate per-case metrics into summary stats."""
        s = {}
        if self.retrieval_results:
            for metric in ("precision@3", "precision@5", "recall@5", "recall@10", "mrr"):
                vals = [r[metric] for r in self.retrieval_results if metric in r]
                s[f"avg_{metric}"] = sum(vals) / len(vals) if vals else 0.0

        scored = [r for r in self.response_results if not r.get("skipped")]
        if scored:
            s["avg_response_score"] = sum(r.get("overall", 0) for r in scored) / len(scored)
            s["response_cases_scored"] = len(scored)

        s["response_cases_skipped"] = sum(1 for r in self.response_results if r.get("skipped"))
        self.summary = s


def _extract_doc_id(result: dict) -> str:
    """Extract a matchable doc ID from a search result dict."""
    # Journal results have 'path', intel results have 'url'
    if "path" in result:
        p = result["path"]
        return str(p.stem) if hasattr(p, "stem") else str(Path(str(p)).stem)
    if "url" in result:
        return result["url"]
    if "title" in result:
        return result["title"]
    return str(result)


class EvalRunner:
    def __init__(
        self,
        journal_search=None,
        intel_search=None,
        advisor_engine=None,
        judge: ResponseJudge | None = None,
    ):
        self.journal_search = journal_search
        self.intel_search = intel_search
        self.advisor = advisor_engine
        self.judge = judge

    def run_retrieval(self, dataset_path: Path | None = None, k: int = 5) -> EvalReport:
        """Run retrieval eval: query search, score against expected docs."""
        path = dataset_path or DATASETS_DIR / "retrieval.yaml"
        cases = load_retrieval_dataset(path)
        report = EvalReport()

        for case in cases:
            results = []
            if self.journal_search:
                journal_hits = self.journal_search.hybrid_search(
                    case.query, n_results=k * 2, entry_type=case.entry_type
                )
                results.extend(journal_hits)
            if self.intel_search:
                intel_hits = self.intel_search.hybrid_search(case.query, n_results=k * 2)
                results.extend(intel_hits)

            doc_ids = [_extract_doc_id(r) for r in results]
            scores = score_retrieval_case(case, doc_ids)
            report.retrieval_results.append(scores)

        report.compute_summary()
        return report

    def run_response(self, dataset_path: Path | None = None) -> EvalReport:
        """Run response eval: generate advice, judge quality."""
        path = dataset_path or DATASETS_DIR / "response.yaml"
        cases = load_response_dataset(path)
        report = EvalReport()

        if not self.advisor or not self.judge:
            for case in cases:
                report.response_results.append(
                    {"skipped": True, "reason": "no advisor or judge", "query": case.query}
                )
            report.compute_summary()
            return report

        for case in cases:
            try:
                response = self.advisor.ask(case.query, advice_type=case.advice_type)
            except Exception as e:
                logger.warning("Advisor failed for query '%s': %s", case.query, e)
                report.response_results.append(
                    {"skipped": True, "reason": str(e), "query": case.query}
                )
                continue

            score = self.judge.score(case, response)
            report.response_results.append(score)

        report.compute_summary()
        return report

    def run_all(
        self, retrieval_path: Path | None = None, response_path: Path | None = None, k: int = 5
    ) -> EvalReport:
        """Run both retrieval and response evals, merge into single report."""
        r_report = self.run_retrieval(retrieval_path, k=k)
        s_report = self.run_response(response_path)

        combined = EvalReport(
            retrieval_results=r_report.retrieval_results,
            response_results=s_report.response_results,
        )
        combined.compute_summary()
        return combined
