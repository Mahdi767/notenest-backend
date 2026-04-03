from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import NotificationViewset

router = DefaultRouter()
router.register('', NotificationViewset, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]