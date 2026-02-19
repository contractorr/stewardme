"""Journal entry templates for structured journaling."""

BUILTIN_TEMPLATES = {
    "daily": {
        "name": "Daily Reflection",
        "type": "daily",
        "content": """## What went well today?


## What challenged me?


## Key learnings


## Tomorrow's priorities

""",
    },
    "weekly": {
        "name": "Weekly Review",
        "type": "reflection",
        "content": """## Accomplishments this week


## What didn't go as planned?


## Patterns I noticed


## Goals progress


## Focus for next week

""",
    },
    "goal": {
        "name": "Goal Setting",
        "type": "goal",
        "content": """## Goal


## Why this matters


## Success criteria


## First steps


## Potential obstacles

""",
    },
    "project": {
        "name": "Project Update",
        "type": "project",
        "content": """## Status


## Progress since last update


## Blockers


## Next milestones


## Questions/decisions needed

""",
    },
    "learning": {
        "name": "Learning Log",
        "type": "insight",
        "content": """## What I learned


## Key concepts


## How this connects to my work


## Next: apply this by

""",
    },
}


def get_template(name: str, custom_templates: dict | None = None) -> dict | None:
    """Get template by name. Custom templates override builtins."""
    all_templates = {**BUILTIN_TEMPLATES}
    if custom_templates:
        all_templates.update(custom_templates)
    return all_templates.get(name)


def list_templates(custom_templates: dict | None = None) -> dict:
    """List all available templates."""
    all_templates = {**BUILTIN_TEMPLATES}
    if custom_templates:
        all_templates.update(custom_templates)
    return all_templates
