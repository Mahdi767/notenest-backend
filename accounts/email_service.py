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
        
        # Log config status for debugging
        if not self.api_key:
            logger.error("BREVO_API_KEY is not set in environment variables!")
        else:
            logger.info(f"BREVO_API_KEY loaded: {self.api_key[:10]}...***")  # Log first 10 chars only

    def _get_sender_identity(self):
        sender_name = getattr(settings, "BREVO_SENDER_NAME", "NoteNest")
        sender_email = getattr(settings, "BREVO_SENDER_EMAIL", "").strip()

        if not sender_email:
            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@notenestmu.me").strip()
            sender_email = from_email

            if "<" in from_email and ">" in from_email:
                sender_name = from_email.split("<")[0].strip() or sender_name
                sender_email = from_email.split("<")[1].split(">")[0].strip()

        return sender_name, sender_email

    def send_verification_email(self, to_email, verify_link):
        """
        Send verification email using Brevo API.
        """
        logger.info(f"Preparing to send verification email via API to {to_email}...")
        
        try:
            if not self.api_key:
                return {
                    "status": "error",
                    "message": "BREVO_API_KEY is not configured",
                }

            subject = "Verify Your NoteNest Account"
            html_content = render_to_string(
                "verification_email.html",
                {"verify_link": verify_link},
            )
            
            sender_name, sender_email = self._get_sender_identity()
            
            logger.info(f"Using sender - Name: '{sender_name}', Email: '{sender_email}'")
            
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

            logger.info(f"Sending request to Brevo API with payload: {json.dumps({**payload, 'htmlContent': 'HTML_TRUNCATED'})}")
            logger.info(f"Headers being sent: accept={headers['accept']}, content-type={headers['content-type']}, api-key={'***' if headers['api-key'] else 'MISSING'}")
            response = requests.post(self.api_url, headers=headers, data=json.dumps(payload), timeout=10)
            
            logger.info(f"Brevo API Response: Status {response.status_code}")
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"SUCCESS: Email sent via Brevo API to {to_email}")
                return {"status": "success", "email": to_email}
            else:
                logger.error(f"API Error: Status {response.status_code}")
                logger.error(f"Response Text: {response.text}")
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
            if not self.api_key:
                return {
                    "status": "error",
                    "message": "BREVO_API_KEY is not configured",
                }

            subject = "Reset Your NoteNest Password"
            html_content = render_to_string(
                "password_reset_email.html",
                {"reset_link": reset_link},
            )
            
            sender_name, sender_email = self._get_sender_identity()
            
            logger.info(f"Using sender - Name: '{sender_name}', Email: '{sender_email}'")

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

            logger.info(f"Sending request to Brevo API with payload: {json.dumps({**payload, 'htmlContent': 'HTML_TRUNCATED'})}")
            logger.info(f"Headers being sent: accept={headers['accept']}, content-type={headers['content-type']}, api-key={'***' if headers['api-key'] else 'MISSING'}")
            response = requests.post(self.api_url, headers=headers, data=json.dumps(payload), timeout=10)
            
            logger.info(f"Brevo API Response: Status {response.status_code}")
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"SUCCESS: Password reset email sent via Brevo API to {to_email}")
                return {"status": "success", "email": to_email}
            else:
                logger.error(f"API Error: Status {response.status_code}")
                logger.error(f"Response Text: {response.text}")
                return {"status": "error", "message": response.text}

        except Exception as error:
            logger.exception(f"CRITICAL: Unexpected error in Brevo API service: {str(error)}")
            return {"status": "error", "message": str(error)}


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
