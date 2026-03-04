"""Eval CLI command — run retrieval & response quality evaluations."""

import json as json_mod
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

console = Console()


@click.group("eval")
def eval_cmd():
    """Run retrieval, response, intel, radar, and grounding evaluations."""


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


@eval_cmd.command("intel")
@click.option("--db", type=click.Path(), default=None, help="Path to intel.db")
@click.option("--freshness-days", default=7, help="Freshness window in days")
@click.option("--json", "as_json", is_flag=True, help="Output raw JSON")
def intel(db, freshness_days, as_json):
    """Evaluate intel scraping quality (no LLM, pure SQLite)."""
    from cli.config import get_paths, load_config
    from eval.intel import run_intel_eval

    if db is None:
        config = load_config()
        paths = get_paths(config)
        db = str(paths["intel_db"])

    db_path = Path(db)
    if not db_path.exists():
        console.print(f"[red]DB not found: {db_path}[/]")
        sys.exit(1)

    with console.status("Running intel eval..."):
        report = run_intel_eval(db_path, freshness_days=freshness_days)

    if as_json:
        console.print(json_mod.dumps(report.to_dict(), indent=2, default=str))
        return

    # Freshness
    f = report.freshness
    console.print(f"\n[bold]Freshness[/] (window={freshness_days}d)")
    console.print(f"  Items: {f.get('total_items', 0)}, Fresh: {f.get('pct_fresh', 0):.1%}")
    console.print(f"  Staleness P50: {f.get('staleness_p50_days', 'N/A')}d")
    if f.get("buckets"):
        console.print(f"  Buckets: {f['buckets']}")

    # Diversity
    d = report.diversity
    console.print("\n[bold]Source Diversity[/]")
    console.print(
        f"  Sources: {d.get('unique_sources', 0)}, Families: {d.get('unique_families', 0)}, Gini: {d.get('gini', 0):.3f}"
    )

    # Dedup
    dd = report.dedup
    console.print("\n[bold]Dedup[/]")
    console.print(
        f"  Duplicates: {dd.get('duplicate_of_count', 0)}/{dd.get('total_items', 0)} ({dd.get('overall_dedup_ratio', 0):.1%})"
    )

    # Reliability
    r = report.reliability
    console.print("\n[bold]Scraper Reliability[/]")
    console.print(f"  Status: {r.get('status_counts', {})}")
    console.print(f"  Avg error rate: {r.get('avg_error_rate', 0)}%")

    # Content quality
    cq = report.content_quality
    console.print("\n[bold]Content Quality[/]")
    console.print(f"  Avg summary len: {cq.get('avg_summary_len', 0)}")
    console.print(
        f"  Has tags: {cq.get('pct_has_tags', 0):.1%}, Valid URLs: {cq.get('pct_valid_url', 0):.1%}"
    )

    # Summary
    s = report.summary
    if s.get("passed"):
        console.print("\n[green]PASS[/]")
    else:
        console.print(f"\n[red]FAIL[/]: {', '.join(s.get('failures', []))}")
        sys.exit(1)


@eval_cmd.command("radar")
@click.option("--db", type=click.Path(), default=None, help="Path to intel.db")
@click.option(
    "--profile",
    type=click.Path(exists=True),
    default=None,
    help="Profile YAML for personalization check",
)
@click.option("--with-coherence", is_flag=True, help="Run LLM coherence scoring (needs API key)")
@click.option("--json", "as_json", is_flag=True, help="Output raw JSON")
def radar(db, profile, with_coherence, as_json):
    """Evaluate trending radar quality."""
    from cli.config import get_paths, load_config
    from eval.radar import run_radar_eval
    from intelligence.search import ProfileTerms

    if db is None:
        config = load_config()
        paths = get_paths(config)
        db = str(paths["intel_db"])

    db_path = Path(db)
    if not db_path.exists():
        console.print(f"[red]DB not found: {db_path}[/]")
        sys.exit(1)

    # Load profile terms if provided
    profile_terms = None
    if profile:
        import yaml

        data = yaml.safe_load(Path(profile).read_text())
        # Support both single profile and profiles list
        p = data if "skills" in data else (data.get("profiles", [{}])[0])
        profile_terms = ProfileTerms(
            skills=p.get("skills", []),
            tech=p.get("tech", []),
            interests=p.get("interests", []),
            goal_keywords=p.get("goal_keywords", []),
            project_keywords=p.get("project_keywords", []),
        )

    judge_llm = None
    if with_coherence:
        from cli.utils import get_components

        c = get_components(skip_advisor=True)
        advisor = c.get("advisor")
        if advisor and hasattr(advisor, "cheap_llm"):
            judge_llm = advisor.cheap_llm
        elif advisor and hasattr(advisor, "llm"):
            judge_llm = advisor.llm

    with console.status("Running radar eval..."):
        report = run_radar_eval(db_path, profile_terms=profile_terms, judge_llm=judge_llm)

    if as_json:
        console.print(json_mod.dumps(report.to_dict(), indent=2, default=str))
        return

    # Cross-source
    cs = report.cross_source
    console.print("\n[bold]Cross-Source[/]")
    console.print(
        f"  Topics: {cs.get('total_topics', 0)}, Violations: {cs.get('violation_count', 0)}"
    )
    if cs.get("violations"):
        for v in cs["violations"]:
            console.print(f"    - {v['topic']}: {v['count']} families ({v['families']})")

    # Temporal
    t = report.temporal
    console.print("\n[bold]Temporal Validity[/]")
    console.print(f"  Age: {t.get('age_hours', '?')}h, Fresh: {t.get('snapshot_fresh', '?')}")
    if t.get("stale_topics"):
        console.print(f"  Stale topics: {t['stale_topics']}")

    # Personalization
    if report.personalization:
        p = report.personalization
        console.print("\n[bold]Personalization[/]")
        console.print(f"  Relevant: {p.get('relevant_topics', 0)}/{p.get('total_topics', 0)}")

    # Coherence
    scored = [r for r in report.coherence_results if not r.get("skipped")]
    if scored:
        table = Table(title="Coherence Scores", show_header=True)
        table.add_column("Topic", max_width=40)
        table.add_column("Score", justify="right")
        table.add_column("Reasoning", max_width=50)
        for r in scored:
            table.add_row(r["topic"][:40], str(r["coherence"]), r.get("reasoning", "")[:50])
        console.print(table)

    # Summary
    s = report.summary
    if s.get("passed"):
        console.print("\n[green]PASS[/]")
    else:
        console.print("\n[red]FAIL[/]: structural checks failed")
        sys.exit(1)


@eval_cmd.command("grounding")
@click.option(
    "--dataset", type=click.Path(exists=True), default=None, help="Custom grounding dataset"
)
@click.option("--json", "as_json", is_flag=True, help="Output raw JSON")
def grounding(dataset, as_json):
    """Evaluate advisor response grounding (needs API key)."""
    from cli.utils import get_components
    from eval.grounding import GroundingJudge
    from eval.runner import EvalRunner

    c = get_components()
    advisor = c.get("advisor")
    judge_llm = None
    if advisor and hasattr(advisor, "cheap_llm"):
        judge_llm = advisor.cheap_llm
    elif advisor and hasattr(advisor, "llm"):
        judge_llm = advisor.llm

    grounding_judge = GroundingJudge(judge_llm) if judge_llm else None
    rag = c.get("rag") if "rag" in c else getattr(advisor, "rag", None)

    runner = EvalRunner(
        advisor_engine=advisor,
        grounding_judge=grounding_judge,
        rag=rag,
    )

    dataset_path = Path(dataset) if dataset else None

    with console.status("Running grounding eval..."):
        report = runner.run_grounding(dataset_path)

    if as_json:
        console.print(
            json_mod.dumps(
                {"grounding_results": report.grounding_results, "summary": report.summary},
                indent=2,
                default=str,
            )
        )
        return

    scored = [r for r in report.grounding_results if not r.get("skipped")]
    if scored:
        table = Table(title="Grounding Eval", show_header=True)
        table.add_column("Query", max_width=30)
        table.add_column("Ground", justify="right")
        table.add_column("Halluc", justify="right")
        table.add_column("Cover", justify="right")
        table.add_column("Reasoning", max_width=40)

        for r in scored:
            table.add_row(
                r.get("query", "")[:30],
                str(r.get("grounding", "-")),
                str(r.get("hallucination_risk", "-")),
                str(r.get("context_coverage", "-")),
                r.get("reasoning", "")[:40],
            )
        console.print(table)

    skipped = sum(1 for r in report.grounding_results if r.get("skipped"))
    if skipped:
        console.print(f"[yellow]{skipped} case(s) skipped[/]")

    # Summary
    if report.summary:
        console.print("\n[bold]Summary[/]")
        for key, val in report.summary.items():
            if isinstance(val, float):
                console.print(f"  {key}: {val:.2f}")
            else:
                console.print(f"  {key}: {val}")
