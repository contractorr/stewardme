"""Research CLI commands."""

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

from cli.utils import get_components
from intelligence.scheduler import IntelScheduler

console = Console()


@click.group()
def research():
    """Deep research on topics from your goals and journal."""
    pass


@research.command("run")
@click.option("--topic", "-t", help="Specific topic to research (overrides auto-selection)")
def research_run(topic: str):
    """Run deep research on selected topics."""
    c = get_components()

    scheduler = IntelScheduler(
        c["intel_storage"],
        c["config"].get("sources", {}),
        journal_storage=c["storage"],
        embeddings=c["embeddings"],
        full_config=c["config"],
    )

    # Check if research is enabled
    if not c["config"].get("research", {}).get("enabled", False):
        console.print(
            "[yellow]Research not enabled. Add 'research.enabled: true' to config.yaml[/]"
        )
        return

    with console.status("Running deep research..."):
        results = scheduler.run_research_now(topic=topic)

    if not results:
        console.print("[yellow]No topics to research or research not configured.[/]")
        return

    for r in results:
        if r["success"]:
            console.print(
                f"[green]✓[/] {r['topic']} -> {r['filepath'].name if r['filepath'] else 'N/A'}"
            )
        else:
            error = r.get("error", "Unknown error")
            console.print(f"[red]✗[/] {r['topic']}: {error}")


@research.command("topics")
def research_topics():
    """Show suggested research topics based on your goals and journal."""
    c = get_components(skip_advisor=True)

    scheduler = IntelScheduler(
        c["intel_storage"],
        c["config"].get("sources", {}),
        journal_storage=c["storage"],
        embeddings=c["embeddings"],
        full_config=c["config"],
    )

    # Enable temporarily to get topics
    if "research" not in c["config"]:
        c["config"]["research"] = {}
    c["config"]["research"]["enabled"] = True

    topics = scheduler.get_research_topics()

    if not topics:
        console.print("[yellow]No research topics identified. Add goals or journal entries.[/]")
        return

    table = Table(show_header=True, title="Suggested Research Topics")
    table.add_column("Topic", style="cyan")
    table.add_column("Source", style="green")
    table.add_column("Score", justify="right")
    table.add_column("Reason")

    for t in topics:
        table.add_row(
            t["topic"],
            t["source"],
            str(t["score"]),
            t["reason"][:50],
        )

    console.print(table)


@research.command("list")
@click.option("-n", "--limit", default=10, help="Max entries to show")
def research_list(limit: int):
    """List recent research reports."""
    c = get_components(skip_advisor=True)
    entries = c["storage"].list_entries(entry_type="research", limit=limit)

    if not entries:
        console.print("[yellow]No research reports yet. Run 'coach research run' first.[/]")
        return

    table = Table(show_header=True)
    table.add_column("Date", style="cyan")
    table.add_column("Topic")
    table.add_column("Tags", style="dim")

    for e in entries:
        date = e["created"][:10] if e["created"] else "?"
        topic = e["title"].replace("Research: ", "")
        tags = ", ".join(e["tags"][:3]) if e["tags"] else ""
        table.add_row(date, topic[:40], tags)

    console.print(table)


@research.command("view")
@click.argument("filename")
def research_view(filename: str):
    """View a research report."""
    c = get_components(skip_advisor=True)
    journal_dir = c["paths"]["journal_dir"].resolve()

    # Find by partial match
    matches = [
        m
        for m in journal_dir.glob(f"*research*{filename}*")
        if m.resolve().is_relative_to(journal_dir)
    ]

    if not matches:
        # Try broader search
        matches = [
            m for m in journal_dir.glob(f"*{filename}*") if m.resolve().is_relative_to(journal_dir)
        ]

    if not matches:
        console.print(f"[red]Not found:[/] {filename}")
        return

    filepath = matches[0]
    post = c["storage"].read(filepath)

    console.print(f"\n[cyan bold]{post.get('title', filepath.stem)}[/]")
    console.print(f"[dim]Created: {post.get('created', '?')[:10]}[/]")
    if post.get("topic"):
        console.print(f"[dim]Topic: {post['topic']}[/]")
    console.print()
    console.print(Markdown(post.content))
