from rest_framework import serializers
from .models import Notification
from django.contrib.contenttypes.models import ContentType
from resources.models import Resource
from interactions.models import Comment

class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    link_type = serializers.SerializerMethodField()
    link_id = serializers.SerializerMethodField()
    
    def get_link_type(self, obj):
        """Return the type of object this notification links to (resource or comment)"""
        if obj.content_type:
            return obj.content_type.model  # 'resource' or 'comment'
        return None
    
    def get_link_id(self, obj):
        """Return the ID of the resource or comment"""
        return obj.object_id
    
    class Meta:
        model = Notification
        fields = ['id', 'user', 'title', 'message', 'is_read', 'created_at', 'link_type', 'link_id']