from django.contrib import admin
from django.db import models
from . models import Tag,Resource
# Register your models here.
class ResourceDetails(admin.ModelAdmin):
    list_display = ['title','uploaded_by','department','course']

admin.site.register(Tag)
admin.site.register(Resource,ResourceDetails)


