from django.urls import path
from users.views import AccountView, ProfileView, AccountChangePassword
from .views import add_to_cart, ShoppingCartView, increase_item, remove_from_cart, clear_cart, TypeOfUserView, \
    OrderBizCreateView, ConfirmOrderView, OrderBizUpdateView, FinalOrderView, OrderUserCreateView, OrderUserUpdateView

urlpatterns = [
    path('', AccountView.as_view(), name='account'),
    path('cart/add/<int:pk>/', add_to_cart, name='add-to-cart'),
    path('cart/increase/<int:pk>/', increase_item, name='increase-item'),
    path('cart/decrease/<int:pk>/', remove_from_cart, name='decrease-item'),
    path('cart/clear/', clear_cart, name='clear-cart'),
    path('pre-order/', TypeOfUserView.as_view(), name='type-of-user'),
    path('order-business/', OrderBizCreateView.as_view(), name='order-biz'),
    path('order-business/update/<int:pk>', OrderBizUpdateView.as_view(), name='order-biz-update'),
    path('order-user/', OrderUserCreateView.as_view(), name='order-user'),
    path('order-user/update/<int:pk>', OrderUserUpdateView.as_view(), name='order-user-update'),
    path('confirm-order/<int:pk>/', ConfirmOrderView.as_view(), name='confirm'),
    path('final-order/<int:pk>/', FinalOrderView.as_view(), name='finish'),
    path('cart/view/', ShoppingCartView.as_view(), name='view-cart'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/change-password/', AccountChangePassword.as_view(), name='change-password'),
]
