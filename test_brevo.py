#!/usr/bin/env python
"""Test Brevo SMTP credentials"""
import os
import smtplib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

print(f"Testing Brevo SMTP Credentials:")
print(f"Host: {EMAIL_HOST}")
print(f"Port: {EMAIL_PORT}")
print(f"Username: {EMAIL_HOST_USER}")
print(f"Password: {'*' * 20}... (length: {len(EMAIL_HOST_PASSWORD)})")
print()

try:
    print("Connecting to Brevo SMTP server...")
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    
    print("Authenticating...")
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    print("✓ SUCCESS! Credentials are correct.")
    
    server.quit()
except smtplib.SMTPAuthenticationError as e:
    print(f"✗ AUTHENTICATION FAILED: {e}")
    print("Check your Brevo credentials in .env file")
except Exception as e:
    print(f"✗ ERROR: {e}")
