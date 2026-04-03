from django.urls import path

from .views import (
    RegisterView, 
    ActivateAccountView,
    UserLoginApiView,
    LogoutView,
    CurrentUserView,
    UserDetailView,
    ChangePasswordView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    ResendVerificationEmailView
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", UserLoginApiView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("activate/<str:uid64>/<str:token>/", ActivateAccountView.as_view(), name="activate"),
    path("resend-verification/", ResendVerificationEmailView.as_view(), name="resend-verification"),
    
    # Profile endpoints
    path("me/", CurrentUserView.as_view(), name="current-user"),
    path("users/<str:id>/", UserDetailView.as_view(), name="user-detail"),
    
    # Password management
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password-reset"),
    path("password-reset-confirm/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
]