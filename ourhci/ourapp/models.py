from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class User(AbstractUser):
    hciclass = models.CharField(max_length=3, null=False, blank=False)
    consortium = models.CharField(max_length=8, null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    reputation = models.IntegerField(null=False, blank=False, default=100)
    email = models.EmailField(null=False, max_length=26, blank=False)
    reputation_multiplier = models.IntegerField(default = 1)
    darkModeOn = models.BooleanField(default=True)
    name_colour = models.CharField(max_length=7, default="#000000")

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=False)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    # image = models.ImageField(upload_to="uploads/images", blank=True)

class UserFollow(models.Model):
    follower = models.ForeignKey(User, related_name = "follower", on_delete = models.CASCADE)
    following = models.ForeignKey(User, related_name = "following", on_delete = models.CASCADE)

class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    commented_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_content = models.TextField(null=False)