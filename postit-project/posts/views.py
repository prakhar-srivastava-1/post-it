from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
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


# deleting posts
class PostRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    # function to delete one's own post only
    def delete(self, request, *args, **kwargs):
        # grab the post if its created by current user
        post = Post.objects.filter(pk=kwargs['pk'], poster=self.request.user)
        if post.exists():
            # delete the post
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('This isn\'t your post to delete!')


# use mixins for deleting votes - added later
class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
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

    # delete your vote if it exists
    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You never voted for this post!')
