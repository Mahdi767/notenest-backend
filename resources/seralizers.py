
from accounts.models import User
from rest_framework import serializers
from resources.models import Resource,Tag
from academic.serializers import DepartmentSerializer,CourseSerializer,SemesterSerializer


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

    class Meta:
        model = Resource
        fields = '__all__'


class ResourceCreateSerializer(serializers.ModelSerializer):#for post methpd
    class Meta:
        model = Resource
        fields = ['title', 'description', 'file', 'resource_type', 'tags', 'department', 'course', 'semester']



