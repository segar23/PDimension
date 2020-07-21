from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Category
from .forms import CategoryCreateForm


class ControlPanelView (LoginRequiredMixin, UserPassesTestMixin, AccessMixin, TemplateView):
    template_name = 'control_panel/control_panel.html'
    model = User

    def test_func(self):
        return self.request.user.is_staff


class CategoriesView (LoginRequiredMixin, UserPassesTestMixin, AccessMixin, ListView):
    model = Category
    template_name = 'control_panel/categories.html'
    context_object_name = 'categories'
    ordering = ['name']

    def test_func(self):
        return self.request.user.is_staff


class CategoriesCreateView (LoginRequiredMixin, AccessMixin, CreateView):
    model = Category
    form_class = CategoryCreateForm
    context_object_name = 'category'

    def get_success_url(self):
        return reverse('categories')


class CategoriesDeleteView (LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse('categories')


class CategoriesUpdateView (LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['name', 'isMacro']

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse('categories')
