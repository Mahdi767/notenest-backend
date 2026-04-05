from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from moderation.models import ModerationAction, ResourceReport
from interactions.models import Comment, Like
from resources.models import Resource
from accounts.models import User
from .models import Notification


@receiver(post_save, sender=ModerationAction)
def notify_resource_moderation(sender, instance, created, **kwargs):
    if created and instance.resource.uploaded_by:
        # Get ContentType for Resource
        resource_ct = ContentType.objects.get_for_model(Resource)
        
        # Use get_or_create to prevent duplicate notifications
        notification, is_new = Notification.objects.get_or_create(
            user=instance.resource.uploaded_by,
            content_type=resource_ct,
            object_id=instance.resource.id,
            defaults={
                'title': f"Resource {instance.action.capitalize()}",
                'message': f"Your resource '{instance.resource.title}' has been {instance.action}. {instance.feedback}"
            }
        )
        # If already exists, update the message with latest feedback
        if not is_new:
            notification.title = f"Resource {instance.action.capitalize()}"
            notification.message = f"Your resource '{instance.resource.title}' has been {instance.action}. {instance.feedback}"
            notification.is_read = False
            notification.save()


@receiver(post_save, sender=Comment)
def notify_comment_reply(sender, instance, created, **kwargs):
    """Send notification when someone replies to a comment"""
    if created and instance.parent and instance.parent.user:
        # Get ContentType for Comment
        comment_ct = ContentType.objects.get_for_model(Comment)
        
        # Use get_or_create to prevent duplicate notifications
        notification, is_new = Notification.objects.get_or_create(
            user=instance.parent.user,
            content_type=comment_ct,
            object_id=instance.id,
            defaults={
                'title': "New reply to your comment",
                'message': f"{instance.user} replied to your comment on '{instance.resource.title}'"
            }
        )


@receiver(post_save, sender=Comment)
def notify_resource_comment(sender, instance, created, **kwargs):
    """Send notification to resource uploader when someone comments on their resource"""
    if created and instance.resource.uploaded_by:
        # Don't notify if the commenter is the uploader themselves
        if instance.user == instance.resource.uploaded_by:
            return
        
        # Don't notify for replies (only top-level comments)
        if instance.parent:
            return
        
        # Get ContentType for Resource
        resource_ct = ContentType.objects.get_for_model(Resource)
        
        # Create notification for the resource uploader
        Notification.objects.create(
            user=instance.resource.uploaded_by,
            content_type=resource_ct,
            object_id=instance.resource.id,
            title="New comment on your resource",
            message=f"{instance.user.first_name or instance.user.username} commented on '{instance.resource.title}': {instance.content[:50]}..."
        )


@receiver(post_save, sender=Like)
def notify_resource_like(sender, instance, created, **kwargs):
    """Send notification to resource uploader when someone likes their resource"""
    if created and instance.resource.uploaded_by:
        # Get ContentType for Resource
        resource_ct = ContentType.objects.get_for_model(Resource)
        
        # Create notification for the resource uploader
        Notification.objects.create(
            user=instance.resource.uploaded_by,
            content_type=resource_ct,
            object_id=instance.resource.id,
            title="New like on your resource",
            message=f"{instance.user.first_name} {instance.user.last_name} liked your '{instance.resource.title}'"
        )


@receiver(post_save, sender=ResourceReport)
def notify_admins_new_report(sender, instance, created, **kwargs):
    """Send notification to all admins when a new resource report is created"""
    if created:
        # Get ContentType for Resource (what was reported)
        resource_ct = ContentType.objects.get_for_model(Resource)
        
        # Get all admin users
        admin_users = User.objects.filter(is_staff=True)
        
        # Create notification for each admin
        for admin in admin_users:
            Notification.objects.create(
                user=admin,
                content_type=resource_ct,
                object_id=instance.resource.id,
                title="New resource report",
                message=f"'{instance.resource.title}' has been reported by {instance.reported_by.username}. Reason: {instance.reason[:50]}..."
            )