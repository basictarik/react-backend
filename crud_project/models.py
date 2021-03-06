from django.db import models
from django.contrib.auth.models import User
import os


class NormalTextField(models.TextField):
    def db_type(self, connection):
        return 'text'


class Post(models.Model):
    post_title = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True, blank=True)
    post_text = NormalTextField(default="Message Deleted")
    original_poster = models.CharField(max_length=100, default="AnonymousUser")

    class Meta:
        ordering = ('date_posted',)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default='first_name')
    last_name = models.CharField(max_length=100, default='last_name')
    profile_image = models.ImageField(upload_to='images', default='no-image.jpg')
