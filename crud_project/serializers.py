from rest_framework import serializers
from crud_project.models import Post
from rest_framework import validators


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'post_title', 'post_text', 'date_posted')
        read_only_fields = ('date_posted',)