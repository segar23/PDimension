from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import ListView, TemplateView, CreateView, UpdateView
from control_panel.models import Product
from .models import Cart, OrderItem, Order
from .forms import OrderBizCreateForm, OrderUserCreateForm


@login_required
def add_to_cart(request, pk):
    product = Product.objects.get(id=pk)
    cart = None
    try:
        cart = request.user.cart
    except:
        cart = Cart(user=request.user)
        cart.save()
    finally:
        if cart.products.filter(product__exact=product).exists():
            order_item = cart.products.get(product=product)
            order_item.quantity += 1
            order_item.save()
            cart.save()
        else:
            order_item = OrderItem(product=product, quantity=1)
            order_item.save()
            cart.products.add(order_item)
        return redirect('catalog')


@login_required
def increase_item(request, pk):
    product = Product.objects.get(id=pk)
    cart = request.user.cart
    order_item = cart.products.get(product=product)
    order_item.quantity += 1
    order_item.save()
    cart.save()
    return redirect('view-cart')


@login_required
def remove_from_cart(request, pk):
    product = Product.objects.get(id=pk)
    cart = request.user.cart
    order_item = cart.products.get(product=product)
    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
        cart.save()
    else:
        order_item.delete()
        cart.save()
    return redirect('view-cart')


@login_required
def clear_cart(request):
    cart = request.user.cart
    cart.clear_cart()
    return redirect('view-cart')


class ShoppingCartView(LoginRequiredMixin, AccessMixin, ListView):
    template_name = 'orders/shopping-cart.html'
    model = OrderItem
    context_object_name = 'items'
    paginate_by = 10
    ordering = ['product__name']

    def get_queryset(self):
        queryset = OrderItem.objects.filter(cart__user=self.request.user)
        return queryset


class TypeOfUserView(LoginRequiredMixin, AccessMixin, TemplateView):
    template_name = 'orders/type-of-user.html'


class OrderBizCreateView(LoginRequiredMixin, AccessMixin, CreateView):
    model = Order
    form_class = OrderBizCreateForm
    context_object_name = 'order'

    def get_initial(self):
        initial = super().get_initial()
        initial['name'] = self.request.user.first_name + ' ' + self.request.user.last_name
        initial['email'] = self.request.user.email

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.request.user.cart

        return context

    def form_valid(self, form):
        cart = Cart.objects.get(user_id=self.request.user.id)
        form.instance.user = cart.user
        form.instance.isBusinessUser = True
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('confirm', kwargs={'pk': self.object.id})


class OrderBizUpdateView(LoginRequiredMixin, UserPassesTestMixin, AccessMixin, UpdateView):
    model = Order
    form_class = OrderBizCreateForm
    context_object_name = 'order'

    def test_func(self):
        current_order = Order.objects.get(id=self.kwargs.get('pk'))
        return current_order.user == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        o_num = self.kwargs.get('pk')
        order = Order.objects.get(id=o_num)
        context['form'] = OrderBizCreateForm(instance=order)

        return context

    def get_success_url(self):
        return reverse('confirm', kwargs={'pk': self.object.id})


class OrderUserCreateView(LoginRequiredMixin, AccessMixin, CreateView):
    model = Order
    form_class = OrderUserCreateForm
    context_object_name = 'order'

    def get_initial(self):
        initial = super().get_initial()
        initial['name'] = self.request.user.first_name + ' ' + self.request.user.last_name
        initial['email'] = self.request.user.email

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.request.user.cart

        return context

    def form_valid(self, form):
        cart = Cart.objects.get(user_id=self.request.user.id)
        form.instance.user = cart.user
        form.instance.isBusinessUser = False
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('confirm', kwargs={'pk': self.object.id})


class OrderUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, AccessMixin, UpdateView):
    model = Order
    form_class = OrderUserCreateForm
    context_object_name = 'order'

    def test_func(self):
        current_order = Order.objects.get(id=self.kwargs.get('pk'))
        return current_order.user == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        o_num = self.kwargs.get('pk')
        order = Order.objects.get(id=o_num)
        context['form'] = OrderUserCreateForm(instance=order)

        return context

    def get_success_url(self):
        return reverse('confirm', kwargs={'pk': self.object.id})


class ConfirmOrderView(LoginRequiredMixin, UserPassesTestMixin, AccessMixin, ListView):
    model = OrderItem
    template_name = 'orders/confirm-order.html'
    context_object_name = 'items'
    paginate_by = 10

    def test_func(self):
        current_order = Order.objects.get(id=self.kwargs.get('pk'))
        return current_order.user == self.request.user

    def get_queryset(self):
        cart = self.request.user.cart
        order = Order.objects.get(id=self.kwargs.get('pk'))
        order.products.set(cart.products.all())
        order.total = cart.get_total()
        order.adjust_shipping()
        order.save()
        queryset = order.products.all().order_by('product__name')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.get(id=self.kwargs.get('pk'))
        return context


class FinalOrderView(LoginRequiredMixin, AccessMixin, TemplateView):
    model = Order
    template_name = 'orders/final-order.html'

    def get_context_data(self, **kwargs):
        cart = self.request.user.cart
        cart.clear_cart()
        order = Order.objects.get(id=self.kwargs.get('pk'))
        order.isFinalized = True
        order.save()
        context = super().get_context_data(**kwargs)
        context['order'] = order
        return context


class MyOrdersView(LoginRequiredMixin, AccessMixin, ListView):
    model = Order
    template_name = 'orders/my-orders.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        queryset = Order.objects.filter(user__exact=self.request.user).order_by('-created')
        return queryset


class MyOrderDetailsView(LoginRequiredMixin, UserPassesTestMixin, AccessMixin, ListView):
    model = OrderItem
    template_name = 'orders/order-detail.html'
    context_object_name = 'items'
    paginate_by = 10

    def test_func(self):
        current_order = Order.objects.get(id=self.kwargs.get('pk'))
        return current_order.user == self.request.user

    def get_queryset(self):
        order = Order.objects.get(id=self.kwargs.get('pk'))
        queryset = order.products.all().order_by('product__name')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.get(id=self.kwargs.get('pk'))
        return context
