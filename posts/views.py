import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView

from posts.forms import PostCreationForm
from posts.models import Post, VISIBILITY_PUBLIC


class HomeView(ListView):

    queryset = Post.objects.all().filter(visibility=VISIBILITY_PUBLIC).order_by('-created_at')
    context_object_name = 'post_list'
    template_name = 'posts/home.html'


class PostDetailView(View):

    def get(self, request, username, pk):
        """
        Renderiza el detalle de un post
        :param request: objeto HttpRequest
        :param username: nombre de usuario
        :param pk: clave primaria
        :return: HttpResponse con la plantilla
        """
        queryset = PostQueryset.get_posts_by_user(request.user).filter(owner__username=username, pk=pk)
        if len(queryset) == 0:
            return HttpResponseNotFound("El post que buscas no existe")
        elif len(queryset) > 1:
            return HttpResponse("Múltiples opciones", status=300)

        post = queryset[0]
        context = {'post': post}
        return render(request, 'posts/post_detail.html', context)


class PostCreationView(View):

    @method_decorator(login_required())
    def get(self, request):
        """
        Presenta el formulario para crear un post y, en caso de que la petición sea POST la valida
        y la crea en caso de que sea válida
        :param request: objeto HttpRequest con los datos de la petición
        :return: HttpResponse con la plantilla
        """
        message = None
        photo_form = PostCreationForm()
        context = {'form': photo_form, 'message': message}
        return render(request, 'posts/post_creation.html', context)

    @method_decorator(login_required())
    def post(self, request):
        """
        Presenta el formulario para crear un post
        :param request: objeto HttpRequest con los datos de la petición
        :return: HttpResponse con la plantilla
        """
        message = None
        post_with_user = Post(owner=request.user)
        post_form = PostCreationForm(request.POST, instance=post_with_user)
        if post_form.is_valid():
            new_post = post_form.save()
            post_form = PostCreationForm()
            message = "Post creado satisfactoriamente. <a href='{0}'>Ver post</a>".format(
                reverse('post_detail', args=(new_post.owner.username, new_post.pk))
            )

        context = {'form': post_form, 'message': message}
        return render(request, 'posts/post_creation.html', context)


class PostListView(View):

    def get(self, request, username):
        """
        Renderiza el detalle de un post
        :param request: objeto HttpRequest
        :param username: nombre de usuario
        :return: HttpResponse con la plantilla
        """
        queryset = PostQueryset.get_posts_by_user(request.user).filter(owner__username=username).order_by('-created_at')
        context = {'post_list': queryset}
        return render(request, 'posts/post_list.html', context)


class PostQueryset(object):

    @staticmethod
    def get_posts_by_user(user):
        post_queryset = Post.objects.all().select_related('owner')
        if not user.is_authenticated():
            post_queryset = post_queryset.filter(Q(visibility=VISIBILITY_PUBLIC) & Q(publicate_at__lte=datetime.datetime.now()))
        elif not user.is_superuser:
            post_queryset = post_queryset.filter(Q(visibility=VISIBILITY_PUBLIC) | Q(owner=user))
        return post_queryset
