from django.shortcuts import render
from resources.models import Resource
from resources.serializers import ResourceSerializer,ResourceCreateSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets

class ResourceViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ResourceCreateSerializer
        return ResourceSerializer
        
    def get_queryset(self):
        return Resource.objects.filter(status='approved')
        #return Resource.objects.all()
    
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)
    

