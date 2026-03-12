from django.urls import path

from .views import RegisterView, ActivateAccountView,UserLoginApiView,LogoutView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", UserLoginApiView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("activate/<str:uid64>/<str:token>/", ActivateAccountView.as_view(), name="activate"),
]