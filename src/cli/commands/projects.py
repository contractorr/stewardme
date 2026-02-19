"""Project discovery CLI commands."""

import sys

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

from cli.utils import get_components, get_profile_storage

console = Console()


@click.group()
def projects():
    """Discover open-source contributions and side-project ideas."""
    pass


@projects.command("discover")
@click.option("-n", "--limit", default=15, help="Max issues to show")
@click.option("--days", default=14, help="Lookback window in days")
def projects_discover(limit: int, days: int):
    """Find matching open-source issues based on your skills."""
    from advisor.projects import get_matching_issues

    c = get_components(skip_advisor=True)
    ps = get_profile_storage(c["config"])
    profile = ps.load()

    issues = get_matching_issues(c["intel_storage"], profile=profile, limit=limit, days=days)

    if not issues:
        console.print("[yellow]No matching issues found. Run [cyan]coach scrape[/] first.[/]")
        return

    table = Table(title="Matching Open-Source Issues", show_header=True)
    table.add_column("Match", justify="right", style="green")
    table.add_column("Issue")
    table.add_column("Repo", style="cyan")
    table.add_column("Labels", style="dim")

    for issue in issues:
        match_score = issue.get("_match_score", 0)
        title = issue.get("title", "")[:45]
        # Extract repo from summary
        summary = issue.get("summary", "")
        repo = ""
        if "Repo: " in summary:
            repo = summary.split("Repo: ")[1].split(" |")[0][:30]
        tags = issue.get("tags", "")
        if isinstance(tags, list):
            tags = ", ".join(tags[:3])
        elif isinstance(tags, str):
            tags = ", ".join(tags.split(",")[:3])

        table.add_row(str(match_score), title, repo, tags[:30])

    console.print(table)
    console.print(f"\n[dim]Showing {len(issues)} issues. Set up profile ([cyan]coach profile update[/]) for better matching.[/]")


@projects.command("ideas")
def projects_ideas():
    """Generate side-project ideas from your journal entries."""
    from advisor.engine import LLMError
    from advisor.projects import ProjectIdeaGenerator

    c = get_components()
    generator = ProjectIdeaGenerator(c["rag"], c["advisor"]._call_llm)

    try:
        with console.status("Generating project ideas from your journal..."):
            ideas = generator.generate_ideas()
        console.print()
        console.print(Markdown(ideas))
    except LLMError as e:
        console.print(f"[red]Error:[/] {e}")
        sys.exit(1)


@projects.command("list")
@click.option("--days", default=14, help="Lookback window")
def projects_list(days: int):
    """List tracked project opportunities from intelligence."""
    c = get_components(skip_advisor=True)
    items = c["intel_storage"].get_recent(days=days, limit=50)
    issues = [i for i in items if i.get("source") == "github_issues"]

    if not issues:
        console.print("[yellow]No project opportunities tracked. Enable github_issues scraper in config.[/]")
        return

    for issue in issues[:20]:
        console.print(f"\n[cyan]{issue['title'][:60]}[/]")
        console.print(f"[dim]{issue['summary'][:100]}[/]")
        if issue.get("url"):
            console.print(f"[blue underline]{issue['url']}[/]")
