from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Correo Electrónico', required=True,)
    username = forms.CharField(label='Nombre de Usuario', max_length=150,
                               help_text='Requerido. 150 caracteres o menos. Letras o dígitos solamente.')
    first_name = forms.CharField(label='Nombre', max_length=100, required=True)
    last_name = forms.CharField(label='Apellido', max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
