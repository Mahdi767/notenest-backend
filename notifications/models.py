from django.db import models
from accounts.models import User

# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title =  models.CharField(max_length=255)
    message =  models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user} - {self.title[:20]}"