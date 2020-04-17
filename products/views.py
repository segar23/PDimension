from django.shortcuts import render
from django.views.generic import ListView
from .models import Product


def home(request):
    return render(request, 'products/home.html')


class ProductsListView(ListView):
    model = Product
    paginate_by = 20
