from django import forms
from django.forms import ModelForm
from .models import Order


class OrderBizCreateForm(ModelForm):
    enterprise = forms.CharField(label='Razón Social:', required=True)
    person_id = forms.IntegerField(label='NIT:', required=True)
    verification_digit = forms.IntegerField(label='Dígito de Verificación:', required=True)
    address = forms.CharField(label='Dirección:', required=True)
    city = forms.ChoiceField(label='Ciudad:', required=True, choices=Order.CityChoices.choices)
    email = forms.EmailField(label='Correo:', required=True)
    name = forms.CharField(label='Nombre de Contacto:', required=True)
    phone = forms.CharField(label='Teléfono:', required=True)
    payment = forms.ChoiceField(label='Método de Pago:', required=True, widget=forms.RadioSelect,
                                choices=Order.PaymentMethod.choices)
    needsEReceipt = forms.BooleanField(label='Necesitas Facturación Electrónica?', required=False)
    comments = forms.CharField(label='Instrucciones Especiales:', required=False, widget=forms.Textarea)

    class Meta:
        model = Order
        fields = ['enterprise', 'person_id', 'verification_digit', 'address', 'city', 'email', 'name', 'phone',
                  'payment', 'needsEReceipt', 'comments']


class OrderUserCreateForm(ModelForm):
    name = forms.CharField(label='Nombre de Contacto:', required=True)
    person_id = forms.IntegerField(label='CC:', required=True)
    address = forms.CharField(label='Dirección:', required=True)
    city = forms.ChoiceField(label='Ciudad:', required=True, choices=Order.CityChoices.choices)
    email = forms.EmailField(label='Correo:', required=True)
    phone = forms.CharField(label='Teléfono:', required=True)
    payment = forms.ChoiceField(label='Método de Pago:', required=True, widget=forms.RadioSelect,
                                choices=Order.PaymentMethod.choices)
    comments = forms.CharField(label='Instrucciones Especiales:', required=False, widget=forms.Textarea)

    class Meta:
        model = Order
        fields = ['name', 'person_id', 'address', 'city', 'email', 'phone', 'payment', 'comments']