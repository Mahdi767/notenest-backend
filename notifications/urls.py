from django.urls import path
from .views import NotificationViewset

urlpatterns = [
    path('notifications/', NotificationViewset.as_view(), name='notifications'),
]