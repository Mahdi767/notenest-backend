from django.shortcuts import render
from rest_framework import viewsets
from . models import ResourceReport,ModerationAction
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .serializers import ModerationActionSerializer,ResourceReportSerializer
from django_filters.rest_framework import DjangoFilterBackend
from resources.models import Resource
# Create your views here.

class ModerationActionViewSet(viewsets.ModelViewSet):
    serializer_class = ModerationActionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['action', 'resource__status']

    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:  # admin/moderator
            return ModerationAction.objects.all()
        # normal user
        return ModerationAction.objects.filter(resource__uploaded_by=user)
        
    
    

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]  # moderator check in view logic
    
    def perform_create(self, serializer):
        serializer.save(moderator=self.request.user)
        # The ModerationAction.save() method already handles updating resource status
        
class ResourceReportViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceReportSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'resource__status']

    def get_queryset(self):
        user = self.request.user
        # Only staff/admin can see all reports
        if user.is_staff:
            return ResourceReport.objects.all()
        # Users can only see their own reports
        return ResourceReport.objects.filter(reported_by=user)

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]  # Any user can report
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]  # Any user can view their reports
        # Only admins can update/delete reports
        return [IsAdminUser()]

    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)

   