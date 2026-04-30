"""
Email service module for sending transactional emails via Brevo API.
This module provides a production-ready interface for sending emails using
the Brevo (Sendinblue) transactional email service.
"""

import logging
import requests
import json
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


class BrevoEmailService:
    """
    Service class for handling email sending via Brevo API (v3).
    This uses HTTPS which bypasses port blocking on hosting providers like Render.
    """

    def __init__(self):
        self.api_key = settings.BREVO_API_KEY
        self.api_url = "https://api.brevo.com/v3/smtp/email"

    def send_verification_email(self, to_email, verify_link):
        """
        Send verification email using Brevo API.
        """
        logger.info(f"Preparing to send verification email via API to {to_email}...")
        
        try:
            subject = "Verify Your NoteNest Account"
            html_content = render_to_string(
                "verification_email.html",
                {"verify_link": verify_link},
            )
            
            # Extract sender from DEFAULT_FROM_EMAIL
            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@notenestmu.me")
            sender_name = "NoteNest"
            sender_email = from_email
            if "<" in from_email:
                sender_name = from_email.split("<")[0].strip()
                sender_email = from_email.split("<")[1].rstrip(">")

            payload = {
                "sender": {"name": sender_name, "email": sender_email},
                "to": [{"email": to_email}],
                "subject": subject,
                "htmlContent": html_content
            }

            headers = {
                "accept": "application/json",
                "api-key": self.api_key,
                "content-type": "application/json"
            }

            logger.info("Sending request to Brevo API...")
            response = requests.post(self.api_url, headers=headers, data=json.dumps(payload))
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"SUCCESS: Email sent via Brevo API to {to_email}")
                return {"status": "success", "email": to_email}
            else:
                logger.error(f"API Error: Status {response.status_code} - {response.text}")
                return {"status": "error", "message": response.text}

        except Exception as error:
            logger.exception(f"CRITICAL: Unexpected error in Brevo API service: {str(error)}")
            return {"status": "error", "message": str(error)}

    def send_password_reset_email(self, to_email, reset_link):
        """
        Send password reset email using Brevo API.
        """
        logger.info(f"Preparing to send password reset email via API to {to_email}...")
        
        try:
            subject = "Reset Your NoteNest Password"
            html_content = render_to_string(
                "password_reset_email.html",
                {"reset_link": reset_link},
            )
            
            # Extract sender from DEFAULT_FROM_EMAIL
            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@notenestmu.me")
            sender_name = "NoteNest"
            sender_email = from_email
            if "<" in from_email:
                sender_name = from_email.split("<")[0].strip()
                sender_email = from_email.split("<")[1].rstrip(">")

            payload = {
                "sender": {"name": sender_name, "email": sender_email},
                "to": [{"email": to_email}],
                "subject": subject,
                "htmlContent": html_content
            }

            headers = {
                "accept": "application/json",
                "api-key": self.api_key,
                "content-type": "application/json"
            }

            logger.info("Sending request to Brevo API...")
            response = requests.post(self.api_url, headers=headers, data=json.dumps(payload))
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"SUCCESS: Password reset email sent via Brevo API to {to_email}")
                return {"status": "success", "email": to_email}
            else:
                logger.error(f"API Error: Status {response.status_code} - {response.text}")
                return {"status": "error", "message": response.text}

        except Exception as error:
            logger.exception(f"CRITICAL: Unexpected error in Brevo API service: {str(error)}")
            return {"status": "error", "message": str(error)}

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
