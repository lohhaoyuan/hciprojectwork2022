from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class User(AbstractUser):
    hciclass = models.CharField(max_length=3, null=False, blank=False)
    bio = models.CharField(max_length=500, null=True, blank=True)
    