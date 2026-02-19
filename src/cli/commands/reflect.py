"""Reflection prompts CLI command."""

import sys

import click
from rich.console import Console
from rich.markdown import Markdown

from advisor.engine import LLMError
from cli.utils import get_components

console = Console()

REFLECT_PROMPT = """Based on the user's recent journal entries and goal status, generate 3-5 targeted coaching questions.

RECENT JOURNAL ENTRIES:
{journal_context}

GOAL STATUS:
{goal_context}

Generate thoughtful, specific questions that:
1. Surface blind spots or unexamined assumptions
2. Connect recent experiences to larger goals
3. Challenge the user to think more deeply about priorities
4. Identify areas where they might be stuck or avoiding something

Format as numbered questions. Be specific — reference their actual entries and goals, not generic coaching questions."""


@click.command()
@click.option("--save", is_flag=True, help="Save prompts as journal entry")
def reflect(save: bool):
    """Get AI-generated reflection questions based on your journal and goals."""
    c = get_components()

    try:
        journal_ctx = c["rag"].get_recent_entries(days=14)
        goal_entries = c["storage"].list_entries(entry_type="goal", limit=10)
        goal_ctx = ""
        for g in goal_entries:
            post = c["storage"].read(g["path"])
            status = post.get("status", "active")
            goal_ctx += f"- {g['title']} ({status})\n"

        if not goal_ctx:
            goal_ctx = "(No goals set yet)"

        prompt = REFLECT_PROMPT.format(
            journal_context=journal_ctx,
            goal_context=goal_ctx,
        )

        with console.status("Generating reflection prompts..."):
            from advisor.prompts import PromptTemplates
            response = c["advisor"]._call_llm(PromptTemplates.SYSTEM, prompt, max_tokens=800)

        console.print()
        console.print(Markdown(response))

        if save:
            filepath = c["storage"].create(
                content=response,
                entry_type="reflection",
                title="Reflection Prompts",
                tags=["reflection", "coaching"],
            )
            console.print(f"\n[green]Saved to {filepath.name}[/]")

    except LLMError as e:
        console.print(f"[red]Error:[/] {e}")
        sys.exit(1)
