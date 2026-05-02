from rest_framework import serializers
from .models import Notification
from django.contrib.contenttypes.models import ContentType
from resources.models import Resource
from interactions.models import Comment

class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    link_type = serializers.SerializerMethodField()
    link_id = serializers.SerializerMethodField()
    target_resource_id = serializers.SerializerMethodField()
    target_comment_id = serializers.SerializerMethodField()
    
    def get_link_type(self, obj):
        """Return the type of object this notification links to (resource or comment)"""
        if obj.content_type:
            return obj.content_type.model  # 'resource' or 'comment'
        return None
    
    def get_link_id(self, obj):
        """Return the ID of the resource or comment"""
        return obj.object_id

    def get_target_resource_id(self, obj):
        """Return the resource id this notification ultimately points to.

        - For a `resource` notification this is `object_id`.
        - For a `comment` notification we try to lookup the comment and
          return its `resource` id so frontend can navigate directly to
          the resource page.
        """
        if not obj.content_type or not obj.object_id:
            return None
        model = obj.content_type.model
        if model == 'resource':
            return obj.object_id
        if model == 'comment':
            try:
                comment = Comment.objects.select_related('resource').get(pk=obj.object_id)
                return comment.resource.id if comment.resource else None
            except Comment.DoesNotExist:
                return None
        return None

    def get_target_comment_id(self, obj):
        """Return the comment id if this notification is about a comment/reply."""
        if not obj.content_type or not obj.object_id:
            return None
        if obj.content_type.model == 'comment':
            return obj.object_id
        return None
    
    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'title', 'message', 'is_read', 'created_at',
            'link_type', 'link_id', 'target_resource_id', 'target_comment_id'
        ]