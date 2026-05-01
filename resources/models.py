
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
    updated_at =  models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Reset status to pending if an approved resource is edited by non-staff user
        # Only apply if this is an update (not a new resource)
        if self.pk:
            update_fields = kwargs.get('update_fields')
            
            # Core fields that should trigger a status reset if modified
            core_fields = {
                'title', 'description', 'file', 'resource_type', 
                'department', 'course', 'semester',
                'department_id', 'course_id', 'semester_id'
            }
            
            # Check if any core fields are being updated
            should_check_content = True
            if update_fields is not None:
                # If update_fields is provided, only check content if it contains core fields
                should_check_content = any(field in update_fields for field in core_fields)
            
            if should_check_content:
                try:
                    original = Resource.objects.get(pk=self.pk)
                    # Only reset status if content actually changed, not auto-increment fields
                    if original.status == 'approved' and self.uploaded_by and not self.uploaded_by.is_staff:
                        # Check if any content fields were actually modified
                        # Use str() for file comparison as CloudinaryField objects might differ
                        content_changed = (
                            original.title != self.title or
                            original.description != self.description or
                            str(original.file) != str(self.file) or
                            original.resource_type != self.resource_type or
                            original.department_id != self.department_id or
                            original.course_id != self.course_id or
                            original.semester_id != self.semester_id
                        )
                        if content_changed:
                            self.status = 'pending'
                            # If update_fields is present, ensure 'status' is included so it gets saved
                            if update_fields is not None:
                                update_fields = set(update_fields)
                                if 'status' not in update_fields:
                                    update_fields.add('status')
                                    kwargs['update_fields'] = list(update_fields)
                except Resource.DoesNotExist:
                    pass
        super().save(*args, **kwargs)

class ResourceView(models.Model):
    resource = models.ForeignKey(Resource,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ip_address = models.GenericIPAddressField(null=True)
    created_at =  models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('resource', 'user')