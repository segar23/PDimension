from django.urls import path
from users.views import AccountView, ProfileView, AccountChangePassword
from .views import add_to_cart, ShoppingCartView

urlpatterns = [
    path('', AccountView.as_view(), name='account'),
    path('cart/add/<int:pk>', add_to_cart, name='add-to-cart'),
    path('cart/view', ShoppingCartView.as_view(), name='view-cart'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/change-password/', AccountChangePassword.as_view(), name='change-password'),
]
