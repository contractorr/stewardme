"""Tests for rate limit email notifications."""

from unittest.mock import patch

from cli.config_models import CoachConfig, EmailConfig
from cli.rate_limit_notifier import RateLimitNotifier, get_notifier, init_notifier


def _make_config(enabled=True, smtp_host="smtp.test.com"):
    """Build a CoachConfig with email settings for testing."""
    return CoachConfig(
        email=EmailConfig(
            enabled=enabled,
            smtp_host=smtp_host,
            smtp_port=587,
            username="user@test.com",
            password="secret",
            to="user@test.com",
        )
    )


class TestRateLimitNotifier:
    def test_notify_sends_email(self):
        config = _make_config()
        notifier = RateLimitNotifier(config)

        with patch("cli.email_digest.send_digest", return_value=True) as mock_send:
            result = notifier.notify("claude", "rate limit exceeded")

        assert result is True
        mock_send.assert_called_once()
        call_kwargs = mock_send.call_args
        assert "claude" in call_kwargs[1]["subject"] or "claude" in call_kwargs[0][0]

    def test_notify_cooldown(self):
        config = _make_config()
        notifier = RateLimitNotifier(config, cooldown_seconds=3600)

        with patch("cli.email_digest.send_digest", return_value=True):
            first = notifier.notify("claude", "rate limit 1")
            second = notifier.notify("claude", "rate limit 2")

        assert first is True
        assert second is False

    def test_notify_separate_providers(self):
        config = _make_config()
        notifier = RateLimitNotifier(config, cooldown_seconds=3600)

        with patch("cli.email_digest.send_digest", return_value=True):
            r1 = notifier.notify("claude", "rate limit")
            r2 = notifier.notify("openai", "rate limit")

        assert r1 is True
        assert r2 is True

    def test_notify_disabled(self):
        config = _make_config(enabled=False)
        notifier = RateLimitNotifier(config)

        with patch("cli.email_digest.send_digest") as mock_send:
            result = notifier.notify("claude", "rate limit")

        assert result is False
        mock_send.assert_not_called()

    def test_notify_no_smtp_host(self):
        config = _make_config(smtp_host=None)
        notifier = RateLimitNotifier(config)

        with patch("cli.email_digest.send_digest") as mock_send:
            result = notifier.notify("claude", "rate limit")

        assert result is False
        mock_send.assert_not_called()

    def test_notify_email_failure(self):
        config = _make_config()
        notifier = RateLimitNotifier(config)

        with patch("cli.email_digest.send_digest", side_effect=Exception("SMTP down")):
            result = notifier.notify("claude", "rate limit")

        assert result is False

    def test_cooldown_expires(self):
        config = _make_config()
        notifier = RateLimitNotifier(config, cooldown_seconds=0)

        with patch("cli.email_digest.send_digest", return_value=True):
            r1 = notifier.notify("claude", "err 1")
            r2 = notifier.notify("claude", "err 2")

        assert r1 is True
        assert r2 is True


class TestModuleSingleton:
    def test_init_and_get(self):
        config = _make_config()
        init_notifier(config)
        n = get_notifier()
        assert n is not None
        assert isinstance(n, RateLimitNotifier)
