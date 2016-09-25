from rest_framework import serializers
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post


class PostListSerializer(PostSerializer):

    class Meta(PostSerializer.Meta):
        fields = ("title", "intro", "media_url", "publicate_at")

