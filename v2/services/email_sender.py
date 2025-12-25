"""
Email Service - Gmail SMTP sender with templates.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional, List, Tuple
from dataclasses import dataclass
from ..config import GMAIL_USER, GMAIL_APP_PASSWORD
from ..utils import get_logger, retry_with_backoff

logger = get_logger("email_sender")


@dataclass
class EmailResult:
    """Result of email operation."""
    success: bool
    error: Optional[str] = None


class EmailService:
    """Service for sending emails via Gmail SMTP."""

    def __init__(self, user: str = None, password: str = None):
        self.user = user or GMAIL_USER
        self.password = password or GMAIL_APP_PASSWORD
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def is_configured(self) -> bool:
        """Check if email is configured."""
        return bool(self.password)

    @retry_with_backoff(max_attempts=2, initial_delay=2.0, exceptions=(smtplib.SMTPException,))
    def send(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        attachments: List[Tuple[str, bytes]] = None,
        from_name: str = "Kandidatentekort.nl"
    ) -> EmailResult:
        """
        Send HTML email with optional attachments.

        Args:
            to_email: Recipient email
            subject: Email subject
            html_body: HTML content
            attachments: List of (filename, content_bytes) tuples
            from_name: Display name for sender

        Returns:
            EmailResult with success status
        """
        if not self.is_configured():
            logger.error("Email not configured - GMAIL_APP_PASSWORD missing")
            return EmailResult(success=False, error="Email not configured")

        try:
            logger.info(f"Sending email to: {to_email}")

            # Build message
            if attachments:
                msg = MIMEMultipart('mixed')
                html_part = MIMEMultipart('alternative')
                html_part.attach(MIMEText(html_body, 'html', 'utf-8'))
                msg.attach(html_part)

                # Add attachments
                for filename, content in attachments:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(content)
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                    msg.attach(part)
            else:
                msg = MIMEMultipart('alternative')
                msg.attach(MIMEText(html_body, 'html', 'utf-8'))

            msg['Subject'] = subject
            msg['From'] = f"{from_name} <{self.user}>"
            msg['To'] = to_email

            # Send
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=30) as server:
                server.starttls()
                # Clean password (remove accidental spaces)
                password = self.password.replace(" ", "") if self.password else ""
                server.login(self.user, password)
                server.send_message(msg)

            logger.info(f"Email sent successfully to {to_email}")
            return EmailResult(success=True)

        except smtplib.SMTPException as e:
            logger.error(f"SMTP error: {e}")
            raise  # Let retry handle it
        except Exception as e:
            logger.error(f"Email failed: {e}")
            return EmailResult(success=False, error=str(e))

    def send_with_pdf_attachments(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        pdf_bytes_list: List[Tuple[str, bytes]]
    ) -> EmailResult:
        """Convenience method for sending emails with PDF attachments."""
        return self.send(to_email, subject, html_body, attachments=pdf_bytes_list)


# Singleton instance
_email_service = None


def get_email_service() -> EmailService:
    """Get singleton email service instance."""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service


def send_email(to_email: str, subject: str, html_body: str) -> bool:
    """Convenience function for sending email."""
    result = get_email_service().send(to_email, subject, html_body)
    return result.success
