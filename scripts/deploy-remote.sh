#!/usr/bin/env bash
# Server-side deploy: validate → backup → build → health-gated swap → prune.
# Invoked by .github/workflows/deploy.yml after `git pull`; safe to run
# manually from the repo root on the server.
set -euo pipefail

COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.prod.yml}"
compose() { docker compose -f "$COMPOSE_FILE" "$@"; }

echo "==> Validating configuration"
compose config > /dev/null

if ! grep -q "./content:/app/content" "$COMPOSE_FILE"; then
  echo "ERROR: $COMPOSE_FILE missing curriculum content mount" >&2
  exit 1
fi
if [ ! -d "content/curriculum" ]; then
  echo "ERROR: content/curriculum directory not found" >&2
  exit 1
fi
echo "✓ Configuration validated"

echo "==> Pre-deploy backup"
bash scripts/backup.sh

echo "==> Preserving rollback tags"
# Compose default image names: <project>-<service>. Best-effort — the very
# first deploy has nothing to tag.
project="$(basename "$(pwd)")"
for svc in backend frontend; do
  img="${project}-${svc}"
  if docker image inspect "$img:latest" > /dev/null 2>&1; then
    docker tag "$img:latest" "$img:rollback"
    echo "✓ tagged $img:rollback"
  fi
done

echo "==> Building images"
compose build

echo "==> Swapping containers (waiting on healthchecks)"
if ! compose up -d --remove-orphans --wait --wait-timeout 180; then
  echo "ERROR: containers failed to become healthy" >&2
  compose logs --tail=100 >&2
  echo "Rollback: docker tag ${project}-backend:rollback ${project}-backend:latest && docker tag ${project}-frontend:rollback ${project}-frontend:latest && docker compose -f $COMPOSE_FILE up -d" >&2
  exit 1
fi

echo "==> Verifying public health endpoint"
DOMAIN="$(grep -E '^DOMAIN=' .env 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' || true)"
if [ -n "$DOMAIN" ]; then
  ok=""
  for i in 1 2 3 4 5; do
    if curl -fsS --max-time 10 "https://${DOMAIN}/api/health" > /dev/null; then
      ok=1
      break
    fi
    echo "  attempt $i failed; retrying in 5s"
    sleep 5
  done
  if [ -z "$ok" ]; then
    echo "ERROR: https://${DOMAIN}/api/health not responding after deploy" >&2
    compose logs --tail=100 >&2
    echo "Rollback: docker tag ${project}-backend:rollback ${project}-backend:latest && docker tag ${project}-frontend:rollback ${project}-frontend:latest && docker compose -f $COMPOSE_FILE up -d" >&2
    exit 1
  fi
  echo "✓ https://${DOMAIN}/api/health OK"
else
  echo "WARN: DOMAIN not readable from .env — skipping external health check (container healthchecks passed)"
fi

echo "==> Pruning dangling images older than 7 days"
docker image prune -f --filter "until=168h"

echo "✓ Deploy complete"
