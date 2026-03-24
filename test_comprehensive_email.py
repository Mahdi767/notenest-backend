#!/usr/bin/env python
"""Comprehensive email settings and sending test"""
import os
import django
import threading
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Note_nest_backend.settings')
django.setup()

from django.conf import settings
from django.core.mail import get_connection, EmailMultiAlternatives
from django import db

print("="*60)
print("EMAIL SETTINGS CHECK")
print("="*60)
print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"EMAIL_HOST_PASSWORD: {'*' * 20}... (length: {len(settings.EMAIL_HOST_PASSWORD)})")
print()

def test_email_in_thread():
    """Test email sending in a thread"""
    print(f"[THREAD] Starting...")
    print(f"[THREAD] settings.EMAIL_HOST_USER = {settings.EMAIL_HOST_USER}")
    
    try:
        db.close_old_connections()
        conn = get_connection()
        print(f"[THREAD] Connection: {conn}")
        print(f"[THREAD] Connection host: {conn.host}")
        print(f"[THREAD] Connection username: {conn.username}")
        
        email = EmailMultiAlternatives(
            subject="Test",
            body="",
            from_email=settings.EMAIL_HOST_USER,
            to=["test@example.com"],
            connection=conn
        )
        email.attach_alternative("<h1>Test</h1>", "text/html")
        
        print(f"[THREAD] Email object created")
        print(f"[THREAD] from_email: {email.from_email}")
        print(f"[THREAD] to: {email.to}")
        
        result = email.send(fail_silently=False)
        print(f"[THREAD] ✓ SENT! Result: {result}")
        
    except Exception as e:
        print(f"[THREAD] ✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close_old_connections()
        print(f"[THREAD] Done")

print("="*60)
print("TESTING EMAIL IN THREAD")
print("="*60)

thread = threading.Thread(target=test_email_in_thread)
thread.daemon = False
thread.start()
thread.join(timeout=10)

if thread.is_alive():
    print("✗ TIMEOUT!")
else:
    print("✓ Thread completed")
