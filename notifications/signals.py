from django.db.models.signals import post_save
from django.dispatch import receiver
from moderation.models import ModerationAction
from interactions.models import Comment
from .models import Notification


@receiver(post_save, sender=ModerationAction)
def notify_resource_moderation(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.resource.uploaded_by,
            title=f"Resource {instance.action}",
            message=f"Your resource '{instance.resource.title}' has been {instance.action}. {instance.feedback}"
        )


@receiver(post_save, sender=Comment)
def notify_comment_reply(sender, instance, created, **kwargs):
    if created and instance.parent:
        Notification.objects.create(
            user=instance.parent.user,
            title="New reply to your comment",
            message=f"{instance.user} replied to your comment on '{instance.resource.title}'"
        )