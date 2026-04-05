
from accounts.models import User
from rest_framework import serializers
from resources.models import Resource,Tag
from academic.serializers import DepartmentSerializer,CourseSerializer,SemesterSerializer
from django.db.models import Count
import cloudinary
import cloudinary.utils
import os
from django.conf import settings
from interactions.models import Like,Bookmark,Comment


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer): #for readonly
    uploaded_by = UploadSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    semester = SemesterSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    file = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    bookmarks_count = serializers.SerializerMethodField()

    def get_file(self, obj):
        if not obj.file:
            return None
        
        try:
            file_path = str(obj.file)

            if file_path.startswith('http'):
                return file_path
            
            # Use cloudinary.utils to build the proper URL
            cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME') or cloudinary.config().cloud_name
            
            # Generate URL using cloudinary utils - handles the full transformation
            url = cloudinary.utils.cloudinary_url(file_path, secure=True)[0]
            
            return url if url else file_path
        except Exception as e:
            # Log error and return fallback
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error generating Cloudinary URL: {str(e)}")
            return str(obj.file) if obj.file else None

    def get_likes_count(self, obj):
        
        return Like.objects.filter(resource=obj).count()

    def get_comments_count(self, obj):
        
        return Comment.objects.filter(resource=obj).count()

    def get_bookmarks_count(self, obj):
       
        return Bookmark.objects.filter(resource=obj).count()

    class Meta:
        model = Resource
        fields = '__all__'


class ResourceCreateSerializer(serializers.ModelSerializer):#for post method
    file = serializers.FileField(required=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Tag.objects.all(),
        required=False
    )
    
    class Meta:
        model = Resource
        fields = ['title', 'description', 'file', 'resource_type', 'tags', 'department', 'course', 'semester']
    
    def validate(self, data):
        #Validate required fields
        if not data.get('title'):
            raise serializers.ValidationError({"title": "Title is required"})
        if not data.get('description'):
            raise serializers.ValidationError({"description": "Description is required"})
        if not data.get('resource_type'):
            raise serializers.ValidationError({"resource_type": "Resource type is required"})
        if not data.get('department'):
            raise serializers.ValidationError({"department": "Department is required"})
        return data
    
    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        resource = Resource.objects.create(**validated_data)
        resource.tags.set(tags)
        return resource



