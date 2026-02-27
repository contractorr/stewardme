"""Heartbeat CLI commands — status, history, run-once."""

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from cli.utils import get_components

console = Console()


@click.group()
def heartbeat():
    """Proactive intel-to-goal matching heartbeat."""
    pass


@heartbeat.command("status")
def heartbeat_status():
    """Show last run time and active notification count."""
    c = get_components(skip_advisor=True)
    db_path = Path(c["config"]["paths"]["intel_db"]).expanduser()

    from intelligence.heartbeat import ActionBriefStore

    store = ActionBriefStore(db_path)
    last_run = store.get_last_run_at()
    active = store.get_active(limit=100)

    console.print(f"Last run: {last_run or 'never'}")
    console.print(f"Active notifications: {len(active)}")


@heartbeat.command("history")
@click.option("--limit", "-n", default=10, help="Number of recent runs to show")
def heartbeat_history(limit: int):
    """Show recent heartbeat run history."""
    c = get_components(skip_advisor=True)
    db_path = Path(c["config"]["paths"]["intel_db"]).expanduser()

    from intelligence.heartbeat import ActionBriefStore

    store = ActionBriefStore(db_path)
    runs = store.get_runs(limit=limit)

    if not runs:
        console.print("No heartbeat runs recorded.")
        return

    table = Table(title="Heartbeat Runs")
    table.add_column("ID", style="dim")
    table.add_column("Started")
    table.add_column("Checked")
    table.add_column("Passed")
    table.add_column("Saved")
    table.add_column("LLM")
    table.add_column("Error")

    for r in runs:
        table.add_row(
            str(r.get("id", "")),
            str(r.get("started_at", ""))[:19],
            str(r.get("items_checked", 0)),
            str(r.get("items_passed", 0)),
            str(r.get("briefs_saved", 0)),
            str(r.get("llm_used", 0)),
            (r.get("error") or "")[:40],
        )

    console.print(table)


@heartbeat.command("run-once")
def heartbeat_run_once():
    """Run a single heartbeat cycle immediately."""
    c = get_components(skip_advisor=True)
    config = c["config"]
    db_path = Path(config["paths"]["intel_db"]).expanduser()

    from advisor.goals import GoalTracker
    from intelligence.heartbeat import HeartbeatPipeline
    from journal.storage import JournalStorage

    journal_dir = Path(config["paths"]["journal_dir"]).expanduser()
    storage = JournalStorage(journal_dir)
    tracker = GoalTracker(storage)
    goals = tracker.get_goals(include_inactive=False)

    if not goals:
        console.print("[yellow]No active goals found[/]")
        return

    hb_config = config.get("heartbeat", {})
    pipeline = HeartbeatPipeline(
        intel_storage=c["intel_storage"],
        goals=goals,
        db_path=db_path,
        config=hb_config,
    )
    result = pipeline.run()

    console.print(f"Checked: {result['items_checked']}")
    console.print(f"Passed filter: {result['items_passed']}")
    console.print(f"Saved: {result['briefs_saved']}")
