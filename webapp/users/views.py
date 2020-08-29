from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from .forms import UserRegisterForm, UserLoginForm


class UserCreateView (SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    model = User
    form_class = UserRegisterForm
    context_object_name = 'user'
    success_message = 'Tu cuenta ha sido creada exitosamente!'

    def get_success_url(self):
        return reverse('login')


class LoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
