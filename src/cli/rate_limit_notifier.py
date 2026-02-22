"""Rate limit email notifications with per-provider cooldown."""

import time
from datetime import datetime, timezone

import structlog

from cli.email_digest import send_digest
from observability import metrics

logger = structlog.get_logger()


class RateLimitNotifier:
    """Sends email alerts when rate limits are hit, with per-provider cooldown."""

    def __init__(self, config, cooldown_seconds: int = 3600):
        self._config = config
        self._email_config = config.email
        self._cooldown = cooldown_seconds
        self._last_sent: dict[str, float] = {}

    def _is_enabled(self) -> bool:
        return self._email_config.enabled and bool(self._email_config.smtp_host)

    def notify(self, provider: str, error_msg: str) -> bool:
        """Send email if not in cooldown. Returns True if sent."""
        if not self._is_enabled():
            logger.debug("rate_limit_notifier_disabled", provider=provider)
            return False

        now = time.monotonic()
        last = self._last_sent.get(provider)
        if last is not None and now - last < self._cooldown:
            metrics.counter("rate_limit_notification_cooldown")
            logger.debug("rate_limit_notification_cooldown", provider=provider)
            return False

        body = self._build_body(provider, error_msg)
        try:
            config_dict = self._config_as_dict()
            sent = send_digest(
                subject=f"Rate limit hit: {provider}",
                body_markdown=body,
                config=config_dict,
            )
            if sent:
                self._last_sent[provider] = now
                metrics.counter("rate_limit_notification_sent")
                logger.info("rate_limit_notification_sent", provider=provider)
                return True
            return False
        except Exception as e:
            logger.error("rate_limit_notification_failed", provider=provider, error=str(e))
            return False

    def _config_as_dict(self) -> dict:
        """Convert email config to dict format expected by send_digest."""
        ec = self._email_config
        return {
            "email": {
                "smtp_host": ec.smtp_host,
                "smtp_port": ec.smtp_port,
                "username": ec.username,
                "password": ec.password,
                "to": ec.to,
                "from": ec.from_addr or ec.username,
            }
        }

    def _build_body(self, provider: str, error_msg: str) -> str:
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        return (
            f"# Rate Limit Alert\n\n"
            f"**Provider:** {provider}\n\n"
            f"**Time:** {ts}\n\n"
            f"**Error:** {error_msg}\n\n"
            f"## Suggested Actions\n\n"
            f"- Check usage dashboard for {provider}\n"
            f"- Upgrade plan or add credits\n"
            f"- Reduce request frequency\n"
            f"- Rotate API key if needed\n"
        )


# Module-level lazy singleton
_notifier: RateLimitNotifier | None = None


def init_notifier(config) -> None:
    """Initialize the global notifier from CoachConfig."""
    global _notifier
    _notifier = RateLimitNotifier(config)


def get_notifier() -> RateLimitNotifier | None:
    """Get the global notifier instance (None if not initialized)."""
    return _notifier
