from django.shortcuts import render, redirect
from functools import reduce
from operator import or_ as OR
from django.db.models import Q
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Category, Product, ProductVariant, ProductSearchTag
from .forms import CategoryCreateForm, ProductCreateForm, ProductVariantForm, ProductSearchTagForm


class ControlPanelView(LoginRequiredMixin, UserPassesTestMixin, AccessMixin, TemplateView):
    template_name = 'control_panel/control_panel.html'
    model = User

    def test_func(self):
        return self.request.user.is_staff


class ProductsView(LoginRequiredMixin, UserPassesTestMixin, AccessMixin, ListView):
    template_name = 'control_panel/products.html'
    model = Product
    context_object_name = 'products'
    ordering = ['name']
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        query = self.request.GET.get('search')
        complete_set = Product.objects.all()

        if query is None or query == '':
            return complete_set
        else:
            query = reduce(OR, (Q(name__icontains=item) | Q(sku__icontains=item) for item in query.split()))
            return Product.objects.filter(query)


class ProductsCreateView(LoginRequiredMixin, UserPassesTestMixin, AccessMixin, CreateView):
    model = Product
    form_class = ProductCreateForm
    context_object_name = 'product'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse('products')


class ProductVariantCreateView(LoginRequiredMixin, UserPassesTestMixin, AccessMixin, CreateView):
    model = ProductVariant
    form_class = ProductVariantForm
    context_object_name = 'productvariant'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.product = Product.objects.get(id=self.request.GET.get('id'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.request.GET.get('id')})


class ProductVariantDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ProductVariant

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.request.GET.get('id')})


class ProductSearchTagCreateView(LoginRequiredMixin, UserPassesTestMixin, AccessMixin, CreateView):
    model = ProductSearchTag
    form_class = ProductSearchTagForm
    context_object_name = 'productsearchtag'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.product = Product.objects.get(id=self.request.GET.get('id'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.request.GET.get('id')})


class ProductSearchTagDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ProductSearchTag

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.request.GET.get('id')})


class PostsDetailView(DetailView):
    model = Product


class ProductsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductCreateForm

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.object.pk})


class ProductsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse('products')

    @receiver(post_delete, sender=Product)
    def delete_image(sender, instance, using, **kwargs):
        instance.picture.delete(save=False)


class CategoriesView(LoginRequiredMixin, UserPassesTestMixin, AccessMixin, ListView):
    model = Category
    template_name = 'control_panel/categories.html'
    context_object_name = 'categories'
    ordering = ['name']
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_staff


class CategoriesCreateView(LoginRequiredMixin, AccessMixin, CreateView):
    model = Category
    form_class = CategoryCreateForm
    context_object_name = 'category'

    def get_success_url(self):
        return reverse('categories')


class CategoriesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse('categories')


class CategoriesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['name', 'isMacro']

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse('categories')
