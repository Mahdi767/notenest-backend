from django.shortcuts import render, redirect
from . serializers import RegisterSerializer,UserLoginSerializer
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

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()

            return Response(
                {"message": "Account activated successfully. You can now login."},
                status=status.HTTP_200_OK
            )

        return Response(
            {"error": "Activation link is invalid or expired."},
            status=status.HTTP_400_BAD_REQUEST
        )


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

            return Response({
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                },
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