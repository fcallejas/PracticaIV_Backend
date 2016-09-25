# -*- coding: utf-8 -*-
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from posts.serializers import PostSerializer, PostListSerializer
from posts.views import PostQueryset

class PostViewSet(ModelViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)
    search_fields = ('title', 'body',)
    order_fields = ('title', 'created_at')
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)

    def get_queryset(self):
        return PostQueryset.get_posts_by_user(self.request.user)

    def get_serializer_class(self):
        return PostSerializer if self.action != 'list' else PostListSerializer

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        return serializer.save(owner=self.request.user)

    def perform_destroy(self, serializer):
        return serializer.delete()
