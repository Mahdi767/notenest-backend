from django.contrib import admin
from .models import User
# Register your models here.


class UserFullInfo(admin.ModelAdmin):
    list_display = ['first_name','last_name','email']
admin.site.register(User,UserFullInfo)