from django.shortcuts import render
from resources.models import Resource,ResourceView,Tag
from resources.serializers import ResourceSerializer,ResourceCreateSerializer,TagSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.http import FileResponse
from django.db.models import Q
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


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving tags.
    Allows all users to view available tags.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination


class ResourceViewSet(viewsets.ModelViewSet):

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter] 
    filterset_fields = ['department', 'course', 'semester', 'semester__year', 'resource_type']  
    search_fields = ['title']  
    ordering_fields = ['created_at', 'view_count', 'download_count']  
    pagination_class = PageNumberPagination

    def get_throttles(self):
        """
        Apply throttles only to specific actions:
        - Create/Upload: Strict rate limit (ResourceUploadRateThrottle)
        - Download: Moderate rate limit (ResourceDownloadRateThrottle)
        - List/Retrieve/Search/Filter: No throttle (unlimited browsing)
        """
        if self.action == 'create':
            return [ResourceUploadRateThrottle()]
        elif self.action == 'download':
            return [ResourceDownloadRateThrottle()]
        else:
            # List, retrieve, update, destroy use default throttles or none
            return []

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ResourceCreateSerializer
        return ResourceSerializer
        
    def get_queryset(self):
        user = self.request.user
        
        # Admin/staff can see all resources
        if user.is_staff:
            return Resource.objects.all()
        
        # Authenticated users can see: approved resources + their own resources
        if user.is_authenticated:
            if self.action in ['download']:
                # Allow download of approved resources or own resources
                return Resource.objects.filter(
                    Q(status='approved') | Q(uploaded_by=user)
                )
            elif self.action in ['update', 'partial_update', 'destroy']:
                # Can only edit/delete own resources
                return Resource.objects.filter(uploaded_by=user)
            else:
                # List/Retrieve: approved resources + own resources
                return Resource.objects.filter(
                    Q(status='approved') | Q(uploaded_by=user)
                )
        
        # Anonymous users only see approved resources
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
    def download(self, request, pk=None):
        """
        Download endpoint that increments download count and returns file URL.
        Frontend handles the actual file download using the returned URL.
        """
        resource = self.get_object()
        
        # Check if resource has a file
        if not resource.file:
            return Response(
                {'error': 'No file associated with this resource'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Increment download count
        resource.download_count += 1
        resource.save(update_fields=['download_count'])
        
        # Get file URL from Cloudinary
        try:
            file_url = resource.file.url
        except Exception as e:
            return Response(
                {'error': f'Could not generate file URL: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Return JSON response with file URL and updated count
        return Response({
            'success': True,
            'file_url': file_url,
            'download_count': resource.download_count,
            'filename': resource.file.name if resource.file else f'{resource.title}.pdf'
        }, status=status.HTTP_200_OK)
    

