# Profile

## Overview

The profile module manages a persistent `UserProfile` Pydantic model stored as YAML at `~/coach/profile.yaml` (per-user path in web mode). It provides two rendering modes — `summary()` for compact one-paragraph LLM context and `structured_summary()` for multi-section recommendation context — plus two interview flows: a 10-turn CLI interviewer (`ProfileInterviewer`) and a richer 15-turn web onboarding variant (`routes/onboarding.py`) that additionally creates goals and embeds the profile into ChromaDB. A staleness check (`is_stale(days=90)`) drives re-interview prompts.

## Dependencies

**Depends on:** `pydantic` (UserProfile, Skill, MemoryConfig), `yaml` (ProfileStorage serialization), `llm` (ProfileInterviewer, web onboarding LLM calls), `journal` (web onboarding creates goal entries), `shared_types` (CareerStage StrEnum), `chromadb` (web onboarding embeds profile into "profile" collection)

**Depended on by:** `advisor` (profile context injected into prompts), `intelligence.scheduler` (EventScraper loads location, GitHubIssuesScraper loads languages), `research` (DeepResearchAgent._get_user_context), `web` (profile routes, onboarding routes), `cli` (profile commands), `coach_mcp` (profile tools, learning_gaps, events_upcoming)

## Components

### Skill
**File:** `src/profile/storage.py`

#### Behavior
Pydantic model representing a single technical skill with a validated proficiency level.

#### Inputs / Outputs
| Field | Type | Default | Constraints |
|---|---|---|---|
| `name` | `str` | required | no default |
| `proficiency` | `int` | required | `ge=1, le=5`; description: "1=beginner, 5=expert" |

Validation is enforced by Pydantic `Field(ge=1, le=5)`. In `_build_profile` the value is additionally clamped manually via `max(1, min(5, int(...)))` before the model is constructed, with a default of `3` if proficiency is absent from the LLM JSON.

#### Invariants

- Direct construction with out-of-range `proficiency` raises `ValidationError` — use `_build_profile()` for untrusted data.
- `proficiency` is always an int in `[1, 5]` when loaded from a saved profile (clamping in `_build_profile` prevents invalid storage).

#### Error Handling
Pydantic raises `ValidationError` if proficiency is outside `[1, 5]` when constructing directly. `_build_profile` prevents this by clamping first.

#### Configuration
None.

---

### UserProfile
**File:** `src/profile/storage.py`

#### Behavior
Main Pydantic model representing a user's professional profile. All fields have defaults so an empty profile can be constructed with `UserProfile()`. The `is_stale()` method signals when a re-interview is needed.

#### Inputs / Outputs
All fields and defaults:

| Field | Type | Default | Notes |
|---|---|---|---|
| `skills` | `list[Skill]` | `[]` | |
| `interests` | `list[str]` | `[]` | |
| `career_stage` | `CareerStage` | `CareerStage.MID` (`"mid"`) | StrEnum: `junior/mid/senior/lead/exec` |
| `current_role` | `str` | `""` | |
| `aspirations` | `str` | `""` | |
| `location` | `str` | `""` | |
| `languages_frameworks` | `list[str]` | `[]` | |
| `learning_style` | `str` | `"mixed"` | Accepted values: `visual/reading/hands-on/mixed` |
| `weekly_hours_available` | `int` | `5` | |
| `goals_short_term` | `str` | `""` | 6-month horizon |
| `goals_long_term` | `str` | `""` | 3-year horizon |
| `industries_watching` | `list[str]` | `[]` | |
| `technologies_watching` | `list[str]` | `[]` | |
| `constraints` | `dict` | `{}` | Known keys: `time_per_week`, `geography`, `budget_sensitivity` |
| `fears_risks` | `list[str]` | `[]` | |
| `active_projects` | `list[str]` | `[]` | |
| `updated_at` | `Optional[str]` | `None` | ISO format datetime string; set automatically on every `save()` |

**`is_stale(days: int = 90) -> bool`:**
- Returns `True` if `updated_at` is `None` or empty.
- Returns `True` if `(datetime.now() - datetime.fromisoformat(updated_at)).days > days`.
- Default threshold: **90 days**. All callers (`ProfileInterviewer.needs_refresh`, `GET /api/onboarding/profile-status`) use the default.

#### Invariants

- All fields have defaults — `UserProfile()` always constructs without arguments.
- `career_stage` defaults to `"mid"`; `learning_style` defaults to `"mixed"` — these are never `None`.
- `is_stale()` returns `True` when `updated_at is None` — a freshly constructed `UserProfile()` is always stale.
- `updated_at` is an ISO string, not a `datetime` object — callers must parse it.

#### Error Handling
Pydantic `ValidationError` if YAML data passed to `UserProfile(**data)` contains invalid types or values. No explicit try/except in `ProfileStorage.load()`.

#### Configuration
`CareerStage` imported from `src/shared_types.py`.

---

### summary()
**File:** `src/profile/storage.py` (method on `UserProfile`)

#### Behavior
Produces a compact one-paragraph string for LLM prompt context. Fields are joined with `" | "`. Only non-empty fields are included. `learning_style` is always appended as the final segment.

#### Inputs / Outputs
No parameters. Returns a single `str`.

Field rendering and truncation/cap limits:

| Field | Label | Limit |
|---|---|---|
| `current_role` | `"Role: {role} ({career_stage})"` | none |
| `skills` | `"Skills: name(N), ..."` | top **5** by proficiency descending |
| `languages_frameworks` | `"Tech: ..."` | first **8** entries |
| `interests` | `"Interests: ..."` | first **6** entries |
| `aspirations` | `"Aspirations: ..."` | truncated to **200** chars |
| `goals_short_term` | `"6-month goals: ..."` | truncated to **200** chars |
| `goals_long_term` | `"3-year goals: ..."` | truncated to **200** chars |
| `industries_watching` | `"Industries: ..."` | first **6** entries |
| `technologies_watching` | `"Watching: ..."` | first **6** entries |
| `active_projects` | `"Projects: ..."` | first **5** entries |
| `fears_risks` | `"Risks: ..."` | first **4** entries |
| `location` | `"Location: ..."` | none |
| `constraints` | `"Constraints: Nh/week, geo, budget: X"` | rendered if any of `time_per_week`, `geography`, `budget_sensitivity` are set |
| `weekly_hours_available` | `"Available: Nh/week"` | fallback when `constraints` dict is empty/falsy |
| `learning_style` | `"Learning style: ..."` | always appended last |

#### Invariants

- `learning_style` is always the last segment — it is appended unconditionally.
- Empty fields are silently omitted — the paragraph length is variable.
- Skills are sorted by proficiency descending before capping at 5.
- `constraints` dict rendering takes priority over `weekly_hours_available` — only one appears.

#### Error Handling
No exceptions raised; empty fields are silently skipped.

#### Configuration
None.

---

### structured_summary()
**File:** `src/profile/storage.py` (method on `UserProfile`)

#### Behavior
Produces a multi-section string optimized for LLM recommendation context. Sections are separated by `"\n\n"`. No truncation on goals or aspirations (full text). No list caps anywhere. Only renders sections with content, except `[CONSTRAINTS]` which is always rendered.

#### Inputs / Outputs
No parameters. Returns a `str`.

Sections in output order:

| Section header | Content | Rendered when |
|---|---|---|
| `[IDENTITY]` | `current_role`, `career_stage`, `location` | always (career_stage always present) |
| `[GOALS & ASPIRATIONS]` | `goals_short_term` labeled `"6-month goals"`, `goals_long_term` labeled `"3-year vision"`, `aspirations` labeled `"Career aspirations"` | if any goal/aspiration is non-empty |
| `[SKILLS]` | all skills, sorted by proficiency descending, grouped by level; labels: `5=Expert, 4=Advanced, 3=Intermediate, 2=Beginner, 1=Novice`; format: `"  Label (N/5): skill1, skill2"` | if `skills` list non-empty |
| `[TECH STACK]` | all `languages_frameworks` joined by `", "` | if list non-empty |
| `[INTERESTS & WATCHING]` | `interests` labeled `"Professional interests"`, `industries_watching` labeled `"Industries watching"`, `technologies_watching` labeled `"Technologies watching"` | if any list non-empty |
| `[ACTIVE PROJECTS]` | bulleted `"- project"` per entry | if list non-empty |
| `[CONSTRAINTS]` | `time_per_week` from `constraints` dict (falls back to `weekly_hours_available`), `geography`, `budget_sensitivity`, `learning_style` (always) | always |
| `[CONCERNS & RISKS]` | bulleted `"- risk"` per entry | if `fears_risks` non-empty |

Key difference from `summary()`: goals/aspirations are full text (no 200-char truncation); skills include all entries (not top 5); no list caps on any field.

#### Invariants

- `[CONSTRAINTS]` section is always rendered — it always appears even with no constraints set.
- `[IDENTITY]` is always rendered — `career_stage` is never empty.
- No truncation or list caps anywhere — full content is always included.
- Sections are omitted when their data is empty, except `[IDENTITY]` and `[CONSTRAINTS]`.

#### Error Handling
No exceptions raised.

#### Configuration
None.

---

### ProfileStorage
**File:** `src/profile/storage.py`

#### Behavior
YAML-backed CRUD for `UserProfile`. Default storage path is `~/coach/profile.yaml` for CLI/MCP mode. In web mode the path is per-user: `get_user_paths(user_id)["profile"]` under `~/coach/users/{safe_user_id}/`.

```python
class ProfileStorage:
    def __init__(self, path: str | Path = "~/coach/profile.yaml")
    def exists(self) -> bool
    def load(self) -> Optional[UserProfile]
    def save(self, profile: UserProfile) -> Path
    def update_field(self, field: str, value) -> UserProfile
    def get_or_empty(self) -> UserProfile
```

**`save()` behavior:**
- Mutates `profile.updated_at` in-place to `datetime.now().isoformat()` before writing.
- Creates parent directories with `mkdir(parents=True, exist_ok=True)`.
- Converts `career_stage` to plain `str` to avoid YAML Python-object tags.
- Converts skills to plain dicts: `[{"name": str, "proficiency": int}]`.
- Writes via `yaml.dump(data, f, default_flow_style=False, sort_keys=False)`.
- Returns the resolved `Path`.

**`load()` behavior:**
- Returns `None` if file does not exist.
- Returns `None` if `yaml.safe_load()` returns empty/falsy.
- Passes YAML data directly to `UserProfile(**data)`; Pydantic validation applies.

**`get_or_empty()` behavior:**
- Returns `load()` result if profile exists, else returns `UserProfile()`.

#### Inputs / Outputs
`update_field(field, value)` raises `ValueError("Unknown profile field: {field}")` if the field is not an attribute of `UserProfile`. Falls back to `UserProfile()` (empty) if no profile file exists yet, then sets the field and saves.

#### Invariants

- `save()` mutates `profile.updated_at` in-place — the passed object is modified as a side effect.
- `load()` returns `None` on missing or empty file — never raises `FileNotFoundError`.
- `get_or_empty()` never returns `None` — always returns a valid `UserProfile`.
- `update_field()` creates a new profile file if one doesn't exist yet — it does not require a pre-existing profile.
- `career_stage` is serialized as a plain string to YAML — not as a Python enum object.

#### Error Handling
- `load()`: silently returns `None` on missing or empty file; Pydantic `ValidationError` propagates on malformed YAML data.
- `update_field()`: raises `ValueError` for unknown fields.
- `save()`: propagates `OSError` on filesystem failures.

#### Configuration
Default path `~/coach/profile.yaml` is overridden by callers (web routes pass per-user path).

---

### ProfileInterviewer
**File:** `src/profile/interview.py`

#### Behavior
Conducts an adaptive LLM-driven profile interview in a loop, then extracts and persists the resulting `UserProfile`. Operates on stdin/stdout by default but accepts injectable `input_fn`/`output_fn` for testing.

**`run_interactive()` flow:**

1. Calls `llm_caller(INTERVIEW_SYSTEM, INTERVIEW_START)` (no `max_tokens` on the first call) to get the opening question.
2. Loops up to **10 turns** (`for _ in range(10)`).
3. Each turn: reads user input; appends to conversation history; calls `llm_caller(INTERVIEW_SYSTEM, prompt, max_tokens=1500)` where `prompt` is `"Interview so far:\n{history}\n\nContinue the interview or finalize the profile if you have enough info."`.
4. Calls `_extract_profile_json()` on each response. On success: calls `_build_profile()`, saves via `storage.save()`, logs `profile_created` with skill count, returns the profile.
5. **Force-extraction fallback** (after 10 turns without JSON): sends `"Based on this interview, generate the profile JSON now.\n\n{history}\n\nOutput the JSON profile block now."` with `max_tokens=1500`. On success: builds, saves, returns.
6. **Absolute fallback** (force extraction also fails): logs `interview_extraction_failed` warning; saves and returns empty `UserProfile()`.

**`needs_refresh(days=90) -> bool`:**
- Returns `True` if `storage.load()` returns `None`.
- Returns `profile.is_stale(days)` otherwise.

**`INTERVIEW_SYSTEM` prompt instructs the LLM to:**
- Ask one question at a time.
- Gather 8 items: role/career stage, skills (1-5), languages/frameworks, interests, aspirations, location, learning style, weekly hours.
- Target **5-7 questions** before finalizing.
- Output a fenced JSON block with `{"done": true, "profile": {...}}`.

**`INTERVIEW_START`:** `"Start the profile interview. Ask your first question to understand who this person is professionally. Be warm but concise."`

#### Inputs / Outputs
- `__init__(llm_caller: Callable, storage: ProfileStorage)`
- `run_interactive(input_fn=None, output_fn=None) -> UserProfile`
- `needs_refresh(days: int = 90) -> bool`

**`_extract_profile_json(text: str) -> dict | None`** (module-level):

Two strategies in order:
1. Regex for fenced code block: `` r"```json\s*(\{.*?\})\s*```" `` with `re.DOTALL`. Parses JSON; validates `data.get("done") and "profile" in data`; returns `data["profile"]`.
2. Regex for bare JSON: `r'\{"done"\s*:\s*true.*?"profile"\s*:\s*\{.*\}\s*\}'` with `re.DOTALL`. Same validation.
3. Returns `None` if both fail or JSON is malformed.

**`_build_profile(data: dict) -> UserProfile`** (module-level):

Normalization applied before constructing the model:

| Field | Normalization |
|---|---|
| `skills` | requires each entry to be a `dict` with `"name"`; proficiency: `max(1, min(5, int(s.get("proficiency", 3))))` |
| `career_stage` | validated against `{"junior", "mid", "senior", "lead", "exec"}`; falls back to `"mid"` |
| `learning_style` | validated against `{"visual", "reading", "hands-on", "mixed"}`; falls back to `"mixed"` |
| `weekly_hours_available` | `max(1, min(40, int(hours)))`; default `5`; falls back to `5` on `ValueError`/`TypeError` |
| `industries_watching`, `technologies_watching`, `fears_risks`, `active_projects` | passed through `_as_list()`: list → cast elements to `str`; non-empty `str` → split on `","` and strip; anything else → `[]` |
| `constraints` | must be `dict`; replaced with `{}` if not |
| `interests`, `languages_frameworks` | passed through as-is from JSON (no normalization) |

#### Invariants

- Always returns a `UserProfile` — never raises or returns `None`.
- Loop runs exactly 10 turns (`range(10)`) — not while-loop with early exit.
- Force-extraction fires after all 10 turns regardless of partial JSON seen in earlier turns.
- `needs_refresh()` returns `True` for a brand-new profile (no file) and for stale profiles.
- `_build_profile()` is a module-level function shared with the web onboarding variant.

#### Error Handling
- JSON extraction failures are silent (returns `None`).
- `_build_profile` catches `ValueError`/`TypeError` for `weekly_hours_available` conversion.
- Absolute fallback prevents crash when all extraction fails.

#### Configuration
`max_tokens=1500` per turn (both normal and force-extraction calls). Target turns: 5-7 (LLM instruction); hard limit: 10 turns before fallback.

---

### Web Onboarding Variant
**File:** `src/web/routes/onboarding.py`

#### Behavior
A richer web-specific version of `ProfileInterviewer` that runs over HTTP as a stateful chat session. Sessions stored in-memory dict `_sessions` keyed by `user_id`. On completion, saves the profile, embeds it into ChromaDB, and creates goal entries in `JournalStorage`.

**Routes:**
- `POST /api/onboarding/start` — initializes session, calls LLM with `ONBOARDING_SYSTEM` + `ONBOARDING_START`, returns `OnboardingResponse(message, done=False, turn=0)`.
- `POST /api/onboarding/chat` — accepts `OnboardingChat(message)`, increments turn counter, calls LLM, checks for completion JSON, returns `OnboardingResponse`.
- `GET /api/onboarding/feed-categories` — returns feed categories pre-selected against user profile.
- `POST /api/onboarding/feeds` — bulk-inserts RSS feeds for selected categories.
- `GET /api/onboarding/profile-status` — returns `ProfileStatus(has_profile, is_stale, has_api_key, has_own_key, using_shared_key)`.

**Chat loop:**

1. Normal turns (`turn < MAX_TURNS`): prompt is `"Interview so far:\n{history}\n\nContinue the interview or finalize if you have enough info."` with `max_tokens=2000`.
2. At `turn >= MAX_TURNS` (15): force-extraction prompt is `"Based on this interview, generate the profile and goals JSON now.\n\n{history}\n\nOutput the JSON block now with whatever information you have."` with `max_tokens=2000`.
3. If the forced response still lacks JSON: a second LLM call is made with `max_tokens=2000`. If that also fails: session is cleared, returns `OnboardingResponse(done=True, goals_created=0)` with no profile save.
4. On success: calls `_save_results()` → `_build_profile()` (reuses `interview.py` function) → `ProfileStorage.save()` → `_embed_profile()` → goal creation. Clears session. Strips JSON from response text before returning conversational message.

**`ONBOARDING_SYSTEM` expands the interview to 13 items** (vs 8 in CLI):
- Adds: `goals_short_term` (6-month), `goals_long_term` (3-year vision), `industries_watching`, `technologies_watching`, `constraints` (time/geography/budget), `fears_risks`, `active_projects`, and 1-3 concrete goals to track.
- Output JSON also contains `"goals": [{"title": "...", "description": "..."}]`.
- Target: **5-8 exchanges**.
- Ends with the closing line: `"Your profile will continue to deepen over time as you journal and interact with your steward."`

**`ONBOARDING_START`:** `"Start the onboarding interview. Greet the user warmly, briefly explain you'll ask a few questions to understand who they are and what they're working toward, then ask your first question. Be concise and curious."`

**Profile embedding (`_embed_profile`):**
- Uses `EmbeddingManager(paths["chroma_dir"], collection_name="profile")`.
- Doc ID: `"profile:{user_id}"`.
- Text: `profile.summary()` + `"Short-term goals: ..."` + `"Long-term vision: ..."` + `"Concerns: ..."` + `"Active projects: ..."` + `"Geography: ..."` + `"Budget sensitivity: ..."` (each only if non-empty).
- Metadata: `{"type": "profile", "user_id": user_id}`.
- Failures are caught and logged as warnings (`onboarding.embed_failed`), not propagated.

**Goal creation:**
- Iterates `data.get("goals", [])`.
- For each `dict` with a `"title"`, calls `JournalStorage.create(content=description, entry_type="goal", title=title, metadata=get_goal_defaults())`.
- Individual goal creation failures are caught and logged; total count returned as `goals_created`.

**`_extract_completion_json`:** same two-regex strategy as CLI `_extract_profile_json` but returns the full `data` dict (not just `data["profile"]`) so the `"goals"` key is preserved.

**`_strip_json_block`:** removes fenced and bare JSON blocks from the LLM response text before returning the conversational message to the client. Falls back to a hardcoded message if the cleaned text is empty.

#### Inputs / Outputs
Requires authenticated user (JWT). Returns `OnboardingResponse(message, done, goals_created, turn)`.

#### Invariants

- Session state is in-memory dict `_sessions` — lost on server restart; sessions are not persisted.
- Completion always clears the session — a completed or failed onboarding requires a fresh `/start` call.
- Profile embedding failures are caught — profile is still saved even if ChromaDB embedding fails.
- Goal creation failures are caught individually — partial goal creation is possible.
- JSON block is always stripped from the response text before returning to the client.
- `_build_profile()` is the same function as the CLI interviewer — normalization rules are identical.

#### Caveats

- `_sessions` is a module-level dict — not safe for multi-process deployments (use Redis or DB-backed sessions for production scale).
- Force-extraction at `MAX_TURNS=15` can make two LLM calls if the first force attempt fails.

#### Error Handling
- Missing session on `POST /chat`: raises `HTTP 400 "No active onboarding session"`.
- LLM call failures: raises `HTTP 502 "LLM call failed"`.
- Profile/goal save failures: caught, `goals_created=0` returned, session cleared.
- Embed failures: logged as warnings, not propagated.
- Rate limiting: shared-key users checked via `check_shared_key_rate_limit()` on both `/start` and `/chat`.

#### Configuration
| Constant | Value |
|---|---|
| `MAX_TURNS` | `15` |
| `max_tokens` per turn | `2000` |
| ChromaDB collection | `"profile"` |
| Goal entry type | `"goal"` |

---

## Constants and Thresholds Reference

| Constant | Value | Location |
|---|---|---|
| Staleness threshold (default) | 90 days | `UserProfile.is_stale()`, `ProfileInterviewer.needs_refresh()` |
| Max interview turns (CLI) | 10 | `ProfileInterviewer.run_interactive()` |
| Max interview turns (web) | 15 (`MAX_TURNS`) | `onboarding.py` |
| LLM `max_tokens` per turn (CLI) | 1500 | `run_interactive()` |
| LLM `max_tokens` per turn (web) | 2000 | `onboarding.py` |
| Skill proficiency range | 1–5 | `Skill.proficiency`, `_build_profile` |
| Default proficiency if missing | 3 | `_build_profile` |
| Weekly hours clamp | 1–40 | `_build_profile` |
| Default weekly hours | 5 | `UserProfile`, `_build_profile` |
| `summary()` top skills shown | 5 | `summary()` |
| `summary()` tech stack cap | 8 | `summary()` |
| `summary()` interests cap | 6 | `summary()` |
| `summary()` industries cap | 6 | `summary()` |
| `summary()` technologies watching cap | 6 | `summary()` |
| `summary()` projects cap | 5 | `summary()` |
| `summary()` risks cap | 4 | `summary()` |
| `summary()` aspirations/goals truncation | 200 chars | `summary()` |
| `structured_summary()` all list caps | none | `structured_summary()` |
| Default storage path (CLI/MCP) | `~/coach/profile.yaml` | `ProfileStorage.__init__` |
| Target interview turns (LLM instruction, CLI) | 5-7 questions | `INTERVIEW_SYSTEM` |
| Target interview turns (LLM instruction, web) | 5-8 exchanges | `ONBOARDING_SYSTEM` |
| Valid `career_stage` values | `junior, mid, senior, lead, exec` | `_build_profile`, `INTERVIEW_SYSTEM` |
| Valid `learning_style` values | `visual, reading, hands-on, mixed` | `_build_profile`, `INTERVIEW_SYSTEM` |
| Default `career_stage` fallback | `"mid"` | `UserProfile`, `_build_profile` |
| Default `learning_style` fallback | `"mixed"` | `UserProfile`, `_build_profile` |
---

## Test Expectations

- `UserProfile.is_stale()`: verify `True` when `updated_at=None`; verify `True` when > 90 days old; verify `False` when recent.
- `ProfileStorage.load()`: verify `None` on missing file; verify `None` on empty YAML; verify Pydantic validation applied.
- `ProfileStorage.update_field()`: verify `ValueError` on unknown field; verify creates new profile if file absent.
- `ProfileStorage.save()`: verify `updated_at` mutated in-place; verify career_stage serialized as plain string (not Python enum object).
- `_build_profile()`: verify proficiency clamped 1–5; verify invalid career_stage falls back to `"mid"`; verify `weekly_hours_available` clamped 1–40; verify `_as_list()` handles string CSV input.
- `ProfileInterviewer.run_interactive()`: mock LLM caller; verify force-extraction triggered after 10 turns; verify absolute fallback returns empty `UserProfile()`; verify `_extract_profile_json()` tries both regex strategies.
- Web onboarding: verify `MAX_TURNS=15` force-extraction; verify profile embedded into `"profile"` ChromaDB collection; verify goal creation failures don't abort profile save; verify JSON stripped from conversational response.
- `_extract_profile_json()`: unit-test both fenced and bare-JSON regex strategies with synthetic LLM output.
- Mocks required: LLM provider, `ProfileStorage`, ChromaDB client (web onboarding), `JournalStorage` (goal creation).
