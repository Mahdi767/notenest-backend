from django.db import models

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=200)
    course_code = models.CharField(max_length=15)
    department =  models.ForeignKey(Department,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course_code} - {self.title}"

class Semester(models.Model):
    name = models.CharField(max_length=50)
    year = models.IntegerField()
    is_active = models.BooleanField(default=False)  # Track if this is current semester
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.year}"
