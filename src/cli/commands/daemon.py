"""Daemon CLI commands."""

import time

import click
from rich.console import Console

from cli.utils import get_components
from intelligence.scheduler import IntelScheduler

console = Console()

_daemon_scheduler = None


@click.group()
def daemon():
    """Manage background scheduler."""
    pass


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
