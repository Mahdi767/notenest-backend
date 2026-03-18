from django.shortcuts import render
from rest_framework import viewsets
from . models import ResourceReport,ModerationAction
from rest_framework.permissions import IsAuthenticated
from .serializers import ModerationActionSerializer,ResourceReportSerializer
# Create your views here.
class ModerationActionViewSet(viewsets.ModelViewSet):
    queryset = ModerationAction.objects.all()
    serializer_class = ModerationActionSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]  # moderator check in view logic
    
    def perform_create(self, serializer):
        action = serializer.save(moderator=self.request.user)
        resource = action.resource
        resource.status = action.action
        resource.save()
        
class ResourceReportViewSet(viewsets.ModelViewSet):
    queryset = ResourceReport.objects.all()
    serializer_class =  ResourceReportSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)

   