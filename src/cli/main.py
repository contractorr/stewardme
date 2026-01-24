"""CLI commands for AI Coach."""

import logging
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from cli.config import load_config, get_paths, setup_logging, get_limits
from journal import JournalStorage, EmbeddingManager, JournalSearch
from advisor import AdvisorEngine, RAGRetriever
from advisor.engine import APIKeyMissingError, LLMError
from intelligence.scraper import IntelStorage
from intelligence.scheduler import IntelScheduler
from intelligence.search import IntelSearch
from intelligence.embeddings import IntelEmbeddingManager

console = Console()
logger = logging.getLogger(__name__)


def get_components(skip_advisor: bool = False):
    """Initialize all components from config.

    Args:
        skip_advisor: If True, skip advisor init (for commands that don't need LLM)
    """
    config = load_config()
    paths = get_paths(config)

    storage = JournalStorage(paths["journal_dir"])
    embeddings = EmbeddingManager(paths["chroma_dir"])
    search = JournalSearch(storage, embeddings)
    intel_storage = IntelStorage(paths["intel_db"])

    # Initialize intel semantic search
    intel_embeddings = IntelEmbeddingManager(paths["chroma_dir"] / "intel")
    intel_search = IntelSearch(intel_storage, intel_embeddings)

    # Pass intel_search to RAG for semantic intel retrieval
    rag = RAGRetriever(search, paths["intel_db"], intel_search=intel_search)

    advisor = None
    if not skip_advisor:
        try:
            advisor = AdvisorEngine(rag, model=config["llm"].get("model", "claude-sonnet-4-20250514"))
        except APIKeyMissingError as e:
            console.print(f"[red]Config error:[/] {e}")
            sys.exit(1)

    return {
        "config": config,
        "paths": paths,
        "storage": storage,
        "embeddings": embeddings,
        "search": search,
        "intel_storage": intel_storage,
        "intel_search": intel_search,
        "rag": rag,
        "advisor": advisor,
    }


@click.group()
@click.version_option(version="0.1.0")
@click.option("-v", "--verbose", is_flag=True, help="Enable debug logging")
def cli(verbose: bool):
    """AI Coach - Personal professional advisor."""
    config = load_config()
    if verbose:
        config["logging"] = {"level": "DEBUG", "file_level": "DEBUG"}
    setup_logging(config)


# === Journal Commands ===

@cli.group()
def journal():
    """Manage journal entries."""
    pass


@journal.command("add")
@click.option("-t", "--type", "entry_type", default="daily",
              type=click.Choice(["daily", "project", "goal", "reflection"]),
              help="Entry type")
@click.option("--title", help="Entry title (defaults to date)")
@click.option("--tags", help="Comma-separated tags")
@click.argument("content", required=False)
def journal_add(entry_type: str, title: str, tags: str, content: str):
    """Add new journal entry. Opens editor if no content provided."""
    c = get_components()

    if not content:
        content = click.edit("# Write your entry here\n\n")
        if not content:
            console.print("[yellow]No content provided, cancelled.[/]")
            return

    tag_list = [t.strip() for t in tags.split(",")] if tags else []

    filepath = c["storage"].create(
        content=content,
        entry_type=entry_type,
        title=title,
        tags=tag_list,
    )

    # Add to embeddings
    c["embeddings"].add_entry(
        str(filepath),
        content,
        {"type": entry_type, "tags": ",".join(tag_list)},
    )

    console.print(f"[green]Created:[/] {filepath.name}")


@journal.command("list")
@click.option("-t", "--type", "entry_type", help="Filter by type")
@click.option("--tag", help="Filter by tag")
@click.option("-n", "--limit", default=10, help="Max entries to show")
def journal_list(entry_type: str, tag: str, limit: int):
    """List recent journal entries."""
    c = get_components(skip_advisor=True)
    entries = c["storage"].list_entries(entry_type=entry_type, limit=limit)

    # Filter by tag if specified
    if tag:
        entries = [e for e in entries if tag in e.get("tags", [])]

    if not entries:
        console.print("[yellow]No entries found.[/]")
        return

    table = Table(show_header=True)
    table.add_column("Date", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("Title")
    table.add_column("Tags", style="dim")

    for e in entries:
        date = e["created"][:10] if e["created"] else "?"
        tags = ", ".join(e["tags"][:3]) if e["tags"] else ""
        table.add_row(date, e["type"], e["title"][:40], tags)

    console.print(table)


@journal.command("search")
@click.argument("query")
@click.option("-n", "--limit", default=5, help="Max results")
def journal_search(query: str, limit: int):
    """Semantic search across journal."""
    c = get_components()

    with console.status("Searching..."):
        results = c["search"].semantic_search(query, n_results=limit)

    if not results:
        console.print("[yellow]No matches found.[/]")
        return

    for r in results:
        score = f"{r['relevance']:.0%}"
        console.print(f"\n[cyan]{r['title']}[/] ({r['type']}) - {score} match")
        console.print(f"[dim]{r['created'][:10] if r['created'] else ''}[/]")
        preview = r["content"][:200].replace("\n", " ")
        console.print(f"{preview}...")


@journal.command("sync")
def journal_sync():
    """Sync all entries to embedding store."""
    c = get_components()

    with console.status("Syncing embeddings..."):
        added, removed = c["search"].sync_embeddings()

    console.print(f"[green]Synced:[/] {added} added, {removed} removed")
    console.print(f"Total entries: {c['embeddings'].count()}")


@journal.command("view")
@click.argument("filename")
def journal_view(filename: str):
    """View a journal entry."""
    c = get_components()
    journal_dir = c["paths"]["journal_dir"].resolve()
    filepath = (journal_dir / filename).resolve()

    # Security: validate path is within journal_dir
    if not str(filepath).startswith(str(journal_dir)):
        console.print("[red]Error:[/] Invalid path")
        return

    if not filepath.exists():
        # Try to find by partial match (safe - glob is within journal_dir)
        matches = [m for m in journal_dir.glob(f"*{filename}*")
                   if m.resolve().is_relative_to(journal_dir)]
        if matches:
            filepath = matches[0]
        else:
            console.print(f"[red]Not found:[/] {filename}")
            return

    post = c["storage"].read(filepath)
    console.print(f"\n[cyan bold]{post.get('title', filepath.stem)}[/]")
    console.print(f"[dim]Type: {post.get('type')} | Created: {post.get('created', '?')[:10]}[/]")
    if post.get("tags"):
        console.print(f"[dim]Tags: {', '.join(post['tags'])}[/]")
    console.print()
    console.print(Markdown(post.content))


@journal.command("edit")
@click.argument("filename")
def journal_edit(filename: str):
    """Edit a journal entry in $EDITOR."""
    import os
    import subprocess

    c = get_components(skip_advisor=True)
    journal_dir = c["paths"]["journal_dir"].resolve()
    filepath = (journal_dir / filename).resolve()

    # Security: validate path
    if not str(filepath).startswith(str(journal_dir)):
        console.print("[red]Error:[/] Invalid path")
        return

    if not filepath.exists():
        matches = [m for m in journal_dir.glob(f"*{filename}*")
                   if m.resolve().is_relative_to(journal_dir)]
        if matches:
            filepath = matches[0]
        else:
            console.print(f"[red]Not found:[/] {filename}")
            return

    editor = os.environ.get("EDITOR", "vim")
    try:
        subprocess.run([editor, str(filepath)], check=True)
        # Re-sync embeddings after edit
        post = c["storage"].read(filepath)
        c["embeddings"].add_entry(
            str(filepath),
            post.content,
            {"type": post.get("type", ""), "tags": ",".join(post.get("tags", []))},
        )
        console.print(f"[green]Updated:[/] {filepath.name}")
    except subprocess.CalledProcessError:
        console.print("[red]Editor exited with error[/]")
    except FileNotFoundError:
        console.print(f"[red]Editor not found:[/] {editor}")


@journal.command("delete")
@click.argument("filename")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
def journal_delete(filename: str, yes: bool):
    """Delete a journal entry."""
    c = get_components(skip_advisor=True)
    journal_dir = c["paths"]["journal_dir"].resolve()
    filepath = (journal_dir / filename).resolve()

    # Security: validate path
    if not str(filepath).startswith(str(journal_dir)):
        console.print("[red]Error:[/] Invalid path")
        return

    if not filepath.exists():
        matches = [m for m in journal_dir.glob(f"*{filename}*")
                   if m.resolve().is_relative_to(journal_dir)]
        if matches:
            filepath = matches[0]
        else:
            console.print(f"[red]Not found:[/] {filename}")
            return

    if not yes:
        if not click.confirm(f"Delete {filepath.name}?"):
            return

    filepath.unlink()
    c["embeddings"].delete_entry(str(filepath))
    console.print(f"[green]Deleted:[/] {filepath.name}")


# === Ask Commands ===

@cli.command()
@click.argument("question")
@click.option("--type", "advice_type", default="general",
              type=click.Choice(["general", "career", "goals", "opportunities"]),
              help="Type of advice to get")
def ask(question: str, advice_type: str):
    """Ask a question and get contextual advice."""
    c = get_components()

    try:
        with console.status("Thinking..."):
            response = c["advisor"].ask(question, advice_type=advice_type)
        console.print()
        console.print(Markdown(response))
    except LLMError as e:
        console.print(f"[red]Error:[/] {e}")
        sys.exit(1)


@cli.command()
def review():
    """Generate weekly review from recent entries."""
    c = get_components()

    try:
        with console.status("Generating weekly review..."):
            response = c["advisor"].weekly_review()
        console.print()
        console.print(Markdown(response))
    except LLMError as e:
        console.print(f"[red]Error:[/] {e}")
        sys.exit(1)


@cli.command()
def opportunities():
    """Detect opportunities based on your profile and trends."""
    c = get_components()

    try:
        with console.status("Analyzing opportunities..."):
            response = c["advisor"].detect_opportunities()
        console.print()
        console.print(Markdown(response))
    except LLMError as e:
        console.print(f"[red]Error:[/] {e}")
        sys.exit(1)


@cli.command()
@click.argument("goal", required=False)
def goals(goal: str):
    """Analyze goal progress. Optionally specify a goal to focus on."""
    c = get_components()

    try:
        with console.status("Analyzing goals..."):
            response = c["advisor"].analyze_goals(specific_goal=goal)
        console.print()
        console.print(Markdown(response))
    except LLMError as e:
        console.print(f"[red]Error:[/] {e}")
        sys.exit(1)


# === Intelligence Commands ===

@cli.command()
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


@cli.command()
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


@cli.command()
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


@cli.command()
def init():
    """Initialize coach directories and config."""
    config = load_config()
    paths = get_paths(config)

    for name, path in paths.items():
        if name == "intel_db":
            path.parent.mkdir(parents=True, exist_ok=True)
        else:
            path.mkdir(parents=True, exist_ok=True)
        console.print(f"[green]✓[/] {name}: {path}")

    # Create default config if not exists
    config_path = Path.home() / "coach" / "config.yaml"
    if not config_path.exists():
        import yaml
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False)
        console.print(f"[green]✓[/] Created config: {config_path}")

    console.print("\n[bold]Ready![/] Add ANTHROPIC_API_KEY to your environment.")


# === Daemon Commands ===

@cli.group()
def daemon():
    """Manage background scheduler."""
    pass


_daemon_scheduler = None


@daemon.command("start")
@click.option("--cron", default="0 6 * * *", help="Cron expression (default: daily 6am)")
def daemon_start(cron: str):
    """Start background intelligence gathering."""
    global _daemon_scheduler
    c = get_components(skip_advisor=True)

    if _daemon_scheduler is not None:
        console.print("[yellow]Daemon already running[/]")
        return

    _daemon_scheduler = IntelScheduler(c["intel_storage"], c["config"].get("sources", {}))
    _daemon_scheduler.start(cron_expr=cron)

    console.print(f"[green]Started[/] scheduler with cron: {cron}")
    console.print("Press Ctrl+C to stop")

    try:
        import time
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        _daemon_scheduler.stop()
        _daemon_scheduler = None
        console.print("\n[yellow]Stopped[/]")


@daemon.command("run-once")
def daemon_run_once():
    """Run intelligence gathering once (for cron/launchd integration)."""
    c = get_components(skip_advisor=True)
    scheduler = IntelScheduler(c["intel_storage"], c["config"].get("sources", {}))
    results = scheduler.run_now()

    # Sync embeddings
    c["intel_search"].sync_embeddings()

    total_new = sum(d.get("new", 0) for d in results.values() if "error" not in d)
    console.print(f"Gathered {total_new} new items")


if __name__ == "__main__":
    cli()
