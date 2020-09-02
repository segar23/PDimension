from django.urls import path
from users.views import AccountView, ProfileView, AccountChangePassword

urlpatterns = [
    path('', AccountView.as_view(), name='account'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/change-password/', AccountChangePassword.as_view(), name='change-password'),
]
