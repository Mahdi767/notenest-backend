from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter() # amader router

router.register('action', views.ModerationActionViewSet, basename='action')
router.register('report', views.ResourceReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls)),
]