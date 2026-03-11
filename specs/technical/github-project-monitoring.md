# GitHub Project Monitoring

**Status:** Draft

## Overview

Read-only monitoring of a user's GitHub repositories, feeding repo health signals into goals, Radar, advisor context, and the outcome harvester. Builds on existing intelligence scheduler, signal detection, and watchlist infrastructure. All GitHub API access is strictly read-only — no write operations.

**Implements:** `specs/functional/github-project-monitoring.md`

## Dependencies

**Depends on:** `intelligence.scheduler`, `intelligence.scraper` (IntelStorage, BaseScraper patterns), `advisor.signals` (SignalDetector, SignalStore), `advisor.rag` (context injection), `advisor.goals` (GoalTracker), `profile.storage` (UserProfile), `web.user_store` (secrets, engagement), `web.routes.settings` (secret management, feature toggles), `intelligence.watchlist` (WatchlistStore patterns), `intelligence.goal_intel_match` (goal linkage patterns)

**Depended on by:** `advisor.rag` (repo context slot), `advisor.signals` (repo signal detectors), `intelligence.scheduler` (polling jobs), `web.routes.settings` (monitoring config UI)

---

## Components

### GitHubRepoClient

**File:** `src/intelligence/github_repos.py`
**Status:** New

#### Behavior

Thin wrapper around GitHub REST API for read-only repo data. Uses `httpx.AsyncClient` with bearer token auth when available, unauthenticated for public-only access.

- Constructor: `GitHubRepoClient(token: str | None = None)`
- Sets `Accept: application/vnd.github+json` and `X-GitHub-Api-Version: 2022-11-28` headers
- Token can be a fine-grained PAT with `repo:read` + `actions:read` scopes, or the OAuth token from GitHub auth
- Unauthenticated rate limit: 60 req/hr. Authenticated: 5000 req/hr

#### Inputs / Outputs

| Method | Params | Returns |
|--------|--------|---------|
| `list_user_repos(username)` | `username: str` | `list[RepoSummary]` — id, name, full_name, private, archived, default_branch, pushed_at, open_issues_count, language, html_url |
| `get_repo_stats(owner, repo)` | `owner: str, repo: str` | `RepoSnapshot` — commits_30d, open_issues, open_prs, latest_release, ci_status, contributors_30d, pushed_at |
| `get_commit_activity(owner, repo)` | `owner: str, repo: str` | `list[WeeklyCommitCount]` — last 12 weeks of commit counts from `/stats/participation` |
| `get_ci_status(owner, repo, branch)` | `owner: str, repo: str, branch: str` | `CIStatus` — state (success/failure/pending/none), updated_at, workflow_name |

#### Error Handling

| Error | Behavior |
|-------|----------|
| 401 Unauthorized | Log warning, mark token as invalid, fall back to unauthenticated |
| 403 Rate limited | Log warning, return cached data if available, set backoff flag |
| 404 Not found | Return `None`; caller handles missing repo gracefully |
| Network error | Tenacity retry (3 attempts, exponential backoff), then return `None` |

#### Configuration

| Key | Default | Source |
|-----|---------|--------|
| `github_monitoring.api_base_url` | `https://api.github.com` | config.yaml |
| `github_monitoring.request_timeout_s` | `15` | config.yaml |

---

### RepoSnapshot (dataclass)

**File:** `src/intelligence/github_repos.py`
**Status:** New

| Field | Type | Description |
|-------|------|-------------|
| `repo_full_name` | `str` | `owner/repo` |
| `snapshot_at` | `datetime` | UTC timestamp of this snapshot |
| `commits_30d` | `int` | Commits to default branch in last 30 days |
| `open_issues` | `int` | Current open issue count |
| `open_prs` | `int` | Current open PR count |
| `latest_release` | `str \| None` | Tag name of latest release |
| `ci_status` | `str` | `success`, `failure`, `pending`, or `none` |
| `contributors_30d` | `int` | Unique contributors in last 30 days |
| `pushed_at` | `datetime \| None` | Last push timestamp |
| `weekly_commits` | `list[int]` | Last 12 weeks of commit counts for trend |

---

### GitHubRepoStore

**File:** `src/intelligence/github_repo_store.py`
**Status:** New

#### Behavior

SQLite persistence for monitored repo config and health snapshots. Co-located in `intel.db` using `db.wal_connect()`, consistent with `IntelStorage`, `SignalStore`, and `GoalIntelMatchStore`.

Two tables:

```sql
CREATE TABLE IF NOT EXISTS monitored_repos (
    id TEXT PRIMARY KEY,              -- uuid4
    user_id TEXT NOT NULL,
    repo_full_name TEXT NOT NULL,     -- owner/repo
    html_url TEXT NOT NULL,
    is_private INTEGER DEFAULT 0,
    linked_goal_path TEXT,            -- FK to goal markdown path
    poll_tier TEXT DEFAULT 'moderate', -- active/moderate/stale
    last_polled_at TIMESTAMP,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, repo_full_name)
);

CREATE TABLE IF NOT EXISTS repo_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_id TEXT NOT NULL REFERENCES monitored_repos(id) ON DELETE CASCADE,
    snapshot_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    commits_30d INTEGER,
    open_issues INTEGER,
    open_prs INTEGER,
    latest_release TEXT,
    ci_status TEXT,
    contributors_30d INTEGER,
    pushed_at TIMESTAMP,
    weekly_commits_json TEXT          -- JSON array of 12 ints
);

CREATE INDEX IF NOT EXISTS idx_snapshots_repo_date ON repo_snapshots(repo_id, snapshot_at);
```

#### Inputs / Outputs

| Method | Params | Returns |
|--------|--------|---------|
| `add_repo(user_id, repo_full_name, html_url, is_private, linked_goal_path)` | see signature | `str` (repo id) |
| `remove_repo(user_id, repo_id)` | | `bool` (deleted?) |
| `list_repos(user_id)` | | `list[MonitoredRepo]` |
| `link_goal(repo_id, goal_path)` | | `None` |
| `unlink_goal(repo_id)` | | `None` |
| `save_snapshot(repo_id, snapshot: RepoSnapshot)` | | `None` |
| `get_latest_snapshot(repo_id)` | | `RepoSnapshot \| None` |
| `get_snapshot_history(repo_id, days=90)` | | `list[RepoSnapshot]` |
| `get_repos_due_for_poll(user_id)` | | `list[MonitoredRepo]` — filters by poll_tier cadence |
| `update_poll_tier(repo_id, tier)` | | `None` |
| `prune_snapshots(max_age_days=90)` | | `int` (rows deleted) |

#### Invariants

- `(user_id, repo_full_name)` is unique — no duplicate monitoring.
- Snapshots cascade-delete when a monitored repo is removed.
- `prune_snapshots()` only deletes rows where `snapshot_at < now - max_age_days`.
- `get_repos_due_for_poll()` checks `last_polled_at` against tier cadence: active=1d, moderate=3d, stale=7d.

#### Poll Tier Assignment

After each snapshot:
- `pushed_at` within 7 days → `active`
- `pushed_at` within 30 days → `moderate`
- `pushed_at` older than 30 days or `None` → `stale`

---

### GitHubRepoPoller

**File:** `src/intelligence/github_repo_poller.py`
**Status:** New

#### Behavior

Scheduled job that polls monitored repos and saves snapshots. Registered in `IntelScheduler.start_with_research()` alongside existing pipeline jobs.

```python
class GitHubRepoPoller:
    def __init__(self, client: GitHubRepoClient, store: GitHubRepoStore):
        ...

    async def poll_user_repos(self, user_id: str) -> list[RepoSnapshot]:
        """Poll all repos due for this user. Returns new snapshots."""
        repos = self.store.get_repos_due_for_poll(user_id)
        snapshots = await asyncio.gather(
            *[self._poll_one(repo) for repo in repos],
            return_exceptions=True
        )
        return [s for s in snapshots if isinstance(s, RepoSnapshot)]

    async def _poll_one(self, repo: MonitoredRepo) -> RepoSnapshot:
        snapshot = await self.client.get_repo_stats(owner, name)
        self.store.save_snapshot(repo.id, snapshot)
        new_tier = self._compute_tier(snapshot)
        self.store.update_poll_tier(repo.id, new_tier)
        return snapshot
```

#### Scheduler Integration

In `scheduler.py`, add a new job alongside existing pipelines:

```python
# In start_with_research():
self.scheduler.add_job(
    self._run_github_repo_poll,
    CronTrigger(hour="*/4"),  # every 4 hours, filters by per-repo cadence internally
    id="github_repo_poll",
    ...
)
```

The job iterates all users with monitored repos, calls `poll_user_repos()` per user. Individual repo cadence is enforced by `get_repos_due_for_poll()`, not the cron schedule.

#### Error Handling

- Individual repo poll failure does not block other repos (caught by `return_exceptions=True`)
- Rate limit 403 → skip remaining repos for this user, retry next cycle
- All errors logged via structlog with `user_id` and `repo_full_name` context

---

### GitHubRepoSignalDetector

**File:** `src/advisor/signals.py` (extend existing `SignalDetector`)
**Status:** New

#### New SignalTypes

Add to `SignalType` enum:

```python
REPO_STALE = "repo_stale"
REPO_VELOCITY_CHANGE = "repo_velocity_change"
REPO_ISSUE_SPIKE = "repo_issue_spike"
REPO_CI_FAILURE = "repo_ci_failure"
```

#### New Detector Methods

Added to `SignalDetector.detect_all()`:

| Method | Trigger | Severity |
|--------|---------|----------|
| `_detect_repo_stale()` | No commits in `repo_stale_threshold_days` (default 14) | 6 if linked to goal, 4 otherwise |
| `_detect_repo_velocity_change()` | >50% change in commit rate vs 4-week baseline from `weekly_commits` history | 5 (increase) or 7 (decrease, goal-linked) |
| `_detect_repo_issue_spike()` | >2x open issues vs previous snapshot | 5 |
| `_detect_repo_ci_failure()` | `ci_status == "failure"` on latest snapshot | 7 if goal-linked, 5 otherwise |

#### Velocity Change Detection

Uses `weekly_commits` from the two most recent snapshots:
- Compute `mean(recent_4_weeks)` vs `mean(prior_4_weeks)` from the 12-week history
- If `abs(delta) / max(prior_mean, 1) > 0.5` → signal fires
- Direction captured in signal detail text

#### Dedup

Same hash-based dedup as existing signals: `SHA256(type|repo_full_name|week_bucket)`. Week bucket prevents re-firing within the same 7-day window.

---

### Advisor Context: RepoContextProvider

**File:** `src/advisor/rag.py` (extend existing `RAGRetriever`)
**Status:** New

#### Behavior

New method `get_repo_context(user_id, query)` on `RAGRetriever`:

1. Check if query references a goal linked to a monitored repo (keyword match on repo name, goal title)
2. If matched, fetch latest snapshot + 4-week trend from `GitHubRepoStore`
3. Format as XML block:

```xml
<github_project repo="{full_name}" linked_goal="{goal_title}">
  Last commit: {pushed_at}
  Commits (30d): {commits_30d} ({trend})
  Open issues: {open_issues} | Open PRs: {open_prs}
  CI: {ci_status}
  Latest release: {latest_release}
</github_project>
```

4. Inject into `AskContext` as a new `repo_context` field
5. Budget ceiling: 5% of `max_context_chars` — repo data is compact

#### Query Relevance Check

Simple heuristic: query tokens overlap with `repo_full_name.split("/")[-1]` or linked goal title tokens. No LLM call needed — repo names are distinctive enough.

If no monitored repos match the query, `get_repo_context()` returns `None` and no block is injected.

---

### Profile Extension

**File:** `src/profile/storage.py`
**Status:** Modify existing

Add field to `UserProfile`:

```python
github_username: str | None = None
```

Populated from:
- GitHub OAuth `login` claim during auth (extracted in `web.routes.user.py`)
- Manual entry via `PATCH /api/settings/profile`

No migration needed — Pydantic model handles missing field with default `None`.

---

### Settings & API Routes

**File:** `src/web/routes/github_repos.py`
**Status:** New

#### Endpoints

| Method | Path | Body / Params | Returns |
|--------|------|---------------|---------|
| `GET` | `/api/github/repos` | — | `list[RepoSummary]` — user's discoverable repos |
| `POST` | `/api/github/repos/monitor` | `{repo_full_name, html_url, is_private?}` | `MonitoredRepo` |
| `DELETE` | `/api/github/repos/monitor/{repo_id}` | — | `204` |
| `GET` | `/api/github/repos/monitored` | — | `list[MonitoredRepo]` with latest snapshot |
| `PATCH` | `/api/github/repos/monitor/{repo_id}/link` | `{goal_path}` | `MonitoredRepo` |
| `PATCH` | `/api/github/repos/monitor/{repo_id}/unlink` | — | `MonitoredRepo` |
| `POST` | `/api/github/repos/monitor/{repo_id}/refresh` | — | `RepoSnapshot` (immediate poll) |

All endpoints require JWT auth. User isolation enforced via `user_id` from token.

#### GitHub Token Management

Reuses existing `set_user_secret` / `get_user_secret` pattern from `settings.py`:

- `github_pat` secret key for fine-grained PAT (opt-in private access)
- Falls back to OAuth token from GitHub auth when no PAT is set
- Feature toggle: `feature_github_monitoring` in `FEATURE_TOGGLE_FIELDS`

#### Route Registration

Add router to `src/web/app.py`:

```python
from src.web.routes.github_repos import router as github_repos_router
app.include_router(github_repos_router)
```

---

### Outcome Harvester Integration

**File:** Extend existing outcome evaluation logic
**Status:** New

#### Behavior

When evaluating a recommendation or action item outcome:

1. Check if the linked goal has a monitored repo
2. If yes, query `repo_snapshots` for the review window (action created_at → now)
3. Positive evidence: `commits_30d > 0` in snapshots after action creation, or `pushed_at` after action creation
4. Negative evidence: zero commits in all snapshots during the review window AND repo was previously active
5. This repo evidence supplements (does not replace) existing journal/goal check-in evidence

---

## Cross-Cutting Concerns

### Rate Limiting

GitHub API limits are shared across all features using the same token. The poller should track remaining quota via `X-RateLimit-Remaining` response header and pause when below 100 requests remaining.

### Security

- Tokens stored via Fernet encryption (existing `user_store` pattern)
- No repo content (file contents, diffs) is ever fetched — only metadata
- Private repo flag stored to prevent accidental exposure in shared contexts
- Path traversal protection on `repo_full_name` (validate `owner/repo` format, reject `/`, `..`, etc.)

### Observability

- `metrics.counter("github_polls_total", labels={"status": "success|error|rate_limited"})`
- `metrics.counter("github_signals_emitted", labels={"type": signal_type})`
- `metrics.timer("github_poll_duration_seconds")`
- Structlog fields: `user_id`, `repo_full_name`, `poll_tier`

### Pruning

`prune_snapshots(max_age_days=90)` called by scheduler daily alongside existing cleanup jobs. Expected row volume: ~1 snapshot/repo/day × 90 days = ~90 rows per monitored repo.

---

## Configuration

| Key | Default | Source |
|-----|---------|--------|
| `github_monitoring.enabled` | `false` | config.yaml |
| `github_monitoring.poll_cron` | `0 */4 * * *` | config.yaml |
| `github_monitoring.stale_threshold_days` | `14` | config.yaml |
| `github_monitoring.snapshot_retention_days` | `90` | config.yaml |
| `github_monitoring.velocity_change_threshold` | `0.5` | config.yaml |
| `github_monitoring.api_base_url` | `https://api.github.com` | config.yaml |
| `github_monitoring.request_timeout_s` | `15` | config.yaml |

---

## Test Expectations

### Happy path
- `GitHubRepoClient` returns well-formed `RepoSnapshot` from mocked API responses
- `GitHubRepoStore` round-trips monitored repos and snapshots correctly
- `GitHubRepoPoller` polls only repos due per tier cadence
- Signal detectors fire for stale, velocity change, issue spike, CI failure conditions
- Advisor context injects `<github_project>` block when query matches linked goal
- Pruning deletes only rows older than retention window

### Edge cases
- Rate limit 403 → poller backs off, no crash
- Repo deleted on GitHub → 404 handled, marked inactive
- No token → only public repos accessible
- Zero commit history → no misleading velocity signals
- Multiple repos linked to same goal → signals from all repos

### Mocking required
- `httpx.AsyncClient` for all GitHub API calls
- `db.wal_connect` for SQLite (use tmp path)
- `get_user_secret` for token retrieval
- Clock/datetime for snapshot pruning and poll tier checks
