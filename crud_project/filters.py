from django_filters import rest_framework as filters
from crud_project.models import Post


class PostFilter(filters.FilterSet):
    class Meta:
        model = Post
        fields = ('original_poster',)
