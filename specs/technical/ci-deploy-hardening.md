# CI / Deploy Hardening

## Overview

Implements specs/functional/ci-deploy-hardening.md: PR-gate parity for web
tests, verified reversible deploys, compose validation with a stub `.env`,
server-side backups, and dependency hygiene automation.

## Components

### test.yml

- New `test-web` job (PR-only: `if: github.event_name == 'pull_request'`)
  running `uv run pytest -m "web" --durations=20`. The guard avoids double
  web runs on main pushes, where `extended-tests` already covers
  `web or integration or slow`.
- `coverage` job marker widens from
  `not slow and not web and not integration` to `not slow` — web tests are
  TestClient-based and fast; integration tests carry the `slow` marker via
  `tests/conftest.py` auto-marking, so they stay excluded. `fail_under = 55`
  (pyproject) is unchanged; measured coverage rises because `src/web` is now
  exercised.

### deploy.yml + scripts/deploy-remote.sh

- `concurrency: cancel-in-progress: false` — deploys queue.
- Inline SSH script shrinks to: `git checkout -- . && git pull && exec
  bash scripts/deploy-remote.sh` so deploy logic is versioned.
- `scripts/deploy-remote.sh` (runs on the server, `set -euo pipefail`):
  1. compose config validation + content-mount checks (moved from YAML)
  2. `scripts/backup.sh` (pre-deploy snapshot; failure aborts deploy)
  3. tag current `stewardme-backend`/`stewardme-frontend` images as
     `:rollback` (best-effort — first deploy has none)
  4. `docker compose -f docker-compose.prod.yml build` (no `--no-cache`;
     layer cache is correct because the Dockerfile COPYs the checkout)
  5. `up -d --remove-orphans --wait --wait-timeout 180` — respects the
     healthchecks already defined in docker-compose.prod.yml
  6. external verification: read `DOMAIN` from `.env`, retry
     `curl -fsS https://$DOMAIN/api/health` up to 5×; skipped with a
     warning if `DOMAIN` unreadable
  7. on step 5/6 failure: dump `docker compose logs --tail=100`, print the
     rollback one-liner, exit 1
  8. `docker image prune -f --filter "until=168h"` — dangling images
     younger than 7 days (including `:rollback`-tagged layers) survive
- Rollback procedure (manual, documented in the script output and
  docs/development.md): re-tag `:rollback` images as the compose image
  names and `up -d`.

### validate-deploy.yml

- Before `docker compose config`, generate a stub `.env`
  (`SECRET_KEY`, `NEXTAUTH_SECRET`, `DOMAIN` = dummy values) when absent so
  validation always runs in CI. The skip branch is removed.

### scripts/backup.sh

- Host-side; `BACKUP_DIR` (default `$HOME/coach-backups`),
  `RETENTION_DAYS` (default 14), `COMPOSE_FILE` (default
  `docker-compose.prod.yml`).
- Stages a consistent snapshot **inside** the backend container with the
  Python sqlite3 backup API (`src` connection → `backup()` → staging dir;
  consistent under WAL) for every `*.db` under `COACH_HOME`, then copies
  journal/, chroma/, users/, and yaml/json config files into the same
  staging dir with `shutil.copytree`.
- `docker compose cp backend:/tmp/coach-backup-staging` → host, tarred to
  `$BACKUP_DIR/coach-backup-<UTC timestamp>.tar.gz`, staging removed,
  archives older than `RETENTION_DAYS` deleted.
- Also invocable standalone (nightly cron):
  `0 3 * * * cd /root/stewardme && ./scripts/backup.sh >> /var/log/coach-backup.log 2>&1`
- Restore: untar, `docker compose cp` the payload back into the volume (or
  copy into the volume mountpoint with containers stopped), restart.

### .github/dependabot.yml

- Weekly, grouped: `uv` (root), `npm` (`/web`), `github-actions`.

### .github/workflows/audit.yml

- Weekly cron + `workflow_dispatch`. Jobs: `uv export --format
  requirements-txt` piped to `pip-audit`; `npm audit --audit-level=high`
  in `web/`. Failures notify via the workflow run; not wired into merge
  gates.

## Test Expectations

- No Python code changes → no new pytest coverage. Verification is the
  first post-merge deploy run (health-gated) plus `docker compose config`
  running in the validate workflow on this PR.
- `scripts/backup.sh` is exercised on the server; its Python staging block
  is plain stdlib and safe to run repeatedly.

## Cross-Cutting

- CLAUDE.md CI section updated to describe the new gates.
- deploy.yml keeps `environment: production` and the same SSH secrets.
