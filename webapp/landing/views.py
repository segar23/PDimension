import re
from functools import reduce
from operator import or_ as OR
from django.db.models import Q
from django.views.generic import TemplateView, ListView
from control_panel.models import Product, Category
from orders.models import OrderItem


class LandingHome (TemplateView):
    template_name = 'landing/landing.html'


class AboutUsView (TemplateView):
    template_name = 'landing/about.html'


class LocationView (TemplateView):
    template_name = 'landing/location.html'


class CatalogView (ListView):
    template_name = 'landing/catalog.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 15

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['macro_categories'] = Category.objects.filter(isMacro=True)
        context['sub_categories'] = Category.objects.filter(isMacro=False)
        if self.request.user.is_authenticated:
            order_items = OrderItem.objects.filter(cart__user=self.request.user)
            context['order_items'] = order_items
            context['order_products'] = Product.objects.filter(orderitem__cart__products__in=order_items)
        return context

    def get_queryset(self):
        query = self.request.GET.get('search')
        cat = self.request.GET.get('cat')
        complete_set = Product.objects.all()

        if (query is None or query == '') and (cat is None):
            return complete_set
        elif cat is not None:
            return Product.objects.filter(macroCategories__name__icontains=cat)
        else:
            queryset_full = Product.objects.filter(name__icontains=query)
            if queryset_full.count() > 0:
                return queryset_full
            else:
                query = re.sub('( [Dd][Ee] )', ' ', query)
                query = reduce(OR, (Q(name__icontains=item) | Q(productsearchtag__name__icontains=item) for item in query.split()))
                queryset_partial = Product.objects.filter(query)
                return queryset_partial
