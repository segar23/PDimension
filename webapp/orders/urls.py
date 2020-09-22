from django.urls import path
from users.views import AccountView, ProfileView, AccountChangePassword
from .views import add_to_cart, ShoppingCartView, increase_item, remove_from_cart, clear_cart

urlpatterns = [
    path('', AccountView.as_view(), name='account'),
    path('cart/add/<int:pk>/', add_to_cart, name='add-to-cart'),
    path('cart/increase/<int:pk>/', increase_item, name='increase-item'),
    path('cart/decrease/<int:pk>/', remove_from_cart, name='decrease-item'),
    path('cart/clear/', clear_cart, name='clear-cart'),
    path('cart/view/', ShoppingCartView.as_view(), name='view-cart'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/change-password/', AccountChangePassword.as_view(), name='change-password'),
]
