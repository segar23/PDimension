from django.urls import path
from .views import ControlPanelView, CategoriesView, CategoriesCreateView, CategoriesDeleteView, CategoriesUpdateView


urlpatterns = [
    path('', ControlPanelView.as_view(), name='control-panel'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('categories/new/', CategoriesCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/delete/', CategoriesDeleteView.as_view(), name='category-delete'),
    path('categories/<int:pk>/update/', CategoriesUpdateView.as_view(), name='category-update'),
]
