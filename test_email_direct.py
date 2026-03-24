#!/usr/bin/env python
"""Test email sending directly"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Note_nest_backend.settings')
django.setup()

from django.core.mail import EmailMultiAlternatives, get_connection
from django.conf import settings

print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print()

try:
    connection = get_connection()
    print("Connection created successfully")
    
    email = EmailMultiAlternatives(
        subject="Test Email from NoteNest",
        body="",
        from_email=settings.EMAIL_HOST_USER,
        to=["test@example.com"],
        connection=connection
    )
    email.attach_alternative("<h1>Test</h1><p>This is a test email from Brevo</p>", "text/html")
    
    print("Sending email...")
    result = email.send(fail_silently=False)
    print(f"✓ Email sent successfully! Result: {result}")
    
except Exception as e:
    print(f"✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
