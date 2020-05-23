"""PDimension URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from landing import views as landing_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_views.LandingHome.as_view(), name='landing-page'),
    path('about/', landing_views.AboutUsView.as_view(), name='about-us'),
    path('location/', landing_views.LocationView.as_view(), name='location'),
    path('catalog/', landing_views.CatalogView.as_view(), name='catalog'),
    path('products/', include('products.urls')),
    path('register/', user_views.register, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
