from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter() # amader router

router.register('tags', views.TagViewSet, basename='tag')
router.register('resources', views.ResourceViewSet, basename='resource')

urlpatterns = [
    path('', include(router.urls)),
]