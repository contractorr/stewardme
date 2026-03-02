# {Module Name}

## Overview

{1-3 sentence description: what the module does, how it fits in the system, key architectural decisions.}

## Dependencies

{Which other modules this module depends on, and which modules depend on it. Use a simple list.}

**Depends on:** `module_a`, `module_b`
**Depended on by:** `module_c`, `module_d`

---

## Components

### {ComponentName}

**File:** `src/{module}/{file}.py`
**Status:** Stable | Experimental | Deprecated

#### Behavior

{What the component does. Include:
- Constructor signature + defaults
- Decision trees / state machines if applicable
- Algorithmic details: formulas, thresholds, sort orders
- Key implementation notes (e.g., "uses WAL mode", "lazy-initialized")}

#### Inputs / Outputs

{Public method signatures with parameter types, defaults, and return types.
Use tables for multi-field inputs/outputs (e.g., dict shapes, dataclass fields).
Document optional vs required params explicitly.}

#### Invariants

{Preconditions, postconditions, and guarantees that must hold. Examples:
- "After sync(), ChromaDB ID set equals storage ID set"
- "Filenames are globally unique within journal_dir"
- "A soft-deleted fact is never returned by get_all_active()"

Also note what is NOT guaranteed:
- "Not thread-safe for concurrent writes"
- "Order of results is undefined when scores are equal"}

#### Error Handling

{For each error path, specify:
- What triggers it (bad input, missing resource, external failure)
- What happens (raises X, returns default, logs + swallows, propagates)
- Whether callers need to handle it

Distinguish: raises vs catches-and-returns vs silently-swallows.}

#### Configuration

{Constants, config keys, thresholds, SQL schemas, environment variables.
Use tables for config keys with columns: Key | Default | Source.
Include any hardcoded values that affect behavior.}

#### Caveats

{Optional section. Include only when relevant:
- Known bugs or misleading return values
- Deliberate deviations from expected behavior
- Non-obvious interactions with other components
- Performance cliffs (e.g., "O(n) scan over all entries")}

---

{Repeat ### ComponentName blocks for each component}

---

## Cross-Cutting Concerns

{Optional section for module-level patterns that span multiple components. Examples:
- Error handling summary table (like mcp.md)
- Cross-component comparison table (like llm.md)
- Concurrency / lifecycle constraints
- Security considerations}

## Test Expectations

{What a correct test suite must verify for this module:
- Key happy-path behaviors
- Edge cases that MUST be covered (empty inputs, boundary values, first-run state)
- What requires mocking (LLM calls, external APIs, filesystem)
- Known non-deterministic paths}
