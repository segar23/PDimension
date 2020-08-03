from decimal import Decimal

from django import forms
from django.forms import ModelForm
from .models import Category, Product, ProductVariant


class CategoryCreateForm (ModelForm):
    name = forms.CharField(label='Nombre', required=True, error_messages={'unique': 'Esta categoría ya existe'})
    isMacro = forms.BooleanField(label='Es Macro-Categoría?', required=False)

    def clean_name(self):
        name = self.cleaned_data['name'].title()
        return name

    class Meta:
        model = Category
        fields = ['name', 'isMacro']


class ProductCreateForm (ModelForm):
    picture = forms.ImageField(label='Imagen:', required=True)
    name = forms.CharField(label='Nombre del Producto:', required=True)
    sku = forms.IntegerField(label='SKU:', required=True, error_messages={'unique': 'Este SKU ya existe'})
    price = forms.DecimalField(label='Precio', max_digits=8, min_value=Decimal('1'), required=True,
                               error_messages={'min_value': 'El Precio no puede ser negativo'})
    description = forms.CharField(label='Descripción:', widget=forms.Textarea)
    isReference = forms.BooleanField(label='Es Imagen de Referencia?', required=False)
    macroCategories = forms.ModelMultipleChoiceField(label='Macro-Categorías:',widget=forms.CheckboxSelectMultiple,
                                                     required=False, queryset=Category.objects.filter(isMacro=True))
    subCategories = forms.ModelMultipleChoiceField(label='Sub-Categorías:', widget=forms.CheckboxSelectMultiple,
                                                   required=False, queryset=Category.objects.filter(isMacro=False))

    def clean_name(self):
        name = self.cleaned_data['name'].title()
        return name

    def clean_description(self):
        description = self.cleaned_data['description'].capitalize()
        return description

    class Meta:
        model = Product
        fields = ['picture', 'name', 'sku', 'price', 'description', 'isReference', 'macroCategories', 'subCategories']


class ProductVariantForm (ModelForm):
    name = forms.CharField(label='Nombre del Sub-Tipo:', required=True)

    def clean_name(self):
        name = self.cleaned_data['name'].title()
        return name

    class Meta:
        model = ProductVariant
        fields = ['name']
