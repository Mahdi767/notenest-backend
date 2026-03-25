from django.shortcuts import render
from rest_framework import viewsets
from . models import Department,Semester,Course
from .serializers import DepartmentSerializer,SemesterSerializer,CourseSerializer
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class =  DepartmentSerializer  
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]
    
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class =  CourseSerializer 
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['department']
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]
    
class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class =  SemesterSerializer  
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]

