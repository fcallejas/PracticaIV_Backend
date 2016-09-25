from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from posts.api import PostViewSet
from posts.views import PostCreationView, PostDetailView, PostListView

router = DefaultRouter()
router.register('api/1.0/posts', PostViewSet, base_name='api_post')

urlpatterns = [
    url(r'^new-post/$', PostCreationView.as_view(), name='post_creation'),
    url(r'^blogs/(?P<username>\w+)/$', PostListView.as_view(), name='post_list'),
    url(r'^blogs/(?P<username>\w+)/(?P<pk>\d+)$', PostDetailView.as_view(), name='post_detail'),

    url(r'', include(router.urls))
]
