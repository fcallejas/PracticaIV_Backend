from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_202_ACCEPTED, HTTP_204_NO_CONTENT
from rest_framework.viewsets import ViewSet

from users.permissions import UserPermission
from users.serializers import UserSerializer, UserListSerializer, BlogListSerializer


class UserViewSet(ViewSet):
    """
    Endpoint de listado de usuarios
    """
    permission_classes = (UserPermission,)

    def list(self, request):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        if request.user.is_superuser or (request.user.is_authenticated and user.pk == request.user.pk):
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        if request.user.is_superuser or (request.user.is_authenticated and user.pk == request.user.pk):
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        if request.user.is_superuser or (request.user.is_authenticated and user.pk == request.user.pk):
            user.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class BlogViewSet(ViewSet):

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get('q', None)
        if username is not None:
            queryset = queryset.filter(username__contains=username).order_by('username')
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = BlogListSerializer(queryset, many=True)
        return Response(serializer.data)
