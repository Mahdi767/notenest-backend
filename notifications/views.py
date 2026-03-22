from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from . models import Notification
from .serializers import NotificationSerializer
# Create your views here.
class NotificationViewset(ListAPIView):
    queryset =  Notification.objects.all()
    serializer_class =  NotificationSerializer

    #permission
    def get_permissions(self):
        return [IsAuthenticated()]
    
    #user should get their own notification

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

