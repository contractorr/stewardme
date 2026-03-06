# Goal-Learning Merge

## Overview

Merges the standalone learning path system into the goal tracking system. Learning paths become goals with `type="learning"` and auto-generated milestones. Eliminates `LearningPathStorage`, `LearningPathGenerator`, `SubModuleGenerator`, 5 MCP tools, 5 web routes, and 5 CLI commands. Adds a `type` field to goal frontmatter, an advisor auto-milestone generation prompt mode, and a one-time migration script.

## Dependencies

**Depends on:** `advisor/goals`, `advisor/engine`, `advisor/prompts`, `journal/storage`, `advisor/learning_paths` (migration source only)
**Depended on by:** `web/routes/goals`, `coach_mcp/tools/goals`, `cli/main`

---

## Components

### Goal Type Field

**File:** `src/advisor/goals.py`
**Status:** Stable

#### Behavior

Add `goal_type` field to goal frontmatter (not `type` — that's reserved for entry type by `JournalStorage`). `get_goal_defaults()` updated:

```python
def get_goal_defaults(goal_type: str = "general") -> dict:
    return {
        "status": str(GoalStatus.ACTIVE),
        "goal_type": goal_type,  # career, learning, project, general
        "last_checked": datetime.now().isoformat(),
        "check_in_days": 14,
    }
```

Valid types: `career`, `learning`, `project`, `general` (default).

Existing goals without a `goal_type` field are treated as `general` — no backfill needed, reading code uses `.get("goal_type", "general")`.

#### Inputs / Outputs

All `GoalTracker` list/get methods include `goal_type` in returned dicts. `get_goals()` gains optional `goal_type: str | None = None` filter param.

#### Invariants

- `goal_type` field is informational only — does not change staleness logic, check-in behavior, or milestone mechanics
- Missing `goal_type` field → `"general"` (backward compat)
- Field is `goal_type` not `type` to avoid collision with `JournalStorage` entry type field

---

### Auto-Milestone Generation

**File:** `src/advisor/engine.py`, `src/advisor/prompts.py`
**Status:** Stable

#### Behavior

New `AdvisorEngine.generate_milestones(goal_path: Path) -> list[str]` method:
1. Reads goal content + metadata via `JournalStorage`
2. Loads profile context via `rag.get_profile_context()`
3. Calls cheap LLM with `MILESTONE_GENERATION` prompt template
4. Parses numbered list from LLM response
5. Calls `GoalTracker.add_milestone()` for each parsed title
6. Returns list of milestone titles added

New prompt template `MILESTONE_GENERATION` in `prompts.py`:

| Name | Slots | Used by |
|------|-------|---------|
| `MILESTONE_GENERATION` | `goal_title`, `goal_content`, `goal_type`, `profile_context` | `AdvisorEngine.generate_milestones()` |

Template instructs LLM to produce 4-8 ordered milestones. For `type="learning"`, milestones correspond to learning steps calibrated to user's learning style and weekly hours.

#### Inputs / Outputs

```python
def generate_milestones(
    self,
    goal_path: Path,
    journal_storage: JournalStorage | None = None,
) -> list[str]
# Returns list of milestone title strings added to the goal
# Raises ValueError if goal not found
```

#### Error Handling

- Goal not found → `ValueError`
- LLM failure → empty list returned, warning logged
- Parse failure (no numbered list in response) → empty list, warning logged

---

### Skill Gap as Advisor Prompt Mode

**File:** `src/advisor/prompts.py`
**Status:** Stable

#### Behavior

`SKILL_GAP_ANALYSIS` template already exists. No new template needed. Skill gap detection becomes a usage pattern: user asks "what skills should I work on?" → advisor uses existing `SKILL_GAP_ANALYSIS` prompt → advisor can then create `learning`-type goals with auto-milestones via agentic tool calls.

The agentic `goals_add` tool gains an optional `type` parameter (default `"general"`).

---

### Learning Path Migration

**File:** `src/advisor/migrate_learning_paths.py` (new)
**Status:** One-time migration

#### Behavior

`migrate_learning_paths(user_base_dir: Path, journal_storage: JournalStorage, tracker: GoalTracker) -> dict`:

1. Scans `{user_base_dir}/learning_paths/` for markdown files
2. For each learning path file:
   a. Reads frontmatter: `skill`, `status`, `progress`, `completed_modules`, `total_modules`
   b. Creates goal via `journal_storage.create()` with `entry_type="goal"`, `title=skill`, `metadata=get_goal_defaults(goal_type="learning")`
   c. Parses modules from path content (numbered list or `## Module N` sections)
   d. Adds each module as a milestone via `tracker.add_milestone()`
   e. Marks completed milestones via `tracker.complete_milestone()` based on `completed_modules` count
   f. If source status is `"completed"`, updates goal status to `completed`
3. Returns `{"migrated": count, "skipped": count, "errors": list[str]}`

Does NOT delete original learning path files (rollback safety).

`run_migration_if_needed(user_base_dir: Path) -> dict | None`:
- Checks for marker file `{user_base_dir}/.learning_paths_migrated`
- If marker exists, returns `None` (already migrated)
- Runs migration, writes marker file on success
- Returns migration result dict

#### Invariants

- Migration is idempotent via marker file
- Original files untouched
- Partial failures (individual path errors) don't block other paths
- Missing `learning_paths/` dir → no-op, returns `{"migrated": 0}`

#### Error Handling

- Individual path parse/create errors → logged, added to `errors` list, migration continues
- Missing learning_paths dir → returns immediately with 0 migrated
- Marker file write failure → logged warning (migration still happened)

---

### Removals

#### Files to Delete

| File | Reason |
|------|--------|
| `src/advisor/learning_paths.py` | `LearningPathStorage`, `LearningPathGenerator`, `SubModuleGenerator` |
| `src/coach_mcp/tools/learning.py` | 5 MCP tools: `learning_gaps`, `learning_paths_list`, `learning_path_get`, `learning_path_progress`, `learning_check_in` |
| `src/web/routes/learning.py` | 5 web routes under `/api/learning` |

#### Code Changes for Removal

| File | Change |
|------|--------|
| `src/web/app.py` | Remove `learning` from router imports and `include_router` |
| `src/coach_mcp/server.py` | Remove `learning` from `_load_tools()` import list |
| `src/web/deps.py` | Remove `learning_paths_dir` from `get_user_paths()` return dict |
| `src/advisor/engine.py` | Remove `generate_learning_path()` method |
| `src/advisor/prompts.py` | Deprecate `LEARNING_PATH_GENERATION`, `CHECK_IN_ANALYSIS`, `DEEP_DIVE_GENERATION` templates (keep for reference, add `# DEPRECATED` comment) |
| `src/web/routes/briefing.py` | Remove `LearningPathStorage` import and learning paths section from `get_briefing()` |
| `src/advisor/daily_brief.py` | Remove `learning_paths` param from `DailyBriefBuilder.build()` and learning-related item generation |

#### CLI Commands to Remove

5 commands under `coach learn`: `gaps`, `paths`, `start`, `progress`, `check-in`

---

## Cross-Cutting Concerns

### Migration Timing

Migration runs on first web app startup per user (in `get_user_paths()` or a lifespan hook) and on first MCP bootstrap. CLI migration triggered by `coach migrate` command or auto-detected on `coach goals list`.

### Backward Compatibility

- Goals without `type` field → treated as `general`
- `/api/learning/*` routes return 404 after removal (no redirect)
- MCP learning tools return "Unknown tool" after removal
- `learning_paths/` directory left on disk; not cleaned up

---

## Test Expectations

- Migration: mock learning path files with various states (active, completed, partial); verify goals created with correct type, milestones match modules, completion preserved
- Migration idempotency: run twice, verify no duplicates (marker file check)
- Migration with missing dir: verify no-op
- `generate_milestones()`: mock cheap LLM; verify milestones added to goal; verify empty list on LLM failure
- `get_goal_defaults(goal_type="learning")`: verify `type` field in returned dict
- `GoalTracker.get_goals(goal_type="learning")`: verify filter works
- Removal verification: import `web.app` and verify no `learning` router; verify MCP tool count decremented by 5
- Mocks required: `JournalStorage`, `GoalTracker`, `LLMProvider`, filesystem (temp dirs)
