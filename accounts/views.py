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

logger = logging.getLogger(__name__)


# Helper function to send email in background
def send_verification_email(user_email, confirm_link):
    try:
        logger.info(f"Starting email send to: {user_email}")
        email_subject = "Confirm Your Email for NoteNest"
        email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
        email = EmailMultiAlternatives(email_subject, '', to=[user_email])
        email.attach_alternative(email_body, "text/html")
        result = email.send(fail_silently=False)
        logger.info(f"Email sent successfully to {user_email}. Result: {result}")
    except Exception as e:
        logger.error(f"Background email sending failed to {user_email}: {type(e).__name__}: {str(e)}", exc_info=True)

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

            # Send verification email in background thread (non-blocking)
            try:
                scheme = request.scheme
                domain = request.get_host()
                confirm_link = f"{scheme}://{domain}/api/accounts/activate/{uid}/{token}/"
                
                logger.info(f"Creating email thread for user: {user.email}")
                # Start email sending in background thread
                email_thread = threading.Thread(
                    target=send_verification_email,
                    args=(user.email, confirm_link)
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

class TestEmailView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Test endpoint to verify email sending works"""
        email = request.data.get('email')
        if not email:
            return Response(
                {"error": "Email is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            logger.info(f"Testing email send to: {email}")
            test_email = EmailMultiAlternatives(
                subject="Test Email from NoteNest",
                body="This is a test email",
                to=[email]
            )
            test_email.send(fail_silently=False)
            logger.info(f"Test email sent successfully to {email}")
            return Response(
                {"message": f"Test email sent to {email}"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Test email failed: {type(e).__name__}: {str(e)}", exc_info=True)
            return Response(
                {"error": f"Failed to send test email: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )