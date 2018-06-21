from rest_framework import serializers
from crud_project.models import Post
from django.contrib.auth.models import User
from rest_framework import validators


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'post_title', 'post_text', 'date_posted', 'original_poster')
        read_only_fields = ('date_posted',)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[validators.UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(required=True,
                                     validators=[validators.UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], email=validated_data['email'],
                                        password=validated_data['password'], first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name'])
        return user

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'email')
