from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from interactions.serializers import LikeSerializer,CommentSerializer,BookmarkSerializer
from .models import Like,Bookmark,Comment
from rest_framework import viewsets
from django.db import IntegrityError

class InteractionRateThrottle(UserRateThrottle):
    """Rate throttle for interaction endpoints (likes, bookmarks, comments)"""
    scope = 'interactions'
    rate = '100/hour'

class AnonInteractionRateThrottle(AnonRateThrottle):
    """Rate throttle for anonymous user interactions"""
    scope = 'anon_interactions'
    rate = '50/hour'

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [InteractionRateThrottle, AnonInteractionRateThrottle]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            return Response({'error': 'You already liked this resource'}, status=400)


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [InteractionRateThrottle, AnonInteractionRateThrottle]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            return Response({'error': 'You already bookmarked this resource'}, status=400)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [InteractionRateThrottle, AnonInteractionRateThrottle]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def destroy(self, request, pk=None):
        """Allow user to delete only their own comments"""
        comment = self.get_object()
        if comment.user != request.user:
            return Response({'error': 'You can only delete your own comments'}, status=403)
        
        # Check if comment has replies
        if comment.replies.exists():
            return Response({
                'error': 'Cannot delete comment with replies. Delete replies first.',
                'reply_count': comment.replies.count()
            }, status=400)
        
        comment.delete()
        return Response({'status': 'comment deleted'})



