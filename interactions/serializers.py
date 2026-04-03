from rest_framework import serializers
from .models import Like, Bookmark, Comment
from resources.models import Resource
from django.utils.html import escape

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    resource = serializers.PrimaryKeyRelatedField(
        queryset=Resource.objects.filter(status='approved')
    )
    class Meta:
        model = Like
        fields = "__all__"

class BookmarkSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    resource = serializers.PrimaryKeyRelatedField(
        queryset=Resource.objects.filter(status='approved')
    )
    class Meta:
        model = Bookmark
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    resource = serializers.PrimaryKeyRelatedField(
        queryset=Resource.objects.filter(status='approved')
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Comment
        fields = "__all__"
    
    def validate_content(self, value):
        """Sanitize comment content to prevent XSS attacks"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Comment cannot be empty")
        
        # Escape HTML to prevent XSS
        sanitized_content = escape(value)
        
        # Limit comment length
        if len(sanitized_content) > 5000:
            raise serializers.ValidationError("Comment cannot exceed 5000 characters")
        
        return sanitized_content