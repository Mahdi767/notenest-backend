from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter() # amader router

router.register('like', views.LikeViewSet, basename='like')
router.register('comment', views.CommentViewSet, basename='comment')
router.register('bookmark', views.BookmarkViewSet, basename='bookmark')

urlpatterns = [
    path('', include(router.urls)),
]