# CI / Deploy Hardening

**Status:** Draft
**Author:** Raj
**Date:** 2026-07-02

## Problem

Four gaps found in an infrastructure review:

1. All web route tests (~41 files covering every API route) run only
   post-merge — a PR can break every route and merge green; the failure
   surfaces inside the deploy pipeline.
2. The deploy script ends with `up -d --force-recreate` followed by
   `docker image prune -f`, which deletes the just-replaced images —
   destroying the instant-rollback path. There is no post-deploy health
   verification, and `cancel-in-progress: true` can kill a deploy between
   `git pull` and `up -d`, leaving new code with old containers.
3. Compose config validation in CI is always skipped because `.env` never
   exists there — syntax/interpolation errors surface only during the SSH
   deploy.
4. All user data (SQLite DBs, ChromaDB vectors, journal markdown, encrypted
   secrets) lives in one Docker volume with zero automated backups — the
   only unrecoverable failure mode in the system. There is also no
   dependency-update or vulnerability-audit automation.

## Users

The operator (deploys, restores, sleeps at night) and all end users whose
data survives a disk failure.

## Desired Behavior

### PR gate parity

1. Web route tests run on every pull request, not just after merge.
2. The coverage measurement includes the web test suite so the gate
   reflects the code that actually ships.

### Verified, reversible deploys

1. A deploy waits for container healthchecks and then verifies the public
   `/api/health` endpoint end-to-end; on failure it dumps recent container
   logs and exits non-zero.
2. Before replacing containers, the current images are tagged as rollback
   images; pruning only removes dangling images older than a week, so the
   previous image always survives.
3. A running deploy is never cancelled mid-SSH — concurrent pushes queue.
4. The remote deploy logic lives in a versioned script in the repo
   (`scripts/deploy-remote.sh`), not inline YAML.

### Compose validation in CI

1. CI generates a stub `.env` (dummy values for required vars) so
   `docker compose config` actually runs for both compose files on every
   relevant PR.

### Backups

1. `scripts/backup.sh` produces a consistent snapshot: every SQLite DB via
   the sqlite backup API (safe under WAL, no downtime), plus journal,
   chroma, users, and config files, tarred to a timestamped archive on the
   host with N-day rotation.
2. Every deploy takes a backup before replacing containers.
3. A nightly cron invocation and the restore procedure are documented.

### Dependency hygiene

1. Dependabot opens weekly grouped update PRs for Python (uv), npm (web/),
   and GitHub Actions.
2. A weekly audit workflow runs `pip-audit` and `npm audit` and fails on
   known high-severity vulnerabilities (notification, not a merge gate).

## Acceptance Criteria

- [ ] A PR that breaks a web route test fails CI before merge.
- [ ] Coverage on CI includes the `web` marker suite.
- [ ] A deploy where the backend never becomes healthy fails the workflow
      with container logs in the output, and the previous image is still
      present on the server.
- [ ] Two rapid pushes to main result in two sequential deploys, not a
      cancelled half-deploy.
- [ ] `docker compose config` runs (not skipped) in CI for both compose
      files.
- [ ] Running `scripts/backup.sh` on the server produces a tar archive
      containing every `.db` file plus journal/chroma/users dirs, and
      removes archives older than the retention window.
- [ ] `dependabot.yml` covers uv, npm, and github-actions ecosystems.

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| Health verification fails after `--wait` succeeds (proxy/domain issue) | Deploy fails with logs; containers stay up for diagnosis; rollback tags available |
| Backup runs while the app is writing | sqlite backup API yields a consistent snapshot under WAL; file copies of markdown/chroma are best-effort |
| Backup directory missing | Created on first run |
| `DOMAIN` unreadable from server `.env` | External health check is skipped with a warning; container healthchecks still gate |
| Deploy triggered while another is running | Second run queues (no cancellation) |
| pip-audit/npm audit find a vulnerability | Weekly workflow fails → GitHub notification; merges are not blocked |

## Out of Scope

- Offsite backup replication (restic/rclone target) — documented as a
  recommended follow-up, not automated here.
- Blue/green or automated rollback execution — rollback stays a documented
  one-liner using the preserved tags.
- Frontend unit test runner (vitest) — separate decision.
