from django.shortcuts import render
from resources.models import Resource,ResourceView
from resources.serializers import ResourceSerializer,ResourceCreateSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.http import FileResponse
import os
from django.http import HttpResponseRedirect


class ResourceUploadRateThrottle(UserRateThrottle):
    """Rate throttle for resource uploads"""
    scope = 'resource_upload'
    rate = '10/hour'

class ResourceDownloadRateThrottle(UserRateThrottle):
    """Rate throttle for resource downloads"""
    scope = 'resource_download'
    rate = '500/hour'

class ResourceViewSet(viewsets.ModelViewSet):

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter] 
    filterset_fields = ['department', 'course', 'semester', 'resource_type']  
    search_fields = ['title']  
    ordering_fields = ['created_at', 'view_count', 'download_count']  
    pagination_class = PageNumberPagination
    throttle_classes = [ResourceUploadRateThrottle, ResourceDownloadRateThrottle]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ResourceCreateSerializer
        return ResourceSerializer
        
    def get_queryset(self):
        user = self.request.user
        # Admin/staff can see all resources
        if user.is_staff:
            return Resource.objects.all()
        # Users can edit/delete their own pending resources
        if self.action in ['update', 'partial_update', 'destroy']:
            return Resource.objects.filter(uploaded_by=user)
        # Everyone else sees only approved resources
        return Resource.objects.filter(status='approved')
    
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_client_ip(self, request):
        """Extract client IP from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_authenticated:
            view, created = ResourceView.objects.get_or_create(
                resource=instance,
                user=request.user,
                defaults={'ip_address': None}
            )
            if created:
                instance.view_count += 1
                instance.save()
        else:
            # Track anonymous views by IP
            ip = self.get_client_ip(request)
            view, created = ResourceView.objects.get_or_create(
                resource=instance,
                user=None,
                ip_address=ip
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
    

