from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .models import Post, Vote
from .serializers import PostSerializer, VoteSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # override this built-in function to get user
    # currently logged in and put him as the poster
    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)


class VoteCreate(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permissions_class = [permissions.IsAuthenticated]

    # handle upvote
    def get_queryset(self):
        # grab the user
        user = self.request.user
        # grab the post from db
        post = Post.objects.get(pk=self.kwargs['pk'])
        # fetch a vote object for this user, post combination
        return Vote.objects.filter(voter=user, post=post)

    # override this built-in function to get user
    # currently logged in and put him as the poster
    def perform_create(self, serializer):
        # if query_set returns a Vote object - user has already voted
        if self.get_queryset().exists():
            raise ValidationError('You have already voted for this post!')
        # else save the vote
        serializer.save(voter=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))