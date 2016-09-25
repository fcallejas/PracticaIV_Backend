from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm, PasswordInput


class LoginForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput())


class SignUpForm(ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        labels = {
            'first_name': "Nombre",
            'last_name': "Apellidos",
            'email': "Correo electrónico",
            'username': "Nombre de usuario",
            'password': "Contraseña"
        }
        help_texts = {
            'username': ''
        }
        widgets = {
            'password': PasswordInput()
        }
