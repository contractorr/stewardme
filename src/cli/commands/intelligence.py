"""Intelligence CLI commands."""

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from cli.utils import get_components
from intelligence.scheduler import IntelScheduler

console = Console()


@click.command()
def scrape():
    """Run intelligence gathering now."""
    c = get_components(skip_advisor=True)
    scheduler = IntelScheduler(c["intel_storage"], c["config"].get("sources", {}))

    with console.status("Gathering intelligence..."):
        results = scheduler.run_now()

    # Sync to embeddings for semantic search
    with console.status("Syncing embeddings..."):
        c["intel_search"].sync_embeddings()

    table = Table(show_header=True)
    table.add_column("Source")
    table.add_column("Scraped", justify="right")
    table.add_column("New", justify="right", style="green")

    for source, data in results.items():
        if "error" in data:
            table.add_row(source, "[red]error[/]", data["error"][:30])
        else:
            table.add_row(source, str(data["scraped"]), str(data["new"]))

    console.print(table)


@click.command()
@click.option("-n", "--days", default=7, help="Days to look back")
@click.option("--limit", default=20, help="Max items to show")
def brief(days: int, limit: int):
    """Show recent intelligence brief."""
    c = get_components(skip_advisor=True)
    items = c["intel_storage"].get_recent(days=days, limit=limit)

    if not items:
        console.print("[yellow]No intelligence items found. Run 'coach scrape' first.[/]")
        return

    for item in items:
        console.print(f"\n[cyan]{item['title'][:60]}[/]")
        console.print(f"[dim]{item['source']} | {item['scraped_at'][:10]}[/]")
        if item["summary"]:
            console.print(item["summary"][:150])
        console.print(f"[blue]{item['url']}[/]")


@click.command()
def sources():
    """Show configured intelligence sources."""
    c = get_components(skip_advisor=True)
    sources_config = c["config"].get("sources", {})

    console.print("\n[bold]Enabled sources:[/]")
    for src in sources_config.get("enabled", []):
        console.print(f"  [green]✓[/] {src}")

    console.print("\n[bold]RSS Feeds:[/]")
    for url in sources_config.get("rss_feeds", []):
        console.print(f"  {url}")

    console.print("\n[bold]Custom Blogs:[/]")
    for url in sources_config.get("custom_blogs", []):
        console.print(f"  {url}")


@click.command("intel-export")
@click.option("-o", "--output", required=True, type=click.Path(), help="Output file path")
@click.option(
    "-f",
    "--format",
    "fmt",
    default="json",
    type=click.Choice(["json", "csv", "markdown"]),
    help="Export format",
)
@click.option("-d", "--days", type=int, default=30, help="Only last N days")
@click.option("-s", "--source", help="Filter by source")
@click.option("-n", "--limit", type=int, help="Max items to export")
def intel_export(output: str, fmt: str, days: int, source: str, limit: int):
    """Export intelligence items to file."""
    from intelligence.export import IntelExporter

    c = get_components(skip_advisor=True)
    exporter = IntelExporter(c["intel_storage"])

    output_path = Path(output)

    with console.status(f"Exporting to {fmt}..."):
        if fmt == "json":
            count = exporter.export_json(output_path, days=days, source=source, limit=limit)
        elif fmt == "csv":
            count = exporter.export_csv(output_path, days=days, source=source, limit=limit)
        else:
            count = exporter.export_markdown(output_path, days=days, source=source, limit=limit)

    console.print(f"[green]Exported {count} items to {output_path}[/]")
