from django.db import models
from django.contrib.auth.models import AbstractUser
from .constants import ROLE_CHOICES
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="student"
    )

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email
