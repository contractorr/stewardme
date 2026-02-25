# Security Guide

Self-hosting security hardening for AI Coach.

## Secret Management

### SECRET_KEY (Flask/FastAPI session encryption)

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Set in `config.yaml` or env:

```bash
export SECRET_KEY="your-generated-key"
```

### NEXTAUTH_SECRET (web UI sessions)

```bash
openssl rand -base64 32
```

Set in `web/.env.local`:

```
NEXTAUTH_SECRET=your-generated-secret
NEXTAUTH_URL=https://your-domain.com
```

### Key Rotation

1. Generate new key
2. Update env var / config
3. Restart services — active sessions will be invalidated
4. For Fernet-encrypted data, decrypt with old key then re-encrypt with new key

## Network Security

### Firewall (only expose 443)

**UFW:**

```bash
ufw default deny incoming
ufw allow ssh
ufw allow 443/tcp
ufw enable
```

**firewalld:**

```bash
firewall-cmd --permanent --add-service=https
firewall-cmd --permanent --remove-service=http
firewall-cmd --reload
```

### Reverse Proxy (Caddy)

```
your-domain.com {
    reverse_proxy localhost:3000

    header {
        Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
        X-Frame-Options "DENY"
        X-Content-Type-Options "nosniff"
        Referrer-Policy "strict-origin-when-cross-origin"
        Permissions-Policy "camera=(), microphone=(), geolocation=()"
    }
}
```

Caddy handles TLS certs automatically via Let's Encrypt. Internal API (port 8000) should NOT be exposed externally.

## Data Protection

### File Permissions

```bash
chmod 700 ~/coach
chmod 600 ~/coach/config.yaml
chmod 600 ~/coach/intel.db
chmod 600 ~/coach/journal/*
```

### Backups

```bash
# SQLite safe backup (while running)
sqlite3 ~/coach/intel.db ".backup ~/coach/backups/intel-$(date +%F).db"

# Journal + config
tar czf ~/coach/backups/coach-$(date +%F).tar.gz \
    ~/coach/journal/ ~/coach/config.yaml ~/coach/recommendations/
```

### LLM API Keys

- Store in env vars or config.yaml (chmod 600), never in code
- Keys are redacted from structlog output automatically
- Use separate keys for dev/prod if provider supports it

## OAuth Considerations

### Callback URLs

- Dev: `http://localhost:3000/api/auth/callback/<provider>`
- Prod: `https://your-domain.com/api/auth/callback/<provider>`

### Per-Environment OAuth Apps

Create separate OAuth apps for dev and prod. Never reuse client secrets across environments.

### Public vs Private Hosting

- **Private (recommended):** VPN/tailnet access only. OAuth optional, can use simple token auth
- **Public:** OAuth required. Ensure callback URLs are HTTPS. Enable CSRF protection

### Session Security

- `NEXTAUTH_SECRET` must be cryptographically random (32+ bytes)
- Sessions expire after 30 days by default (configurable in `[...nextauth].ts`)
- Cookies set with `httpOnly`, `secure`, `sameSite=lax`

## Monitoring

### Log Filtering

Structlog is configured to redact patterns matching API keys. Verify with:

```bash
coach daemon 2>&1 | grep -i "key\|secret\|token"
```

Should show `[REDACTED]` for any sensitive values.

### Health Endpoint

`GET /api/intel/health` returns scraper status (auth-protected). Monitor for:

- `consecutive_errors >= 3` — source may be down or rate-limited
- `last_success_at` older than 72h — check network/config
- `backoff_until` in future — automatic recovery pending

Use external monitoring (e.g., uptime checker on `/api/intel/health`) for alerting.
