
from rest_framework import serializers
from moderation.models import ModerationAction,ResourceReport
from resources.models import Resource
import cloudinary
import cloudinary.utils
import os


class ResourceDetailSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    
    def get_file(self, obj):
        if not obj.file:
            return None
        
        file_path = str(obj.file)

        if file_path.startswith('http'):
            return file_path
        
        # Use cloudinary.utils to build the proper URL
        cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME') or cloudinary.config().cloud_name
        url = cloudinary.utils.cloudinary_url(file_path, secure=True)[0]
        return url if url else file_path
    
    class Meta:
        model = Resource
        fields = ['id', 'title', 'file', 'description', 'resource_type']


class ModerationActionSerializer(serializers.ModelSerializer):
    resource = ResourceDetailSerializer(read_only=True)
    resource_id = serializers.PrimaryKeyRelatedField(
        queryset=Resource.objects.filter(status='pending'),
        source='resource',
        write_only=True
    )
    moderator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = ModerationAction
        fields = ['id', 'resource', 'resource_id', 'moderator', 'action', 'feedback', 'created_at']

class ResourceReportSerializer(serializers.ModelSerializer):
    reported_by = serializers.StringRelatedField(read_only=True)
    resource_details = ResourceDetailSerializer(source='resource', read_only=True)
    resource_id = serializers.PrimaryKeyRelatedField(
        queryset=Resource.objects.all(),
        source='resource',
        write_only=True
    )
    
    class Meta:
        model = ResourceReport
        fields = ['id', 'resource_id', 'resource_details', 'reported_by', 'reason', 'status', 'created_at']
        read_only_fields = ['status', 'created_at', 'reported_by']
