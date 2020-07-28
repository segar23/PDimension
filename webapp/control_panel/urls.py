from django.urls import path
from .views import ControlPanelView, CategoriesView, CategoriesCreateView, CategoriesDeleteView, \
    CategoriesUpdateView, ProductsView, ProductsCreateView


urlpatterns = [
    path('', ControlPanelView.as_view(), name='control-panel'),
    path('products/', ProductsView.as_view(), name='products'),
    path('products/new/', ProductsCreateView.as_view(), name='product-create'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('categories/new/', CategoriesCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/delete/', CategoriesDeleteView.as_view(), name='category-delete'),
    path('categories/<int:pk>/update/', CategoriesUpdateView.as_view(), name='category-update'),
]
