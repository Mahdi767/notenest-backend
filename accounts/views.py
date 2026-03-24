from django.shortcuts import render, redirect
from . serializers import RegisterSerializer,UserLoginSerializer
from django.contrib.auth import login,logout
from .models import User
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
import threading
import logging
import requests
import json

logger = logging.getLogger(__name__)

# Helper function to send email via Brevo API
def send_email_via_brevo(to_email, subject, html_body):
    """Send email using Brevo REST API (non-blocking)"""
    try:
        # Extract email from "Name <email@domain.com>" format
        from_email = settings.DEFAULT_FROM_EMAIL
        if '<' in from_email:
            from_email = from_email.split('<')[1].rstrip('>')
        
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "accept": "application/json",
            "api-key": settings.BREVO_API_KEY,
            "content-type": "application/json"
        }
        payload = {
            "to": [{"email": to_email}],
            "sender": {"name": "NoteNest", "email": from_email},
            "subject": subject,
            "htmlContent": html_body
        }
        
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            logger.info(f"Email sent successfully to {to_email} via Brevo API")
            return True
        else:
            logger.error(f"Brevo API error for {to_email}: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"Failed to send email to {to_email} via Brevo: {type(e).__name__}: {str(e)}", exc_info=True)
        return False

# Create your views here.
class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate token and uid
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Send verification email via Brevo API in background thread
            try:
                scheme = request.scheme
                domain = request.get_host()
                confirm_link = f"{scheme}://{domain}/api/accounts/activate/{uid}/{token}/"
                email_subject = "Confirm Your Email for NoteNest"
                email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
                
                # Start email sending in background thread via Brevo API
                email_thread = threading.Thread(
                    target=send_email_via_brevo,
                    args=(user.email, email_subject, email_body)
                )
                email_thread.daemon = True
                email_thread.start()
                logger.info(f"Email thread started for: {user.email}")
            except Exception as e:
                logger.error(f"Failed to start email thread: {str(e)}", exc_info=True)
            
            return Response(
                {"message": "User registered successfully, please check your email to verify your account."},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uid64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uid64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()
            # Redirect to frontend login page in production, returning simple response for now
            return Response({"message": "Account activated successfully. You can now login."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Activation link is invalid or has expired."}, status=status.HTTP_400_BAD_REQUEST)

        
class UserLoginApiView(APIView):
     def post(self, request):
          serializer = UserLoginSerializer(data=request.data)
          if serializer.is_valid():
               username = serializer.validated_data.get('username')
               password = serializer.validated_data.get('password')

               user = authenticate(username=username, password=password)
               if user:
                    token, _ = Token.objects.get_or_create(user=user)
                    login(request,user)
                    return Response({'token': token.key, 'user_id': user.id})
               return Response({'Error': 'Invalid Credentials'})
          return Response(serializer.errors)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logged out successfully"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )