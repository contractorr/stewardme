"""Trends CLI command."""

import click
from rich.console import Console
from rich.table import Table

from cli.utils import get_components

console = Console()


@click.command()
@click.option("-d", "--days", default=90, help="Lookback period in days")
@click.option("-w", "--window", default="weekly", type=click.Choice(["weekly", "monthly"]))
@click.option("-n", "--clusters", default=8, help="Number of topic clusters")
def trends(days: int, window: str, clusters: int):
    """Detect emerging and declining journal topics."""
    from journal.trends import TrendDetector

    c = get_components(skip_advisor=True)
    detector = TrendDetector(c["search"])

    with console.status("Analyzing trends..."):
        all_trends = detector.detect_trends(days=days, window=window, n_clusters=clusters)

    if not all_trends:
        console.print("[yellow]Not enough entries to detect trends. Need more journal data.[/]")
        return

    table = Table(title=f"Topic Trends (past {days} days, {window})", show_header=True)
    table.add_column("Topic", max_width=30)
    table.add_column("Direction", justify="center")
    table.add_column("Growth", justify="right")
    table.add_column("Entries", justify="right")
    table.add_column("Trend", min_width=10)

    for t in all_trends:
        direction = t["direction"]
        if direction == "emerging":
            dir_style = "[green]emerging[/]"
            sparkline = "".join("+" if c > 0 else "." for c in t["counts"])
        elif direction == "declining":
            dir_style = "[red]declining[/]"
            sparkline = "".join("-" if c > 0 else "." for c in t["counts"])
        else:
            dir_style = "[dim]stable[/]"
            sparkline = "".join("=" if c > 0 else "." for c in t["counts"])

        table.add_row(
            t["topic"][:30],
            dir_style,
            f"{t['growth_rate']:+.0%}",
            str(t["total_entries"]),
            sparkline,
        )

    console.print(table)

    emerging = [t for t in all_trends if t["direction"] == "emerging"]
    declining = [t for t in all_trends if t["direction"] == "declining"]
    if emerging:
        console.print(f"\n[green]{len(emerging)} emerging topic(s)[/]")
    if declining:
        console.print(f"[red]{len(declining)} declining topic(s)[/]")
