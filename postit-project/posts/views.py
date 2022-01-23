from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # override this built-in function to get user
    # currently logged in and put him as the poster
    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)
