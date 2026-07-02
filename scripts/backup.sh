#!/usr/bin/env bash
# Snapshot all coach data (SQLite DBs via the sqlite backup API — consistent
# under WAL with no downtime — plus journal/chroma/users/config files) from
# the backend container's volume to a timestamped tar on the host.
#
# Called automatically by scripts/deploy-remote.sh before every deploy.
# For nightly backups, add a cron entry on the server:
#   0 3 * * * cd /root/stewardme && ./scripts/backup.sh >> /var/log/coach-backup.log 2>&1
#
# Restore (containers stopped or accepting brief inconsistency):
#   tar -xzf coach-backup-<ts>.tar.gz
#   docker compose -f docker-compose.prod.yml cp coach-backup-staging/. backend:/data/coach/
#   docker compose -f docker-compose.prod.yml restart backend
set -euo pipefail

COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.prod.yml}"
BACKUP_DIR="${BACKUP_DIR:-$HOME/coach-backups}"
RETENTION_DAYS="${RETENTION_DAYS:-14}"
STAGING="/tmp/coach-backup-staging"

compose() { docker compose -f "$COMPOSE_FILE" "$@"; }

if ! compose ps --status running backend | grep -q backend; then
  echo "WARN: backend container not running — skipping backup" >&2
  exit 0
fi

echo "==> Staging snapshot inside backend container"
compose exec -T backend python - <<'PY'
import os
import shutil
import sqlite3
from pathlib import Path

coach_home = Path(os.environ.get("COACH_HOME", "/data/coach"))
staging = Path("/tmp/coach-backup-staging")
if staging.exists():
    shutil.rmtree(staging)
staging.mkdir(parents=True)

# SQLite: the backup API yields a consistent snapshot even under WAL
db_count = 0
for db in coach_home.rglob("*.db"):
    rel = db.relative_to(coach_home)
    dest = staging / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    src = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    dst = sqlite3.connect(dest)
    with dst:
        src.backup(dst)
    src.close()
    dst.close()
    db_count += 1

# Directories: best-effort file copies (markdown, vectors, per-user data)
dir_count = 0
for name in ("journal", "chroma", "users", "recommendations", "research"):
    d = coach_home / name
    if d.is_dir():
        shutil.copytree(
            d,
            staging / name,
            ignore=shutil.ignore_patterns("*.db", "*.db-wal", "*.db-shm"),
            dirs_exist_ok=True,
        )
        dir_count += 1

# Top-level config/state files
file_count = 0
for pattern in ("*.yaml", "*.yml", "*.json", "*.jsonl"):
    for f in coach_home.glob(pattern):
        shutil.copy2(f, staging / f.name)
        file_count += 1

print(f"staged {db_count} DBs, {dir_count} dirs, {file_count} config files")
PY

STAMP="$(date -u +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

echo "==> Copying snapshot to host"
compose cp backend:"$STAGING" "$WORK/coach-backup-staging"
compose exec -T backend rm -rf "$STAGING"

echo "==> Writing archive"
tar -czf "$BACKUP_DIR/coach-backup-$STAMP.tar.gz" -C "$WORK" coach-backup-staging
echo "✓ $BACKUP_DIR/coach-backup-$STAMP.tar.gz ($(du -h "$BACKUP_DIR/coach-backup-$STAMP.tar.gz" | cut -f1))"

echo "==> Pruning archives older than $RETENTION_DAYS days"
find "$BACKUP_DIR" -name 'coach-backup-*.tar.gz' -mtime "+$RETENTION_DAYS" -delete

echo "✓ Backup complete"
