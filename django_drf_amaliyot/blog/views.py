from django.db import IntegrityError
from .models import Post
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .serializer import PostSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.views.decorators.cache import cache_page
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    created_by = request.user

    try:
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=created_by)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response([e])


class PostListApiView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ['id', 'title', 'created_at']
    search_fields = ['title', "created_at"]


@api_view(['GET'])
def get_post(request, pk):

    try:
        post = Post.objects.get(pk=pk)

    except Post.DoesNotFound:
        return Response({"message": " Post Not Found"})

    serializer = PostSerializer(post)

    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_post(request, pk):

    try:
        post = Post.objects.get(pk=pk, created_by=request.user)

    except Post.DoesNotExist:
        return Response({"error": "Post Not Found.!"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PostSerializer(post, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, pk):

    try:
        post = Post.objects.get(pk=pk, created_by=request.user)
        post.delete()

        return Response({"message": "Post Successfully Deleted.!"})

    except Post.DoesNotExist:
        return Response({"error": "Post Not Found.!"}, status=status.HTTP_404_NOT_FOUND)






