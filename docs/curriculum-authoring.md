# Curriculum Authoring

Curriculum chapters should converge on a shared chapter contract so rewrites feel consistent
instead of editorially improvised.

## Chapter format

Every chapter should live in a guide directory as `NN-topic.mdx` and start with frontmatter:

```mdx
---
schema_version: 1
title: Introduction to Philosophy
summary: A short paragraph describing the chapter.
objectives:
  - Identify the central questions philosophy asks.
  - Distinguish major branches of philosophy.
checkpoints:
  - Explain the difference between metaphysics and epistemology.
  - Summarize the historical eras covered in the chapter.
references:
  - curriculum:01-philosophy-guide/02-logic-reasoning
content_format: mdx
---

# Introduction to Philosophy
...
```

The canonical working example lives in `docs/templates/curriculum-chapter-template.mdx`.

## Required frontmatter

- `schema_version`: current schema version. Use `1`.
- `title`: human-readable chapter title.
- `summary`: one short paragraph for indexing, previews, and migration review.
- `objectives`: specific learning outcomes for the chapter.
- `checkpoints`: quick checks that verify the learner can apply the material.

## Standard chapter shape

Every rewrite and net-new chapter should follow the same reader-facing flow:

1. Executive summary
2. Why this is worth understanding (optional)
3. Core model or framework
4. Worked example
5. Failure modes
6. Checkpoint
7. Next-step connections

This is a content contract, not just a formatting preference. The relevance section is optional
because some topics justify themselves through conceptual, historical, or aesthetic value rather
than direct workplace transfer.

### Section intent

- **Executive summary**: Give the reader the 60-second version and the key distinction they must retain.
- **Why this is worth understanding (optional)**: Explain why the topic matters. Use workplace transfer when it helps, but broader framing is valid when it is more honest to the subject.
- **Core model/framework**: Present the durable mental model, not a loose survey.
- **Worked example**: Show the model in action on a concrete case.
- **Failure modes**: Cover common misreads, edge cases, and misuse.
- **Checkpoint**: End with prompts that force application, not recall alone.
- **Next-step connections**: Link forward into adjacent guides or applied modules.

### Mid-career writing rules

- Assume high general intelligence but limited uninterrupted study time.
- Prefer executive clarity over textbook completeness.
- Use one core model per section before layering nuance.
- Keep jargon only when it is professionally necessary; define it fast.
- End each chapter with where the learner should go next.

## Optional frontmatter

- `references`: canonical chapter references, for example `curriculum:01-philosophy-guide/02-logic-reasoning`, or relative file paths.
- `content_format`: keep as `mdx` for authored schema files.

## Applied modules / industry capstones

One-file industry guides should be authored as applied modules, not mini-textbooks.

Use this shape for industry modules:

1. Sector brief
2. How value is created and captured
3. Core workflow / operating model
4. Important metrics, constraints, and regulation
5. Decision case or capstone exercise
6. Suggested next guides

## Reference conventions

- Prefer `curriculum:<guide-id>/<chapter-stem>` for stable chapter-to-chapter references.
- Relative links to `.md` or `.mdx` files are acceptable during migration.
- External URLs should be supplementary, not the primary connection structure.
