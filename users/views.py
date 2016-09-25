from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password, MinimumLengthValidator
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from users.forms import LoginForm, SignUpForm


class LoginView(View):

    def get(self, request):
        """
        Presenta el formulario de login
        :param request: objeto HttpRequest con los datos de la petición
        :return: HttpResponse con la plantilla
        """
        error_message = ""
        login_form = LoginForm()
        context = {'error': error_message, 'form': login_form}
        return render(request, 'users/login.html', context)

    def post(self, request):
        """
        Gestiona el login de un usuario
        :param request: objeto HttpRequest con los datos de la petición
        :return: HttpResponse con la plantilla
        """
        error_message = ""
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is None:
                error_message = "Nombre de usuario o contraseña incorrecto"
            else:
                if user.is_active:
                    django_login(request, user)
                    return redirect(request.GET.get('next', 'post_home'))
                else:
                    error_message = "Cuenta de usuario inactiva"

        context = {'error': error_message, 'form': login_form}
        return render(request, 'users/login.html', context)


class LogoutView(View):

    def get(self, request):
        """
        Hace el logout de un usuario y redirige al login
        :param request: objeto HttpRequest con los datos de la petición
        :return: HttpResponse con la plantilla
        """
        if request.user.is_authenticated():
            django_logout(request)
        return redirect("post_home")


class SignUpView(View):

    def get(self, request):
        """
        Presenta el formulario de registro
        :param request: objeto HttpRequest con los datos de la petición
        :return: HttpResponse con la plantilla
        """
        form = SignUpForm()
        context = {'message': "", 'form': form}
        return render(request, 'users/sign_up.html', context)

    def post(self, request):
        """
        Gestiona el registro de un usuario
        :param request: objeto HttpRequest con los datos de la petición
        :return: HttpResponse con la plantilla
        """
        error_message = ""
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            name = signup_form.cleaned_data.get('first_name')
            last_name = signup_form.cleaned_data.get('last_name')
            email = signup_form.cleaned_data.get('email')
            username = signup_form.cleaned_data.get('username')
            password = signup_form.cleaned_data.get('password')

            try:
                validate_password(password, User)
                user = User.objects.create_user(username, email, password)
                user.first_name = name
                user.last_name = last_name
                user.save()

                if user.is_authenticated:
                    return redirect(request.GET.get('next', reverse('post_list', args={user.username})))

            except ValidationError as errors:
                error_message = '\n'.join(errors)

        context = {'message': error_message, 'form': signup_form}
        return render(request, 'users/sign_up.html', context)


class BlogListView(ListView):
    model = User
    context_object_name = "blog_list"
    template_name = "users/blog_list.html"
