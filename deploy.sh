#!/usr/bin/env bash
set -euo pipefail

echo "=== AI Coach VPS Deploy ==="

# --- Install Docker if missing ---
if ! command -v docker &>/dev/null; then
    echo "Installing Docker..."
    apt-get update -qq
    apt-get install -y -qq ca-certificates curl gnupg
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    chmod a+r /etc/apt/keyrings/docker.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" > /etc/apt/sources.list.d/docker.list
    apt-get update -qq
    apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-compose-plugin
    systemctl enable --now docker
    echo "Docker installed."
else
    echo "Docker already installed."
fi

# --- Validate .env ---
if [ ! -f .env ]; then
    echo "ERROR: .env not found. Copy .env.example to .env and fill in values."
    echo "  cp .env.example .env && nano .env"
    exit 1
fi

REQUIRED_VARS=(DOMAIN SECRET_KEY NEXTAUTH_SECRET)
MISSING=()
for var in "${REQUIRED_VARS[@]}"; do
    val=$(grep "^${var}=" .env | cut -d= -f2-)
    if [ -z "$val" ]; then
        MISSING+=("$var")
    fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
    echo "ERROR: Missing required values in .env: ${MISSING[*]}"
    exit 1
fi

# Check at least one OAuth provider configured
GH_ID=$(grep "^GITHUB_CLIENT_ID=" .env | cut -d= -f2-)
GO_ID=$(grep "^GOOGLE_CLIENT_ID=" .env | cut -d= -f2-)
if [ -z "$GH_ID" ] && [ -z "$GO_ID" ]; then
    echo "WARNING: No OAuth provider configured. Set GITHUB_CLIENT_ID or GOOGLE_CLIENT_ID in .env."
fi

# --- Create data dir ---
mkdir -p ~/coach

# --- Deploy ---
echo "Building and starting containers..."
docker compose -f docker-compose.prod.yml up -d --build

echo ""
echo "=== Deployed ==="
DOMAIN=$(grep "^DOMAIN=" .env | cut -d= -f2-)
echo "Site: https://${DOMAIN}"
echo ""
echo "Useful commands:"
echo "  docker compose -f docker-compose.prod.yml logs -f      # logs"
echo "  docker compose -f docker-compose.prod.yml ps           # status"
echo "  docker compose -f docker-compose.prod.yml down          # stop"
echo "  docker compose -f docker-compose.prod.yml up -d --build # rebuild"
