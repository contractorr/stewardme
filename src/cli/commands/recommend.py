"""Recommendation CLI commands."""

import sys

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

from cli.utils import get_components, get_rec_db_path
from advisor.engine import LLMError
from advisor.recommendation_storage import RecommendationStorage

console = Console()


def _display_recommendations(recs: list):
    """Display recommendations in formatted output."""
    if not recs:
        console.print("[yellow]No recommendations generated (may need more journal context).[/]")
        return

    for rec in recs:
        console.print(f"\n[cyan bold]{rec.title}[/] [dim][{rec.category}][/]")
        console.print(f"[green]Score: {rec.score:.1f}[/]")
        if rec.description:
            console.print(rec.description)
        if rec.rationale:
            console.print(f"\n[dim]Why: {rec.rationale}[/]")
        console.print()


@click.group()
def recommend():
    """Proactive recommendations for learning, career, entrepreneurial, and investment opportunities."""
    pass


@recommend.command("learning")
@click.option("-n", "--limit", default=3, help="Max recommendations")
def recommend_learning(limit: int):
    """Get learning/skills recommendations."""
    c = get_components()
    rec_config = c["config"].get("recommendations", {})
    db_path = get_rec_db_path(c["config"])

    try:
        with console.status("Analyzing skills to learn..."):
            recs = c["advisor"].generate_recommendations(
                "learning", db_path, rec_config, max_items=limit
            )
        _display_recommendations(recs)
    except LLMError as e:
        console.print(f"[red]Error:[/] {e}")
        sys.exit(1)


@recommend.command("career")
@click.option("-n", "--limit", default=3, help="Max recommendations")
def recommend_career(limit: int):
    """Get career move recommendations."""
    c = get_components()
    rec_config = c["config"].get("recommendations", {})
    db_path = get_rec_db_path(c["config"])

    try:
        with console.status("Analyzing career opportunities..."):
            recs = c["advisor"].generate_recommendations(
                "career", db_path, rec_config, max_items=limit
            )
        _display_recommendations(recs)
    except LLMError as e:
        console.print(f"[red]Error:[/] {e}")
        sys.exit(1)


@recommend.command("entrepreneurial")
@click.option("-n", "--limit", default=3, help="Max recommendations")
def recommend_entrepreneurial(limit: int):
    """Get entrepreneurial opportunity recommendations."""
    c = get_components()
    rec_config = c["config"].get("recommendations", {})
    db_path = get_rec_db_path(c["config"])

    try:
        with console.status("Identifying business opportunities..."):
            recs = c["advisor"].generate_recommendations(
                "entrepreneurial", db_path, rec_config, max_items=limit
            )
        _display_recommendations(recs)
    except LLMError as e:
        console.print(f"[red]Error:[/] {e}")
        sys.exit(1)


@recommend.command("investment")
@click.option("-n", "--limit", default=3, help="Max recommendations")
def recommend_investment(limit: int):
    """Get investment opportunity recommendations."""
    c = get_components()
    rec_config = c["config"].get("recommendations", {})
    db_path = get_rec_db_path(c["config"])

    try:
        with console.status("Analyzing investment opportunities..."):
            recs = c["advisor"].generate_recommendations(
                "investment", db_path, rec_config, max_items=limit
            )
        _display_recommendations(recs)
    except LLMError as e:
        console.print(f"[red]Error:[/] {e}")
        sys.exit(1)


@recommend.command("all")
@click.option("-n", "--limit", default=3, help="Max per category")
def recommend_all(limit: int):
    """Get recommendations across all categories."""
    c = get_components()
    rec_config = c["config"].get("recommendations", {})
    db_path = get_rec_db_path(c["config"])

    try:
        with console.status("Generating all recommendations..."):
            recs = c["advisor"].generate_recommendations(
                "all", db_path, rec_config, max_items=limit
            )
        _display_recommendations(recs)
    except LLMError as e:
        console.print(f"[red]Error:[/] {e}")
        sys.exit(1)


@recommend.command("brief")
@click.option("-n", "--limit", default=5, help="Max items in brief")
@click.option("--save", is_flag=True, help="Save as journal entry")
def recommend_brief(limit: int, save: bool):
    """Generate weekly action brief."""
    c = get_components()
    rec_config = c["config"].get("recommendations", {})
    db_path = get_rec_db_path(c["config"])
    min_score = rec_config.get("scoring", {}).get("min_threshold", 6.0)

    try:
        with console.status("Generating action brief..."):
            brief = c["advisor"].generate_action_brief(
                db_path,
                journal_storage=c["storage"] if save else None,
                max_items=limit,
                min_score=min_score,
                save=save,
            )
        console.print()
        console.print(Markdown(brief))
        if save:
            console.print("\n[green]Saved to journal as action_brief entry.[/]")
    except LLMError as e:
        console.print(f"[red]Error:[/] {e}")
        sys.exit(1)


@recommend.command("history")
@click.option("-n", "--limit", default=20, help="Max entries")
@click.option("-c", "--category", help="Filter by category")
@click.option("-s", "--status", help="Filter by status")
def recommend_history(limit: int, category: str, status: str):
    """View recommendation history."""
    c = get_components(skip_advisor=True)
    db_path = get_rec_db_path(c["config"])
    storage = RecommendationStorage(db_path)

    if category:
        recs = storage.list_by_category(category, status=status, limit=limit)
    else:
        recs = storage.list_recent(days=90, status=status, limit=limit)

    if not recs:
        console.print("[yellow]No recommendations found.[/]")
        return

    table = Table(show_header=True)
    table.add_column("ID", style="dim")
    table.add_column("Category", style="cyan")
    table.add_column("Title")
    table.add_column("Score", justify="right")
    table.add_column("Status", style="green")
    table.add_column("Date", style="dim")

    for rec in recs:
        date = rec.created_at[:10] if rec.created_at else "?"
        table.add_row(
            str(rec.id),
            rec.category,
            rec.title[:40],
            f"{rec.score:.1f}",
            rec.status,
            date,
        )

    console.print(table)


@recommend.command("update")
@click.argument("rec_id", type=int)
@click.option("--status", "-s", required=True,
              type=click.Choice(["suggested", "in_progress", "completed", "dismissed"]),
              help="New status")
def recommend_update(rec_id: int, status: str):
    """Update recommendation status."""
    c = get_components(skip_advisor=True)
    db_path = get_rec_db_path(c["config"])
    storage = RecommendationStorage(db_path)

    if storage.update_status(rec_id, status):
        console.print(f"[green]Updated recommendation {rec_id} to {status}[/]")
    else:
        console.print(f"[red]Recommendation {rec_id} not found[/]")


@recommend.command("view")
@click.argument("rec_id", type=int)
def recommend_view(rec_id: int):
    """View a specific recommendation."""
    c = get_components(skip_advisor=True)
    db_path = get_rec_db_path(c["config"])
    storage = RecommendationStorage(db_path)

    rec = storage.get(rec_id)
    if not rec:
        console.print(f"[red]Recommendation {rec_id} not found[/]")
        return

    console.print(f"\n[cyan bold]{rec.title}[/]")
    console.print(f"[dim]Category: {rec.category} | Score: {rec.score:.1f} | Status: {rec.status}[/]")
    console.print(f"[dim]Created: {rec.created_at[:10] if rec.created_at else '?'}[/]")

    # Show rating if present
    if rec.metadata and rec.metadata.get("user_rating"):
        rating = rec.metadata["user_rating"]
        stars = "★" * rating + "☆" * (5 - rating)
        console.print(f"[yellow]Rating: {stars}[/]")

    console.print()
    if rec.description:
        console.print(f"[bold]Description:[/] {rec.description}")
    if rec.rationale:
        console.print(f"\n[bold]Rationale:[/] {rec.rationale}")

    # Show action plan if present
    if rec.metadata and rec.metadata.get("action_plan"):
        console.print(f"\n[bold green]Action Plan:[/]")
        console.print(Markdown(rec.metadata["action_plan"]))

    if rec.metadata and rec.metadata.get("feedback_comment"):
        console.print(f"\n[dim]Your feedback: {rec.metadata['feedback_comment']}[/]")


@recommend.command("rate")
@click.argument("rec_id", type=int)
@click.option("-r", "--rating", type=click.IntRange(1, 5), required=True, help="Rating 1-5")
@click.option("-c", "--comment", help="Optional feedback comment")
def recommend_rate(rec_id: int, rating: int, comment: str):
    """Rate a recommendation's usefulness."""
    c = get_components(skip_advisor=True)
    db_path = get_rec_db_path(c["config"])
    storage = RecommendationStorage(db_path)

    if storage.add_feedback(rec_id, rating, comment):
        stars = "★" * rating + "☆" * (5 - rating)
        console.print(f"[green]Rated recommendation {rec_id}: {stars}[/]")
        if comment:
            console.print(f"[dim]Comment: {comment}[/]")
    else:
        console.print(f"[red]Recommendation {rec_id} not found[/]")
