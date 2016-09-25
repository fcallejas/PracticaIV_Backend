from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from users.api import UserViewSet, BlogViewSet
from users.views import LoginView, LogoutView, BlogListView, SignUpView

router = DefaultRouter()
router.register('api/1.0/users', UserViewSet, base_name='api_users_')
router.register('api/1.0/blogs', BlogViewSet, base_name='api_blogs_')

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='user_login'),
    url(r'^signup/$', SignUpView.as_view(), name='user_sign_up'),
    url(r'^logout/$', LogoutView.as_view(), name='user_logout'),
    url(r'^blogs/$', BlogListView.as_view(), name='blog_list'),

    # API URLS
    url(r'', include(router.urls))
]
