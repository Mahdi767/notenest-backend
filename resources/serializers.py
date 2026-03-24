
from accounts.models import User
from rest_framework import serializers
from resources.models import Resource,Tag
from academic.serializers import DepartmentSerializer,CourseSerializer,SemesterSerializer
import cloudinary
import cloudinary.utils
import os
from django.conf import settings


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

    def get_file(self, obj):
        if not obj.file:
            return None
        
        file_path = str(obj.file)

        if file_path.startswith('http'):
            return file_path
        
        # Use cloudinary.utils to build the proper URL
        cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME') or cloudinary.config().cloud_name
        
        # Generate URL using cloudinary utils - handles the full transformation
        url = cloudinary.utils.cloudinary_url(file_path, secure=True)[0]
        
        return url if url else file_path

    class Meta:
        model = Resource
        fields = '__all__'


class ResourceCreateSerializer(serializers.ModelSerializer):#for post methpd
    class Meta:
        model = Resource
        fields = ['title', 'description', 'file', 'resource_type', 'tags', 'department', 'course', 'semester']



