"""Learning path CLI commands."""

import sys

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

from cli.utils import get_components

console = Console()


def _get_lp_storage(config: dict):
    """Get LearningPathStorage from config."""
    from advisor.learning_paths import LearningPathStorage

    lp_dir = config.get("learning_paths", {}).get("dir", "~/coach/learning_paths")
    return LearningPathStorage(lp_dir)


@click.group()
def learn():
    """Learning paths — skill gaps, structured curricula, progress tracking."""
    pass


@learn.command("gaps")
def learn_gaps():
    """Analyze skill gaps between your profile and aspirations."""
    from advisor.engine import LLMError
    from advisor.skills import SkillGapAnalyzer

    c = get_components()
    analyzer = SkillGapAnalyzer(c["rag"], c["advisor"]._call_llm)

    try:
        with console.status("Analyzing skill gaps..."):
            analysis = analyzer.analyze()
        console.print()
        console.print(Markdown(analysis))
    except LLMError as e:
        console.print(f"[red]Error:[/] {e}")
        sys.exit(1)


@learn.command("paths")
@click.option("-s", "--status", type=click.Choice(["active", "completed", "all"]), default="all")
def learn_paths(status: str):
    """List learning paths."""
    c = get_components(skip_advisor=True)
    storage = _get_lp_storage(c["config"])

    filter_status = status if status != "all" else None
    paths = storage.list_paths(status=filter_status)

    if not paths:
        console.print(
            "[yellow]No learning paths. Run [cyan]coach learn start <skill>[/] to create one.[/]"
        )
        return

    table = Table(title="Learning Paths", show_header=True)
    table.add_column("ID", style="dim")
    table.add_column("Skill", style="cyan")
    table.add_column("Progress")
    table.add_column("Modules", justify="right")
    table.add_column("Status", style="green")
    table.add_column("Created", style="dim")

    for p in paths:
        pct = p["progress"]
        bar = "[green]" + "█" * (pct // 10) + "[/]" + "[dim]" + "░" * (10 - pct // 10) + "[/]"
        table.add_row(
            p["id"],
            p["skill"],
            f"{bar} {pct}%",
            f"{p['completed_modules']}/{p['total_modules']}",
            p["status"],
            p["created_at"][:10] if p["created_at"] else "?",
        )

    console.print(table)


@learn.command("start")
@click.argument("skill")
@click.option("--current", default=1, type=click.IntRange(1, 5), help="Current proficiency 1-5")
@click.option("--target", default=4, type=click.IntRange(1, 5), help="Target proficiency 1-5")
def learn_start(skill: str, current: int, target: int):
    """Generate a new learning path for a skill."""
    from advisor.engine import LLMError
    from advisor.learning_paths import LearningPathGenerator

    c = get_components()
    storage = _get_lp_storage(c["config"])

    generator = LearningPathGenerator(c["rag"], c["advisor"]._call_llm, storage)

    try:
        with console.status(f"Generating learning path for {skill}..."):
            filepath = generator.generate(skill, current_level=current, target_level=target)
        console.print("[green]Learning path created![/]")
        console.print(f"[dim]Saved to: {filepath}[/]")

        # Show the path
        import frontmatter

        post = frontmatter.load(filepath)
        console.print()
        console.print(Markdown(post.content))
    except LLMError as e:
        console.print(f"[red]Error:[/] {e}")
        sys.exit(1)


@learn.command("progress")
@click.argument("path_id")
@click.argument("completed", type=int)
def learn_progress(path_id: str, completed: int):
    """Update progress on a learning path. E.g.: coach learn progress abc123 3"""
    c = get_components(skip_advisor=True)
    storage = _get_lp_storage(c["config"])

    if storage.update_progress(path_id, completed):
        path = storage.get(path_id)
        if path:
            console.print(
                f"[green]Updated {path['skill']}:[/] {path['completed_modules']}/{path['total_modules']} modules ({path['progress']}%)"
            )
            if path["status"] == "completed":
                console.print("[bold green]Learning path completed![/]")
    else:
        console.print(f"[red]Learning path {path_id} not found[/]")


@learn.command("next")
def learn_next():
    """Suggest what to study next based on active learning paths."""
    from advisor.engine import LLMError
    from advisor.learning_paths import LearningPathGenerator

    c = get_components()
    storage = _get_lp_storage(c["config"])
    generator = LearningPathGenerator(c["rag"], c["advisor"]._call_llm, storage)

    try:
        with console.status("Figuring out your next study session..."):
            suggestion = generator.get_next_action()
        if suggestion:
            console.print()
            console.print(Markdown(suggestion))
        else:
            console.print(
                "[yellow]No active learning paths. Run [cyan]coach learn start <skill>[/] to begin.[/]"
            )
    except LLMError as e:
        console.print(f"[red]Error:[/] {e}")
        sys.exit(1)


@learn.command("check-in")
@click.argument("path_id")
def learn_check_in(path_id: str):
    """Interactive check-in on your current learning module."""
    c = get_components(skip_advisor=True)
    storage = _get_lp_storage(c["config"])

    path = storage.get(path_id)
    if not path:
        console.print(f"[red]Learning path {path_id} not found[/]")
        return

    current_module = path.get("completed_modules", 0) + 1
    total = path.get("total_modules", 1)

    if current_module > total:
        console.print("[green]All modules completed![/]")
        return

    # Extract module title from content
    import re

    pattern = rf"###\s+Module\s+{current_module}\b[^\n]*"
    match = re.search(pattern, path.get("content", ""))
    module_title = match.group(0).strip() if match else f"Module {current_module}"

    console.print(f"\n[cyan bold]{path['skill']}[/] — {module_title}")
    console.print(f"[dim]Progress: {path['completed_modules']}/{total} modules[/]\n")

    action = click.prompt(
        "Action",
        type=click.Choice(["continue", "deepen", "skip"], case_sensitive=False),
    )

    result = storage.check_in(path_id, current_module, action)
    if not result:
        console.print("[red]Check-in failed[/]")
        return

    if action == "deepen":
        from advisor.learning_paths import SubModuleGenerator

        try:
            full_c = get_components()
            generator = SubModuleGenerator(full_c["advisor"]._call_llm, storage)
            with console.status("Generating deep dive..."):
                deep_dive = generator.generate_deep_dive(path_id, current_module)
            if deep_dive:
                console.print()
                console.print(Markdown(deep_dive))
            else:
                console.print("[yellow]Could not generate deep dive[/]")
        except Exception as e:
            console.print(f"[yellow]Deep dive unavailable: {e}[/]")
    else:
        console.print(
            f"[green]Updated:[/] {result['completed_modules']}/{result['total_modules']} modules ({result['progress']}%)"
        )
        if result.get("status") == "completed":
            console.print("[bold green]Learning path completed![/]")


@learn.command("view")
@click.argument("path_id")
def learn_view(path_id: str):
    """View a learning path in detail."""
    c = get_components(skip_advisor=True)
    storage = _get_lp_storage(c["config"])

    path = storage.get(path_id)
    if not path:
        console.print(f"[red]Learning path {path_id} not found[/]")
        return

    console.print(f"\n[cyan bold]{path['skill']}[/] ({path['status']})")
    console.print(
        f"[dim]Progress: {path['completed_modules']}/{path['total_modules']} modules ({path['progress']}%)[/]"
    )
    console.print()
    console.print(Markdown(path["content"]))
