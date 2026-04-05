from django.shortcuts import render, redirect
from . serializers import (
    RegisterSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UpdateProfileSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)
from django.contrib.auth import login,authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

import threading
import logging
import requests

logger = logging.getLogger(__name__)



# Email Sender (Brevo API)
def send_email_via_brevo(to_email, subject, html_body):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        
        if "<" in from_email:
            from_email = from_email.split("<")[1].rstrip(">")

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
            logger.info(f"Email sent successfully to {to_email}")
            return True
        else:
            logger.error(f"Brevo error: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        logger.error(f"Email sending failed: {str(e)}")
        return False



# Register User
class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            try:
                scheme = request.scheme
                domain = request.get_host()
                confirm_link = f"{scheme}://{domain}/api/accounts/activate/{uid}/{token}/"

                email_subject = "Confirm Your Email for NoteNest"
                email_body = render_to_string(
                    "confirm_email.html",
                    {"confirm_link": confirm_link}
                )

                email_thread = threading.Thread(
                    target=send_email_via_brevo,
                    args=(user.email, email_subject, email_body)
                )
                email_thread.daemon = True
                email_thread.start()

            except Exception as e:
                logger.error(str(e))

            return Response(
                {"message": "User registered successfully. Please verify your email."},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Activate Account
class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uid64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uid64))
            user = User.objects.get(pk=uid)
        except Exception:
            user = None

        # ✅ Dynamically detect frontend URL from request
        scheme = request.scheme  # http or https
        domain = request.get_host()  # localhost:8000 or your-domain.com
        
        # Determine frontend domain (remove /api suffix if present)
        if domain.startswith('localhost') or domain.startswith('127.0.0.1'):
            # Local development: localhost:8000 → localhost:3000
            host_only = domain.split(':')[0]
            frontend_domain = f'{host_only}:3000'
        else:
            # Production: same domain as backend
            frontend_domain = domain

        frontend_url = f'{scheme}://{frontend_domain}'

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()

            # ✅ Redirect to frontend login page
            return redirect(f"{frontend_url}/login?verified=true&email={user.email}")

        # ❌ Redirect with error message
        return redirect(f"{frontend_url}/login?verified=false&error=Invalid+or+expired+link")


# Login (JWT)


class UserLoginApiView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(username=username, password=password)

            if user is None:
                return Response(
                    {"error": "Invalid username or password"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            if not user.is_active:
                return Response(
                    {"error": "Please verify your email first"},
                    status=status.HTTP_403_FORBIDDEN
                )

            refresh = RefreshToken.for_user(user)
            
            user_serializer = UserProfileSerializer(user)

            return Response({
                "user": user_serializer.data,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Logout (JWT Blacklist)


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

        except Exception:
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )


# Get Current User Profile
class CurrentUserView(generics.RetrieveUpdateAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UpdateProfileSerializer
        return UserProfileSerializer


# Get User by ID
class UserDetailView(generics.RetrieveAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    lookup_field = 'id'


# Change Password (for logged-in users)
class ChangePasswordView(APIView):
   
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'user': request.user}
        )
        
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            
            return Response(
                {"message": "Password changed successfully"},
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Password Reset - Request
class PasswordResetRequestView(APIView):
    """Request password reset via email"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = User.objects.get(email=email)
                
                # Generate token and UID
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Create password reset link
                scheme = request.scheme
                domain = request.get_host()
                reset_link = f"{scheme}://{domain}/api/accounts/reset-password-confirm/?uid={uid}&token={token}"
                
                # Send email
                email_subject = "Reset Your NoteNest Password"
                email_body = render_to_string(
                    "password_reset_email.html",
                    {"reset_link": reset_link, "user": user}
                )
                
                email_thread = threading.Thread(
                    target=send_email_via_brevo,
                    args=(email, email_subject, email_body)
                )
                email_thread.daemon = True
                email_thread.start()
                
                return Response(
                    {"message": "Password reset link sent to your email. Please check your inbox."},
                    status=status.HTTP_200_OK
                )
            
            except User.DoesNotExist:
                # Don't reveal if email exists (security)
                return Response(
                    {"message": "If an account exists with this email, a password reset link has been sent."},
                    status=status.HTTP_200_OK
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Password Reset - Confirm

class PasswordResetConfirmView(APIView):
 
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        
        if serializer.is_valid():
            uid = serializer.validated_data['uid']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            
            try:
                # Decode UID and get user
                uid_decoded = force_str(urlsafe_base64_decode(uid))
                user = User.objects.get(pk=uid_decoded)
                
                # Verify token
                if not default_token_generator.check_token(user, token):
                    return Response(
                        {"error": "Password reset token is invalid or expired."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Set new password
                user.set_password(new_password)
                user.save()
                
                return Response(
                    {"message": "Password reset successfully. You can now login with your new password."},
                    status=status.HTTP_200_OK
                )
            
            except (User.DoesNotExist, ValueError):
                return Response(
                    {"error": "Invalid password reset link."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Resend Verification Email
class ResendVerificationEmailView(APIView):
 
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response(
                {"error": "Email is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(email=email)
            
            # Check if already verified
            if user.is_verified:
                return Response(
                    {"message": "Account is already verified. You can login now."},
                    status=status.HTTP_200_OK
                )
            
            # Generate new token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Create activation link
            scheme = request.scheme
            domain = request.get_host()
            confirm_link = f"{scheme}://{domain}/api/accounts/activate/{uid}/{token}/"
            
            # Send verification email
            email_subject = "Confirm Your Email for NoteNest"
            email_body = render_to_string(
                "confirm_email.html",
                {"confirm_link": confirm_link}
            )
            
            email_thread = threading.Thread(
                target=send_email_via_brevo,
                args=(user.email, email_subject, email_body)
            )
            email_thread.daemon = True
            email_thread.start()
            
            return Response(
                {"message": "Verification email sent successfully. Please check your inbox."},
                status=status.HTTP_200_OK
            )
        
        except User.DoesNotExist:
            # Don't reveal if user exists (security best practice)
            return Response(
                {"message": "If an account exists with this email, a verification link has been sent."},
                status=status.HTTP_200_OK
            )