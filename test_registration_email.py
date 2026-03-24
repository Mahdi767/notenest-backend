#!/usr/bin/env python
"""Test registration email flow exactly"""
import os
import django
import threading
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Note_nest_backend.settings')
django.setup()

from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from accounts.models import User

# Create a test user
print("Creating test user...")
test_user = User.objects.create_user(
    username='testuser_' + str(int(time.time())),
    email='test_user@student.metrouni.ac.bd',
    password='testpass123'
)
print(f"User created: {test_user.email}")

# Generate token and uid
token = default_token_generator.make_token(test_user)
uid = urlsafe_base64_encode(force_bytes(test_user.pk))

# Build confirmation link
confirm_link = f"http://localhost:8000/api/accounts/activate/{uid}/{token}/"
print(f"Confirmation link: {confirm_link}")

# Try to render template
try:
    print("\nTrying to render email template...")
    email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
    print(f"✓ Template rendered successfully ({len(email_body)} chars)")
except Exception as e:
    print(f"✗ Template rendering failed: {e}")
    import traceback
    traceback.print_exc()

# Now try to send email using the async function
print("\nImporting async email function...")
from accounts.views import send_email_async

print("Creating thread to send email...")
thread = threading.Thread(
    target=send_email_async,
    args=("Confirm Your Email for NoteNest", email_body, test_user.email)
)
thread.daemon = False
thread.start()

print("Waiting for thread to complete...")
thread.join(timeout=10)

if thread.is_alive():
    print("✗ Thread timeout!")
else:
    print("✓ Thread completed!")

# Clean up
# test_user.delete()
