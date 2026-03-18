from django.contrib import admin
from django.db import models
from . models import Tag,Resource
# Register your models here.
class ResourceDetails(admin.ModelAdmin):
    list_display = ['title','get_uploaded_by_name','department','course']

    def get_uploaded_by_name(self,obj):
        if obj.uploaded_by:
            return f"{obj.uploaded_by.first_name} {obj.uploaded_by.last_name}"
        return "Deleted User"
    get_uploaded_by_name.short_description = 'Uploaded By'

admin.site.register(Tag)
admin.site.register(Resource,ResourceDetails)


