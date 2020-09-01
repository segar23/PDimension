from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuario:', required=False)
    password = forms.CharField(label='Contraseña:', widget=forms.PasswordInput, required=False)

    error_messages = {
        'invalid_login': 'Nombre de usuario o contraseña son incorrectos',
        'inactive': 'Esta cuenta se encuentra inactiva',
    }

    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Correo Electrónico', required=True)
    first_name = forms.CharField(label='Nombre', required=True)
    last_name = forms.CharField(label='Apellido', required=True)
    username = forms.CharField(label='Nombre de Usuario', required=True,
                               error_messages={'unique': 'Este Nombre de Usuario ya existe'})

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name'].title()
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name'].title()
        return last_name

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        return username

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class UserUpdateForm (forms.ModelForm):
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name'].title()
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name'].title()
        return last_name

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
