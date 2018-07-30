from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, MultiPartParser
from django.contrib.auth.models import User
from crud_project.models import Post, Profile
from crud_project.serializers import PostSerializer, UserSerializer, ProfileSerializer
from django.conf import settings


POSTS_PER_PAGE = 5


@api_view(['GET', 'POST'])
@permission_classes((permissions.IsAuthenticated,))
def post_list(request):
    """
    List all code posts, or create a new post.
    """
    if request.method == 'GET':
        page = int(request.GET.get('page'))
        op = request.GET.get('original_poster')
        posts = Post.objects.all()
        if op:
            posts = posts.filter(**{'original_poster': op})
        number_of_posts = len(posts)
        posts = posts[POSTS_PER_PAGE * page - POSTS_PER_PAGE:POSTS_PER_PAGE * page]
        serializer = PostSerializer(posts, many=True)

        return Response({'allPosts': serializer.data, 'numberOfPosts': number_of_posts})

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def post_detail(request, pk):
    """
    Retrieve, update or delete a post.
    """
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def register_user(request):
    """
    Registering a user
    """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        new_user = ProfileSerializer(data=request.data)

        if new_user.is_valid():
            new_user.save()
            return Response(new_user.data, status=status.HTTP_201_CREATED)
        return Response(new_user.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PATCH'])
@permission_classes((permissions.IsAuthenticated,))
def update_user_profile(request, username):
    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FileUploadParser, )
    permission_classes = (permissions.AllowAny,)

    def post(self, request, username):
        up_file = request.data['image']
        destination = open(settings.MEDIA_ROOT + 'images/' + up_file.name, 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)
            destination.close()

        return Response(up_file.name, status.HTTP_201_CREATED)


class ProfileUpdateView(UpdateAPIView):

    permission_classes = (permissions.AllowAny,)

    def get_object(self, username):
        user = User.objects.filter(username=username)
        profile = Profile.objects.get(user=user[0])
        return profile

    def patch(self, request, username):
        profile = self.get_object(username)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

