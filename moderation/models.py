from django.db import models
from resources.models import Resource
from accounts.models import User
from .constant import ACTION_CHOICES,REPORT_STATUS_CHOICES


class ModerationAction(models.Model):
    resource = models.ForeignKey(Resource,on_delete=models.CASCADE)
    moderator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(choices=ACTION_CHOICES, max_length=20)
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.resource}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.resource and self.resource.status != self.action:
            self.resource.status = self.action
            self.resource.save(update_fields=['status', 'updated_at'])


class ResourceReport(models.Model):
    resource =  models.ForeignKey(Resource,on_delete=models.CASCADE)
    reported_by =  models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    reason = models.TextField()
    status = models.CharField(choices=REPORT_STATUS_CHOICES, max_length=20, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report - {self.resource}"
