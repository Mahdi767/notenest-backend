



from django.db import models
from . constant import RESOURCE_TYPE_CHOICES,STATUS_CHOICES
from accounts.models import User
from academic.models import Department,Semester,Course
from cloudinary.models import CloudinaryField
 
from .validators import validate_file_size,validate_file_type
# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.name
    
class Resource(models.Model):
    title =  models.CharField(max_length=255)
    description = models.TextField()
    file  =  CloudinaryField('file',folder='resources/',null=True,blank=True)
    tags = models.ManyToManyField(Tag,blank=True)
    uploaded_by =  models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    department =  models.ForeignKey(Department,on_delete=models.SET_NULL,null=True)
    course =  models.ForeignKey(Course,on_delete=models.SET_NULL,null=True)
    semester  = models.ForeignKey(Semester,on_delete=models.SET_NULL,null=True)
    resource_type = models.CharField(choices=RESOURCE_TYPE_CHOICES, max_length=20)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='pending')
    view_count = models.IntegerField(default=0)
    download_count = models.IntegerField(default=0)
    created_at =  models.DateTimeField(auto_now_add=True)
    updated_at =  models.DateTimeField(auto_now=True) # when user update his file, it will move again pending stage

    def __str__(self):
        return self.title

class ResourceView(models.Model):
    resource = models.ForeignKey(Resource,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ip_address = models.GenericIPAddressField(null=True)
    created_at =  models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('resource', 'user')