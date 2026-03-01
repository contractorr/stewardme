"""Prediction ledger CLI commands."""

import click
from rich.console import Console
from rich.table import Table

from cli.utils import get_components

console = Console()


@click.group()
def predictions():
    """Track and review prediction outcomes."""
    from cli.utils import warn_experimental

    warn_experimental("Prediction ledger")


@predictions.command("list")
@click.option(
    "--status",
    type=click.Choice(["pending", "confirmed", "rejected", "expired", "skipped", "all"]),
    default="all",
)
@click.option("--category", default=None)
@click.option("--limit", "-n", default=20)
def predictions_list(status, category, limit):
    """List predictions."""
    from predictions.store import PredictionStore

    c = get_components(skip_advisor=True)
    store = PredictionStore(c["paths"]["intel_db"])

    outcome = status if status != "all" else None
    rows = store.get_all(category=category, outcome=outcome, limit=limit)

    if not rows:
        console.print("[yellow]No predictions found.[/]")
        return

    table = Table(show_header=True, title="Predictions")
    table.add_column("Date", style="cyan", width=10)
    table.add_column("Category", style="green")
    table.add_column("Claim", max_width=40)
    table.add_column("Conf", justify="right")
    table.add_column("Due", style="dim", width=10)
    table.add_column("Outcome")

    for r in rows:
        date = r["created_at"][:10] if r["created_at"] else "?"
        due = r["evaluation_due"][:10] if r["evaluation_due"] else "?"
        conf = f"{r['confidence']:.0%}" if r["confidence"] else r["confidence_bucket"]
        outcome_str = r["outcome"]
        if outcome_str == "confirmed":
            outcome_str = f"[green]{outcome_str}[/]"
        elif outcome_str == "rejected":
            outcome_str = f"[red]{outcome_str}[/]"
        table.add_row(date, r["category"], r["claim_text"][:40], conf, due, outcome_str)

    console.print(table)


@predictions.command("review")
def predictions_review():
    """Interactively review past-due predictions."""
    from predictions.store import PredictionStore

    c = get_components(skip_advisor=True)
    store = PredictionStore(c["paths"]["intel_db"])
    due = store.get_review_due(limit=3)

    if not due:
        console.print("[green]No predictions due for review.[/]")
        return

    for pred in due:
        console.print(f"\n[bold]{pred['claim_text']}[/]")
        console.print(
            f"  Category: {pred['category']}  |  Confidence: {pred['confidence_bucket']}  |  Created: {pred['created_at'][:10]}"
        )
        choice = click.prompt(
            "Outcome? [c]onfirmed / [r]ejected / [s]kip / [e]xpire",
            type=click.Choice(["c", "r", "s", "e"]),
        )
        outcome_map = {"c": "confirmed", "r": "rejected", "s": "skipped", "e": "expired"}
        notes = click.prompt("Notes (optional)", default="", show_default=False)
        store.record_outcome(pred["id"], outcome_map[choice], notes=notes or None)
        console.print(f"  -> {outcome_map[choice]}")


@predictions.command("stats")
def predictions_stats():
    """Show prediction accuracy stats."""
    from predictions.stats import PredictionStats
    from predictions.store import PredictionStore

    c = get_components(skip_advisor=True)
    store = PredictionStore(c["paths"]["intel_db"])
    stats = PredictionStats.compute(store)

    console.print(f"\n[bold]Total predictions:[/] {stats['total']}")
    console.print(f"[bold]Review due:[/] {stats['review_due']}")

    if stats["by_outcome"]:
        console.print("\n[bold]By outcome:[/]")
        for k, v in stats["by_outcome"].items():
            console.print(f"  {k}: {v}")

    if stats["by_category"]:
        table = Table(show_header=True, title="By Category")
        table.add_column("Category")
        table.add_column("Total", justify="right")
        table.add_column("Confirmed", justify="right")
        table.add_column("Rejected", justify="right")
        table.add_column("Accuracy", justify="right")
        for cat, v in stats["by_category"].items():
            acc = f"{v['accuracy']:.0%}" if v["accuracy"] is not None else "-"
            table.add_row(cat, str(v["total"]), str(v["confirmed"]), str(v["rejected"]), acc)
        console.print(table)

    if stats["by_confidence_bucket"]:
        table = Table(show_header=True, title="By Confidence Bucket")
        table.add_column("Bucket")
        table.add_column("Total", justify="right")
        table.add_column("Confirmed", justify="right")
        table.add_column("Rejected", justify="right")
        table.add_column("Accuracy", justify="right")
        for bucket, v in stats["by_confidence_bucket"].items():
            acc = f"{v['accuracy']:.0%}" if v["accuracy"] is not None else "-"
            table.add_row(bucket, str(v["total"]), str(v["confirmed"]), str(v["rejected"]), acc)
        console.print(table)
