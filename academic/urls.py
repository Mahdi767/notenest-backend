from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter() # amader router

router.register('departments', views.DepartmentViewSet, basename='department')
router.register('courses', views.CourseViewSet, basename='course')
router.register('semesters', views.SemesterViewSet, basename='semester')
urlpatterns = [
    path('', include(router.urls)),
]