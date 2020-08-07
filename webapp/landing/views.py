from functools import reduce
from operator import or_ as OR
from django.db.models import Q
from django.views.generic import TemplateView, ListView
from control_panel.models import Product


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

    def get_queryset(self):
        query = self.request.GET.get('search')
        complete_set = Product.objects.all()
        if query is None or query == '':
            return complete_set
        else:
            query = reduce(OR, (Q(name__icontains=item) | Q(description__icontains=item) for item in query.split()))
            return Product.objects.filter(query)
