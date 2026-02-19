"""Email digest sender using stdlib smtplib."""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import structlog

logger = structlog.get_logger()


def send_digest(
    subject: str,
    body_markdown: str,
    config: dict,
) -> bool:
    """Send email digest via SMTP.

    Config expected:
        email:
          smtp_host: smtp.gmail.com
          smtp_port: 587
          username: user@gmail.com
          password: app-password
          to: user@gmail.com
          from: coach@example.com (optional, defaults to username)
    """
    email_config = config.get("email", {})
    if not email_config.get("smtp_host"):
        logger.debug("Email not configured, skipping digest")
        return False

    smtp_host = email_config["smtp_host"]
    smtp_port = email_config.get("smtp_port", 587)
    username = email_config.get("username", "")
    password = email_config.get("password", "")
    to_addr = email_config.get("to", username)
    from_addr = email_config.get("from", username)

    if not to_addr or not username:
        logger.warning("Email to/username not configured")
        return False

    # Build email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr

    # Plain text version
    msg.attach(MIMEText(body_markdown, "plain"))

    # Simple HTML version
    html_body = _markdown_to_simple_html(body_markdown)
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.ehlo()
            if smtp_port != 25:
                server.starttls()
            if username and password:
                server.login(username, password)
            server.sendmail(from_addr, [to_addr], msg.as_string())
        logger.info("Digest email sent", to=to_addr, subject=subject)
        return True
    except Exception as e:
        logger.error("Failed to send digest email", error=str(e))
        return False


def _markdown_to_simple_html(md: str) -> str:
    """Minimal markdown→HTML for email (no external deps)."""
    import re
    html = md
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = html.replace('\n\n', '<br><br>')
    return f"<html><body style='font-family:sans-serif;max-width:600px;margin:auto'>{html}</body></html>"
