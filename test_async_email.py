#!/usr/bin/env python
"""Test async email sending like the registration view does"""
import os
import django
import threading

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Note_nest_backend.settings')
django.setup()

from django.core.mail import EmailMultiAlternatives, get_connection
from django.conf import settings
from django import db
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def send_email_async(subject, body, recipient):
    """Send email in a background thread with proper Django context"""
    try:
        print(f"[THREAD] Starting email send for {recipient}")
        
        # Ensure we have a fresh database connection in this thread
        db.close_old_connections()
        
        # Create a fresh connection
        connection = get_connection()
        print(f"[THREAD] Connection created: {connection}")
        
        email = EmailMultiAlternatives(
            subject=subject,
            body='',
            from_email=settings.EMAIL_HOST_USER,
            to=[recipient],
            connection=connection
        )
        email.attach_alternative(body, "text/html")
        
        # Send the email
        print(f"[THREAD] Sending email...")
        result = email.send(fail_silently=False)
        print(f"[THREAD] ✓ Email sent successfully (result: {result})")
        logger.info(f"Email sent successfully to {recipient}")
        
    except Exception as e:
        print(f"[THREAD] ✗ ERROR: {str(e)}")
        logger.error(f"Failed to send email to {recipient}: {str(e)}", exc_info=True)
    finally:
        # Clean up database connection
        db.close_old_connections()
        print(f"[THREAD] Thread completed")


print("Testing async email sending...")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")

# Create and start thread
thread = threading.Thread(
    target=send_email_async,
    args=("Test Subject", "<h1>Test</h1><p>Test body</p>", "test@example.com")
)
thread.daemon = False
print(f"Thread created: {thread}")

thread.start()
print("Thread started, waiting for completion...")

thread.join(timeout=10)  # Wait up to 10 seconds
print(f"Thread alive: {thread.is_alive()}")

if thread.is_alive():
    print("✗ Thread is still running after timeout!")
else:
    print("✓ Thread completed successfully!")
