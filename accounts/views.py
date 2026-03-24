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
import logging
import threading

logger = logging.getLogger(__name__)


def send_email_async(email_obj):
    try:
        email_obj.send()
    except Exception as e:
        logger.warning(f"Failed to send email: {str(e)}")


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

            # Send verification email
            try:
                # Build the confirmation link using the request's host
                protocol = 'https' if request.is_secure() else 'http'
                domain = request.get_host()
                confirm_link = f"{protocol}://{domain}/api/accounts/activate/{uid}/{token}/"
                email_subject = "Confirm Your Email for NoteNest"
                email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
                email = EmailMultiAlternatives(email_subject, '', to=[user.email])
                email.attach_alternative(email_body, "text/html")
                # Send email asynchronously to prevent blocking the request
                thread = threading.Thread(target=send_email_async, args=(email,))
                thread.daemon = True
                thread.start()
            except Exception as e:
                # Log any errors in email preparation, but don't fail the registration
                logger.warning(f"Error preparing email for user {user.email}: {str(e)}")
            
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