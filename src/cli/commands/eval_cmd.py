"""Eval CLI command — run retrieval & response quality evaluations."""

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

console = Console()


@click.group("eval")
def eval_cmd():
    """Run retrieval & response quality evaluations."""


@eval_cmd.command("run")
@click.option("--retrieval-only", is_flag=True, help="Only run retrieval eval")
@click.option("--response-only", is_flag=True, help="Only run response eval")
@click.option("--dataset", type=click.Path(exists=True), help="Custom dataset path")
@click.option("--k", default=5, help="k for precision/recall@k")
def run(retrieval_only, response_only, dataset, k):
    """Run evaluation harness and print results."""
    from cli.utils import get_components
    from eval.response import ResponseJudge
    from eval.runner import EvalRunner

    c = get_components(skip_advisor=response_only is False)

    judge = None
    advisor = c.get("advisor")
    if advisor and hasattr(advisor, "llm"):
        judge = ResponseJudge(advisor.llm)

    runner = EvalRunner(
        journal_search=c.get("search"),
        intel_search=c.get("intel_search"),
        advisor_engine=advisor,
        judge=judge,
    )

    dataset_path = Path(dataset) if dataset else None

    if response_only:
        with console.status("Running response eval..."):
            report = runner.run_response(dataset_path)
    elif retrieval_only:
        with console.status("Running retrieval eval..."):
            report = runner.run_retrieval(dataset_path, k=k)
    else:
        with console.status("Running full eval..."):
            report = runner.run_all(
                retrieval_path=dataset_path,
                response_path=dataset_path,
                k=k,
            )

    # Print retrieval results
    if report.retrieval_results:
        table = Table(title="Retrieval Eval", show_header=True)
        table.add_column("Query", max_width=40)
        table.add_column("P@5", justify="right")
        table.add_column("R@5", justify="right")
        table.add_column("MRR", justify="right")

        for r in report.retrieval_results:
            table.add_row(
                r["query"][:40],
                f"{r.get('precision@5', 0):.2f}",
                f"{r.get('recall@5', 0):.2f}",
                f"{r.get('mrr', 0):.2f}",
            )
        console.print(table)

    # Print response results
    scored = [r for r in report.response_results if not r.get("skipped")]
    if scored:
        table = Table(title="Response Eval", show_header=True)
        table.add_column("Query", max_width=40)
        table.add_column("Score", justify="right")
        table.add_column("Reasoning", max_width=50)

        for r in scored:
            table.add_row(
                r.get("query", "")[:40],
                str(r.get("overall", "-")),
                r.get("reasoning", "")[:50],
            )
        console.print(table)

    skipped = sum(1 for r in report.response_results if r.get("skipped"))
    if skipped:
        console.print(f"[yellow]{skipped} response case(s) skipped (no LLM)[/]")

    # Print summary
    if report.summary:
        console.print("\n[bold]Summary[/]")
        for key, val in report.summary.items():
            if isinstance(val, float):
                console.print(f"  {key}: {val:.3f}")
            else:
                console.print(f"  {key}: {val}")

    # Exit code 1 if retrieval metrics below threshold
    avg_mrr = report.summary.get("avg_mrr", 1.0)
    avg_recall = report.summary.get("avg_recall@5", 1.0)
    if avg_mrr < 0.3 or avg_recall < 0.3:
        console.print("[red]FAIL: metrics below threshold (MRR>=0.3, recall@5>=0.3)[/]")
        sys.exit(1)
