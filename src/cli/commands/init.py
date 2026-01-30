"""Init CLI command."""

from pathlib import Path

import click
import yaml
from rich.console import Console

from cli.config import load_config, get_paths

console = Console()


@click.command()
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
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False)
        console.print(f"[green]✓[/] Created config: {config_path}")

    console.print("\n[bold]Ready![/] Add ANTHROPIC_API_KEY to your environment.")
