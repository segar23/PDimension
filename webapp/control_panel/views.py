from django.contrib.auth.decorators import login_required
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
from orders.forms import OrderBizCreateForm, OrderUserCreateForm
from orders.models import Order, OrderItem
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


class OrdersView(LoginRequiredMixin, UserPassesTestMixin, AccessMixin, ListView):
    model = Order
    template_name = 'control_panel/orders.html'
    context_object_name = 'orders'
    unread = True
    active = False
    closed = False

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        queryset = Order.objects.filter(isFinalized=True).order_by('-created')
        st = self.request.GET.get('st')
        if st == 'unread' or st is None:
            return queryset.filter(status=Order.OrderStatus.UNREAD)
        elif st == 'active':
            self.unread = False
            self.active = True
            return queryset.filter(Q(status=Order.OrderStatus.OPEN) | Q(status=Order.OrderStatus.FACTURADA))
        elif st == 'closed':
            self.unread = False
            self.closed = True
            return queryset.filter(status=Order.OrderStatus.CLOSED)
        else:
            return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unread'] = self.unread
        context['active'] = self.active
        context['closed'] = self.closed
        return context


class OrdersViewDetails(LoginRequiredMixin, UserPassesTestMixin, AccessMixin, ListView):
    model = OrderItem
    template_name = 'control_panel/order-panel.html'
    context_object_name = 'items'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        order = Order.objects.get(id=self.kwargs.get('pk'))
        queryset = order.products.all().order_by('product__name')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.get(id=self.kwargs.get('pk'))
        if order.status == Order.OrderStatus.UNREAD:
            order.status = Order.OrderStatus.OPEN
            order.save()
        context['order'] = order
        return context


class OrderProductsEdit(LoginRequiredMixin, UserPassesTestMixin, AccessMixin, ListView):
    Model = OrderItem
    template_name = 'control_panel/order-products-edit.html'
    context_object_name = 'items'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        order = Order.objects.get(id=self.kwargs.get('pk'))
        queryset = order.products.all().order_by('product__name')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.get(id=self.kwargs.get('pk'))
        order.get_total_order()
        order.save()
        context['order'] = order
        return context


@login_required
def increase_item(request, pkor, pkit):
    product = Product.objects.get(id=pkit)
    order = Order.objects.get(id=pkor)
    order_item = order.products.get(product=product)
    order_item.quantity += 1
    order_item.save()
    order.save()
    return redirect('order-products-edit', pk=order.id)


@login_required
def remove_from_cart(request, pkor, pkit):
    product = Product.objects.get(id=pkit)
    order = Order.objects.get(id=pkor)
    order_item = order.products.get(product=product)
    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
        order.save()
    else:
        order_item.delete()
        order.save()
    return redirect('order-products-edit', pk=order.id)


class OderInfoEdit(LoginRequiredMixin, UserPassesTestMixin, AccessMixin, UpdateView):
    Model = Order
    context_object_name = 'order'
    template_name = 'control_panel/order-info-edit.html'

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        o_num = self.kwargs.get('pk')
        order = Order.objects.get(id=o_num)
        if order.isBusinessUser:
            form = OrderBizCreateForm(instance=order)
        else:
            form = OrderUserCreateForm(instance=order)
        context = {'form': form, 'order': order}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        o_num = self.kwargs.get('pk')
        order = Order.objects.get(id=o_num)
        if order.isBusinessUser:
            form = OrderBizCreateForm(request.POST, instance=order)
        else:
            form = OrderUserCreateForm(request.POST, instance=order)

        if form.is_valid():
            if 'city' in form.changed_data:
                order.adjust_shipping()
                order.save()
            form.save()
            messages.success(self.request, f'La información ha sido actualizada!')

        context = {'form': form, 'order': order}
        return render(request, self.template_name, context)

    def get_success_url(self):
        return reverse('order-details', kwargs={'pk': self.object.id})


@login_required
def set_facturada(request, pk):
    order = Order.objects.get(id=pk)
    order.status = Order.OrderStatus.FACTURADA
    order.save()
    return redirect('order-details', pk=order.id)


@login_required
def set_closed(request, pk):
    order = Order.objects.get(id=pk)
    order.status = Order.OrderStatus.CLOSED
    order.save()
    return redirect('orders')
