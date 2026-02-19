"""Mood tracking CLI command."""

import click
from rich.console import Console
from rich.table import Table

from cli.utils import get_components

console = Console()

MOOD_BAR = {
    "positive": "[green]██[/]",
    "mixed": "[yellow]██[/]",
    "neutral": "[dim]██[/]",
    "negative": "[red]██[/]",
}


@click.command()
@click.option("-d", "--days", default=30, help="Lookback days")
def mood(days: int):
    """Show mood timeline from journal entries."""
    from journal.sentiment import get_mood_history

    c = get_components(skip_advisor=True)
    timeline = get_mood_history(c["storage"], days=days)

    if not timeline:
        console.print("[yellow]No entries found. Add journal entries to track mood.[/]")
        return

    table = Table(show_header=True, title=f"Mood - last {days} days")
    table.add_column("Date", style="dim")
    table.add_column("Mood")
    table.add_column("Score", justify="right")
    table.add_column("Entry")

    for entry in timeline:
        bar = MOOD_BAR.get(entry["label"], "[dim]██[/]")
        score_str = f"{entry['score']:+.2f}"
        table.add_row(entry["date"], bar + f" {entry['label']}", score_str, entry["title"][:35])

    console.print(table)

    # Summary
    scores = [e["score"] for e in timeline]
    avg = sum(scores) / len(scores) if scores else 0
    console.print(f"\n[bold]Average:[/] {avg:+.2f}  |  Entries: {len(timeline)}")
