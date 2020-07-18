from django import forms
from django.forms import ModelForm
from .models import Category


class CategoryCreateForm (ModelForm):
    name = forms.CharField(label='Nombre', required=True, error_messages={'unique': 'Esta categoría ya existe'})
    isMacro = forms.BooleanField(label='Es Macro-Categoría?', required=False)

    class Meta:
        model = Category
        fields = ['name', 'isMacro']
