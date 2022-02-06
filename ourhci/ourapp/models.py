from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class User(AbstractUser):

    hciclass = models.CharField(max_length=3, null=False, blank=False)
    bio = models.TextField(max_length=500, null=True, blank=True)
    reputation = models.IntegerField(null=False, blank=False, default=100)
    email = models.EmailField(null=False, max_length=26, blank=False)