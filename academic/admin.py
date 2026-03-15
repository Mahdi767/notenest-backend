from django.contrib import admin
from . models import Course,Semester,Department
# Register your models here.
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Semester)
