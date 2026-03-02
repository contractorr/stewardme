# Specs

Two-tier spec system: functional specs define *what*, technical specs define *how*.

## Workflow

1. PM writes a functional spec in `functional/` using the template
2. Claude reads the functional spec + relevant technical specs + codebase
3. Claude produces/updates a technical spec in `technical/` + implementation plan
4. Review both → implement

## Structure

```
specs/
  functional/        # What & why (PM-authored)
    TEMPLATE.md
    {feature}.md
  technical/         # How (Claude-generated, developer-reviewed)
    TEMPLATE.md
    {module}.md
```

## Guidelines

- **Functional specs**: No code, no internal details. User-facing language only.
- **Technical specs**: Reference the functional spec they implement. Include component signatures, invariants, error paths.
- One functional spec per feature. One technical spec per module (may cover multiple features).
