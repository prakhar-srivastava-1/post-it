from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    # set fields read-only
    # remember poster is a django.contrib.auth.models User object
    poster = serializers.ReadOnlyField(source='poster.username')
    poster_id = serializers.ReadOnlyField(source='poster.id')

    class Meta:
        model = Post
        fields = ['id', 'title', 'url', 'poster', 'poster_id', 'created']
