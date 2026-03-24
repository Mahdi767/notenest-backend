"""
Email service module for sending transactional emails via Brevo API.
This module provides a production-ready interface for sending emails using
the Brevo (Sendinblue) transactional email service.
"""

import logging
from django.conf import settings
from django.template.loader import render_to_string
import sib_api_v3_sdk
from sib_api_v3_sdk import Configuration, ApiClient, TransactionalEmailsApi, SendSmtpEmail
from sib_api_v3_sdk.rest import ApiException

logger = logging.getLogger(__name__)


class BrevoEmailService:
    """
    Service class for handling email sending via Brevo API.
    Uses the official sib-api-v3-sdk for reliable transactional emails.
    """

    def __init__(self):
        """Initialize Brevo API configuration."""
        self.api_key = settings.BREVO_API_KEY
        if not self.api_key:
            raise ValueError("BREVO_API_KEY is not set in Django settings")

        # Configure API client
        configuration = Configuration()
        configuration.api_key["api-key"] = self.api_key
        self.api_client = ApiClient(configuration)
        self.email_api = TransactionalEmailsApi(self.api_client)

    def send_verification_email(self, to_email, verify_link):
        """
        Send verification email using Brevo API.

        Args:
            to_email (str): Recipient email address
            verify_link (str): Full URL verification link
                e.g., https://notenest.vercel.app/verify/<token>

        Returns:
            dict: Response containing status and message_id from Brevo API

        Raises:
            Exception: If email sending fails (logged but not raised to caller)
        """
        try:
            # Extract sender email from DEFAULT_FROM_EMAIL setting
            sender_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@notenestmu.me")
            if "<" in sender_email:
                # Handle format: "NoteNest <noreply@notenestmu.me>"
                sender_email = sender_email.split("<")[1].rstrip(">")

            # Render HTML template for email
            html_content = render_to_string(
                "verification_email.html",
                {"verify_link": verify_link},
            )

            # Create email object
            email = SendSmtpEmail(
                to=[{"email": to_email}],
                sender={"name": "NoteNest", "email": sender_email},
                subject="Verify Your NoteNest Account",
                html_content=html_content,
            )

            # Send via Brevo API
            response = self.email_api.send_transac_email(email)
            logger.info(
                f"Verification email sent successfully to {to_email}. "
                f"Message ID: {response.message_id}"
            )

            return {
                "status": "success",
                "message_id": response.message_id,
                "email": to_email,
            }

        except ApiException as api_error:
            logger.error(
                f"Brevo API error sending verification email to {to_email}: "
                f"Status {api_error.status} - {api_error.reason}"
            )
            return {
                "status": "error",
                "message": f"API Error: {api_error.reason}",
                "email": to_email,
            }

        except Exception as error:
            logger.exception(
                f"Unexpected error sending verification email to {to_email}: {str(error)}"
            )
            return {
                "status": "error",
                "message": str(error),
                "email": to_email,
            }

    def send_password_reset_email(self, to_email, reset_link):
        """
        Send password reset email using Brevo API.

        Args:
            to_email (str): Recipient email address
            reset_link (str): Full URL password reset link

        Returns:
            dict: Response containing status and message_id from Brevo API
        """
        try:
            sender_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@notenestmu.me")
            if "<" in sender_email:
                sender_email = sender_email.split("<")[1].rstrip(">")

            html_content = render_to_string(
                "password_reset_email.html",
                {"reset_link": reset_link},
            )

            email = SendSmtpEmail(
                to=[{"email": to_email}],
                sender={"name": "NoteNest", "email": sender_email},
                subject="Reset Your NoteNest Password",
                html_content=html_content,
            )

            response = self.email_api.send_transac_email(email)
            logger.info(
                f"Password reset email sent successfully to {to_email}. "
                f"Message ID: {response.message_id}"
            )

            return {
                "status": "success",
                "message_id": response.message_id,
                "email": to_email,
            }

        except ApiException as api_error:
            logger.error(
                f"Brevo API error sending password reset email to {to_email}: "
                f"Status {api_error.status} - {api_error.reason}"
            )
            return {
                "status": "error",
                "message": f"API Error: {api_error.reason}",
                "email": to_email,
            }

        except Exception as error:
            logger.exception(
                f"Unexpected error sending password reset email to {to_email}: {str(error)}"
            )
            return {
                "status": "error",
                "message": str(error),
                "email": to_email,
            }

    def send_bulk_email(self, recipient_emails, subject, html_content):
        """
        Send bulk email to multiple recipients.

        Args:
            recipient_emails (list): List of email addresses
            subject (str): Email subject
            html_content (str): HTML email content

        Returns:
            dict: Response status and message_id
        """
        try:
            sender_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@notenestmu.me")
            if "<" in sender_email:
                sender_email = sender_email.split("<")[1].rstrip(">")

            # Convert emails to recipient list format
            recipients = [{"email": email} for email in recipient_emails]

            email = SendSmtpEmail(
                to=recipients,
                sender={"name": "NoteNest", "email": sender_email},
                subject=subject,
                html_content=html_content,
            )

            response = self.email_api.send_transac_email(email)
            logger.info(
                f"Bulk email sent to {len(recipient_emails)} recipients. "
                f"Message ID: {response.message_id}"
            )

            return {
                "status": "success",
                "message_id": response.message_id,
                "recipients_count": len(recipient_emails),
            }

        except ApiException as api_error:
            logger.error(
                f"Brevo API error sending bulk email: "
                f"Status {api_error.status} - {api_error.reason}"
            )
            return {
                "status": "error",
                "message": f"API Error: {api_error.reason}",
            }

        except Exception as error:
            logger.exception(f"Unexpected error sending bulk email: {str(error)}")
            return {
                "status": "error",
                "message": str(error),
            }


# Singleton instance
_email_service = None


def get_email_service():
    """
    Get or create the Brevo email service instance.
    Uses lazy initialization for better error handling.

    Returns:
        BrevoEmailService: Singleton instance of the email service
    """
    global _email_service
    if _email_service is None:
        _email_service = BrevoEmailService()
    return _email_service


def send_verification_email(to_email, verify_link):
    """
    Convenience function to send verification email.

    Args:
        to_email (str): Recipient email address
        verify_link (str): Full URL verification link

    Returns:
        dict: Response containing status and message details
    """
    service = get_email_service()
    return service.send_verification_email(to_email, verify_link)


def send_password_reset_email(to_email, reset_link):
    """
    Convenience function to send password reset email.

    Args:
        to_email (str): Recipient email address
        reset_link (str): Full URL password reset link

    Returns:
        dict: Response containing status and message details
    """
    service = get_email_service()
    return service.send_password_reset_email(to_email, reset_link)
