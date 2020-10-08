from django.urls import path
from .views import ControlPanelView, CategoriesView, CategoriesCreateView, CategoriesDeleteView, \
    CategoriesUpdateView, ProductsView, ProductsCreateView, PostsDetailView, ProductsUpdateView, ProductsDeleteView, \
    ProductVariantCreateView, ProductVariantDeleteView, ProductSearchTagCreateView, ProductSearchTagDeleteView, \
    OrdersView, OrdersViewDetails, OrderProductsEdit, increase_item, remove_from_cart, OderInfoEdit, set_facturada, \
    set_closed


urlpatterns = [
    path('', ControlPanelView.as_view(), name='control-panel'),
    path('products/', ProductsView.as_view(), name='products'),
    path('products/new/', ProductsCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/', PostsDetailView.as_view(), name='product-detail'),
    path('products/subType/new/', ProductVariantCreateView.as_view(), name='productvariant-create'),
    path('products/subType/<int:pk>/delete/', ProductVariantDeleteView.as_view(), name='productvariant-delete'),
    path('products/tag/new/', ProductSearchTagCreateView.as_view(), name='productsearchtag-create'),
    path('products/tag/<int:pk>/delete/', ProductSearchTagDeleteView.as_view(), name='productsearchtag-delete'),
    path('products/<int:pk>/update/', ProductsUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductsDeleteView.as_view(), name='product-delete'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('categories/new/', CategoriesCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/delete/', CategoriesDeleteView.as_view(), name='category-delete'),
    path('categories/<int:pk>/update/', CategoriesUpdateView.as_view(), name='category-update'),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('orders/<int:pk>/view/', OrdersViewDetails.as_view(), name='order-details'),
    path('orders/<int:pk>/bill/', set_facturada, name='order-bill'),
    path('orders/<int:pk>/close/', set_closed, name='order-close'),
    path('orders/<int:pk>/edit-products/', OrderProductsEdit.as_view(), name='order-products-edit'),
    path('orders/<int:pk>/edit-info/', OderInfoEdit.as_view(), name='order-info-edit'),
    path('orders/<int:pkor>/edit-products/increase/<int:pkit>/', increase_item, name='order-products-edit-increase'),
    path('orders/<int:pkor>/edit-products/decrease/<int:pkit>/', remove_from_cart, name='order-products-edit-decrease'),
]
