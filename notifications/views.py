from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import action
from rest_framework.response import Response

from . models import Notification
from .serializers import NotificationSerializer

class NotificationRateThrottle(UserRateThrottle):
    """Rate throttle for notification operations"""
    scope = 'notifications'
    rate = '200/hour'

class NotificationViewset(ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [NotificationRateThrottle]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')
    
    @action(detail=True, methods=['patch'])
    def mark_as_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response(NotificationSerializer(notification).data)
    
    @action(detail=True, methods=['delete'])
    def delete_notification(self, request, pk=None):
        """Allow user to delete their own notifications"""
        notification = self.get_object()
        if notification.user != request.user:
            return Response({'error': 'You can only delete your own notifications'}, status=403)
        notification.delete()
        return Response({'status': 'notification deleted'})


