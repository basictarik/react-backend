from django.db import models
from datetime import datetime


class NormalTextField(models.TextField):
    def db_type(self, connection):
        return 'text'


class Post(models.Model):
    post_title = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True, blank=True)
    post_text = NormalTextField(default="Message Deleted")

    class Meta:
        ordering = ('date_posted',)
