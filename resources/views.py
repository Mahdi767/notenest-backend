from django.shortcuts import render
from resources.models import Resource,ResourceView
from resources.serializers import ResourceSerializer,ResourceCreateSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from django.http import FileResponse
import os
from django.http import HttpResponseRedirect


class ResourceViewSet(viewsets.ModelViewSet):

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter] 
    filterset_fields = ['department', 'course', 'semester', 'resource_type']  
    search_fields = ['title']  
    ordering_fields = ['created_at', 'view_count', 'download_count']  

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
        if request.user.is_authenticated:
            view, created = ResourceView.objects.get_or_create(
            resource=instance,
            user=request.user
        )
            if created:
                instance.view_count += 1
                instance.save()
        return super().retrieve(request, *args, **kwargs)
    @action(detail=True, methods=['get'])
    def download(self,request,pk=None):
        resource = self.get_object()
        resource.download_count += 1
        resource.save()
        # file_path = resource.file.path
        file_url = resource.file.url
        return HttpResponseRedirect(file_url)
        # return FileResponse(
        #     open(file_path, 'rb'),
        #     as_attachment=True,
        #     filename=os.path.basename(file_path)
        # )
    

