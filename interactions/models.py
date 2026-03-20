from django.db import models
from accounts.models import User
from resources.models import Resource

# Create your models here.
class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    resource =models.ForeignKey(Resource,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','resource') # So that a user can not like twice in a resource

    def __str__(self):
            return f"{self.user} liked {self.resource}"

class Bookmark(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    resource =models.ForeignKey(Resource,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user','resource') # So that a user can not bookmark twice in a resource

   
    def __str__(self):
            return f"{self.user} bookmarked {self.resource}"


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    resource =models.ForeignKey(Resource,on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

  
    def __str__(self):
            return f"{self.user} - {self.content[:30]}"
