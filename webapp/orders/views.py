from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from control_panel.models import Product
from .models import Cart, OrderItem


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


class ShoppingCartView(ListView):
    template_name = 'orders/shopping-cart.html'
    model = OrderItem
    context_object_name = 'items'
    paginate_by = 15

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = OrderItem.objects.filter(cart__user=self.request.user)
        return context
        #
        # def get_queryset(self):
        #     query = self.request.GET.get('search')
        #     cat = self.request.GET.get('cat')
        #     complete_set = Product.objects.all()
        #
        #     if (query is None or query == '') and (cat is None):
        #         return complete_set
        #     elif cat is not None:
        #         return Product.objects.filter(macroCategories__name__icontains=cat)
        #     else:
        #         query = reduce(OR, (Q(name__icontains=item) | Q(productsearchtag__name__icontains=item) for item in
        #                             query.split()))
        #         return Product.objects.filter(query)
