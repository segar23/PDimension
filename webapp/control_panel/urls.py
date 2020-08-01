from django.urls import path
from .views import ControlPanelView, CategoriesView, CategoriesCreateView, CategoriesDeleteView, \
    CategoriesUpdateView, ProductsView, ProductsCreateView, PostsDetailView, ProductsUpdateView, ProductsDeleteView, \
    ProductVariantCreateView, ProductVariantDeleteView


urlpatterns = [
    path('', ControlPanelView.as_view(), name='control-panel'),
    path('products/', ProductsView.as_view(), name='products'),
    path('products/new/', ProductsCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/', PostsDetailView.as_view(), name='product-detail'),
    path('products/subType/new/', ProductVariantCreateView.as_view(), name='productvariant-create'),
    path('products/subType/<int:pk>/delete/', ProductVariantDeleteView.as_view(), name='productvariant-delete'),
    path('products/<int:pk>/update/', ProductsUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductsDeleteView.as_view(), name='product-delete'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('categories/new/', CategoriesCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/delete/', CategoriesDeleteView.as_view(), name='category-delete'),
    path('categories/<int:pk>/update/', CategoriesUpdateView.as_view(), name='category-update'),
]
