from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView, SetPasswordForm
from django.views.generic import CreateView, TemplateView, FormView
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm


class UserCreateView(SuccessMessageMixin, CreateView):
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


class AccountView(LoginRequiredMixin, AccessMixin, TemplateView):
    template_name = 'users/account.html'
    model = User


class ProfileView(LoginRequiredMixin, AccessMixin, FormView):
    template_name = 'users/profile.html'
    model = User

    def get(self, request, *args, **kwargs):
        user = request.user
        form = UserUpdateForm(instance=request.user)
        context = {'form': form, 'user': user}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()

        context = {'form': form}

        return render(request, self.template_name, context)

    def get_success_url(self):
        return reverse('account')


class AccountChangePassword(LoginRequiredMixin, AccessMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    model = User
    form_class = SetPasswordForm

    def get_success_url(self):
        return reverse('account')
